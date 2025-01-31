"""
    Creation date:
        23rd February 2024
    Creator:
        B. Delorme
    Main purpose:
        Hosts the functions of interro router.
"""

from typing import Any, Dict, List

from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse
from loguru import logger

from src.api import authentication as auth_api
from src.data import users
from src.models.user import UserLogin


def create_account(creds: Dict[str, Any], token: str) -> JSONResponse:
    """
    Create the user account if the given user name does not exist yet.
    """
    user_name = auth_api.get_user_name_from_token(token=token)
    logger.info(f"User: {user_name}")
    if creds['input_name'] == '' or creds['input_password'] == '':
        json_response = JSONResponse(
            content=
            {
                'message': "User name or password not provided",
                'token': token
            }
        )
        return json_response
    user_account = users.UserAccount(user_name=creds['input_name'])
    result: bool = user_account.create_account(password=creds['input_password'])
    if result:
        new_token = auth_api.create_token(data={"sub": creds['input_name']})
        json_response = JSONResponse(
            content=
            {
                'message': "User account created successfully",
                'userName': user_account.user_name,
                'token': new_token
            }
        )
    else:
        json_response = JSONResponse(
            content=
            {
                'message': "User name not available",
                'userName': user_account.user_name,
                'token': token
            }
        )
    return json_response


def authenticate_user(token: str, form_data: UserLogin) -> JSONResponse:
    """
    Authenticate the user.
    """
    if '' in [form_data.username, form_data.password]:
        json_response = JSONResponse(
            content=
            {
                'message': "User name or password not provided",
                'token': token
            }
        )
        return json_response
    logger.info(f"User: {form_data.username}")
    users_list: List[Dict[str, Any]] = auth_api.get_users_list()
    user = auth_api.authenticate_user(
        users_list=users_list,
        username=form_data.username,
        password=form_data.password
    )
    if user == "Unknown user":
        json_response = JSONResponse(
            content=
            {
                'message': "Unknown user",
                'token': token
            }
        )
    elif user == "Password incorrect":
        json_response = JSONResponse(
            content=
            {
                'message': "Password incorrect",
                'token': token
            }
        )
    else:
        user_token = auth_api.create_token(data={"sub": form_data.username})
        json_response = JSONResponse(
                content=
                {
                    'message': "User successfully authenticated",
                    'userName': form_data.username,
                    'token': user_token
                }
            )
    return json_response


def authenticate_user_with_oauth(token: str, form_data: UserLogin):
    """
    Authenticate the user with OAuth.
    """
    user = auth_api.authenticate_with_oauth(form_data=form_data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    json_response = JSONResponse(
        content=
        {
            'message': "Vous n'avez pas dit le mot magi-que, ha-ha-ha !",
            'token': token
        }
    )
    return json_response


def load_user_space(request: Request, token: str) -> Dict:
    """
    Call the base page of user space.
    """
    user_name = auth_api.get_user_name_from_token(token=token)
    logger.info(f"User: {user_name}")
    json_response = {
        'request': request,
        'token': token,
        'user_name': user_name
    }
    return json_response
