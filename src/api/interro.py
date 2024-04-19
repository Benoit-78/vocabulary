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
from fastapi.responses import JSONResponse
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src import interro, views
from src.api import authentication as auth_api
from src.api import database as db_api
from src.data import data_handler, users
from src.interro import Updater

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


def get_interro_settings(
        request,
        token
    ):
    """
    API function to load the interro settings.
    """
    databases = db_api.get_user_databases(token)
    request_dict = {
        'request': request,
        'token': token,
        'databases': databases
    }
    return request_dict


def save_interro_settings(
        settings,
        token
    ):
    """
    API function to save the interro settings.
    """
    user_name = auth_api.get_user_name_from_token(token)
    loader, test = load_test(
        user_name=user_name,
        db_name=settings.get('db_name'),
        test_type=settings.get('test_type'),
        test_length=int(settings.get('numWords'))
    )
    save_test_in_redis(test, token)
    save_loader_in_redis(loader, token)
    return JSONResponse(
        content=
        {
            'message': "Settings saved successfully",
            'token': token
        }
    )


def get_interro_question(
        request,
        total,
        count,
        score,
        token
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
    response_dict = {
        "request": request,
        "numWords": total,
        "userName": user_name,
        "count": count,
        "score": score,
        "progressPercent": progress_percent,
        'token': token,
        "content_box1": english
    }
    return response_dict


def load_interro_answer(
        request,
        total,
        count,
        score,
        token
    ):
    """
    Load the interro answer.
    """
    count = int(count)
    test = load_test_from_redis(token)
    progress_percent = int(count / int(total) * 100)
    index = test.interro_df.index[count - 1]
    english = test.interro_df.loc[index][0]
    english = english.replace("'", "\'")
    french = test.interro_df.loc[index][1]
    french = french.replace("'", "\'")
    response_dict = {
        "request": request,
        "token": token,
        "numWords": total,
        "count": count,
        "score": score,
        "progressPercent": progress_percent,
        "content_box1": english,
        "content_box2": french
    }
    return response_dict


def get_user_response(
        data,
        token
    ):
    """
    Get the user response.
    """
    test = load_test_from_redis(token)
    score = data.get('score')
    score = int(score)
    if data["answer"] == 'Yes':
        score += 1
        update = True
    elif data["answer"] == 'No':
        update = False
        test.update_faults_df(
            False,
            [
                data.get('english'),
                data.get('french')
            ]
        )
    if not hasattr(test, 'rattraps'):
        test.update_voc_df(update)
    save_test_in_redis(test, token)
    json_response = JSONResponse(
        content=
        {
            "score": score,
            "message": "User response stored successfully"
        }
    )
    return json_response


def propose_rattraps(
        request,
        total,
        score,
        token
    ):
    """
    Propose the rattraps.
    """
    test = load_test_from_redis(token)
    new_total = test.faults_df.shape[0]
    # Enregistrer les résultats
    if not hasattr(test, 'rattraps'):
        test.compute_success_rate()
        loader = load_loader_from_redis(token)
        updater = Updater(loader, test)
        updater.update_data()
        logger.info("User data updated.")
    # Réinitialisation
    logger.debug(f"New words: {new_total}")
    response_dict = {
        "request": request,
        "token": token,
        "newTotal": new_total,
        "newScore": 0,
        "newCount": 0,
        "score": score,
        "numWords": total
    }
    return response_dict


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


def end_interro(
        request,
        total,
        score,
        token
    ):
    """
    End the interro.
    """
    test = load_test_from_redis(token)
    # Enregistrer les résultats
    if not hasattr(test, 'rattraps'):
        test.compute_success_rate()
        loader = load_loader_from_redis(token)
        updater = Updater(loader, test)
        updater.update_data()
        logger.info("User data updated.")
    response_dict = {
        "request": request,
        "score": score,
        "numWords": total,
        "token": token
    }
    return response_dict




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
