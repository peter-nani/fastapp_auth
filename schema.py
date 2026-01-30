from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str = Field(..., example="johndoe")
    full_name: str = Field(..., example="John Doe")
    email: str = Field(..., example="johndoe@example.com")
    disabled: Optional[bool] = Field(default=False, example=False)
    is_active: bool = Field(default=True, example=True)
    role: str = Field(default="user", example="user")
    created_at: datetime = Field(default_factory=datetime.utcnow, example="2023-01-01T00:00:00Z")
    #hashed_password: str = Field(..., example="$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, example="StrongPassword123!")

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class UserInDB(UserBase):
    hashed_password: str = Field(..., example="$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc")

class UserLogin(BaseModel):
    username: str
    password: str