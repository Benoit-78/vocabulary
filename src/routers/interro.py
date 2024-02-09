"""
    Creation date:
        4th February 2024
    Main purpose:
        Gathers API routes dedicated to user interooooo !!!!!
"""

import os
import sys

import pandas as pd
from loguru import logger
from fastapi import Query, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src import interro, views
from src.utils import interro as interro_utils
from src.data import users, data_handler

interro_router = APIRouter()
cred_checker = users.CredChecker()
templates = Jinja2Templates(directory="src/templates")


@interro_router.get("/interro-settings", response_class=HTMLResponse)
def interro_settings(
    request: Request,
    query: str = Query(None, alias="userName")
    ):
    """Call the page that gets the user settings for one interro."""
    # Authenticate user
    user_name = query.split('?')[0]
    user_password = query.split('?')[1].split('=')[1]
    if user_name:
        cred_checker.check_credentials(user_name, user_password)
    else:
        logger.error("User name not found.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User name not found."
        )
    # Load settings page
    return templates.TemplateResponse(
        "user/interro_settings.html",
        {
            "request": request,
            "userName": user_name,
            "userPassword": user_password
        }
    )


@interro_router.get("/interro-question", response_class=HTMLResponse)
def load_interro_question(
    request: Request,
    query: str = Query(None, alias="userName")
    ):
    """Call the page that asks the user the meaning of a word"""
    # Authenticate user
    user_name = query.split('?')[0]
    user_password = query.split('?')[1].split('=')[1]
    if user_name:
        cred_checker.check_credentials(user_name, user_password
        )
    else:
        logger.error("User name not found.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User name not found."
        )
    # Load question page
    words = query.split('?')[2].split('=')[1]
    count = query.split('?')[3].split('=')[1]
    score = query.split('?')[4].split('=')[1]
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    global test
    try:
        count = int(count)
    except NameError:
        count = 0
    try:
        score = int(score)
    except NameError:
        score = 0
    progress_percent = int(count / int(words) * 100)
    index = test.interro_df.index[count]
    english = test.interro_df.loc[index][0]
    english = english.replace("'", "\'")
    count += 1
    return templates.TemplateResponse(
        "user/interro_question.html",
        {
            "request": request,
            "userName": user_name,
            "numWords": words,
            "count": count,
            "score": score,
            "progressPercent": progress_percent,
            "content_box1": english
        }
    )


@interro_router.get("/interro-answer/{user_name}/{words}/{count}/{score}", response_class=HTMLResponse)
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
    return templates.TemplateResponse(
        "user/interro_answer.html",
        {
            "request": request,
            "userName": user_name,
            "numWords": words,
            "count": count,
            "score": score,
            "progressPercent": progress_percent,
            "content_box1": english,
            "content_box2": french,
        }
    )


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
    score: int):
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
    new_count = 0
    new_score = 0
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
            "newScore": new_score,
            "newWords": new_words,
            "newCount": new_count
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
