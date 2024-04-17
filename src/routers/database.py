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
from src.api import database as database_api
from src.api import authentication as auth_api

database_router = APIRouter(prefix='/database')
cred_checker = users.CredChecker()
templates = Jinja2Templates(directory="src/templates")


@database_router.get("/list-databases", response_class=HTMLResponse)
def user_databases(
        request: Request,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Call the base page of user databases.
    """
    databases = database_api.get_user_databases(token)
    return templates.TemplateResponse(
        "database/choose.html",
        {
            'request': request,
            'token': token,
            'databases': databases
        }
    )


@database_router.post("/choose-database")
async def choose_database(
        data: dict,
        token: str = Depends(auth_api.check_token),
    ):
    """
    Choose a database.
    """
    db_name = data['db_name']
    json_response = database_api.choose_database(db_name, token)
    return json_response


@database_router.post("/create-database")
async def create_database(
        data: dict,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Create a database.
    """
    json_response = database_api.create_database(data, token)
    return json_response


@database_router.get("/fill-database", response_class=HTMLResponse)
def data_page(
        request: Request,
        token: str = Depends(auth_api.check_token),
        db_name: str = Query(None, alias="databaseName"),
    ):
    """
    Base page for data input by the user.
    """
    request_dict = database_api.fill_database(
        request,
        token,
        db_name
    )
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
    # Authenticate user
    user_name = auth_api.get_user_name_from_token(token)
    # Add the word
    db_name = data['db_name']
    user_account = users.UserAccount(user_name)
    result = user_account.insert_word(
        db_name,
        data['foreign'],
        data['native']
    )
    if result is False:
        json_response = JSONResponse(
            content={"message": "Error with the word creation."}
        )
    if result is True:
        json_response =  JSONResponse(
            content={"message": "Word added successfully."}
        )
    return json_response


@database_router.post("/delete-database")
async def delete_database(
        data: dict,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Delete the database.
    """
    db_name = data['db_name']
    json_response = database_api.delete_database(token, db_name)
    return json_response


@database_router.post("/upload-csv", response_class=HTMLResponse)
async def upload_csv(
        csv_file: UploadFile = File(...),
        token: str = Depends(auth_api.check_token)
    ):
    """
    Upload the given CSV file.
    """
    # Check if the file has a CSV extension
    if not csv_file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format, only CSV files are allowed")
    # Read and decode the CSV content
    csv_content = await csv_file.read()
    # Check for malicious code
    if database_api.is_malicious(csv_content.decode('utf-8')):
        raise HTTPException(status_code=400, detail="Malicious code detected in the CSV file")
    # Add CSV content to the user database
    database_api.add_to_database(csv_content.decode('utf-8'))
    return {"message": "CSV file uploaded successfully"}
