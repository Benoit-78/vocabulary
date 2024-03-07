"""
    Creation date:
        4th February 2024
    Main purpose:
        Gathers API routes dedicated to database interactions.
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
from src.api import database as database_api

database_router = APIRouter(prefix='/database')
cred_checker = users.CredChecker()
templates = Jinja2Templates(directory="src/templates")


@database_router.get("/list-databases", response_class=HTMLResponse)
def user_databases(
    request: Request,
    user_name: str = Query(None, alias="userName"),
    user_password: str = Query(None, alias="userPassword"),
    ):
    """
    Call the base page of user databases.
    """
    request_dict = database_api.get_user_databases(request, user_name, user_password)
    return templates.TemplateResponse("user/databases.html", request_dict)


@database_router.post("/create-database")
async def create_database(data: dict):
    """
    Create a database.
    """
    json_response = database_api.create_database(data)
    return json_response


@database_router.post("/choose-database")
async def choose_database(data: dict):
    """
    Choose a database.
    """
    json_response = database_api.choose_database(data)
    return json_response


@database_router.get("/fill_database", response_class=HTMLResponse)
def data_page(
    request: Request,
    user_name: str = Query(None, alias="userName"),
    user_password: str = Query(None, alias="userPassword"),
    db_name: str = Query(None, alias="databaseName"),
    ):
    """
    Base page for data input by the user.
    """
    request_dict = database_api.fill_database(
        request,
        user_name,
        user_password,
        db_name
    )
    return templates.TemplateResponse("database/fill.html", request_dict)


@database_router.post("/add-word")
async def create_word(data: dict):
    """Save the word in the database."""
    # Authenticate user
    user_name = data['usr']
    user_password = data['pwd']
    cred_checker.check_credentials(user_name, user_password)
    # Add the word
    db_name = data['db_name']
    user_account = users.UserAccount(user_name, user_password)
    result = user_account.insert_word(db_name, data['foreign'], data['native'])
    if result == 1:
        json_response = JSONResponse(content={"message": "Error with the word creation."})
    if result == 0:
        json_response =  JSONResponse(content={"message": "Word added successfully."})
    return json_response
