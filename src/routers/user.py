"""
    Creation date:
        4th February 2024
    Main purpose:
        Gathers API routes dedicated to user space.
"""

import os
import sys

from loguru import logger
from fastapi import Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src.data import users
from src.api import user as user_api

user_router = APIRouter(prefix="/user")
cred_checker = users.CredChecker()
templates = Jinja2Templates(directory="src/templates")


@user_router.post("/create-user-account")
async def create_account(creds: dict):
    """Create the user account if the given user name does not exist yet."""
    json_response = user_api.create_account(creds)
    return json_response


@user_router.post("/authenticate-user")
async def authenticate(creds: dict):
    """Acquire the user settings for one interro."""
    json_response = user_api.authenticate_user(creds)
    return json_response


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
    user_password: str = Query(None, alias="userPassword")
    ): 
    """Load the main page for settings."""
    request_dict = user_api.get_user_settings(request, user_name, user_password)
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