"""
    Creation date:
        4th February 2024
    Main purpose:
        Gathers API routes dedicated to user space.
"""

import os
import sys
from typing import Dict, Any

from loguru import logger
from fastapi import Query, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from typing import Annotated

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src.api import authentication
from src.data import users
from src.api import user as user_api

user_router = APIRouter(prefix="/user")
cred_checker = users.CredChecker()
templates = Jinja2Templates(directory="src/templates")


@user_router.post("/create-user-account")
async def create_account(creds: dict):
    """
    Create the user account if the given user name does not exist yet.
    """
    json_response = user_api.create_account(creds)
    return json_response


@user_router.post("/authenticate-user", response_class=HTMLResponse)
def authenticate(request: Request, input_dict: Dict[str, Any]):
    """
    Acquire the user settings for one interro.
    """
    logger.debug(f"input_dict: {input_dict}")
    # request_dict = user_api.authenticate_user(input_dict)
    request_dict = authentication.authenticate_user(input_dict)
    request_dict['request'] = request
    logger.debug(f"Request dict: {request_dict}")
    return templates.TemplateResponse("user/user_space.html", request_dict)


@user_router.post("/user_token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ) -> authentication.Token:
    """
    Create a timedelta with the expiration time of the token.
    Create a real JWT access token and return it.
    """
    users_list = authentication.get_users_names()
    user = authentication.authenticate_user(
        users_list,
        form_data.username,
        form_data.password
    )
    if user in ['User name unknown', 'Password incorrect']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = authentication.create_token(data={"sub": form_data.username})
    result = authentication.Token(
        access_token=access_token,
        token_type="bearer"
    )
    return result


@user_router.get("/user-space", response_class=HTMLResponse)
def user_main_page(
    request: Request,
    user_name: str = Query(None, alias="userName"),
    user_password: str = Query(None, alias="userPassword")
    ):
    """Call the base page of user space"""
    request_dict = user_api.get_user_main_page(request, user_name, user_password)
    return templates.TemplateResponse("user/user_space.html", request_dict)


@user_router.get("/user-settings", response_class=HTMLResponse)
def settings_page(
    request: Request,
    user_name: str = Query(None, alias="userName"),
    user_password: str = Query(None, alias="userPassword"),
    db_name: str = Query(None, alias="dbName"),
    test_type: str = Query(None, alias="testType"),
    total_words: str = Query(None, alias="numWords")
    ): 
    """Load the main page for settings."""
    request_dict = user_api.get_user_settings(
        request,
        user_name,
        user_password,
        db_name,
        test_type,
        total_words
    )
    return templates.TemplateResponse("user/settings.html", request_dict)


@user_router.get("/user-dashboards", response_class=HTMLResponse)
def dashboard_page(
    request: Request,
    user_name: str = Query(None, alias="userName"),
    user_password: str = Query(None, alias="userPassword")
    ): 
    """Load the dashboard page."""
    request_dict = user_api.get_user_dashboards(request, user_name, user_password)
    return templates.TemplateResponse("user/dashboard.html", request_dict)