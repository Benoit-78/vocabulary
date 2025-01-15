"""
    Creation date:
        4th February 2024
    Main purpose:
        Gathers API routes dedicated to guest space.
        The guest is able to do some tests, but nothing more.
        - this page should NOT contain pages like settings, add word, ...
        - a guest should not access the 'root' page, even by accident.
"""

from fastapi import Body, Depends, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates

from src.api import authentication as auth_api
from src.api import guest as guest_api

guest_router = APIRouter(prefix="/v1/guest")
templates = Jinja2Templates(directory="src/templates")


@guest_router.get("/interro-settings", response_class=HTMLResponse, tags=["Guests"])
def interro_settings_guest(
        request: Request,
        token: str=Depends(auth_api.check_token)
    ) -> HTMLResponse:
    """
    Call the page that gets the user settings for one interro.
    """
    response_dict = guest_api.load_guest_settings(
        request=request,
        token=token
    )
    return templates.TemplateResponse(
        "guest/settings.html",
        response_dict
    )


@guest_router.post("/save-interro-settings", tags=["Guests"])
async def save_interro_settings_guest(
        language: dict,
        token: str=Depends(auth_api.check_token)
    ) -> JSONResponse:
    """
    Acquire the user settings for one interro.
    """
    json_response = guest_api.save_interro_settings_guest(
        language=language,
        token=token
    )
    return json_response


@guest_router.get("/interro-question", response_class=HTMLResponse, tags=["Guests"])
def load_interro_question_guest(
        request: Request,
        interro_category: str=Query(None, alias="interroCategory"),
        total: str=Query(None, alias="testLength"),
        count: str=Query(None, alias="testCount"),
        score: str=Query(None, alias="testScore"),
        token: str=Depends(auth_api.check_token),
        language: str=Query('', alias='testLanguage')
    ) -> HTMLResponse:
    """
    Call the page that asks the user the meaning of a word
    """
    response_dict = guest_api.load_interro_question_guest(
        request=request,
        interro_category=interro_category,
        total=total,
        count=count,
        score=score,
        language=language,
        token=token
    )
    return templates.TemplateResponse(
        "guest/question.html",
        response_dict
    )


@guest_router.get("/interro-answer", response_class=HTMLResponse, tags=["Guests"])
def load_interro_answer_guest(
        request: Request,
        interro_category: str=Query(None, alias="interroCategory"),
        total: str=Query(None, alias="testLength"),
        count: str=Query(None, alias="testCount"),
        score: str=Query(None, alias="testScore"),
        token: str=Depends(auth_api.check_token),
        language: str=Query('', alias='testLanguage')
    ) -> HTMLResponse:
    """
    Call the page that displays the right answer
    Asks the user to tell if his guess was right or wrong.
    """
    response_dict = guest_api.load_interro_answer_guest(
        request=request,
        interro_category=interro_category,
        total=total,
        count=count,
        score=score,
        token=token,
        language=language
    )
    return templates.TemplateResponse(
        "guest/answer.html",
        response_dict
    )


@guest_router.post("/user-answer", tags=["Guests"])
async def get_user_response_guest(
        data: dict = Body(...),
        token: str = Depends(auth_api.check_token)
    ) -> JSONResponse:
    """
    Acquire the user decision: was his answer right or wrong.
    """
    json_response = guest_api.get_user_response_guest(data=data, token=token)
    return json_response


@guest_router.get("/propose-rattrap", response_class=HTMLResponse, tags=["Guests"])
def propose_rattrap_guest(
        request: Request,
        interro_category: str=Query(None, alias="interroCategory"),
        total: str = Query(None, alias="testLength"),
        score: str = Query(None, alias="testScore"),
        token: str = Depends(auth_api.check_token),
        language: str = Query('', alias='testLanguage')
    ) -> HTMLResponse:
    """
    Load a page that proposes the user to take a rattrap, or leave the test.
    """
    response_dict = guest_api.propose_rattrap_guest(
        request=request,
        interro_category=interro_category,
        total=total,
        score=score,
        token=token,
        language=language
    )
    return templates.TemplateResponse(
        "guest/rattrap.html",
        response_dict
    )


@guest_router.post("/launch-guest-rattrap", response_class=HTMLResponse, tags=["Guests"])
async def launch_rattrap(
        data: dict = Body(...),
        token: str = Depends(auth_api.check_token)
    ) -> JSONResponse:
    """
    Load the rattrap page.
    """
    json_response = guest_api.load_rattrap(
        data,
        token
    )
    return json_response


@guest_router.get("/interro-end/", response_class=HTMLResponse, tags=["Guests"])
def end_interro_guest(
        request: Request,
        total: str=Query(None, alias="testLength"),
        score: str=Query(None, alias="testScore"),
        token: str = Depends(auth_api.check_token)
    ) -> HTMLResponse:
    """
    Page that ends the interro with a congratulation message,
    or a blaming message depending on the performance.
    """
    response_dict = guest_api.end_interro_guest(
        request=request,
        total=total,
        score=score,
        token=token
    )
    return templates.TemplateResponse(
        "guest/end.html",
        response_dict
    )
