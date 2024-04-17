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
from fastapi.responses import JSONResponse
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src import interro, views
from src.api import authentication as auth_api
from src.data import data_handler, users

cred_checker = users.CredChecker()
redis_db = redis.Redis(
    host='localhost',
    port=6379,
    db=0
)


def load_test(
        user_name,
        db_name,
        test_type,
        test_length
    ):
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


def load_rattraps(
        token,
        data
    ):
    """
    Load the rattraps!
    """
    test = load_test_from_redis(token)
    count = int(data.get('count'))
    total = int(data.get('total'))
    score = int(data.get('score'))
    if hasattr(test, 'rattraps'):
        rattraps_cnt = test.rattraps + 1
    else:
        rattraps_cnt = 0
    guesser = views.FastapiGuesser()
    rattrap = interro.Rattrap(
        test.faults_df,
        rattraps_cnt,
        guesser
    )
    save_test_in_redis(rattrap, token)
    logger.debug(f"rattrap saved in redis")
    message = "Rattraps created successfully"
    return JSONResponse(
        content=
        {
            'message': message,
            'token': token,
            'total': total,
            'score': score,
            'count': count
        }
    )


def get_interro_question(
        request,
        token,
        total,
        count,
        score
    ):
    """
    API function to load the interro question.
    """
    user_name = auth_api.get_user_name_from_token(token)
    # Check input consistency
    try:
        count = int(count)
    except NameError:
        count = 0
    try:
        score = int(score)
    except NameError:
        score = 0
    test = load_test_from_redis(token)
    progress_percent = int(count / int(total) * 100)
    index = test.interro_df.index[count]
    english = test.interro_df.loc[index][0]
    english = english.replace("'", "\'")
    count += 1
    request_dict = {
        "request": request,
        "numWords": total,
        "userName": user_name,
        "count": count,
        "score": score,
        "progressPercent": progress_percent,
        'token': token,
        "content_box1": english
    }
    return request_dict


def save_test_in_redis(test, token):
    """
    Save a test object in redis using token as key.
    """
    test = pickle.dumps(test)
    redis_db.set(token  + '_test', test)


def load_test_from_redis(token):
    """
    Load a test object from redis using token as key.
    """
    pickelized_test = redis_db.get(token + '_test')
    test = pickle.loads(pickelized_test)
    return test


def save_loader_in_redis(loader, token):
    """
    Save a loader object in redis using token as key.
    """
    loader = pickle.dumps(loader)
    redis_db.set(token + '_loader', loader)


def load_loader_from_redis(token):
    """
    Load a test object from redis using token as key.
    """
    pickelized_loader = redis_db.get(token + '_loader')
    loader = pickle.loads(pickelized_loader)
    return loader
