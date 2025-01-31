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
from typing import Any, Dict

from fastapi import Request
from fastapi.responses import JSONResponse
import pandas as pd

from src import interro as core_interro
from src.api.interro import load_test, get_interro_category, turn_df_into_dict
from src.data.redis_interface import save_interro_in_redis, load_interro_from_redis
from src.views import api as api_view



# --------------- API functions --------------- #
def load_guest_settings(request: Request, token: str) -> dict:
    """
    Load guest user settings.
    """
    flags_dict = get_flags_dict()
    settings_dict = flags_dict.copy()
    settings_dict['request'] = request
    settings_dict['token'] = token
    return settings_dict


def save_interro_settings_guest(language: dict, token: str) -> JSONResponse:
    """
    Save guest user interro settings.
    """
    language = language['testLanguage'].lower()
    test_type = 'version'
    _, test = load_test(
        user_name=os.environ['VOC_GUEST_NAME'],
        db_name=language,
        test_type=test_type,
        test_length=10
    )
    interro_category = get_interro_category(test)
    save_interro_in_redis(
        interro=test,
        token=token,
        interro_category=interro_category
    )
    json_response = JSONResponse(
        content=
        {
            'message': "Guest user settings stored successfully",
            'token': token,
            'interroCategory': interro_category
        }
    )
    return json_response


def load_interro_question_guest(
        request: Request,
        interro_category: str,
        total: str,
        count: str,
        score: str,
        language: str,
        token: str,
    ) -> Dict[str, Any]:
    """
    Load the interro question for the guest user.
    """
    total = int(total)
    count = int(count)
    score = int(score)
    progress_percent = int(count / int(total) * 100)
    interro = load_interro_from_redis(
        token=token,
        interro_category=interro_category
    )
    index = interro.interro_df.index[count]
    foreign_word = interro.interro_df.loc[index][0]
    foreign_word = foreign_word.replace("'", "\'")
    count += 1
    flags_dict = get_flags_dict()
    response_dict = {
        'contentBox1': foreign_word,
        'flag': flags_dict[language],
        'interroCategory': interro_category,
        'testCount': count,
        'testLanguage': language,
        'testLength': total,
        'testScore': score,
        'progressPercent': progress_percent,
        'request': request,
        'token': token,
    }
    return response_dict


def load_interro_answer_guest(
        request: Request,
        interro_category: str,
        total: str,
        count: str,
        score: str,
        token: str,
        language: str
    ) -> Dict[str, Any]:
    """
    Load the interro answer for the guest user.
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
    foreign_word = interro.interro_df.loc[index][0]
    foreign_word = foreign_word.replace("'", "\'")
    native_word = interro.interro_df.loc[index][1]
    native_word = native_word.replace("'", "\'")
    flags_dict = get_flags_dict()
    response_dict = {
        "contentBox1": foreign_word,
        "contentBox2": native_word,
        'flag': flags_dict[language],
        "interroCategory": interro_category,
        "progressPercent": progress_percent,
        "request": request,
        "testCount": count,
        "testLength": total,
        "testScore": score,
        'testLanguage': language,
        'token': token,
    }
    return response_dict


def get_user_response_guest(
        data: Dict[str, Any],
        token: str
    ) -> JSONResponse:
    """
    Get the user response.
    data is a dictionnary with keys written in JS way.
    """
    interro_category = data.get('interroCategory')
    interro = load_interro_from_redis(
        token=token,
        interro_category=interro_category
    )
    score = data.get('testScore', 0)
    score = int(score)
    total = data.get('testLength', 0)
    total = int(total)
    if data['userAnswer'] == 'Yes':
        score += 1
    elif data['userAnswer'] == 'No':
        interro.update_faults_df(
            False,
            [
                data.get('foreignWord'),
                data.get('nativeWord')
            ]
        )
    save_interro_in_redis(
        interro=interro,
        token=token,
        interro_category=interro_category
    )
    json_response = JSONResponse(
        content=
        {
            'message': "User response stored successfully.",
            'token': token,
            'interroCategory': interro_category,
            'testScore': score,
            'testLength': total
        }
    )
    return json_response


def propose_rattrap_guest(
        request: Request,
        interro_category: str,
        total: str,
        score: str,
        language: str,
        token: str,
    ) -> Dict[str, Any]:
    """
    Propose the rattrap.
    """
    interro = load_interro_from_redis(
        token=token,
        interro_category=interro_category
    )
    new_total = interro.faults_df.shape[0]
    response_dict = {
        'interroCategory': interro_category,
        'newWords': new_total,
        'newScore': 0,
        'newCount': 0,
        'request': request,
        'testLanguage': language,
        'testLength': total,
        'testScore': score,
        'token': token,
    }
    return response_dict


def load_rattrap(
        data: Dict[str, Any],
        token: str
    ) -> JSONResponse:
    """
    Load the rattrap!
    """
    interro_category = data.get('interroCategory')
    interro = load_interro_from_redis(
        token=token,
        interro_category=interro_category
    )
    guesser = api_view.FastapiGuesser()
    interro.faults_df = interro.faults_df.sample(frac=1)
    interro.faults_df = interro.faults_df.reset_index(drop=True)
    rattrap = core_interro.Rattrap(
        interro_df=interro.faults_df,
        guesser=guesser,
        old_interro_df=pd.DataFrame(),
    )
    new_interro_category = get_interro_category(interro=rattrap)
    save_interro_in_redis(
        interro=rattrap,
        token=token,
        interro_category=new_interro_category
    )
    count = int(data.get('testCount', 0))
    total = int(data.get('testLength', 0))
    score = int(data.get('testScore', 0))
    return JSONResponse(
        content=
        {
            'interroCategory': new_interro_category,
            'message': "Guest rattrap created successfully",
            'testCount': count,
            'testLength': total,
            'testScore': score,
            'token': token,
        }
    )


def end_interro_guest(
        request: Request,
        total: str,
        score: str,
        token: str
    ) -> Dict[str, Any]:
    """
    API fucntion to end the interro for the guest user.
    """
    premier_test = load_interro_from_redis(
        token=token,
        interro_category='test'
    )
    interro_words = premier_test.interro_df[['foreign', 'native']]
    headers, rows = turn_df_into_dict(
        words_df=interro_words
    )
    response_dict = {
        'headers': headers,
        'testLength': total,
        'request': request,
        'rows': rows,
        'testScore': score,
        'token': token,
    }
    return response_dict


# --------------- Helper functions --------------- #
def get_flags_dict() -> Dict[ str, Any]:
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
