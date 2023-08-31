"""
    Author: Benoît DELORME
    Decoupling date: 26th August 2023
    Main purpose: FastAPI user interface of interroooooo !!!!! application.
"""

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from data import data_handler
import interro, views

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
    global words
    words = settings["numWords"]
    global score
    score = 0
    test_type = settings["testType"].lower()
    global interro_df
    interro_df = load_interro_df(test_type, words)
    return JSONResponse(
        content={
            "message": "User response and progress percent stored successfully"
        }
    )


def load_interro_df(test_type, words):
    """Load the words that will be asked to the user."""
    data_handler_ = data_handler.MariaDBHandler(test_type)
    loader = interro.Loader(test_type, 0, data_handler_)
    loader.load_tables()
    guesser = views.FastapiGuesser()
    test = interro.Test(
        loader.tables[loader.test_type + '_voc'],
        words,
        guesser,
        loader.tables[loader.test_type + '_perf'],
        loader.tables[loader.test_type + '_words_count']
    )
    test.get_interro_df()
    return test.interro_df


@app.get("/interro_question", response_class=HTMLResponse)
def interro_page_1(request: Request):
    global progress_percent
    global interro_df
    english = interro_df.loc[progress_percent - 1][0]
    progress_percent += 1
    print("# DEBUG: progress_percent after increment:", progress_percent)
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
    global progress_percent
    global interro_df
    english = interro_df.loc[progress_percent - 2][0]
    french = interro_df.loc[progress_percent - 2][1]
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


@app.post("/user-answer")
async def get_user_response(data: dict):
    user_answer = data["answer"]
    progress_percent = data.get("progress_percent")
    global score
    if user_answer == 'Yes':
        score += 1
    print("# DEBUG: new score:", score)
    return JSONResponse(
        content=
        {
            "message": "User response and progress percent stored successfully"
        }
    )


@app.get("/interro_end", response_class=HTMLResponse)
def display_score(request: Request):
    global score
    global words
    return templates.TemplateResponse(
        "interro_end.html",
        {
            "request": request,
            "score": score,
            "total": words
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
