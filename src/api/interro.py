"""
    Creation date:
        23rd February 2024
    Creator:
        B. Delorme
    Main purpose:
        Hosts the functions of interro API.
"""

import json
import os
import sys

import html
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
    loader = core_interro.Loader(
        words=test_length,
        data_querier=db_querier
    )
    loader.load_tables()
    loader.set_interro_df()
    guesser = api_view.FastapiGuesser()
    premier_test = core_interro.PremierTest(
        interro_df=loader.interro_df,
        words=loader.words,
        guesser=guesser
    )
    return loader, premier_test


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
    except ValueError as exc:
        logger.error(exc)
        return JSONResponse(
            content=
            {
                'message': "Empty table",
                'token': token,
                'test_length': test_length
            }
        )
    interro_category = get_interro_category(
        interro=premier_test
    )
    save_interro_in_redis(
        interro=premier_test,
        token=token,
        interro_category=interro_category
    )
    save_loader_in_redis(
        loader=loader,
        token=token
    )
    # -----
    response_dict = premier_test.to_dict()
    response_dict['token'] = token
    response_dict['message'] = "Settings saved successfully"
    response_dict['interro_category'] = interro_category
    # -----
    json_response = JSONResponse(
        content=response_dict
    )
    return json_response


def get_interro_question(
        request,
        token,
        message,
        interro_category,
        interro_dict,
        test_length,
        index,
        faults_dict,
        perf,
        count,
        score
    ):
    """
    API function to load the interro question.
    """
    count = int(count)
    test_length = int(test_length)
    progress_percent = int(count / test_length * 100)
    interro_df = prepare_interro_df(interro_dict)
    index = int(index)
    english = interro_df.iloc[index][0]
    english = english.replace("'", "\'")
    count += 1
    response_dict = {
        'request': request,
        'token': token,
        'message': message,
        'interroCategory': interro_category,
        'interroDict': interro_dict,
        'testLength': test_length,
        'index': index,
        'faultsDict': faults_dict,
        'perf': perf,
        'count': count,
        'score': score,
        'progressPercent': progress_percent,
        'content_box1': english,
    }
    return response_dict


def load_interro_answer(
        request,
        token,
        interro_category,
        interro_dict,
        test_length,
        index,
        faults_dict,
        perf,
        count,
        score
    ):
    """
    Load the interro answer.
    """
    count = int(count)
    test_length = int(test_length)
    progress_percent = int(count / test_length * 100)
    interro_df = prepare_interro_df(interro_dict)
    index = int(index)
    english = interro_df.iloc[index][0]
    english = english.replace("'", "\'")
    french = interro_df.iloc[index][1]
    french = french.replace("'", "\'")
    response_dict = {
        'request': request,
        'token': token,
        'interroCategory': interro_category,
        'interroDict': interro_dict,
        'testLength': test_length,
        'index': index,
        'faultsDict': faults_dict,
        'perf': perf,
        'count': count,
        'score': score,
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
    score = data.get('score')
    score = int(score)
    interro_df = prepare_interro_df(data.get('interroDict'))
    logger.debug(f"Faults dict: {data.get('faultsDict')}")
    fault_df = prepare_interro_df(data.get('faultsDict'))
    index = int(data.get('index'))
    interro = core_interro.PremierTest.from_dict({
        'test_length': data.get('testLength'),
        'interro_df': interro_df,
        'faults_df': fault_df,
        'index': index,
        'row': data.get('row'),
        'perf': data.get('perf')
    })
    if data["answer"] == 'Yes':
        score += 1
        update = True
    elif data["answer"] == 'No':
        update = False
        english = interro_df.iloc[index][0]
        english = english.replace("'", "\'")
        french = interro_df.iloc[index][1]
        french = french.replace("'", "\'")
        interro.update_faults_df(
            word_guessed=False,
            row=[english, french]
        )
    interro_category = data.get('interroCategory')
    if interro_category == 'test':
        interro.update_interro_df(word_guessed=update)
    attributes_dict = interro.to_dict()
    attributes_dict['message'] = "User response stored successfully"
    attributes_dict['token'] = token
    attributes_dict['interroCategory'] = interro_category
    attributes_dict['score'] = score
    json_response = JSONResponse(
        content=attributes_dict
    )
    return json_response


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
        # -----
        attributes_dict = interro.to_dict()
        # -----
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
    # -----
    attributes_dict = premier_test.to_dict()
    # -----
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
    interro.reshuffle_words_table()
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
    # -----
    attributes_dict = rattrap.to_dict()
    # -----
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
    if hasattr(interro, 'perf'):
        result = 'test'
    elif hasattr(interro, 'rattraps'):
        result = 'rattrap'
    else:
        logger.error("Unknown interro object: no perf or rattraps attribute!")
        raise ValueError
    return result


def turn_df_into_dict(words_df: pd.DataFrame) -> Dict:
    """
    Turn the dataframe into a dictionary.
    """
    headers = list(words_df.columns)
    rows = words_df.values.tolist()
    return headers, rows


def prepare_interro_df(interro_dict):
    """
    Prepare interro_df for words extraction.
    """
    # Two times escaping is necessary
    interro_dict = html.unescape(interro_dict)
    interro_dict = html.unescape(interro_dict)
    interro_json = json.loads(interro_dict)
    interro_df = pd.DataFrame(interro_json)
    return interro_df
