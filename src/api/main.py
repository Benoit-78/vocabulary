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
import sys
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

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


async def get_users_names():
    """
    Function to get the list of users names.
    """
    controller = DbController()
    users_list = controller.get_users_list()
    return users_list



async def generate_token(expires_delta: Optional[int] = None):
    """
    Function to generate a token for a guest
    """
    to_encode = {
        "guest_id": random.randint(1, 1_000_000)
    }
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


def check_token(token: str):
    """
    Function to check if a token is valid.
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
            return 'guest'
        users_list = get_users_names()
        if username not in users_list:
            raise credentials_exception
        return username
    except JWTError as exc:
        # If there's any JWTError, raise credentials_exception
        raise credentials_exception from exc



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
