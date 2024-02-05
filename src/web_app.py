"""
    Author:
        Benoît DELORME
    Creation date:
        26th August 2023
    Main purpose:
        Vocabulary application in its FastAPI version.
"""

import json
import os
import sys

import pandas as pd
from fastapi import FastAPI, Query, Depends, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.routing import APIRouter
# from fastapi.session import Session
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src.data import users
from src.routers import user_router, interro_router, guest_router, database_router, dashboard_router

app = FastAPI(
    title="vocabulary",
    docs_url="/docs",
    redoc_url=None,
    servers=[{"url": "https://www.vocabulary-app.com"}],
)
GUEST_USER_NAME = 'guest'
GUEST_DB_NAME = 'vocabulary'
test = None
loader = None
flag_data_updated = None
cred_checker = users.CredChecker()

with open('conf/hum.json', 'r') as json_file:
    HUM = json.load(json_file)

with open('conf/data.json', 'r') as json_file:
    DATA = json.load(json_file)

# CSS files
app.mount(
    "/static",
    StaticFiles(directory="src/static"),
    name="static"
)

# HTML files
templates = Jinja2Templates(
    directory="src/templates"
)

app.include_router(user_router)
app.include_router(interro_router)
app.include_router(guest_router)
app.include_router(database_router)
app.include_router(dashboard_router)


@app.get("/", response_class=HTMLResponse)
def welcome_page(request: Request):
    """Call the welcome page"""
    return templates.TemplateResponse(
        "welcome.html",
        {
            "request": request,
        }
    )


@app.get("/sign-in", response_class=HTMLResponse)
def sign_in(request: Request):
    """Call the sign-in page"""
    return templates.TemplateResponse(
        "user/sign_in.html",
        {
            "request": request
        }
    )


@app.get("/create-account", response_class=HTMLResponse)
def create_account(request: Request):
    """
    Call the create account page
    """
    return templates.TemplateResponse(
        "user/create_account.html",
        {
            "request": request,
            "errorMessage": ""
        }
    )


@app.get("/about-the-app", response_class=HTMLResponse)
def about_the_app(request: Request):
    """Call the page that helps the user to get started."""
    return templates.TemplateResponse(
        "about_the_app.html",
        {
            "request": request,
        }
    )


@app.get("/help", response_class=HTMLResponse)
def get_help(request: Request):
    """Help!"""
    return templates.TemplateResponse(
        "help.html",
        {
            "request": request,
        }
    )


# ==================================================
#  UNIQUE SESSION
# ==================================================
# def get_session(request: Request):
#     """
#     Return the session object.
#     """
#     return Session(request=request)

# @app.get("/")
# async def read_item(session: Session = Depends(get_session)):
#     # Check the session for user-specific data
#     user_data = session.get("user_data", None)
#     if not user_data:
#         # Initialize user-specific data
#         user_data = initialize_user_data()
#         session["user_data"] = user_data
#     logger.debug(f"Session: {session}")
#     logger.debug(f"User data: {user_data}")
#     # return {"message": "Hello World", "user_data": user_data}
#     return templates.TemplateResponse(
#         "welcome.html",
#         {
#             "request": request,
#         }
#     )