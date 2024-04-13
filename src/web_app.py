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
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

from src.routers import user_router, interro_router, guest_router, database_router, dashboard_router
from src.api import authentication
from src.api import main as main_api

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
async def welcome_page(
        request: Request,
        token: str = Depends(authentication.create_token)
    ):
    """
    Call the welcome page and assign a token to the guest.
    """
    return templates.TemplateResponse(
        "welcome.html",
        {
            "request": request,
            "token": token,
        }
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
    name_message, password_message = main_api.get_error_messages(error_message)
    return templates.TemplateResponse(
        "user/sign_in.html",
        {
            'request': request,
            'token': token,
            'nameUnknownErrorMessage': name_message,
            'passwordIncorrectErrorMessage': password_message
        }
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
    logger.debug(f"token: {token}")
    logger.debug(f"error_message: {error_message}")
    return templates.TemplateResponse(
        "user/sign_up.html",
        {
            'request': request,
            'errorMessage': error_message,
            'token': token
        }
    )


@app.get("/about-the-app", response_class=HTMLResponse)
def about_the_app(
        request: Request,
        token: str = Depends(authentication.check_token)
    ):
    """
    Call the page that helps the user to get started.
    """
    return templates.TemplateResponse(
        "about_the_app.html",
        {
            "request": request,
            'token': token
        }
    )


@app.get("/help", response_class=HTMLResponse)
def get_help(
        request: Request,
        token: str = Depends(authentication.check_token)
    ):
    """
    Help!
    """
    return templates.TemplateResponse(
        "help.html",
        {
            "request": request,
            'token': token
        }
    )
