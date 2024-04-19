
import json
import os
import sys

import pandas as pd
# from loguru import logger
from typing import Dict

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from fastapi.responses import JSONResponse
from src.api.interro import load_test, save_test_in_redis, load_test_from_redis

WORDS = 10


def get_flags_dict() -> Dict:
    """
    Based on the result of the POST method, returns the corresponding error messages
    that will feed the sign-in html page.
    """
    flags_dict = {}
    with open('conf/languages.json', encoding='utf-8') as f:
        flags_dict = json.load(f)
    flags_dict = {
        k: v['flag']
        for k, v in flags_dict.items()
    }
    return flags_dict


def load_guest_settings(request, token):
    flags_dict = get_flags_dict()
    response_dict = flags_dict.copy()
    response_dict['request'] = request
    response_dict['token'] = token
    return response_dict


def save_interro_settings_guest(language, token):
    language = language['language'].lower()
    test_type = 'version'
    _, test = load_test(
        user_name=os.environ['VOC_GUEST_NAME'],
        db_name=language,
        test_type=test_type,
        test_length=WORDS
    )
    save_test_in_redis(test, token)
    json_response = JSONResponse(
        content=
        {
            'message': "Guest user settings stored successfully.",
            'token': token
        }
    )
    return json_response


def load_interro_question_guest(
        request,
        words,
        count,
        score,
        language,
        token: str
    ):
    """
    Load the interro question for the guest user.
    """
    try:
        count = int(count)
    except NameError:
        count = 0
    try:
        score = int(score)
    except NameError:
        score = 0
    test = load_test_from_redis(token)
    progress_percent = int(count / int(words) * 100)
    index = test.interro_df.index[count]
    english = test.interro_df.loc[index][0]
    english = english.replace("'", "\'")
    count += 1
    flags_dict = get_flags_dict()
    response_dict = {
        'request': request,
        'numWords': words,
        'count': count,
        'score': score,
        'progressPercent': progress_percent,
        'content_box1': english,
        'token': token,
        'language': language,
        'flag': flags_dict[language]
    }
    return response_dict


def load_interro_answer_guest(
        request,
        words,
        count,
        score,
        token,
        language
    ):
    test = load_test_from_redis(token)
    count = int(count)
    index = test.interro_df.index[count - 1]
    english = test.interro_df.loc[index][0]
    french = test.interro_df.loc[index][1]
    english = english.replace("'", "\'")
    french = french.replace("'", "\'")
    progress_percent = int(count / int(words) * 100)
    flags_dict = get_flags_dict()
    response_dict = {
        "request": request,
        "numWords": words,
        "count": count,
        "score": score,
        "progressPercent": progress_percent,
        "content_box1": english,
        "content_box2": french,
        'token': token,
        'language': language,
        'flag': flags_dict[language]
    }
    return response_dict


def get_user_response_guest(
        data,
        token
    ):
    test = load_test_from_redis(token)
    score = data.get('score')
    score = int(score)
    if data["answer"] == 'Yes':
        score += 1
        test.update_voc_df(True)
    elif data["answer"] == 'No':
        test.update_voc_df(False)
        test.update_faults_df(
            False,
            [
                data.get('english'),
                data.get('french')
            ]
        )
    save_test_in_redis(test, token)
    json_response = JSONResponse(
        content=
        {
            'score': score,
            'message': "User response stored successfully.",
            'token': token
        }
    )
    return json_response


def propose_rattraps_guest(
        request,
        words,
        count,
        score,
        token,
        language
    ):
    test = load_test_from_redis(token)
    new_count = 0
    new_score = 0
    new_words = test.faults_df.shape[0]
    test.interro_df = test.faults_df
    test.faults_df = pd.DataFrame(columns=[['Foreign', 'Native']])
    save_test_in_redis(test, token)
    response_dict = {
        'request': request,
        'score': score,
        'numWords': words,
        'count': count,
        'newScore': new_score,
        'newWords': new_words,
        'newCount': new_count,
        'token': token,
        'language': language
    }
    return response_dict
