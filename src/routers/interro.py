"""
    Creation date:
        4th February 2024
    Main purpose:
        Gathers API routes dedicated to user interooooo!!!!!
"""


from loguru import logger
from fastapi import Body, Depends, Query, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from src.api import authentication as auth_api
from src.api import interro as interro_api
from src.models.interro import Params

interro_router = APIRouter(prefix='/v1/interro')
templates = Jinja2Templates(directory="src/templates")


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


@interro_router.get("/interro-settings", response_class=HTMLResponse, tags=["Interro"])
def interro_settings(
        request: Request,
        token: str = Depends(auth_api.check_token),
        error_message: str = Query('', alias='errorMessage')
    ) -> HTMLResponse:
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


@interro_router.post("/save-interro-settings", tags=["Interro"])
async def save_interro_settings(
        params: dict = Body(...),
        token: str = Depends(auth_api.check_token)
    ) -> JSONResponse:
    """
    Save the user settings for the interro.
    """
    json_response = interro_api.save_interro_settings(
        token=token,
        params=params
    )
    return json_response


@interro_router.get("/interro-question", response_class=HTMLResponse, tags=["Interro"])
def load_interro_question(
        request: Request,
        params: Params = Depends(get_interro_params),
        token: str=Depends(auth_api.check_token),
    ) -> HTMLResponse:
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


@interro_router.get("/interro-answer", response_class=HTMLResponse, tags=["Interro"])
def load_interro_answer(
        request: Request,
        params: Params = Depends(get_interro_params),
        token: str=Depends(auth_api.check_token),
    ) -> HTMLResponse:
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


@interro_router.post("/user-answer", tags=["Interro"])
async def get_user_answer(
        params: Params = Depends(get_interro_params_from_body),
        token: str = Depends(auth_api.check_token)
    ) -> JSONResponse:
    """
    Acquire the user decision: was his answer right or wrong.
    """
    json_response = interro_api.get_user_answer(
        token=token,
        params=params
    )
    return json_response


@interro_router.get("/interro-end", response_class=HTMLResponse, tags=["Interro"])
def end_interro(
        request: Request,
        params: Params = Depends(get_interro_params),
        token: str=Depends(auth_api.check_token),
    ) -> HTMLResponse:
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


@interro_router.get("/propose-rattrap", response_class=HTMLResponse, tags=["Interro"])
def propose_rattrap(
        request: Request,
        params: Params = Depends(get_interro_params),
        token: str=Depends(auth_api.check_token),
    ) -> HTMLResponse:
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


@interro_router.post("/launch-rattrap", response_class=HTMLResponse, tags=["Interro"])
async def launch_rattrap(
        params: Params = Depends(get_interro_params_from_body),
        token: str = Depends(auth_api.check_token)
    ) -> JSONResponse:
    """
    Load the rattrap page.
    """
    json_response = interro_api.launch_rattrap(
        token=token,
        params=params
    )
    return json_response
