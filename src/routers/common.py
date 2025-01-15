"""
    Creation date:
        9th May 2024
    Main purpose:
        Gathers API routes dedicated to user space.
"""

from fastapi import Depends, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.routing import APIRouter

from src.api import authentication as auth_api
from src.api import common as api_common

common_router = APIRouter(prefix="/v1/common")


@common_router.post("/change-language", response_class=HTMLResponse, tags=["Common"])
async def change_language(
        data: dict = Body(...),
        token: str = Depends(auth_api.check_token)
    ) -> JSONResponse:
    """
    Change the language of the user interface.
    """
    json_response = api_common.change_language(data=data)
    return json_response
