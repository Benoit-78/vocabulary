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

from fastapi.responses import JSONResponse
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src import interro, views
from src.api import authentication as auth_api
from src.api import database as db_api
from src.data import data_handler
from src.data import redis_interface
from src.interro import Updater



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
    loader_ = interro.Loader(db_handler)
    loader_.load_tables()
    guesser = views.FastapiGuesser()
    test_ = interro.PremierTest(
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
    logger.info('african_swallow')
    user_name = auth_api.get_user_name_from_token(token)
    db_name = settings.get('databaseName')
    test_type = settings.get('testType').lower()
    test_length = int(settings.get('numWords'))
    loader, test = load_test(
        user_name=user_name,
        db_name=db_name,
        test_type=test_type,
        test_length=test_length
    )
    redis_interface.save_test_in_redis(test, token)
    redis_interface.save_loader_in_redis(loader, token)
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
    count = int(count)
    score = int(score)
    test = redis_interface.load_test_from_redis(token)
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
    test = redis_interface.load_test_from_redis(token)
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
    test = redis_interface.load_test_from_redis(token)
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
    redis_interface.save_test_in_redis(test, token)
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
    test = redis_interface.load_test_from_redis(token)
    new_total = test.faults_df.shape[0]
    # Enregistrer les résultats
    if not hasattr(test, 'rattraps'):
        test.compute_success_rate()
        loader = redis_interface.load_loader_from_redis(token)
        updater = Updater(loader, test)
        updater.update_data()
        logger.info("User data updated.")
    # Réinitialisation
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
    test = redis_interface.load_test_from_redis(token)
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
    redis_interface.save_test_in_redis(rattrap, token)
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
    logger.info("african_swallow")
    test = redis_interface.load_test_from_redis(token)
    # Enregistrer les résultats
    if not hasattr(test, 'rattraps'):
        test.compute_success_rate()
        loader = redis_interface.load_loader_from_redis(token)
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
