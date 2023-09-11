"""
    Author: Benoît DELORME
    Decoupling date: 26th August 2023
    Main purpose: vocabulary application in its FastAPI version.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from data import data_handler
import interro
import views


app = FastAPI()

# Serve CSS files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)
# Serve HTML files
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
    global count
    count = 0
    test_type = settings["testType"].lower()
    global test
    test = load_test(test_type, words)
    return JSONResponse(
        content=
        {
            "message": "User settings stored successfully."
        }
    )


def load_test(test_type, words_):
    """Load the interroooo!"""
    data_handler_ = data_handler.MariaDBHandler(test_type)
    loader = interro.Loader(test_type, 0, data_handler_)
    loader.load_tables()
    guesser = views.FastapiGuesser()
    test_ = interro.Test(
        loader.tables[loader.test_type + '_voc'],
        words_,
        guesser,
        loader.tables[loader.test_type + '_perf'],
        loader.tables[loader.test_type + '_words_count']
    )
    test_.get_interro_df()
    return test_


@app.get("/interro_question", response_class=HTMLResponse)
def load_interro_question(request: Request):
    global count
    global test
    english = test.interro_df.loc[count][0]
    count += 1
    global words
    global progress_percent
    try:
        progress_percent
    except NameError:
        progress_percent = 0
    return templates.TemplateResponse(
        "interro_question.html",
        {
            "request": request,
            "content_box1": english,
            "count": count,
            "numberOfQuestions": words,
            "progressPercent": progress_percent
        }
    )


@app.get("/interro_answer", response_class=HTMLResponse)
def load_interro_answer(request: Request):
    global count
    global test
    english = test.interro_df.loc[count - 1 ][0]
    french = test.interro_df.loc[count - 1][1]
    global words
    global score
    global progress_percent
    progress_percent = int(count / int(words) * 100)
    return templates.TemplateResponse(
        "interro_answer.html",
        {
            "request": request,
            "count": count,
            "content_box1": english,
            "content_box2": french,
            "numberOfQuestions": words,
            "progressPercent": progress_percent,
            "score": score
        }
    )


@app.post("/user-answer")
async def get_user_response(data: dict):
    global test
    global score
    score = data.get('score')
    if data["answer"] == 'Yes':
        score += 1
    elif data["answer"] == 'No':
        test.update_faults_df(
            False,
            [
                data.get('english'),
                data.get('french')
            ]
        )
        print("# DEBUG: test.faults_df\n", test.faults_df)
    return JSONResponse(
        content=
        {
            "score": score,
            "message": "User response stored successfully."
        }
    )


@app.get("/propose_rattraps", response_class=HTMLResponse)
def propose_rattraps(request: Request):
    global score
    global words
    previous_words = words
    # Réinitialisation
    words = test.faults_df.shape[0]
    global count
    count = 0
    global rattraps_count
    rattraps_count = 0
    return templates.TemplateResponse(
        "rattraps_propose.html",
        {
            "request": request,
            "score": score,
            "total": previous_words
        }
    )


@app.get("/rattraps_question", response_class=HTMLResponse)
def load_rattraps_question(request: Request):
    global count
    global test
    english = test.faults_df.loc[count][0]
    count += 1
    global words
    global progress_percent
    progress_percent = int(count / int(words) * 100)
    return templates.TemplateResponse(
        "interro_question.html",
        {
            "request": request,
            "count": count,
            "content_box1": english,
            "numberOfQuestions": words,
            "progressBar": progress_percent
        }
    )


@app.get("/rattraps_answer", response_class=HTMLResponse)
def load_rattraps_answer(request: Request):
    global count
    global test
    english = test.faults_df.loc[count - 2][0]
    french = test.faults_df.loc[count - 2][1]
    global rattraps_score
    global progress_percent
    return templates.TemplateResponse(
        "interro_answer.html",
        {
            "request": request,
            "count": count,
            "content_box1": english,
            "content_box2": french,
            "numberOfQuestions": test.faults_df.shape[0],
            "progressPercent": progress_percent,
            "score": rattraps_score
        }
    )


@app.get("/interro_end", response_class=HTMLResponse)
def end_interro(request: Request):
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
