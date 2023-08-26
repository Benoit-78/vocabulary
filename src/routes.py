"""
    FastAPI user interface of interroooooo !!!!! application.
"""

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse


global user_response


app = FastAPI()
# Serve static files (HTML and CSS)
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def welcome_page(request: Request):
    return templates.TemplateResponse(
        "welcome.html",
        {
            "request": request,
        }
    )


@app.get("/get_started", response_class=HTMLResponse)
def start_page():
    title = "Get started with interro application."
    return title


@app.get("/interro_settings", response_class=HTMLResponse)
def interro_settings(request: Request):
    global progress_percent
    progress_percent = 1
    return templates.TemplateResponse(
        "interro_settings.html",
        {
            "request": request,
        }
    )


@app.post("/user-settings")
async def get_user_settings(settings: dict):
    print('"# DEBUG: settings', settings)
    global test_type
    test_type = settings["testType"]
    global words
    words = settings["numWords"]
    return JSONResponse(
        content={
            "message": "User response and progress percent stored successfully"
        }
    )


@app.get("/interro_question", response_class=HTMLResponse)
def interro_page_1(request: Request):
    english = "Hello"
    global progress_percent
    progress_percent += 1
    return templates.TemplateResponse(
        "interro_question.html",
        {
            "request": request,
            "content_box1": english,
            "progress_percent": progress_percent,
        }
    )


@app.get("/interro_answer", response_class=HTMLResponse)
def interro_page_2(request: Request):
    english = "Hello"
    french = "Bonjour"
    return templates.TemplateResponse(
        "interro_answer.html",
        {
            "request": request,
            "content_box1": english,
            "content_box2": french,
            "number_of_questions": words,
            "progress_percent": progress_percent
        }
    )



@app.post("/user-response")
async def get_user_response(data: dict):
    print(data)
    global user_answer
    user_answer = data["answer"]
    progress_percent = data.get("progress_percent")
    return JSONResponse(
        content=
        {
            "message": "User response and progress percent stored successfully"
        }
    )


@app.get("/interro_end", response_class=HTMLResponse)
def display_score(request: Request):
    score = 84
    return templates.TemplateResponse(
        "interro_end.html",
        {
            "request": request,
            "score": score
        }
    )


@app.get("/dashboard", response_class=HTMLResponse)
def graphs_page():
    title = "Here are the graphs that represents your progress."
    return title


@app.get("/database", response_class=HTMLResponse)
def data_page():
    title = "Here you can add words to your database."
    return title


@app.get("/settings", response_class=HTMLResponse)
def settings_page():
    title = "Here you can change your personal settings."
    return title
