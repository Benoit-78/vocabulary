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


def get_user_databases(request, user_name, user_password):
    """
    Call the base page of user databases.
    """
    # Authenticate user
    if user_name:
        cred_checker.check_credentials(user_name, user_password)
    else:
        logger.error("User name not found.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User name not found."
        )
    request_dict = {
        "request": request,
        "userName": user_name,
        "userPassword": user_password
    }
    return request_dict


def create_database(data: dict):
    """
    Create the given database.
    """
    # Authenticate user
    user_name = data['usr']
    user_password = data['pwd']
    cred_checker.check_credentials(user_name, user_password)
    # Create database
    db_name = data['db_name']
    user_account = users.UserAccount(user_name, user_password)
    result = user_account.create_database(db_name)
    if result == 1:
        json_response = JSONResponse(
            content=
            {
                "message": f"Database name {db_name} not available.",
                "userName": user_account.user_name,
                "userPassword": user_account.user_password,
                "databaseName": db_name
            }
        )
    if result == 0:
        json_response = JSONResponse(
            content=
            {
                "message": "Database created successfully.",
                "userName": user_account.user_name,
                "userPassword": user_account.user_password
            }
        )
    return json_response


def choose_database(data: dict):
    """
    Choose the given database.
    """
    # Authenticate user
    user_name = data['userName']
    user_password = data['userPassword']
    cred_checker.check_credentials(user_name, user_password)
    # Choose database
    db_name = data['databaseName']
    user_account = users.UserAccount(user_name, user_password)
    result = user_account.check_if_database_exists(db_name)
    if not result:
        json_response = JSONResponse(
            content=
            {
                "message": f"Database name {db_name} not available.",
                "userName": user_account.user_name,
                "userPassword": user_account.user_password
            }
        )
    if result:
        json_response = JSONResponse(
            content=
            {
                "message": "Database chosen successfully.",
                "userName": user_account.user_name,
                "userPassword": user_account.user_password,
                "databaseName": db_name
            }
        )
    return json_response


def create_word(data: dict):
    """
    Save the word in the database.
    """
    # Authenticate user
    user_name = data['usr']
    user_password = data['pwd']
    cred_checker.check_credentials(user_name, user_password)
    # Add the word
    db_name = data['db_name']
    user_account = users.UserAccount(user_name, user_password)
    result = user_account.insert_word(db_name, data['foreign'], data['native'])
    if result == 1:
        return JSONResponse(content={"message": "Error with the word creation."})
    elif result == 0:
        return JSONResponse(content={"message": "Word created successfully."})


def fill_database(request, user_name, user_password, db_name):
    """
    
    """
    # Authenticate user
    if user_name:
        cred_checker.check_credentials(user_name, user_password)
    else:
        logger.error("User name not found.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User name not found."
        )
    # Check if a database has been chosen
    if not db_name:
        logger.error("No database name given.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No database name given."
        )
    # Load database page
    title = "Here you can add words to your database."
    request_dict = {
        "request": request,
        "title": title,
        "userName": user_name,
        "userPassword": user_password,
        "databaseName": db_name
    }
    return request_dict
