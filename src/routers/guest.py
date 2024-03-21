"""
    Creation date:
        4th February 2024
    Main purpose:
        Gathers API routes dedicated to guest space.
        The guest is able to do some tests, but nothing more.
        - this page should NOT contain pages like settings, add word, ...
        - a guest should not access the 'root' page, even by accident.
"""

import json
import pickle
import os
import sys

# import base64
import pandas as pd
from fastapi import Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src.data import users
from src.api import authentication as auth_api
from src.api.interro import load_test, save_test_in_redis, load_test_from_redis

guest_router = APIRouter(prefix='/guest')
cred_checker = users.CredChecker()
templates = Jinja2Templates(directory="src/templates")


with open('conf/hum.json', 'r') as json_file:
    HUM = json.load(json_file)


@guest_router.get("/interro-settings", response_class=HTMLResponse)
def interro_settings_guest(
        request: Request,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Call the page that gets the user settings for one interro.
    """
    return templates.TemplateResponse(
        "guest/settings.html",
        {
            'request': request,
            'token': token
        }
    )


@guest_router.post("/save-interro-settings")
async def save_interro_settings_guest(
        settings: dict,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Acquire the user settings for one interro.
    """
    _, test = load_test(
        user_name='wh0Are_y0u',
        db_name=HUM['user']['guest']['databases'][0],
        test_type=settings['testType'].lower(),
        test_length=settings['numWords'],
        password=HUM['user']['guest']['OK']
    )
    save_test_in_redis(test, token)
    response = JSONResponse(
        content=
        {
            'message': "Guest user settings stored successfully.",
            'token': token
        }
    )
    return response


@guest_router.get("/interro-question/{words}/{count}/{score}", response_class=HTMLResponse)
def load_interro_question_guest(
        request: Request,
        words: int,
        count=None,
        score=None,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Call the page that asks the user the meaning of a word
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
    return templates.TemplateResponse(
        "guest/question.html",
        {
            'request': request,
            'numWords': words,
            'count': count,
            'score': score,
            'progressPercent': progress_percent,
            'content_box1': english,
            'token': token
        }
    )


@guest_router.get("/interro-answer/{words}/{count}/{score}", response_class=HTMLResponse)
def load_interro_answer_guest(
        request: Request,
        words: int,
        count: int,
        score: int,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Call the page that displays the right answer
    Asks the user to tell if his guess was right or wrong.
    """
    test = load_test_from_redis(token)
    count = int(count)
    index = test.interro_df.index[count - 1]
    english = test.interro_df.loc[index][0]
    french = test.interro_df.loc[index][1]
    english = english.replace("'", "\'")
    french = french.replace("'", "\'")
    progress_percent = int(count / int(words) * 100)
    return templates.TemplateResponse(
        "guest/answer.html",
        {
            "request": request,
            "numWords": words,
            "count": count,
            "score": score,
            "progressPercent": progress_percent,
            "content_box1": english,
            "content_box2": french,
            'token': token
        }
    )


@guest_router.post("/user-answer")
async def get_user_response_guest(
        data: dict,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Acquire the user decision: was his answer right or wrong.
    """
    test = load_test_from_redis(token)
    score = data.get('score')
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
    return JSONResponse(
        content=
        {
            'score': score,
            'message': "User response stored successfully.",
            'token': token
        }
    )


@guest_router.get("/propose-rattraps/{words}/{count}/{score}", response_class=HTMLResponse)
def propose_rattraps_guest(
        request: Request,
        words: int,
        count: int,
        score: int,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Load a page that proposes the user to take a rattraps, or leave the test.
    """
    test = load_test_from_redis(token)
    # Réinitialisation
    new_count = 0
    new_score = 0
    new_words = test.faults_df.shape[0]
    test.interro_df = test.faults_df
    test.faults_df = pd.DataFrame(columns=[['Foreign', 'Native']])
    save_test_in_redis(test, token)
    return templates.TemplateResponse(
        "guest/rattraps.html",
        {
            'request': request,
            'score': score,
            'numWords': words,
            'count': count,
            'newScore': new_score,
            'newWords': new_words,
            'newCount': new_count,
            'token': token
        }
    )


@guest_router.get("/interro-end/{words}/{score}", response_class=HTMLResponse)
def end_interro_guest(
        request: Request,
        words: int,
        score: int,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Page that ends the interro with a congratulation message,
    or a blaming message depending on the performance.
    """
    return templates.TemplateResponse(
        "guest/end.html",
        {
            'request': request,
            'score': score,
            'numWords': words,
            'token': token
        }
    )
