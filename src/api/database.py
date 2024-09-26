"""
    Creation date:
        23rd February 2024
    Creator:
        B. Delorme
    Main purpose:
        Hosts the functions of interro router.
"""

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger

from src.data import users
from src.data.database_interface import DbQuerier
from src.api import authentication as auth_api


def get_user_databases(token):
    """
    Call the base page of user databases.
    """
    user_name = auth_api.get_user_name_from_token(token=token)
    user_account = users.UserAccount(user_name=user_name)
    databases = user_account.get_databases_list()
    return databases


def load_user_databases(request, token, error_message):
    """
    Load the user databases.
    """
    databases = get_user_databases(token=token)
    db_message = get_error_messages(error_message=error_message)
    response_dict = {
        'request': request,
        'token': token,
        'databases': databases,
        'createDatabaseErrorMessage': db_message
    }
    return response_dict


def create_database(data: dict, token: str):
    """
    Create the given database.
    """
    user_name = auth_api.get_user_name_from_token(token=token)
    logger.info(f"User: {user_name}")
    user_account = users.UserAccount(user_name=user_name)
    if data['db_name'] == '':
        json_response = JSONResponse(
                content=
                {
                    'message': "No database name given",
                    'token': token,
                    'databaseName': ''
                }
            )
        return json_response
    db_name = data['db_name']
    result = user_account.create_database(db_name=db_name)
    if result is False:
        json_response = JSONResponse(
            content=
            {
                'message': "Database name not available",
                'token': token,
                'databaseName': db_name
            }
        )
    if result is True:
        json_response = JSONResponse(
            content=
            {
                'message': "Database created successfully",
                'token': token,
                'databaseName': db_name
            }
        )
    return json_response


def retrieve_database(data: dict, token: str):
    """
    See the given database.
    """
    user_name = auth_api.get_user_name_from_token(token=token)
    logger.info(f"User: {user_name}")
    db_name = data['db_name']
    db_querier = DbQuerier(
        user_name=user_name,
        db_name=db_name,
        test_type='version'
    )
    tables = db_querier.get_tables()
    version_table = tables['version_voc']
    theme_table = tables['theme_voc']
    json_response = JSONResponse(
        content=
        {
            "message": "Retrieved database words successfully",
            "token": token,
            'versionTable': version_table,
            'themeTable': theme_table,
        }
    )
    return json_response


def see_database(
        request,
        token: str,
        db_name: str,
        version_table: str,
        theme_table: str
    ):
    """
    Base page for data input by the user.
    """
    request_dict = {
        'request': request,
        'token': token,
        'databaseName': db_name,
        'versionTable': version_table,
        'themeTable': theme_table,
    }
    return request_dict


def choose_database(data, token: str):
    """
    Choose the given database.
    """
    user_name = auth_api.get_user_name_from_token(token=token)
    logger.info(f"User: {user_name}")
    user_account = users.UserAccount(user_name=user_name)
    db_name = data['db_name']
    db_exists = user_account.check_if_database_exists(db_name=db_name)
    if not db_exists:
        json_response = JSONResponse(
            content=
            {
                "message": f"Database name {db_name} not available",
            }
        )
    else:
        json_response = JSONResponse(
            content=
            {
                "message": "Database chosen successfully",
            }
        )
    return json_response


def get_error_messages(error_message: str):
    """
    Get the error messages from the error message.
    """
    messages = [
        "No database name given",
        "Database name not available",
        "Database created successfully",
        ''
    ]
    if error_message == messages[0]:
        result = 'No database name given'
    elif error_message == messages[1]:
        result = 'A database of this name already exists'
    elif error_message == messages[2]:
        result = ''
    elif error_message == messages[3]:
        result = ''
    else:
        logger.error(f"Error message incorrect: {error_message}")
        logger.error(f"Should be in: {messages}")
        raise ValueError
    return result


def fill_database(
        request,
        db_name,
        error_message,
        token
    ):
    """
    Back-end function to prepare json response for a new word insertion.
    """
    if not db_name:
        logger.error("No database name given")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No database name given"
        )
    _ = auth_api.get_user_name_from_token(token=token)
    request_dict = {
        'request': request,
        'title': "Here you can add words to your database",
        'token': token,
        'databaseName': db_name,
        'wordAlreadyPresentErrorMessage': error_message,
    }
    return request_dict


def create_word(data: dict, token:str):
    """
    Save the word in the database.
    """
    user_name = auth_api.get_user_name_from_token(token=token)
    db_name = data['db_name']
    user_account = users.UserAccount(user_name=user_name)
    result = user_account.insert_word(
        db_name=db_name,
        foreign=data['foreign'],
        native=data['native']
    )
    if result == 'Word already exists':
        json_response = JSONResponse(
            content={"message": "Word already exists"}
        )
    elif not result:
        json_response = JSONResponse(
            content={"message": "Error with the word creation"}
        )
    else:
        json_response =  JSONResponse(
            content={"message": "Word added successfully"}
        )
    return json_response


def delete_database(data: dict, token: str):
    """
    Remove the given database.
    """
    db_name = data['db_name']
    user_name = auth_api.get_user_name_from_token(token=token)
    logger.info(f"User: {user_name}")
    user_account = users.UserAccount(user_name=user_name)
    result = user_account.remove_database(db_name=db_name)
    if not result:
        json_response = JSONResponse(
            content={"message": "Error with the database removal"}
        )
    else:
        json_response = JSONResponse(
            content={"message": "Database deleted successfully"}
        )
    return json_response


def is_malicious(csv_content):
    """
    Check if the given CSV content is malicious.
    """
    if 'DROP DATABASE' in csv_content:
        return True
    if 'DELETE FROM' in csv_content:
        return True
    return False
