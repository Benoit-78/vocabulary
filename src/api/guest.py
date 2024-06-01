"""
    Creation date:
        How fast is an African swallow?
    Creator:
        B. Delorme
    Main purpose:
        Hosts the functions of guest interro API.
"""

import json
import os
import sys

from fastapi.responses import JSONResponse
from loguru import logger
from typing import Dict

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src import interro as core_interro
from src.api.interro import load_test, get_interro_category, turn_df_into_dict
from src.data.redis_interface import save_interro_in_redis, load_interro_from_redis
from src.views import api as api_view


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
    settings_dict = flags_dict.copy()
    settings_dict['request'] = request
    settings_dict['token'] = token
    return settings_dict


def save_interro_settings_guest(language, token):
    """
    Save guest user interro settings.
    """
    language = language['language'].lower()
    test_type = 'version'
    _, test = load_test(
        user_name=os.environ['VOC_GUEST_NAME'],
        db_name=language,
        test_type=test_type,
        test_length=10
    )
    interro_category = get_interro_category(test)
    save_interro_in_redis(test, token, interro_category)
    json_response = JSONResponse(
        content=
        {
            'message': "Guest user settings stored successfully",
            'token': token,
            "interro_category": interro_category
        }
    )
    return json_response


def load_interro_question_guest(
        request,
        interro_category,
        total,
        count,
        score,
        language,
        token: str,
    ):
    """
    Load the interro question for the guest user.
    """
    total = int(total)
    count = int(count)
    score = int(score)
    progress_percent = int(count / int(total) * 100)
    interro = load_interro_from_redis(token, interro_category)
    index = interro.interro_df.index[count]
    english = interro.interro_df.loc[index][0]
    english = english.replace("'", "\'")
    count += 1
    flags_dict = get_flags_dict()
    response_dict = {
        'request': request,
        'token': token,
        "interroCategory": interro_category,
        'numWords': total,
        'count': count,
        'score': score,
        'progressPercent': progress_percent,
        'content_box1': english,
        'language': language,
        'flag': flags_dict[language]
    }
    return response_dict


def load_interro_answer_guest(
        request,
        interro_category,
        total,
        count,
        score,
        token,
        language
    ):
    total = int(total)
    count = int(count)
    score = int(score)
    progress_percent = int(count / total * 100)
    interro = load_interro_from_redis(token, interro_category)
    index = interro.interro_df.index[count - 1]
    english = interro.interro_df.loc[index][0]
    english = english.replace("'", "\'")
    french = interro.interro_df.loc[index][1]
    french = french.replace("'", "\'")
    flags_dict = get_flags_dict()
    response_dict = {
        "request": request,
        'token': token,
        "interroCategory": interro_category,
        "numWords": total,
        "count": count,
        "score": score,
        "progressPercent": progress_percent,
        "content_box1": english,
        "content_box2": french,
        'language': language,
        'flag': flags_dict[language]
    }
    return response_dict


def get_user_response_guest(
        data,
        token
    ):
    interro_category = data.get('interroCategory')
    interro = load_interro_from_redis(token, interro_category)
    score = data.get('score')
    score = int(score)
    total = data.get('total')
    total = int(total)
    if data["answer"] == 'Yes':
        score += 1
    elif data["answer"] == 'No':
        interro.update_faults_df(
            False,
            [
                data.get('english'),
                data.get('french')
            ]
        )
    save_interro_in_redis(interro, token, interro_category)
    json_response = JSONResponse(
        content=
        {
            'message': "User response stored successfully.",
            'token': token,
            "interroCategory": interro_category,
            'score': score,
            'total': total
        }
    )
    return json_response


def propose_rattraps_guest(
        request,
        interro_category,
        total,
        score,
        language,
        token,
    ):
    """
    Propose the rattraps.
    """
    interro = load_interro_from_redis(token, interro_category)
    new_total = interro.faults_df.shape[0]
    response_dict = {
        'request': request,
        'token': token,
        "interroCategory": interro_category,
        "newWords": new_total,
        "newScore": 0,
        "newCount": 0,
        "score": score,
        "numWords": total,
        'language': language
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
    interro = load_interro_from_redis(token, interro_category)
    if interro_category == 'rattrap':
        rattraps_cnt = interro.rattraps + 1
    else:
        rattraps_cnt = 0
    guesser = api_view.FastapiGuesser()
    interro.faults_df = interro.faults_df.sample(frac=1)
    interro.faults_df = interro.faults_df.reset_index(drop=True)
    rattrap = core_interro.Rattrap(
        interro.faults_df,
        rattraps_cnt,
        guesser
    )
    new_interro_category = get_interro_category(rattrap)
    save_interro_in_redis(rattrap, token, new_interro_category)
    count = int(data.get('count'))
    total = int(data.get('total'))
    score = int(data.get('score'))
    return JSONResponse(
        content=
        {
            'message': "Guest rattraps created successfully",
            'token': token,
            'interroCategory': new_interro_category,
            'total': total,
            'score': score,
            'count': count
        }
    )


def end_interro_guest(
        request,
        total,
        score,
        token
    ):
    logger.info('')
    premier_test = load_interro_from_redis(token, 'test')
    headers, rows = turn_df_into_dict(premier_test.interro_df)
    response_dict = {
        'request': request,
        'token': token,
        "headers": headers,
        "rows": rows,
        'score': score,
        'numWords': total
    }
    return response_dict
