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

database_router = APIRouter()
cred_checker = users.CredChecker()
templates = Jinja2Templates(directory="src/templates")


@database_router.get("/user-databases", response_class=HTMLResponse)
def user_databases(
    request: Request,
    query: str = Query(None, alias="userName")
    ):
    """
    Call the base page of user databases.
    """
    # Authenticate user
    user_name = query.split('?')[0]
    user_password = query.split('?')[1].split('=')[1]
    if user_name:
        cred_checker.check_credentials(user_name, user_password)
    else:
        logger.error("User name not found.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User name not found."
        )
    # Launch database creation page
    return templates.TemplateResponse(
        "user/databases.html",
        {
            "request": request,
            "userName": user_name,
            "userPassword": user_password
        }
    )


@database_router.post("/create-database")
async def create_database(data: dict):
    """Save the word in the database."""
    # Authenticate user
    user_name = data['usr']
    user_password = data['pwd']
    cred_checker = users.CredChecker()
    cred_checker.check_credentials(user_name, user_password)
    # Create database
    db_name = data['db_name']
    user_account = users.UserAccount(user_name, user_password)
    result = user_account.create_database(db_name)
    if result == 1:
        return JSONResponse(
            content=
            {
                "message": "Database name not available.",
                "databaseName": db_name
            }
        )
    elif result == 0:
        return JSONResponse(
            content=
            {
                "message": "Database created successfully.",
                "userName": user_account.user_name,
                "userPassword": user_account.user_password
            }
        )


@database_router.get("/fill_database", response_class=HTMLResponse)
def data_page(
    request: Request,
    query: str = Query(None, alias="userName")
    ):
    """
    Base page for data input by the user.
    """
    # Authenticate user
    user_name = query.split('?')[0]
    user_password = query.split('?')[1].split('=')[1]
    db_name = query.split('?')[2].split('=')[1]
    if user_name:
        cred_checker.check_credentials(user_name, user_password)
    else:
        logger.error("User name not found.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User name not found."
        )
    # Load database page
    title = "Here you can add words to your database."
    return templates.TemplateResponse(
        "user/fill_database.html",
        {
            "request": request,
            "title": title,
            "userName": user_name,
            "userPassword": user_password,
            "databaseName": db_name
        }
    )


@database_router.post("/create-word")
async def create_word(data: dict):
    """Save the word in the database."""
    # Authenticate user
    user_name = data['usr']
    user_password = data['pwd']
    cred_checker = users.CredChecker()
    cred_checker.check_credentials(user_name, user_password)
    # Add the word
    db_name = data['db_name']
    user_account = users.UserAccount(user_name, user_password)
    result = user_account.insert_word(db_name, data['foreign'], data['native'])
    if result == 1:
        return JSONResponse(content={"message": "Error with the word creation."})
    elif result == 0:
        return JSONResponse(content={"message": "Word created successfully."})

