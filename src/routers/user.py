"""
    Creation date:
        4th February 2024
    Main purpose:
        Gathers API routes dedicated to user space.
"""

import os
import sys

from loguru import logger
from fastapi import Query, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src.api import authentication as auth_api
from src.data import users
from src.api import user as user_api

user_router = APIRouter(prefix="/user")
cred_checker = users.CredChecker()
templates = Jinja2Templates(directory="src/templates")



class LoginForm(BaseModel):
    username: str
    password: str



@user_router.post("/create-user-account")
async def create_account(
        creds: dict,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Create the user account if the given user name does not exist yet.
    """
    json_response = user_api.create_account(creds, token)
    return json_response


@user_router.post("/user-token")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends()
    ) -> auth_api.Token:
    """
    Create a timedelta with the expiration time of the token.
    Create a real JWT access token and return it.
    """
    # Identify user
    users_list = auth_api.get_users_list()
    user = auth_api.authenticate_user(
        users_list,
        form_data.username,
        form_data.password
    )
    if user in ['Unknown user', 'Password incorrect']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    # Create a token
    user_token = auth_api.create_token(data={"sub": form_data.username})
    result = auth_api.Token(
        access_token=user_token,
        token_type="bearer"
    )
    return result


@user_router.get("/user-space", response_class=HTMLResponse)
def user_main_page(
        request: Request,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Call the base page of user space.
    """
    user_name = auth_api.get_user_name_from_token(token)
    return templates.TemplateResponse(
        "user/user_space.html",
        {
            'request': request,
            'token': token,
            'user_name': user_name
        }
    )


@user_router.get("/user-settings", response_class=HTMLResponse)
def settings_page(
        request: Request,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Load the main page for settings.
    """
    return templates.TemplateResponse(
        "user/settings.html",
        {
            "request": request,
            "token": token
        }
    )


@user_router.get("/user-dashboards", response_class=HTMLResponse)
def dashboard_page(
        request: Request,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Load the dashboard page.
    """
    return templates.TemplateResponse(
        "user/dashboard.html",
        {
            "request": request,
            "token": token
        }
    )