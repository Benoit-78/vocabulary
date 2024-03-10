"""
    Author:
        Benoît DELORME
    Creation date:
        26th August 2023
    Main purpose:
        Vocabulary application in its FastAPI version.
"""

import os
import sys
from typing import Dict

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from fastapi import FastAPI, HTTPException #Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from typing import Optional
from loguru import logger
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

from src.routers import user_router, interro_router, guest_router, database_router, dashboard_router

GUEST_USER_NAME = 'guest'
GUEST_DB_NAME = 'vocabulary'
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="vocabulary",
    # docs_url="/docs",
    # redoc_url=None,
    # servers=[{"url": "https://www.vocabulary-app.com"}],
)
# Sessions
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
# CSS
app.mount("/static", StaticFiles(directory="src/static"), name="static")
# HTML
templates = Jinja2Templates(directory="src/templates")
# Routers
app.include_router(user_router)
app.include_router(interro_router)
app.include_router(guest_router)
app.include_router(database_router)
app.include_router(dashboard_router)



def create_token(data: dict):
    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    logger.debug("Token created")
    return token


# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(
#             token,
#             SECRET_KEY,
#             algorithms=[ALGORITHM]
#         )
#         return payload
#     except JWTError:
#         raise HTTPException(
#             status_code=401,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )


@app.post("/token")
async def login_for_access_token():
    """
    Example login route that returns a token
    """
    logger.debug("Token route called")
    token_data = {"sub": "testuser"}
    result_dict = {
        "access_token": create_token(token_data),
        "token_type": "bearer"
    }
    return result_dict


# @app.get("/protected")
# async def protected_route(current_user: dict = Depends(get_current_user)):
#     """
#     Example protected route that requires a valid token
#     """
#     result_dict = {
#         "message": "You have access!",
#         "user": current_user
#     }
#     return result_dict





# def get_session(request: Request = Depends()):
#     """
#     Dependency for session, used in specific routes that need it
#     """
#     return request.session


@app.get("/", response_class=HTMLResponse)
def welcome_page(
        request: Request,
        # session: dict = Depends(get_session)
    ):
    """
    Call the welcome page
    """
    return templates.TemplateResponse(
        "welcome.html",
        {
            "request": request,
            # "session": session
        }
    )


@app.get("/sign-in", response_class=HTMLResponse)
def sign_in(
    request: Request,
    # session: dict=Depends()
    ):
    """Call the sign-in page"""
    return templates.TemplateResponse(
        "user/sign_in.html",
        {
            "request": request
        }
    )


@app.get("/create-account", response_class=HTMLResponse)
def create_account(
    request: Request,
    # session: dict=Depends()
    ):
    """
    Call the create account page
    """
    return templates.TemplateResponse(
        "user/create_account.html",
        {
            "request": request,
            "errorMessage": ""
        }
    )


@app.get("/about-the-app", response_class=HTMLResponse)
def about_the_app(
    request: Request,
    # session: dict=Depends()
    ):
    """Call the page that helps the user to get started."""
    return templates.TemplateResponse(
        "about_the_app.html",
        {
            "request": request,
        }
    )


@app.get("/help", response_class=HTMLResponse)
def get_help(
    request: Request,
    # session: dict=Depends()
    ):
    """Help!"""
    return templates.TemplateResponse(
        "help.html",
        {
            "request": request,
        }
    )


# ==================================================
#  UNIQUE SESSION
# ==================================================
# def get_session(request: Request):
#     """
#     Return the session object.
#     """
#     return Session(request=request)


# @app.get("/")
# async def read_item(session: Session = Depends(get_session)):
#     # Check the session for user-specific data
#     user_data = session.get("user_data", None)
#     if not user_data:
#         # Initialize user-specific data
#         user_data = initialize_user_data()
#         session["user_data"] = user_data
#     logger.debug(f"Session: {session}")
#     logger.debug(f"User data: {user_data}")
#     # return {"message": "Hello World", "user_data": user_data}
#     return templates.TemplateResponse(
#         "welcome.html",
#         {
#             "request": request,
#         }
#     )