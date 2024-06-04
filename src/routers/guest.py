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
from src.api import guest as guest_api

guest_router = APIRouter(prefix='/v1/guest')
templates = Jinja2Templates(directory="src/templates")


@guest_router.get("/interro-settings", response_class=HTMLResponse)
def interro_settings_guest(
        request: Request,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Call the page that gets the user settings for one interro.
    """
    response_dict = guest_api.load_guest_settings(
        request=request,
        token=token
    )
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
    json_response = guest_api.save_interro_settings_guest(
        language=language,
        token=token
    )
    return json_response


@guest_router.get("/interro-question", response_class=HTMLResponse)
def load_interro_question_guest(
        request: Request,
        interro_category: str=Query(None, alias="interroCategory"),
        total: str=Query(None, alias="total"),
        count: str=Query(None, alias="count"),
        score: str=Query(None, alias="score"),
        token: str = Depends(auth_api.check_token),
        language: str = Query('', alias='language')
    ):
    """
    Call the page that asks the user the meaning of a word
    """
    response_dict = guest_api.load_interro_question_guest(
        request=request,
        interro_category=interro_category,
        total=total,
        count=count,
        score=score,
        language=language,
        token=token
    )
    return templates.TemplateResponse(
        "guest/question.html",
        response_dict
    )


@guest_router.get("/interro-answer", response_class=HTMLResponse)
def load_interro_answer_guest(
        request: Request,
        interro_category: str=Query(None, alias="interroCategory"),
        total: str=Query(None, alias="total"),
        count: str=Query(None, alias="count"),
        score: str=Query(None, alias="score"),
        token: str = Depends(auth_api.check_token),
        language: str = Query('', alias='language')
    ):
    """
    Call the page that displays the right answer
    Asks the user to tell if his guess was right or wrong.
    """
    response_dict = guest_api.load_interro_answer_guest(
        request=request,
        interro_category=interro_category,
        total=total,
        count=count,
        score=score,
        token=token,
        language=language
    )
    return templates.TemplateResponse(
        "guest/answer.html",
        response_dict
    )


@guest_router.post("/user-answer")
async def get_user_response_guest(
        data: dict = Body(...),
        token: str = Depends(auth_api.check_token)
    ):
    """
    Acquire the user decision: was his answer right or wrong.
    """
    json_response = guest_api.get_user_response_guest(
        data=data,
        token=token
    )
    return json_response


@guest_router.get("/propose-rattraps", response_class=HTMLResponse)
def propose_rattraps_guest(
        request: Request,
        interro_category: str=Query(None, alias="interroCategory"),
        total: str = Query(None, alias="total"),
        score: str = Query(None, alias="score"),
        token: str = Depends(auth_api.check_token),
        language: str = Query('', alias='language')
    ):
    """
    Load a page that proposes the user to take a rattraps, or leave the test.
    """
    response_dict = guest_api.propose_rattraps_guest(
        request=request,
        interro_category=interro_category,
        total=total,
        score=score,
        token=token,
        language=language
    )
    return templates.TemplateResponse(
        "guest/rattraps.html",
        response_dict
    )


@guest_router.post("/launch-guest-rattraps", response_class=HTMLResponse)
async def launch_rattraps(
        data: dict = Body(...),
        token: str = Depends(auth_api.check_token)
    ):
    """
    Load the rattraps page.
    """
    json_response = guest_api.load_rattraps(
        data,
        token
    )
    return json_response


@guest_router.get("/interro-end/", response_class=HTMLResponse)
def end_interro_guest(
        request: Request,
        total: str=Query(None, alias="total"),
        score: str=Query(None, alias="score"),
        token: str = Depends(auth_api.check_token)
    ):
    """
    Page that ends the interro with a congratulation message,
    or a blaming message depending on the performance.
    """
    response_dict = guest_api.end_interro_guest(
        request=request,
        total=total,
        score=score,
        token=token
    )
    return templates.TemplateResponse(
        "guest/end.html",
        response_dict
    )
