"""
    Creation date:
        4th February 2024
    Main purpose:
        Gathers API routes dedicated to database interactions.
"""

import os
import sys

from loguru import logger
from fastapi import Query, Request, Depends, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src.data import users
from src.api import database as db_api
from src.api import authentication as auth_api

database_router = APIRouter(prefix='/database')
templates = Jinja2Templates(directory="src/templates")


@database_router.get("/list-databases", response_class=HTMLResponse)
def user_databases(
        request: Request,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Call the base page of user databases.
    """
    response_dict = db_api.load_user_databases(request, token)
    return templates.TemplateResponse(
        "database/choose.html",
        response_dict
    )


@database_router.post("/choose-database")
async def choose_database(
        data: dict,
        token: str = Depends(auth_api.check_token),
    ):
    """
    Choose a database.
    """
    json_response = db_api.choose_database(data, token)
    return json_response


@database_router.post("/create-database")
async def create_database(
        data: dict,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Create a database.
    """
    json_response = db_api.create_database(data, token)
    return json_response


@database_router.get("/fill-database", response_class=HTMLResponse)
def data_page(
        request: Request,
        token: str = Depends(auth_api.check_token),
        db_name: str = Query(None, alias="databaseName"),
        error_message: str = Query('', alias='errorMessage')
    ):
    """
    Base page for data input by the user.
    """
    request_dict = db_api.fill_database(request, db_name, error_message, token)
    return templates.TemplateResponse(
        "database/fill.html",
        request_dict
    )


@database_router.post("/add-word")
async def create_word(
        data: dict,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Save the word in the database.
    """
    json_response = db_api.create_word(data, token)
    return json_response


@database_router.post("/delete-database")
async def delete_database(
        data: dict,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Delete the database.
    """
    json_response = db_api.delete_database(data, token)
    return json_response


@database_router.post("/upload-csv", response_class=HTMLResponse)
async def upload_csv(
        csv_file: UploadFile = File(...),
        token: str = Depends(auth_api.check_token)
    ):
    """
    Upload the given CSV file.
    """
    response_dict = db_api.upload_csv(csv_file, token)
    return response_dict
