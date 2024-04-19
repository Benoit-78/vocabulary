"""
    Creation date:
        4th February 2024
    Main purpose:
        Gathers API routes dedicated to guest space.
        The guest is able to do some tests, but nothing more.
        - this page should NOT contain pages like settings, add word, ...
        - a guest should not access the 'root' page, even by accident.
"""

import os
import sys

# import base64
import pandas as pd
from fastapi import Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src.data import users
from src.api import authentication as auth_api
from src.api import guest as guest_api

guest_router = APIRouter(prefix='/guest')
cred_checker = users.CredChecker()
templates = Jinja2Templates(directory="src/templates")


@guest_router.get("/interro-settings", response_class=HTMLResponse)
def interro_settings_guest(
        request: Request,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Call the page that gets the user settings for one interro.
    """
    response_dict = guest_api.load_guest_settings(request, token)
    return templates.TemplateResponse(
        "guest/settings.html",
        response_dict
    )


@guest_router.post("/save-interro-settings")
async def save_interro_settings_guest(
        language: dict,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Acquire the user settings for one interro.
    """
    json_response = guest_api.save_interro_settings_guest(language, token)
    return json_response


@guest_router.get("/interro-question/{words}/{count}/{score}", response_class=HTMLResponse)
def load_interro_question_guest(
        request: Request,
        words: int,
        count=None,
        score=None,
        token: str = Depends(auth_api.check_token),
        language: str = Query('', alias='language')
    ):
    """
    Call the page that asks the user the meaning of a word
    """
    response_dict = guest_api.load_interro_question_guest(
        request,
        words,
        count,
        score,
        language,
        token
    )
    return templates.TemplateResponse(
        "guest/question.html",
        response_dict
    )


@guest_router.get("/interro-answer/{words}/{count}/{score}", response_class=HTMLResponse)
def load_interro_answer_guest(
        request: Request,
        words: int,
        count: int,
        score: int,
        token: str = Depends(auth_api.check_token),
        language: str = Query('', alias='language')
    ):
    """
    Call the page that displays the right answer
    Asks the user to tell if his guess was right or wrong.
    """
    response_dict = guest_api.load_interro_answer_guest(
        request,
        words,
        count,
        score,
        token,
        language
    )
    return templates.TemplateResponse(
        "guest/answer.html",
        response_dict
    )


@guest_router.post("/user-answer")
async def get_user_response_guest(
        data: dict,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Acquire the user decision: was his answer right or wrong.
    """
    json_response = guest_api.get_user_response_guest(data, token)
    return json_response


@guest_router.get("/propose-rattraps/{words}/{count}/{score}", response_class=HTMLResponse)
def propose_rattraps_guest(
        request: Request,
        words: int,
        count: int,
        score: int,
        token: str = Depends(auth_api.check_token),
        language: str = Query('', alias='language')
    ):
    """
    Load a page that proposes the user to take a rattraps, or leave the test.
    """
    response_dict = guest_api.propose_rattraps_guest(
        request,
        words,
        count,
        score,
        token,
        language
    )
    return templates.TemplateResponse(
        "guest/rattraps.html",
        response_dict
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
    response_dict = {
        'request': request,
        'score': score,
        'numWords': words,
        'token': token
    }
    return templates.TemplateResponse(
        "guest/end.html",
        response_dict
    )
