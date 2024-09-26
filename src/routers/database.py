"""
    Creation date:
        4th February 2024
    Main purpose:
        Gathers API routes dedicated to database interactions.
"""

from fastapi import Query, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates

from src.api import database as db_api
from src.api import authentication as auth_api

database_router = APIRouter(prefix='/v1/database')
templates = Jinja2Templates(directory="src/templates")


@database_router.get("/list-databases", response_class=HTMLResponse, tags=["Database"])
def user_databases(
        request: Request,
        token: str = Depends(auth_api.check_token),
        error_message: str = Query('', alias='errorMessage')
    ):
    """
    Call the base page of user databases.
    """
    response_dict = db_api.load_user_databases(
        request=request,
        token=token,
        error_message=error_message
    )
    return templates.TemplateResponse(
        "database/choose.html",
        response_dict
    )


@database_router.post("/create-database", tags=["Database"])
async def create_database(
        data: dict,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Create a database.
    """
    json_response = db_api.create_database(
        data=data,
        token=token
    )
    return json_response


@database_router.post("/retrieve-database", tags=["Database"])
async def retrieve_database(
        data: dict,
        token: str = Depends(auth_api.check_token),
    ):
    """
    Choose a database.
    """
    json_response = db_api.retrieve_database(
        data=data,
        token=token
    )
    return json_response


@database_router.get("/see-database", response_class=HTMLResponse, tags=["Database"])
def see_database(
        request: Request,
        token: str = Depends(auth_api.check_token),
        db_name: str = Query(None, alias="databaseName"),
        version_table: str = Query(None, alias="versionTable"),
        theme_table: str = Query(None, alias="themeTable"),
    ):
    """
    Base page for data input by the user.
    """
    request_dict = db_api.see_database(
        request=request,
        token=token,
        db_name=db_name,
        version_table=version_table,
        theme_table=theme_table
    )
    return templates.TemplateResponse(
        "database/see.html",
        request_dict
    )


@database_router.post("/choose-database", tags=["Database"])
async def choose_database(
        data: dict,
        token: str = Depends(auth_api.check_token),
    ):
    """
    Choose a database.
    """
    json_response = db_api.choose_database(
        data=data,
        token=token
    )
    return json_response


@database_router.get("/fill-database", response_class=HTMLResponse, tags=["Database"])
def data_page(
        request: Request,
        token: str = Depends(auth_api.check_token),
        db_name: str = Query(None, alias="databaseName"),
        error_message: str = Query('', alias='errorMessage')
    ):
    """
    Base page for data input by the user.
    """
    request_dict = db_api.fill_database(
        request=request,
        db_name=db_name,
        error_message=error_message,
        token=token
    )
    return templates.TemplateResponse(
        "database/fill.html",
        request_dict
    )


@database_router.post("/add-word", tags=["Database"])
async def create_word(
        data: dict,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Save the word in the database.
    """
    json_response = db_api.create_word(
        data=data,
        token=token
    )
    return json_response


@database_router.delete("/delete-database", tags=["Database"])
async def delete_database(
        data: dict,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Delete the database.
    """
    json_response = db_api.delete_database(
        data=data,
        token=token
    )
    return json_response
