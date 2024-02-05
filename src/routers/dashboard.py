"""
    Creation date:
        4th February 2024
    Main purpose:
        Gathers API routes dedicated to database interactions.
"""

import os
import sys

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src.dashboard import feed_dashboard
from src.data import users

dashboard_router = APIRouter()
cred_checker = users.CredChecker()
templates = Jinja2Templates(directory="src/templates")


@dashboard_router.get("/dashboard/{user_name}", response_class=HTMLResponse)
def graphs_page(request: Request, user_name):
    """Load the main page for performances visualization"""
    cred_checker.check_credentials(user_name)
    graphs = feed_dashboard.load_graphs()
    return templates.TemplateResponse(
        "user/dashboard.html",
        {
            "request": request,
            "graph_1": graphs[0],
            "graph_2": graphs[1],
            "graph_3": graphs[2],
            "graph_4": graphs[3],
            "graph_5": graphs[4],
            "userName": user_name
        }
    )
