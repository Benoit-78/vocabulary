"""
    Creation date:
        23rd February 2024
    Creator:
        B. Delorme
    Main purpose:
        Hosts the functions of interro router.
"""

import os
import sys

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.data import users
from src.dashboard import feed_dashboard

cred_checker = users.CredChecker()


def get_user_dashboards(request, user_name, user_password, db_name):
    """
    Get the user dashboards.
    """
    graphs = feed_dashboard.load_graphs(user_name, user_password, db_name)
    request_dict = {
        "request": request,
        "graph_1": graphs[0],
        "graph_2": graphs[1],
        "graph_3": graphs[2],
        "graph_4": graphs[3],
        "graph_5": graphs[4],
        "userName": user_name,
        "userPassword": user_password
    }
    return request_dict
