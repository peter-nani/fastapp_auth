# from passwords import verify_password
from makefun import wraps
from functools import wraps
from fastapi.params import Depends
from sqlmodel import select
from schema import UserInDB
from typing import Callable, Optional
from db import SessionDep
from models import User


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def with_all_users_temp_db(
        session: SessionDep,
        # *args,
        # **kwargs,
    ):
        # Create a temporary in-memory database of users
        temp_db = {}
        users = session.exec(select(User)).all()
        for user in users:
            temp_db[user.username] = user.model_dump()
        
        # Pass the temporary database to the decorated function
        return temp_db