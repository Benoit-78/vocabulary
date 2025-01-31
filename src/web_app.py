"""
    Author:
        Benoît DELORME
    Creation date:
        26th August 2023
    Main purpose:
        Vocabulary application in its FastAPI version.
"""

import os

from fastapi import FastAPI, Depends, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.routers import common_router, dashboard_router, database_router
from src.routers import guest_router, interro_router, user_router
from src.api import authentication as auth_api

app = FastAPI(
    title="expression",
    docs_url="/docs",
    description="""
        API for Expression application\n
        Provides you with endpoints to pass tests and register new words.
    """,
    servers=[
        {"url": "https://www.vocabulary-app.com/v1", "description": "beta version"},
        {"url": "https://www.vocabulary-app.com/v2", "description": "Super pro premium"},
    ]
)



class CacheControlMiddleware(BaseHTTPMiddleware):
    """
    Middleware to set the cache control header for static files.
    """
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/static/"):
            response.headers["Cache-Control"] = "public, max-age=31536000"
        return response



# Sessions
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ.get("SECRET_KEY")
)
app.add_middleware(
    CacheControlMiddleware
)
# Routers
v1_router = APIRouter()
app.include_router(common_router)
app.include_router(dashboard_router)
app.include_router(database_router)
app.include_router(guest_router)
app.include_router(interro_router)
app.include_router(user_router)

# CSS
app.mount(
    "/static",
    StaticFiles(directory="src/static"),
    name="static"
)
# HTML
templates = Jinja2Templates(
    directory="src/templates"
)


@v1_router.get("/", response_class=HTMLResponse, tags=["Welcome"])
async def root_page(
        request: Request,
        token: str = Depends(auth_api.create_token)
    ) -> RedirectResponse:
    """
    Redirects to the welcome page.
    """
    return RedirectResponse(url="/v1/welcome")


@v1_router.get("/welcome", response_class=HTMLResponse, tags=["Welcome"])
async def welcome_page(
        request: Request,
        token: str = Depends(auth_api.create_token)
    ) -> HTMLResponse:
    """
    Call the welcome page and assign a token to the guest.
    """
    response_dict = {'request': request, 'token': token}
    return templates.TemplateResponse(
        "welcome.html",
        response_dict
    )


@v1_router.get("/sign-in", response_class=HTMLResponse, tags=["Welcome"])
def sign_in(
        request: Request,
        token: str = Depends(auth_api.check_token),
        error_message: str = Query('', alias='errorMessage')
    ) -> HTMLResponse:
    """
    Call the sign-in page.
    """
    response_dict = auth_api.sign_in(
        request=request,
        token=token,
        error_message=error_message
    )
    return templates.TemplateResponse(
        "user/sign_in.html",
        response_dict
    )


@v1_router.get("/sign-up", response_class=HTMLResponse, tags=["Welcome"])
def sign_up(
        request: Request,
        token: str = Depends(auth_api.check_token),
        error_message: str = Query('', alias='errorMessage')
    ) -> HTMLResponse:
    """
    Call the create account page.
    """
    response_dict = {'request': request, 'errorMessage': error_message, 'token': token}
    return templates.TemplateResponse(
        "user/sign_up.html",
        response_dict
    )


@v1_router.get("/about-the-app", response_class=HTMLResponse, tags=["Welcome"])
def about_the_app(
        request: Request,
        token: str = Depends(auth_api.check_token)
    ) -> HTMLResponse:
    """
    Call the page that helps the user to get started.
    """
    response_dict = {'request': request, 'token': token}
    return templates.TemplateResponse(
        "about_the_app.html",
        response_dict
    )


@v1_router.get("/help", response_class=HTMLResponse, tags=["Welcome"])
def get_help(
        request: Request,
        token: str = Depends(auth_api.check_token)
    ) -> HTMLResponse:
    """
    Help!
    """
    response_dict = {'request': request, 'token': token}
    return templates.TemplateResponse(
        "help.html",
        response_dict
    )


app.include_router(v1_router, prefix="/v1")
