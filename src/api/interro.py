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
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src import interro, views
from src.data import data_handler, users

cred_checker = users.CredChecker()


def load_interro_settings(request, query):
    """
    API function to load the interro settings.
    """
    # Authenticate user
    user_name = query.split('?')[0]
    user_password = query.split('?')[1].split('=')[1]
    if user_name:
        cred_checker.check_credentials(user_name, user_password)
    else:
        logger.error("User name not found.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User name not found."
        )
    # Load settings
    result_dict = {
        "request": request,
        "query": query,
        "userName": user_name,
        "userPassword": user_password
    }
    return result_dict


def load_test(user_name, db_name, test_type, test_length, password):
    """Load the interroooo!"""
    db_handler = data_handler.DbManipulator(
        host='localhost',
        user_name=user_name,
        db_name=db_name,
        test_type=test_type,
    )
    db_handler.check_test_type(test_type)
    loader_ = interro.Loader(0, db_handler)
    loader_.load_tables(password)
    guesser = views.FastapiGuesser()
    logger.debug(f"Table names: {loader_.tables.keys()}")
    test_ = interro.Test(
        loader_.tables[loader_.test_type + '_voc'],
        test_length,
        guesser,
        loader_.tables[loader_.test_type + '_perf'],
        loader_.tables[loader_.test_type + '_words_count']
    )
    logger.debug(f"Test created: {test_}")
    test_.set_interro_df()
    return loader_, test_


def get_interro_question(request, query):
    """
    API function to load the interro question.
    """
    # Authenticate user
    user_name = query.split('?')[0]
    user_password = query.split('?')[1].split('=')[1]
    if user_name:
        cred_checker.check_credentials(user_name, user_password)
    else:
        logger.error("User name not found.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User name not found."
        )
    logger.debug(f"query: {query}")
    # Load question page
    words = query.split('?')[2].split('=')[1]
    count = query.split('?')[3].split('=')[1]
    score = query.split('?')[4].split('=')[1]
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    global test
    try:
        count = int(count)
    except NameError:
        count = 0
    try:
        score = int(score)
    except NameError:
        score = 0
    progress_percent = int(count / int(words) * 100)
    index = test.interro_df.index[count]
    english = test.interro_df.loc[index][0]
    english = english.replace("'", "\'")
    count += 1
    request_dict = {
        "request": request,
        "userName": user_name,
        "numWords": words,
        "count": count,
        "score": score,
        "progressPercent": progress_percent,
        "content_box1": english
    }
    return request_dict
