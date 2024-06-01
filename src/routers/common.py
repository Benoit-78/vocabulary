"""
    Creation date:
        9th May 2024
    Main purpose:
        Gathers API routes dedicated to user space.
"""

import os
import sys

from loguru import logger
from fastapi import Depends, Body
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src.api import authentication as auth_api
from src.api import common as api_common

common_router = APIRouter(prefix="/v1/common")


@common_router.post("/change-language", response_class=HTMLResponse)
async def change_language(
        data: dict = Body(...),
        token: str = Depends(auth_api.check_token)
    ):
    """
    Change the language of the user interface.
    """
    json_response = api_common.change_language(data)
    return json_response
