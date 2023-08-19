"""
    FastAPI user interface of interroooooo !!!!! application.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Serve static files (HTML and CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

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
    title = "Here is the starting page."
    return title


@app.get("/interro_0", response_class=HTMLResponse)
def interro_page_0(request: Request):
    return templates.TemplateResponse(
        "interro_0.html",
        {
            "request": request,
        }
    )


@app.get("/interro_1", response_class=HTMLResponse)
def interro_page_1(request: Request):
    english = "Hello"
    progress_percent = 1
    return templates.TemplateResponse(
        "interro_1.html",
        {
            "request": request,
            "content_box1": english,
            "progress_percent": progress_percent
        }
    )


@app.get("/interro_2", response_class=HTMLResponse)
def interro_page_2(request: Request):
    english = "Hello"
    french = "Bonjour"
    progress_percent = 2
    return templates.TemplateResponse(
        "interro_2.html",
        {
            "request": request,
            "content_box1": english,
            "content_box2": french,
            "progress_percent": progress_percent
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
