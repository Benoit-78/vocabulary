"""
    Creation date:
        23rd February 2024
    Creator:
        B. Delorme
    Main purpose:
        Hosts the functions of interro API.
"""

import os
import sys

import pandas as pd
from fastapi.responses import JSONResponse
from loguru import logger
from typing import Dict

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src import interro as core_interro
from src.views import api as api_view
from src.api import authentication as auth_api
from src.api import database as db_api
from src.data import database_interface
from src.data.redis_interface import load_interro_from_redis, save_interro_in_redis
from src.data.redis_interface import load_loader_from_redis, save_loader_in_redis
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
    db_querier = database_interface.DbQuerier(
        user_name=user_name,
        db_name=db_name,
        test_type=test_type,
    )
    loader = core_interro.Loader(data_querier=db_querier)
    loader.load_tables()
    test_length = adjust_test_length(
        test_length=test_length,
        loader=loader
    )
    guesser = api_view.FastapiGuesser()
    premier_test = core_interro.PremierTest(
        words_df_=loader.tables[loader.test_type + '_voc'],
        words=test_length,
        guesser=guesser,
        perf_df_=loader.tables[loader.test_type + '_perf'],
        words_cnt_df=loader.tables[loader.test_type + '_words_count']
    )
    premier_test.set_interro_df()
    return loader, premier_test


def adjust_test_length(test_length, loader):
    """
    Check the test length.
    """
    words_table = loader.tables[loader.test_type + '_voc']
    words_total = words_table.shape[0]
    test_length = min(words_total, test_length)
    if test_length == 0:
        raise ValueError
    return test_length


def get_interro_settings(
        request,
        token,
        error_message
    ):
    """
    API function to load the interro settings.
    """
    databases = db_api.get_user_databases(token=token)
    db_message = get_error_messages(error_message=error_message)
    settings_dict = {
        'request': request,
        'token': token,
        'databases': databases,
        'emptyTableErrorMessage': db_message,
    }
    return settings_dict


def save_interro_settings(settings, token):
    """
    API function to save the interro settings.
    """
    user_name = auth_api.get_user_name_from_token(token=token)
    logger.info(f"User: {user_name}")
    db_name = settings.get('databaseName')
    test_type = settings.get('testType').lower()
    test_length = int(settings.get('numWords'))
    try:
        loader, premier_test = load_test(
            user_name=user_name,
            db_name=db_name,
            test_type=test_type,
            test_length=test_length
        )
    except ValueError:
        return JSONResponse(
            content=
            {
                'message': "Empty table",
                'token': token,
                'test_length': test_length
            }
        )
    interro_category = get_interro_category(interro=premier_test)
    save_interro_in_redis(
        interro=premier_test,
        token=token,
        interro_category=interro_category
    )
    save_loader_in_redis(
        loader=loader,
        token=token
    )
    json_response = JSONResponse(
        content=
        {
            'message': "Settings saved successfully",
            'token': token,
            "test_length": premier_test.words,
            "interro_category": interro_category
        }
    )
    return json_response


def get_interro_question(
        request,
        interro_category,
        total,
        count,
        score,
        token
    ):
    """
    API function to load the interro question.
    """
    user_name = auth_api.get_user_name_from_token(token=token)
    count = int(count)
    score = int(score)
    interro = load_interro_from_redis(
        token=token,
        interro_category=interro_category
    )
    progress_percent = int(count / int(total) * 100)
    index = interro.interro_df.index[count]
    english = interro.interro_df.loc[index][0]
    english = english.replace("'", "\'")
    count += 1
    response_dict = {
        "request": request,
        'token': token,
        "interroCategory": interro_category,
        "numWords": total,
        "userName": user_name,
        "count": count,
        "score": score,
        "progressPercent": progress_percent,
        "content_box1": english,
    }
    return response_dict


def load_interro_answer(
        request,
        interro_category,
        total,
        count,
        score,
        token
    ):
    """
    Load the interro answer.
    """
    total = int(total)
    count = int(count)
    score = int(score)
    progress_percent = int(count / total * 100)
    interro = load_interro_from_redis(
        token=token,
        interro_category=interro_category
    )
    index = interro.interro_df.index[count - 1]
    english = interro.interro_df.loc[index][0]
    english = english.replace("'", "\'")
    french = interro.interro_df.loc[index][1]
    french = french.replace("'", "\'")
    response_dict = {
        "request": request,
        "token": token,
        "interroCategory": interro_category,
        "numWords": total,
        "count": count,
        "score": score,
        "progressPercent": progress_percent,
        "content_box1": english,
        "content_box2": french
    }
    return response_dict


def get_user_answer(
        data,
        token
    ):
    """
    Get the user response.
    """
    interro_category = data.get('interroCategory')
    interro = load_interro_from_redis(
        token=token,
        interro_category=interro_category
    )
    score = data.get('score')
    score = int(score)
    if data["answer"] == 'Yes':
        score += 1
        update = True
    elif data["answer"] == 'No':
        update = False
        interro.update_faults_df(
            word_guessed=False,
            row=[
                data.get('english'),
                data.get('french')
            ]
        )
    if interro_category == 'test':
        interro.update_voc_df(word_guessed=update)
    save_interro_in_redis(
        interro=interro,
        token=token,
        interro_category=interro_category
    )
    json_response = JSONResponse(
        content=
        {
            "message": "User response stored successfully",
            'token': token,
            "interroCategory": interro_category,
            "score": score,
        }
    )
    return json_response


def propose_rattraps(
        request,
        interro_category,
        total,
        score,
        token
    ):
    """
    Propose the rattraps.
    """
    interro = load_interro_from_redis(
        token=token,
        interro_category=interro_category
    )
    new_total = interro.faults_df.shape[0]
    # Enregistrer les résultats
    if interro_category == 'test':
        interro.compute_success_rate()
        loader = load_loader_from_redis(token=token)
        updater = Updater(
            loader=loader,
            interro=interro
        )
        updater.update_data()
    # Réinitialisation
    response_dict = {
        "request": request,
        "token": token,
        "interroCategory": interro_category,
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
    interro_category = data.get('interroCategory')
    interro = load_interro_from_redis(
        token=token,
        interro_category=interro_category
    )
    if interro_category == 'rattrap':
        rattraps_cnt = interro.rattraps + 1
    else:
        rattraps_cnt = 0
    guesser = api_view.FastapiGuesser()
    interro.faults_df = interro.faults_df.sample(frac=1)
    interro.faults_df = interro.faults_df.reset_index(drop=True)
    rattrap = core_interro.Rattrap(
        faults_df_=interro.faults_df,
        rattraps=rattraps_cnt,
        guesser=guesser
    )
    new_interro_category = get_interro_category(interro=rattrap)
    save_interro_in_redis(
        interro=rattrap,
        token=token,
        interro_category=new_interro_category
    )
    count = int(data.get('count'))
    total = int(data.get('total'))
    score = int(data.get('score'))
    return JSONResponse(
        content=
        {
            'message': "Rattraps created successfully",
            'token': token,
            'interroCategory': new_interro_category,
            'total': total,
            'score': score,
            'count': count
        }
    )


def end_interro(
        request,
        interro_category,
        total,
        score,
        token
    ):
    """
    End the interro.
    """
    user_name = auth_api.get_user_name_from_token(token=token)
    logger.info(f"User: {user_name}")
    # Enregistrer les résultats
    if interro_category == 'test':
        interro = load_interro_from_redis(
            token=token,
            interro_category=interro_category
        )
        interro.compute_success_rate()
        loader = load_loader_from_redis(token=token)
        updater = Updater(
            loader=loader,
            interro=interro
        )
        updater.update_data()
    premier_test = load_interro_from_redis(
        token=token,
        interro_category='test'
    )
    headers, rows = turn_df_into_dict(
        words_df=premier_test.interro_df
    )
    response_dict = {
        "request": request,
        "token": token,
        "headers": headers,
        "rows": rows,
        "score": score,
        "numWords": total,
    }
    return response_dict


def get_error_messages(error_message: str):
    """
    Get the error messages from the error message.
    """
    messages = [
        "Empty table",
        "Settings saved successfully",
        ''
    ]
    if error_message == messages[0]:
        result = 'No words in the selected table'
    elif error_message == messages[1]:
        result = ''
    elif error_message == messages[2]:
        result = ''
    else:
        logger.error(f"Error message incorrect: {error_message}")
        logger.error(f"Should be in: {messages}")
        raise ValueError
    return result


def get_interro_category(interro: core_interro.Interro) -> str:
    """
    Check if the interro object is a premier test or a rattrap.
    """
    if hasattr(interro, 'perf') and hasattr(interro, 'step'):
        result = 'test'
    elif hasattr(interro, 'rattraps'):
        result = 'rattrap'
    else:
        logger.error('Unknown interro object, no perf, step or rattraps attribute.')
        raise ValueError
    return result


def turn_df_into_dict(words_df: pd.DataFrame) -> Dict:
    """
    Turn the dataframe into a dictionary.
    """
    headers = list(words_df.columns)
    rows = words_df.values.tolist()
    return headers, rows
