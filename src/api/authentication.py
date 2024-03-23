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
from typing import Dict, List, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from loguru import logger
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
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
    disabled: bool | None = None



class UserInDB(User):
    password_hash: str



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


def get_users_list() -> List[Dict]:
    """
    Function to get the list of users names.
    User names are the keys of each dictionnary.
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
        if username not in list(users_list.keys()):
            raise credentials_exception
        return token
    except JWTError as exc:
        # If there's any JWTError, raise credentials_exception
        raise credentials_exception from exc



# -------------------------
#  O A U T H
# -------------------------

def get_password_hash(password):
    """
    Return the hashed password.
    """
    return pwd_context.hash(password)


def get_username_from_token(token: str = Depends(oauth2_scheme)):
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
    controller = DbController()
    users_list = controller.get_users_list()
    users_names = [
        element['username']
        for element in users_list
    ]
    if username not in users_names:
        raise credentials_exception
    return username



def authenticate_user(
        users_list: dict,
        username: str,
        password: str
    ) -> UserInDB:
    """
    Return the user data if the user exists.
    """
    def get_user(
            users_list: dict,
            username: str
        ) -> UserInDB:
        user_dict = [
            user_dict
            for user_dict in users_list
            if user_dict['username'] == username
        ]
        try:
            user_dict = user_dict[0]
        except IndexError as exc:
            logger.error("Unknown user")
            raise exc
        logger.debug(f"User dict: {user_dict}")
        return UserInDB(**user_dict)

    def verify_password(
            plain_password: str,
            password_hash
        ):
        logger.debug(f"Input password: {plain_password}")
        logger.debug(f"Password hash: {password_hash}")
        # input_hash = pwd_context.hash(plain_password)
        logger.debug(f"Input hash: {plain_password}")
        result = pwd_context.verify(
            plain_password,
            # input_hash,
            password_hash
        )
        return result

    user_in_db_model = get_user(users_list, username)
    if user_in_db_model is None:
        return 'Unknown user'
    try:
        verify_password(
            password,
            user_in_db_model.password_hash
        )
    except UnknownHashError:
        return 'Password incorrect'
    return user_in_db_model
