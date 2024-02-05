"""
    Creation date:
        4th February 2024
    Main purpose:
        Gathers API routes dedicated to user space.
"""

import os
import sys

from loguru import logger
from fastapi import Query, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src.data import users

user_router = APIRouter()
cred_checker = users.CredChecker()
templates = Jinja2Templates(directory="src/templates")


@user_router.post("/create-user-account")
async def create_account(request: Request, creds: dict):
    """
    Create the user account if the given user name does not exist yet.
    """
    # A lot of things to do
    user_account = users.UserAccount(creds['input_name'], creds['input_password'])
    result = user_account.create_account()
    if result == 1:
        return JSONResponse(
            content=
            {
                "message": "User name not available.",
                "userName": user_account.user_name
            }
        )
    elif result == 0:
        return JSONResponse(
            content=
            {
                "message": "User account created successfully",
                "userName": user_account.user_name,
                "userPassword": user_account.user_password
            }
        )


@user_router.post("/authenticate-user")
async def authenticate(creds: dict):
    """
    Acquire the user settings for one interro.
    """
    global cred_checker
    cred_checker.check_credentials(
        creds['input_name'],
        creds['input_password']
    )
    return JSONResponse(
        content={
            "message": "User credentials validated successfully",
            "userName": creds['input_name'],
            "userPassword": creds['input_password']
        }
    )


@user_router.get("/user-space", response_class=HTMLResponse)
def user_main_page(
    request: Request,
    query: str = Query(None, alias="userName")
    ):
    """
    Call the base page of user space
    """
    user_name = query.split('?')[0]
    user_password = query.split('?')[1].split('=')[1]
    if user_name:
        cred_checker.check_credentials(user_name, user_password)
    else:
        logger.error("No user name found in cookies.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No user name found in cookies."
        )
    return templates.TemplateResponse(
        "user/user_space.html",
        {
            "request": request,
            "userName": user_name,
            "userPassword": user_password
        }
    )


@user_router.get("/sign-out/{user_name}", response_class=HTMLResponse)
def sign_out(request: Request):
    """
    Deconnect the user and return to the welcome page.
    """
    cred_checker = users.CredChecker()
    return templates.TemplateResponse(
        "welcome.html",
        {
            "request": request
        }
    )


@user_router.get("/user-settings/{user_name}", response_class=HTMLResponse)
def settings_page(request: Request, user_name):
    """Load the main page for settings."""
    cred_checker.check_credentials(user_name)
    return templates.TemplateResponse(
        "user/settings.html",
        {
            "request": request,
            "userName": user_name
        }
    )
