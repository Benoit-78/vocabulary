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
from typing import Any, Dict, List, Union

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from loguru import logger
from passlib.context import CryptContext
from pydantic import BaseModel

from src.data.database_interface import DbController
from src.models.user import UserLogin

ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
original_users_list = [
    {
        'username': 'guest',
        'password_hash': ''
    }
]
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)



class User(BaseModel):
    """
    Base model class for the user.
    """
    username: str
    email: str=''
    disabled: bool=False



class UserInDB(User):
    """
    Base model class for the user in the database,
    that includes the hashed password.
    """
    password_hash: str



# -------------------------
#  A P I
# -------------------------
def sign_in(
        request: Request,
        token: str,
        error_message: str
    ) -> dict:
    """
    Function to sign in the user.
    """
    response_dict: Dict[str, Any] = {
        'request': request,
        'token': token,
        'errorMessage': error_message,
    }
    return response_dict



# -------------------------
#  T O K E N
# -------------------------
def create_guest_user_name() -> Dict[str, str]:
    """
    Function to create a guest user name.
    """
    guest_user_name = f"guest_{random.randint(1, 1_000_000)}"
    response = {"sub": guest_user_name}
    return response


def create_token(
        data: dict = {'sub': 'undefined'},
        expires_delta: int = 15
    ) -> str:
    """
    Function to generate a token for a guest or an existing user.
    """
    if data['sub'] == 'undefined':
        data = create_guest_user_name()
    logger.info(f"User: {data['sub']}")
    to_encode = data.copy()
    if not expires_delta:
        expires_delta = 15
    expire = datetime.now() + timedelta(minutes=expires_delta)
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
    user_name: str = payload.get('sub', '')
    return user_name


def check_token(token: str) -> str:
    """
    Function to check if a token is valid.
    - if the user is a guest, return the token.
    - if the user is logged in, returns the user name.
    """
    logger.debug("Check token called")
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
        user_names = [element['username'] for element in users_list]
        if user_name not in user_names:
            raise credentials_exception
        return token
    except JWTError as exc:
        raise credentials_exception from exc



# -------------------------
#  O A U T H
# -------------------------
def get_password_hash(password: str) -> str:
    """
    Return the hashed password.
    """
    return pwd_context.hash(password)


def get_user_name_from_token_oauth(
        token: str = Depends(oauth2_scheme)
    ) -> str:
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
        username : str = payload.get('sub', '')
        if username == '':
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
        users_list: List[Dict[str, Any]],
        username: str,
        password: str
    ) -> Union[str, UserInDB]:
    """
    Return the user data if the user exists.
    """
    def get_user(
            users_list: List[Dict[str, Any]],
            username: str
        ) -> Union[UserInDB, None]:
        user_list = [
            user_dict
            for user_dict in users_list
            if user_dict['username'] == username
        ]
        try:
            user_dict = user_list[0]
            user = UserInDB(**user_dict)
        except IndexError:
            logger.warning("Unknown user")
            return None
        return user

    def verify_password(
            plain_password: str,
            password_hash: str
        ) -> bool:
        result = pwd_context.verify(
            plain_password,
            password_hash
        )
        return result

    user_in_db_model = get_user(
        users_list=users_list,
        username=username
    )
    if user_in_db_model is None:
        return 'Unknown user'
    else:
        password_correct = verify_password(
            plain_password=password,
            password_hash=user_in_db_model.password_hash
        )
        if password_correct:
            user = user_in_db_model
        else:
            logger.error("Password incorrect")
            return 'Password incorrect'
    return user


def authenticate_with_oauth(
        # form_data: OAuth2PasswordRequestForm
        form_data: UserLogin
    ) -> Union[str, UserInDB]:
    """
    Authenticate the user using OAuth2.
    """
    user = authenticate_user(
        users_list=original_users_list,
        username=form_data.username,
        password=form_data.password
    )
    return user
