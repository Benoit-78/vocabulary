"""
    Creation date:
        4th February 2024
    Main purpose:
        Gathers API routes dedicated to user interooooo!!!!!
"""

import os
import sys

import pandas as pd
from loguru import logger
from fastapi import Query, Request, Depends, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.interro import Updater
from src.api import authentication as auth_api
from src.api import database as database_api
from src.api import interro as interro_api
from src.data import users


interro_router = APIRouter(prefix='/interro')
cred_checker = users.CredChecker()
templates = Jinja2Templates(directory="src/templates")


@interro_router.get("/interro-settings", response_class=HTMLResponse)
def interro_settings(
        request: Request,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Call the page that gets the user settings for one interro.
    """
    databases = database_api.get_user_databases(token)
    return templates.TemplateResponse(
        "interro/settings.html",
        {
            'request': request,
            'token': token,
            'databases': databases
        }
    )


@interro_router.post("/save-interro-settings")
async def save_interro_settings(
        settings: dict,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Save the user settings for the interro.
    """
    user_name = auth_api.get_user_name_from_token(token)
    loader, test = interro_api.load_test(
        user_name=user_name,
        db_name=settings['databaseName'],
        test_type=settings['testType'].lower(),
        test_length=settings['numWords']
    )
    interro_api.save_loader_in_redis(loader, token)
    interro_api.save_test_in_redis(test, token)
    response = JSONResponse(
        content=
        {
            'message': "Guest user settings stored successfully",
            'token': token
        }
    )
    return response


@interro_router.get("/interro-question", response_class=HTMLResponse)
def load_interro_question(
        request: Request,
        total: str = Query(None, alias="total"),
        count: str = Query(None, alias="count"),
        score: str = Query(None, alias="score"),
        token: str = Depends(auth_api.check_token)
    ):
    """
    Call the page that asks the user the meaning of a word.
    """
    request_dict = interro_api.get_interro_question(
        request,
        token,
        total,
        count,
        score
    )
    return templates.TemplateResponse(
        "interro/question.html",
        request_dict
    )


@interro_router.get("/interro-answer", response_class=HTMLResponse)
def load_interro_answer(
        request: Request,
        total: str = Query(None, alias="total"),
        count: str = Query(None, alias="count"),
        score: str = Query(None, alias="score"),
        token: str = Depends(auth_api.check_token)
    ):
    """
    Call the page that displays the right answer
    Asks the user to tell if his guess was right or wrong.
    """
    count = int(count)
    test = interro_api.load_test_from_redis(token)
    progress_percent = int(count / int(total) * 100)
    index = test.interro_df.index[count - 1]
    english = test.interro_df.loc[index][0]
    english = english.replace("'", "\'")
    french = test.interro_df.loc[index][1]
    french = french.replace("'", "\'")
    request_dict = {
        "request": request,
        "token": token,
        "numWords": total,
        "count": count,
        "score": score,
        "progressPercent": progress_percent,
        "content_box1": english,
        "content_box2": french
    }
    return templates.TemplateResponse(
        "interro/answer.html",
        request_dict
    )


@interro_router.post("/user-answer")
async def get_user_response(
        data: dict = Body(...),
        token: str = Depends(auth_api.check_token)
    ):
    """
    Acquire the user decision: was his answer right or wrong.
    """
    test = interro_api.load_test_from_redis(token)
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
    interro_api.save_test_in_redis(test, token)
    return JSONResponse(
        content=
        {
            "score": score,
            "message": "User response stored successfully"
        }
    )


@interro_router.get("/propose-rattraps", response_class=HTMLResponse)
def propose_rattraps(
        request: Request,
        total: str = Query(None, alias="total"),
        score: str = Query(None, alias="score"),
        token: str = Depends(auth_api.check_token)
    ):
    """
    Load a page that proposes the user to take a rattraps, or leave the test.
    """
    test = interro_api.load_test_from_redis(token)
    new_total = test.faults_df.shape[0]
    # Enregistrer les résultats
    if not hasattr(test, 'rattraps'):
        test.compute_success_rate()
        loader = interro_api.load_loader_from_redis(token)
        updater = Updater(loader, test)
        updater.update_data()
        logger.info("User data updated.")
    # Réinitialisation
    logger.debug(f"New words: {new_total}")
    return templates.TemplateResponse(
        "interro/rattraps.html",
        {
            "request": request,
            "token": token,
            "newTotal": new_total,
            "newScore": 0,
            "newCount": 0,
            "score": score,
            "numWords": total
        }
    )


@interro_router.post("/launch-rattraps", response_class=HTMLResponse)
async def launch_rattraps(
        data: dict = Body(...),
        token: str = Depends(auth_api.check_token)
    ):
    """
    Load the rattraps page.
    """
    json_response = interro_api.load_rattraps(token, data)
    return json_response


@interro_router.get("/interro-end", response_class=HTMLResponse)
def end_interro(
        request: Request,
        total: str = Query(None, alias="total"),
        score: str = Query(None, alias="score"),
        token: str = Depends(auth_api.check_token)
    ):
    """
    Page that ends the interro with a congratulation message,
    or a blaming message depending on the performances.
    """
    test = interro_api.load_test_from_redis(token)
    # Enregistrer les résultats
    if not hasattr(test, 'rattraps'):
        test.compute_success_rate()
        loader = interro_api.load_loader_from_redis(token)
        updater = Updater(loader, test)
        updater.update_data()
        logger.info("User data updated.")
    return templates.TemplateResponse(
        "interro/end.html",
        {
            "request": request,
            "score": score,
            "numWords": total,
            "token": token
        }
    )
