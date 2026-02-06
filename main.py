from fastapi import Depends, FastAPI
from typing import Optional
from models import User
from db import SessionDep
from sqlmodel import SQLModel, select
from db import engine
from schema import UserCreate
from passwords import authenticate_user, get_password_hash
from schema import UserLogin, UserBase
from fastapi import HTTPException, status
from manage_token import create_access_token
from schema import Token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from manage_token import create_access_token
from user_utils import with_all_users_temp_db
# from config import oauth2_scheme

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()



@app.get("/greet")
def greet(token: Annotated[str, Depends(oauth2_scheme)], name: Optional[str] = "World"):
    return {"message": f"Hello, {name}!"}

# Code above omitted 👆
@app.on_event("startup")
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.get("/users")
def all_users(session:SessionDep):
    users = session.exec(select(User)).all()
    return users

@app.post("/users")
def create_user(userbase: UserCreate, session:SessionDep):
    user = User(**userbase.model_dump(), hashed_password=get_password_hash(userbase.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# @app.post("/login", response_model=UserBase)
# def login(login_data: UserLogin, session: SessionDep):
#     # 1. Query the database for the user
#     statement = select(User).where(User.username == login_data.username)
#     db_user = session.exec(statement).first()
    
#     # 2. Reconstruct the dictionary format exactly as the utility expects
#     # We use .model_dump() to turn the SQLModel object into a raw dict
#     if db_user:
#         # This creates: {"para": {"username": "para", "hashed_password": "...", ...}}
#         temp_db = {db_user.username: db_user.model_dump()}
#     else:
#         temp_db = {}

#     # 3. Call your original function
#     # Now get_user will receive a dict and UserInDB(**user_dict) will work!
#     user = authenticate_user(temp_db, login_data.username, login_data.password)
    
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid username or password"
#         )
        
#     return user

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    fake_users_db = Depends(with_all_users_temp_db)
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)