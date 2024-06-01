"""
    Creation date:
        4th February 2024
    Main purpose:
        Gathers API routes dedicated to user interooooo!!!!!
"""

import os
import sys

# from loguru import logger
from fastapi import Body, Depends, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.api import authentication as auth_api
from src.api import interro as interro_api

interro_router = APIRouter(prefix='/v1/interro')
templates = Jinja2Templates(directory="src/templates")


@interro_router.get("/interro-settings", response_class=HTMLResponse)
def interro_settings(
        request: Request,
        token: str = Depends(auth_api.check_token),
        error_message: str = Query('', alias='errorMessage')
    ):
    """
    Call the page that gets the user settings for one interro.
    """
    response_dict = interro_api.get_interro_settings(request, token, error_message)
    return templates.TemplateResponse(
        "interro/settings.html",
        response_dict
    )


@interro_router.post("/save-interro-settings")
async def save_interro_settings(
        settings: dict,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Save the user settings for the interro.
    """
    json_response = interro_api.save_interro_settings(settings, token)
    return json_response


@interro_router.get("/interro-question", response_class=HTMLResponse)
def load_interro_question(
        request: Request,
        interro_category: str=Query(None, alias="interroCategory"),
        total: str=Query(None, alias="total"),
        count: str=Query(None, alias="count"),
        score: str=Query(None, alias="score"),
        token: str=Depends(auth_api.check_token)
    ):
    """
    Call the page that asks the user the meaning of a word.
    """
    response_dict = interro_api.get_interro_question(
        request,
        interro_category,
        total,
        count,
        score,
        token
    )
    return templates.TemplateResponse(
        "interro/question.html",
        response_dict
    )


@interro_router.get("/interro-answer", response_class=HTMLResponse)
def load_interro_answer(
        request: Request,
        interro_category: str=Query(None, alias="interroCategory"),
        total: str=Query(None, alias="total"),
        count: str=Query(None, alias="count"),
        score: str=Query(None, alias="score"),
        token: str=Depends(auth_api.check_token)
    ):
    """
    Call the page that displays the right answer
    Asks the user to tell if his guess was right or wrong.
    """
    request_dict = interro_api.load_interro_answer(
        request,
        interro_category,
        total,
        count,
        score,
        token
    )
    return templates.TemplateResponse(
        "interro/answer.html",
        request_dict
    )


@interro_router.post("/user-answer")
async def get_user_answer(
        data: dict = Body(...),
        token: str = Depends(auth_api.check_token)
    ):
    """
    Acquire the user decision: was his answer right or wrong.
    """
    json_response = interro_api.get_user_answer(data, token)
    return json_response


@interro_router.get("/propose-rattraps", response_class=HTMLResponse)
def propose_rattraps(
        request: Request,
        interro_category: str=Query(None, alias="interroCategory"),
        total: str = Query(None, alias="total"),
        score: str = Query(None, alias="score"),
        token: str = Depends(auth_api.check_token)
    ):
    """
    Load a page that proposes the user to take a rattraps, or leave the test.
    """
    response_dict = interro_api.propose_rattraps(
        request,
        interro_category,
        total,
        score,
        token
    )
    return templates.TemplateResponse(
        "interro/rattraps.html",
        response_dict
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
        interro_category: str=Query(None, alias="interroCategory"),
        total: str=Query(None, alias="total"),
        score: str=Query(None, alias="score"),
        token: str=Depends(auth_api.check_token)
    ):
    """
    Page that ends the interro with a congratulation message,
    or a blaming message depending on the performances.
    """
    response_dict = interro_api.end_interro(
        request,
        interro_category,
        total,
        score,
        token
    )
    return templates.TemplateResponse(
        "interro/end.html",
        response_dict
    )
