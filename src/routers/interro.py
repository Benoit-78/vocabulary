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
from fastapi import Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from typing import Dict, Any

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.api import interro as interro_api
from src.data import users

interro_router = APIRouter(prefix='/interro')
cred_checker = users.CredChecker()
templates = Jinja2Templates(directory="src/templates")


@interro_router.post("/interro-settings", response_class=HTMLResponse)
def interro_settings(request: Request, input_dict: Dict[str, Any]):
    """
    Call the page that gets the user settings for one interro.
    """
    request_dict = interro_api.load_interro_settings(request, input_dict)
    return templates.TemplateResponse("user/interro_settings.html", request_dict)


@interro_router.get("/interro-question", response_class=HTMLResponse)
def load_interro_question(
    request: Request,
    user_name: str = Query(None, alias="userName"),
    user_password: str = Query(None, alias="userPassword"),
    db_name: str = Query(None, alias="databaseName"),
    test_type: str = Query(None, alias="testType"),
    total: str = Query(None, alias="total"),
    count: str = Query(None, alias="count"),
    score: str = Query(None, alias="score")
    ):
    """
    Call the page that asks the user the meaning of a word.
    """
    request_dict = interro_api.get_interro_question(
        request,
        user_name,
        user_password,
        db_name,
        test_type,
        total,
        count,
        score
    )
    return templates.TemplateResponse("user/interro_question.html", request_dict)


@interro_router.get("/interro-answer", response_class=HTMLResponse)
def load_interro_answer(
    request: Request,
    user_name,
    words: int,
    count: int,
    score: int):
    """
    Call the page that displays the right answer
    Asks the user to tell if his guess was right or wrong.
    """
    cred_checker.check_credentials(user_name)
    count = int(count)
    global test
    index = test.interro_df.index[count - 1]
    english = test.interro_df.loc[index][0]
    french = test.interro_df.loc[index][1]
    english = english.replace("'", "\'")
    french = french.replace("'", "\'")
    progress_percent = int(count / int(words) * 100)
    request_dict = {
        "request": request,
        "userName": user_name,
        "numWords": words,
        "count": count,
        "score": score,
        "progressPercent": progress_percent,
        "content_box1": english,
        "content_box2": french
    }
    request_dict = interro_api.get_user_response(user_name)
    return templates.TemplateResponse("user/interro_answer.html", request_dict)


@interro_router.post("/user-answer/{user_name}")
async def get_user_response(data: dict, user_name):
    """Acquire the user decision: was his answer right or wrong."""
    cred_checker.check_credentials(user_name)
    global test
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
    return JSONResponse(
        content=
        {
            "score": score,
            "message": "User response stored successfully."
        }
    )


@interro_router.get("/propose-rattraps/{user_name}/{words}/{count}/{score}", response_class=HTMLResponse)
def propose_rattraps(
    request: Request,
    user_name,
    words: int,
    count: int,
    score: int
    ):
    """Load a page that proposes the user to take a rattraps, or leave the test."""
    cred_checker.check_credentials(user_name)
    global test
    # Enregistrer les résultats
    global flag_data_updated
    if flag_data_updated is False:
        global loader
        test.compute_success_rate()
        updater = interro.Updater(loader, test)
        updater.update_data()
        logger.info("User data updated.")
        flag_data_updated = True
    else:
        logger.info("User data not updated yet.")
    # Réinitialisation
    new_words = test.faults_df.shape[0]
    test.interro_df = test.faults_df
    test.faults_df = pd.DataFrame(columns=[['Foreign', 'Native']])
    return templates.TemplateResponse(
        "user/rattraps_propose.html",
        {
            "request": request,
            "userName": user_name,
            "score": score,
            "numWords": words,
            "count": count,
            "newScore": 0,
            "newWords": new_words,
            "newCount": 0
        }
    )


@interro_router.get("/interro-end/{user_name}/{words}/{score}", response_class=HTMLResponse)
def end_interro(
    request: Request,
    user_name,
    words: int,
    score: int):
    """
    Page that ends the interro with a congratulation message,
    or a blaming message depending on the performances.
    """
    cred_checker.check_credentials(user_name)
    # Execution
    global flag_data_updated
    if flag_data_updated is False:
        global loader
        global test
        test.compute_success_rate()
        updater = interro.Updater(loader, test)
        updater.update_data()
        logger.info("User data updated.")
    return templates.TemplateResponse(
        "user/interro_end.html",
        {
            "request": request,
            "score": score,
            "numWords": words,
            "userName": user_name
        }
    )
