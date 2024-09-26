"""
    Creation date:
        4th February 2024
    Main purpose:
        Gathers API routes dedicated to user space.
"""

from fastapi import Body, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from src.api import authentication as auth_api
from src.api import user as user_api

user_router = APIRouter(prefix="/v1/user")
templates = Jinja2Templates(directory="src/templates")



class Token(BaseModel):
    """
    Base model class for the token.
    """
    access_token: str
    token_type: str



class UserLogin(BaseModel):
    username: str = Field(..., min_length=1, error_msg="Username cannot be empty")
    password: str = Field(..., min_length=1, error_msg="Password cannot be empty")



@user_router.post("/create-user-account", tags=["Users"])
async def create_account(
        creds: dict,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Create the user account if the given user name does not exist yet.
    """
    json_response = user_api.create_account(
        creds=creds,
        token=token
    )
    return json_response


@user_router.post("/user-token", tags=["Users"])
async def login_for_access_token(
        token: str=Depends(auth_api.check_token),
        form_data: UserLogin = Body(...)
    ) -> Token:
    """
    Create a timedelta with the expiration time of the token.
    Create a real JWT access token and return it.
    """
    if not form_data.username or not form_data.password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username and password must not be empty."
        )
    json_response = user_api.authenticate_user(
        token=token,
        form_data=form_data
    )
    return json_response


@user_router.get("/user-space", response_class=HTMLResponse, tags=["Users"])
def user_main_page(
        request: Request,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Call the base page of user space.
    """
    response_dict = user_api.load_user_space(
        request=request,
        token=token
    )
    return templates.TemplateResponse(
        "user/user_space.html",
        response_dict
    )


@user_router.get("/user-settings", response_class=HTMLResponse, tags=["Users"])
def settings_page(
        request: Request,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Load the main page for settings.
    """
    response_dict = {
        "request": request,
        "token": token
    }
    return templates.TemplateResponse(
        "user/settings.html",
        response_dict
    )


@user_router.get("/user-dashboards", response_class=HTMLResponse, tags=["Users"])
def dashboard_page(
        request: Request,
        token: str = Depends(auth_api.check_token)
    ):
    """
    Load the dashboard page.
    """
    response_dict = {
        "request": request,
        "token": token
    }
    return templates.TemplateResponse(
        "user/dashboard.html",
        response_dict
    )
