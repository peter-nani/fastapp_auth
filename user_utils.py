# from passwords import verify_password
from schema import UserInDB

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)