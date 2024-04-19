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
    user_name = auth_api.get_user_name_from_token(token)
    user_account = users.UserAccount(user_name)
    databases = user_account.get_databases_list()
    return databases


def load_user_databases(request, token):
    """
    Load the user databases.
    """
    databases = get_user_databases(token)
    response_dict = {
        'request': request,
        'token': token,
        'databases': databases
    }
    return response_dict


def choose_database(data, token: str):
    """
    Choose the given database.
    """
    db_name = data['db_name']
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


def create_database(data: dict, token: str):
    """
    Create the given database.
    """
    user_name = auth_api.get_user_name_from_token(token)
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


def fill_database(
        request,
        db_name,
        error_message,
        token
    ):
    """
    
    """
    if not db_name:
        logger.error("No database name given.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No database name given."
        )
    _ = auth_api.get_user_name_from_token(token)
    request_dict = {
        'request': request,
        'title': "Here you can add words to your database.",
        'token': token,
        'databaseName': db_name,
        'wordAlreadyPresentErrorMessage': error_message,
    }
    return request_dict


def create_word(data: dict, token:str):
    """
    Save the word in the database.
    """
    user_name = auth_api.get_user_name_from_token(token)
    db_name = data['db_name']
    user_account = users.UserAccount(user_name)
    result = user_account.insert_word(
        db_name,
        data['foreign'],
        data['native']
    )
    if result == 'Word already exists':
        json_response = JSONResponse(
            content={"message": "Word already exists"}
        )
    elif result is False:
        json_response = JSONResponse(
            content={"message": "Error with the word creation."}
        )
    elif result is True:
        json_response =  JSONResponse(
            content={"message": "Word added successfully."}
        )
    return json_response


def delete_database(data: dict, token: str):
    """
    Remove the given database.
    """
    db_name = data['db_name']
    user_name = auth_api.get_user_name_from_token(token)
    user_account = users.UserAccount(user_name)
    result = user_account.remove_database(db_name)
    if result is False:
        json_response = JSONResponse(
            content={"message": "Error with the database removal."}
        )
    if result is True:
        json_response = JSONResponse(
            content={"message": "Database deleted successfully."}
        )
    return json_response


async def upload_csv(csv_file, token: str):
    """
    """
    if not csv_file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format, only CSV files are allowed"
        )
    csv_content = await csv_file.read()
    if is_malicious(csv_content.decode('utf-8')):
        raise HTTPException(
            status_code=400,
            detail="Malicious code detected in the CSV file"
        )
    add_to_database(csv_content.decode('utf-8'))
    response_dict = {"message": "CSV file uploaded successfully"}
    return response_dict


def is_malicious(csv_content):
    """
    Check if the given CSV content is malicious.
    """
    if 'DROP DATABASE' in csv_content:
        return True
    if 'DELETE FROM' in csv_content:
        return True
    return False


def add_to_database(csv_content):
    """
    Add the CSV content to the database.
    """
    pass
