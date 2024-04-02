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

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.data import users

cred_checker = users.CredChecker()


def create_account(creds, token):
    """
    Create the user account if the given user name does not exist yet.
    """
    user_account = users.UserAccount(creds['input_name'])
    result = user_account.create_account(creds['input_password'])
    json_response = {}
    if result is False:
        json_response = JSONResponse(
            content=
            {
                "message": "User name not available.",
                "userName": user_account.user_name,
                'token': token
            }
        )
    if result is True:
        json_response = JSONResponse(
            content=
            {
                "message": "User account created successfully",
                "userName": user_account.user_name,
                'token': token
            }
        )
    return json_response


def authenticate_user(input_dict):
    """
    Acquire the user credentials.
    """
    input_name = input_dict.get('input_name')
    input_password = input_dict.get('input_password')
    cred_checker.check_credentials(input_name, input_password)
    request_dict = {
        "message": "User credentials validated successfully",
        "userName": input_name,
        "userPassword": input_password
    }
    return request_dict


def get_user_main_page(
        request,
        user_name: str,
        user_password: str,
        token: str
    ):
    """
    API function to load the interro settings.
    """
    # Authenticate user
    if user_name:
        cred_checker.check_credentials(user_name, user_password)
    else:
        logger.error("No user name found in cookies.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No user name found in cookies."
        )
    # Load settings
    request_dict = {
        'request': request,
        'userName': user_name,
        'userPassword': user_password,
        'token': token
    }
    return request_dict
