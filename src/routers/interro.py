"""
    Creation date:
        4th February 2024
    Main purpose:
        Gathers API routes dedicated to user interooooo!!!!!
"""

import ast
import os
import sys

from loguru import logger
from fastapi import Body, Depends, Query, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ValidationError
from typing import Optional

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.api import authentication as auth_api
from src.api import interro as interro_api
# from src.utils.debug import print_arguments_and_output

interro_router = APIRouter(prefix='/v1/interro')
templates = Jinja2Templates(directory="src/templates")



class Params(BaseModel):
    """
    Standard arguments for interro API.
    """
    # Mandatory
    databaseName: str
    faultsDict: list
    index: int
    interroCategory: str
    interroDict: list
    oldInterroDict: list
    score: int
    testLength: int
    testType: str
    # Optional
    answer: Optional[str]=None
    content_box1: Optional[str]=None
    content_box2: Optional[str]=None
    count: Optional[int]=None
    message: Optional[str]=''
    perf: Optional[int]=None

    @classmethod
    def from_query_params(cls, params: dict):
        for dict_name in ['interroDict', 'oldInterroDict', 'faultsDict']:
            while isinstance(params[dict_name], str):
                params[dict_name] = ast.literal_eval(params[dict_name])
        logger.debug(f"Query params: \n{params}")
        return cls(**params)



def get_interro_params(request: Request) -> Params:
    """
    Handle Params object from GET requests.
    """
    query_params = dict(request.query_params)
    return Params.from_query_params(query_params)


async def get_interro_params_from_body(request: Request) -> Params:
    """
    Handle Params object from POST requests.
    """
    try:
        body = await request.json()
        logger.debug(f"Query body: \n{body}")
        return Params.from_query_params(body)
    except ValidationError as ve:
        detail = [
            {"loc": err["loc"], "msg": err["msg"], "type": err["type"]}
            for err in ve.errors()
        ]
        raise HTTPException(
            status_code=422, detail={"errors": detail, "body": body}
        ) from ve
    except ValueError as ve:
        raise HTTPException(
            status_code=400, detail=str(ve)
        ) from ve
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=str(e)
        ) from e


@interro_router.get("/interro-settings", response_class=HTMLResponse)
def interro_settings(
        request: Request,
        token: str = Depends(auth_api.check_token),
        error_message: str = Query('', alias='errorMessage')
    ):
    """
    Call the page that gets the user settings for one interro.
    """
    response_dict = interro_api.get_interro_settings(
        token=token,
        error_message=error_message
    )
    response_dict["request"] = request
    return templates.TemplateResponse(
        "interro/settings.html",
        response_dict
    )


@interro_router.post("/save-interro-settings")
async def save_interro_settings(
        params: dict = Body(...),
        token: str = Depends(auth_api.check_token)
    ):
    """
    Save the user settings for the interro.
    """
    json_response = interro_api.save_interro_settings(
        token=token,
        params=params
    )
    return json_response


@interro_router.get("/interro-question", response_class=HTMLResponse)
def load_interro_question(
        request: Request,
        params: Params = Depends(get_interro_params),
        token: str=Depends(auth_api.check_token),
    ):
    """
    Call the page that asks the user the meaning of a word.
    """
    response_dict = interro_api.get_interro_question(
        token=token,
        params=params
    )
    response_dict["request"] = request
    return templates.TemplateResponse(
        "interro/question.html",
        response_dict
    )


@interro_router.get("/interro-answer", response_class=HTMLResponse)
def load_interro_answer(
        request: Request,
        params: Params = Depends(get_interro_params),
        token: str=Depends(auth_api.check_token),
    ):
    """
    Call the page that displays the right answer
    Asks the user to tell if his guess was right or wrong.
    """
    response_dict = interro_api.load_interro_answer(
        token=token,
        params=params
    )
    response_dict["request"] = request
    return templates.TemplateResponse(
        "interro/answer.html",
        response_dict
    )


@interro_router.post("/user-answer")
async def get_user_answer(
        params: Params = Depends(get_interro_params_from_body),
        token: str = Depends(auth_api.check_token)
    ):
    """
    Acquire the user decision: was his answer right or wrong.
    """
    json_response = interro_api.get_user_answer(
        token=token,
        params=params
    )
    return json_response


@interro_router.get("/interro-end", response_class=HTMLResponse)
def end_interro(
        request: Request,
        params: Params = Depends(get_interro_params),
        token: str=Depends(auth_api.check_token),
    ):
    """
    Page that ends the interro with a congratulation message,
    or a blaming message depending on the performances.
    """
    response_dict = interro_api.end_interro(
        token=token,
        params=params
    )
    response_dict["request"] = request
    return templates.TemplateResponse(
        "interro/end.html",
        response_dict
    )


@interro_router.get("/propose-rattrap", response_class=HTMLResponse)
def propose_rattrap(
        request: Request,
        params: Params = Depends(get_interro_params),
        token: str=Depends(auth_api.check_token),
    ):
    """
    Load a page that proposes the user to take a rattrap, or leave the test.
    """
    response_dict = interro_api.propose_rattrap(
        token=token,
        params=params
    )
    response_dict["request"] = request
    return templates.TemplateResponse(
        "interro/rattrap.html",
        response_dict
    )


@interro_router.post("/launch-rattrap", response_class=HTMLResponse)
async def launch_rattrap(
        params: Params = Depends(get_interro_params_from_body),
        token: str = Depends(auth_api.check_token)
    ):
    """
    Load the rattrap page.
    """
    json_response = interro_api.launch_rattrap(
        token=token,
        params=params
    )
    return json_response
