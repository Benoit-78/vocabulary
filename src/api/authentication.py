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


def create_token(
        data: dict = None,
        expires_delta: Optional[int] = None
    ):
    """
    Function to generate a token for a guest or an existing user.
    """
    logger.info('african_swallow')
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
        os.environ['SECRET_KEY'],
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


def get_user_name_from_token(token: str):
    """
    Function to get the user name from a token.
    """
    payload = jwt.decode(
        token,
        os.environ['SECRET_KEY'],
        algorithms=[ALGORITHM]
    )
    user_name: str = payload.get('sub')
    return user_name


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
        user_name = get_user_name_from_token(token)
        if user_name.startswith('guest_'):
            return token
        users_list = get_users_list()
        # logger.debug(f"users_list: {users_list}")
        user_names = [element['username'] for element in users_list]
        if user_name not in user_names:
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
            os.environ['SECRET_KEY'],
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
        # logger.debug(f"users_list: {users_list}")
        # logger.debug(f"username: {username}")
        user_dict = [
            user_dict
            for user_dict in users_list
            if user_dict['username'] == username
        ]
        # logger.debug(f"user_dict: {user_dict}")
        try:
            user_dict = user_dict[0]
            user = UserInDB(**user_dict)
        except IndexError:
            logger.warning("Unknown user")
            user = None
        return user

    def verify_password(
            plain_password: str,
            password_hash
        ):
        result = pwd_context.verify(
            plain_password,
            password_hash
        )
        return result

    user_in_db_model = get_user(users_list, username)
    if user_in_db_model is None:
        user = 'Unknown user'
    else:
        try:
            verify_password(
                password,
                user_in_db_model.password_hash
            )
            user = user_in_db_model
        except UnknownHashError:
            logger.error("Password incorrect")
            user = 'Password incorrect'
    return user



# -------------------------
#  A U T R E
# -------------------------

def get_error_messages(error_message: str) -> tuple:
    """
    Based on the result of the POST method, returns the corresponding error messages
    that will feed the sign-in html page.
    """
    messages = [
        "User successfully authenticated",
        "Unknown user",
        "Password incorrect",
        ''
    ]
    if error_message == messages[0]:
        result = ("", "")
    elif error_message == messages[1]:
        result = ("Unknown user name", "")
    elif error_message == messages[2]:
        result = ("", "Password incorrect")
    elif error_message == messages[3]:
        result = ("", "")
    else:
        logger.error(f"Error message incorrect: {error_message}")
        logger.error(f"Should be in: {messages}")
    return result
