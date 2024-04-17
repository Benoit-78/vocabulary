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
from src.api import authentication as auth_api

cred_checker = users.CredChecker()


def get_user_databases(token):
    """
    Call the base page of user databases.
    """
    # Authenticate user
    user_name = auth_api.get_user_name_from_token(token)
    user_account = users.UserAccount(user_name)
    databases = user_account.get_databases_list()
    return databases


def create_database(data: dict, token: str):
    """
    Create the given database.
    """
    # Authenticate user
    user_name = auth_api.get_user_name_from_token(token)
    # Create database
    db_name = data['db_name']
    user_account = users.UserAccount(user_name)
    result = user_account.create_database(db_name)
    if result is False:
        json_response = JSONResponse(
            content=
            {
                'message': f"Database name {db_name} not available.",
                'token': token,
                'databaseName': db_name
            }
        )
    if result is True:
        json_response = JSONResponse(
            content=
            {
                'message': "Database created successfully.",
                'token': token,
                'databaseName': db_name
            }
        )
    return json_response


def choose_database(db_name: str, token: str):
    """
    Choose the given database.
    """
    user_name = auth_api.get_user_name_from_token(token)
    user_account = users.UserAccount(user_name)
    db_exists = user_account.check_if_database_exists(db_name)
    if db_exists:
        json_response = JSONResponse(
            content=
            {
                "message": f"Database name {db_name} not available.",
            }
        )
    if not db_exists:
        json_response = JSONResponse(
            content=
            {
                "message": "Database chosen successfully.",
            }
        )
    return json_response


def create_word(data: dict):
    """
    Save the word in the database.
    """
    # Authenticate user
    user_name = data['usr']
    cred_checker.check_credentials(user_name)
    # Add the word
    db_name = data['db_name']
    result = user_account.insert_word(db_name, data['foreign'], data['native'])
    if result == 1:
        return JSONResponse(content={"message": "Error with the word creation."})
    if result == 0:
        return JSONResponse(content={"message": "Word created successfully."})


def fill_database(request, token, db_name):
    """
    
    """
    user_name = auth_api.get_user_name_from_token(token)
    if not db_name:
        logger.error("No database name given.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No database name given."
        )
    request_dict = {
        "request": request,
        "title": "Here you can add words to your database.",
        "token": token,
        "databaseName": db_name
    }
    return request_dict


def delete_database(token: str, db_name: str):
    """
    Remove the given database.
    """
    # Authenticate user
    user_name = auth_api.get_user_name_from_token(token)
    # Remove the database
    user_account = users.UserAccount(user_name)
    result = user_account.remove_database(db_name)
    if result is False:
        return JSONResponse(
            content={"message": "Error with the database removal."}
        )
    if result is True:
        return JSONResponse(
            content={"message": "Database deleted successfully."}
        )


def upload_csv():
    """
    """
    