"""
    Creator:
        B.Delorme
    Creation date:
        14th March 2024
    Main purpose:
        Contains the functions used to create and check tokens.
"""

import os
import random
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from loguru import logger
from passlib.context import CryptContext
from pydantic import BaseModel

from src.data.data_handler import DbController

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
users_dict = {
    "guest": {
        "username": "guest",
        "password": None,
    }
}
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)



class Token(BaseModel):
    access_token: str
    token_type: str



class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None



class UserInDB(User):
    hashed_password: str



# -------------------------
#  T O K E N
# -------------------------

def create_guest_user_name():
    """
    Function to create a guest user name.
    """
    guest_user_name = f"guest_{random.randint(1, 1_000_000)}"
    return {"sub": guest_user_name}


async def create_token(
        data: dict = None,
        expires_delta: Optional[int] = None
    ):
    """
    Function to generate a token for a guest or an existing user.
    """
    if data is None:
        data = create_guest_user_name()
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt


def get_users_names():
    """
    Function to get the list of users names.
    """
    controller = DbController()
    users_list = controller.get_users_list()
    return users_list


def check_token(token: str):
    """
    Function to check if a token is valid.
    - if the user is a guest, return the token.
    - if the user is logged in, returns the user name.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username: str = payload.get('sub')
        if username.startswith('guest_'):
            return token
        users_list = get_users_names()
        if username not in users_list:
            raise credentials_exception
        return token
    except JWTError as exc:
        # If there's any JWTError, raise credentials_exception
        raise credentials_exception from exc



# -------------------------
#  O A u t h 2
# -------------------------

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Given a token, return the user name.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    if username not in list(users_dict.keys()):
        raise credentials_exception
    return username



def authenticate_user(
        users_list: list,
        username: str,
        password: str
    ):
    def get_user(
            users_list: list,
            username: str
        ):
        if username in users_list:
            user_dict = users_list[username]
            return UserInDB(**user_dict)

    def verify_password(
            plain_password,
            hashed_password
        ):
        return pwd_context.verify(plain_password, hashed_password)

    user = get_user(users_list, username)
    if user is None:
        return 'Unknown user'
    if not verify_password(password, user.hashed_password):
        return 'Password incorrect'
    return user
