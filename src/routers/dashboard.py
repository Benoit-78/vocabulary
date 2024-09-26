"""
    Creation date:
        4th February 2024
    Main purpose:
        Gathers API routes dedicated to database interactions.
"""

from fastapi import Query, Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates

from src.api import dashboard as dashboard_api

dashboard_router = APIRouter(prefix='/v1/dashboard')
templates = Jinja2Templates(directory="src/templates")


@dashboard_router.get("/dashboards", response_class=HTMLResponse, tags=["Dashboard"])
def graphs_page(
        request: Request,
        user_name: str=Query(None, alias="userName"),
        user_password: str=Query(None, alias="userPassword"),
        db_name: str=Query(None, alias="databaseName")
    ):
    """
    Load the main page for performances visualization
    """
    request_dict = dashboard_api.get_user_dashboards(
        request=request,
        user_name=user_name,
        user_password=user_password,
        db_name=db_name
    )
    return templates.TemplateResponse(
        "user/dashboard.html",
        request_dict
    )
