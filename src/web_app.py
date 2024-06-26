"""
    Author:
        Benoît DELORME
    Creation date:
        26th August 2023
    Main purpose:
        Vocabulary application in its FastAPI version.
"""

import os
import sys

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from fastapi import FastAPI, Depends, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

from src.routers import common_router, dashboard_router, database_router, guest_router, interro_router, user_router
from src.api import authentication

app = FastAPI(
    title="vocabulary",
    docs_url="/docs",
    # servers=[{"url": "https://www.vocabulary-app.com"}],
)
# Sessions
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ.get("SECRET_KEY")
)
# Routers
app.include_router(common_router)
app.include_router(dashboard_router)
app.include_router(database_router)
app.include_router(guest_router)
app.include_router(interro_router)
app.include_router(user_router)
# CSS
app.mount(
    "/static",
    StaticFiles(directory="src/static"),
    name="static"
)
# HTML
templates = Jinja2Templates(directory="src/templates")


@app.get("/", response_class=HTMLResponse)
async def root_page(
        request: Request,
        token: str = Depends(authentication.create_token)
    ):
    """
    Redirects to the welcome page.
    """
    return RedirectResponse(url="/welcome")


@app.get("/welcome", response_class=HTMLResponse)
async def welcome_page(
        request: Request,
        token: str = Depends(authentication.create_token)
    ):
    """
    Call the welcome page and assign a token to the guest.
    """
    response_dict = {'request': request, 'token': token}
    return templates.TemplateResponse(
        "welcome.html",
        response_dict
    )


@app.get("/sign-in", response_class=HTMLResponse)
def sign_in(
        request: Request,
        token: str = Depends(authentication.check_token),
        error_message: str = Query('', alias='errorMessage')
    ):
    """
    Call the sign-in page.
    """
    response_dict = authentication.sign_in(request, token, error_message)
    return templates.TemplateResponse(
        "user/sign_in.html",
        response_dict
    )


@app.get("/sign-up", response_class=HTMLResponse)
def sign_up(
        request: Request,
        token: str = Depends(authentication.check_token),
        error_message: str = Query('', alias='errorMessage')
    ):
    """
    Call the create account page.
    """
    response_dict = {'request': request, 'errorMessage': error_message, 'token': token}
    return templates.TemplateResponse(
        "user/sign_up.html",
        response_dict
    )


@app.get("/about-the-app", response_class=HTMLResponse)
def about_the_app(
        request: Request,
        token: str = Depends(authentication.check_token)
    ):
    """
    Call the page that helps the user to get started.
    """
    response_dict = {'request': request, 'token': token}
    return templates.TemplateResponse(
        "about_the_app.html",
        response_dict
    )


@app.get("/help", response_class=HTMLResponse)
def get_help(
        request: Request,
        token: str = Depends(authentication.check_token)
    ):
    """
    Help!
    """
    response_dict = {'request': request, 'token': token}
    return templates.TemplateResponse(
        "help.html",
        response_dict
    )
