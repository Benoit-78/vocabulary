"""
    Creation date:
        23rd February 2024
    Creator:
        B. Delorme
    Main purpose:
        Hosts the functions of interro router.
"""

import os
import pickle
import sys

import redis
from fastapi import HTTPException, status
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src import interro, views
from src.data import data_handler, users

cred_checker = users.CredChecker()
redis_db = redis.Redis(
    host='localhost',
    port=6379,
    db=0
)


def load_test(user_name, db_name, test_type, test_length):
    """
    Load the interroooo!
    """
    db_handler = data_handler.DbManipulator(
        user_name=user_name,
        db_name=db_name,
        test_type=test_type,
    )
    db_handler.check_test_type(test_type)
    loader_ = interro.Loader(0, db_handler)
    loader_.load_tables()
    guesser = views.FastapiGuesser()
    test_ = interro.Test(
        loader_.tables[loader_.test_type + '_voc'],
        test_length,
        guesser,
        loader_.tables[loader_.test_type + '_perf'],
        loader_.tables[loader_.test_type + '_words_count']
    )
    test_.set_interro_df()
    return loader_, test_


def get_interro_question(
        request,
        user_name,
        user_password,
        db_name,
        test_type,
        total,
        count,
        score
    ):
    """
    API function to load the interro question.
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
    # Check input consistency
    try:
        count = int(count)
    except NameError:
        count = 0
    try:
        score = int(score)
    except NameError:
        score = 0
    # Test instanciation
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    _, test = load_test(
        user_name,
        db_name,
        test_type,
        total
    )
    progress_percent = int(count / int(total) * 100)
    index = test.interro_df.index[count]
    english = test.interro_df.loc[index][0]
    english = english.replace("'", "\'")
    count += 1
    request_dict = {
        "request": request,
        "userName": user_name,
        "numWords": total,
        "count": count,
        "score": score,
        "progressPercent": progress_percent,
        "content_box1": english
    }
    return request_dict


def save_test_in_redis(test, token):
    """
    Save a test object in redis using token as key.
    """
    test = pickle.dumps(test)
    redis_db.set(token, test)


def load_test_from_redis(token):
    """
    Load a test object from redis using token as key.
    """
    pickelized_test = redis_db.get(token)
    test = pickle.loads(pickelized_test)
    return test
