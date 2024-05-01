"""
    Creation date:
        23rd February 2024
    Creator:
        B. Delorme
    Main purpose:
        Hosts the functions of interro router.
"""

import os
import sys
from typing import Dict

from fastapi.responses import JSONResponse
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.api import authentication as auth_api
from src.data import users


def create_account(
        creds: dict,
        token: str
    ) -> Dict:
    """
    Create the user account if the given user name does not exist yet.
    """
    logger.info('african_swallow')
    user_account = users.UserAccount(creds['input_name'])
    result = user_account.create_account(creds['input_password'])
    json_response = {}
    if result is False:
        json_response = JSONResponse(
            content=
            {
                'message': "User name not available",
                'userName': user_account.user_name,
                'token': token
            }
        )
    if result is True:
        new_token = auth_api.create_token({"sub": creds['input_name']})
        json_response = JSONResponse(
            content=
            {
                'message': "User account created successfully",
                'userName': user_account.user_name,
                'token': new_token
            }
        )
    return json_response


def authenticate_user(
        token: str,
        form_data
    ) -> Dict:
    """
    Authenticate the user.
    """
    logger.info('african_swallow')
    users_list = auth_api.get_users_list()
    user = auth_api.authenticate_user(
        users_list,
        form_data.username,
        form_data.password
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


def load_user_space(
        request,
        token
    ) -> Dict:
    """
    Call the base page of user space.
    """
    logger.info('african_swallow')
    user_name = auth_api.get_user_name_from_token(token)
    json_response = {
        'request': request,
        'token': token,
        'user_name': user_name
    }
    return json_response
