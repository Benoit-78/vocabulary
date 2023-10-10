"""
    Author: Benoît DELORME
    Decoupling date: 26th August 2023
    Main purpose: vocabulary application in its FastAPI version.
"""

import pandas as pd

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

from data import data_handler
import interro
import views


app = FastAPI()
test = None
loader = None
flag_data_updated = None

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
    """Call the welcome page"""
    return templates.TemplateResponse(
        "welcome.html",
        {
            "request": request,
        }
    )



# ==================================================
#  G E T   S T A R T E D
# ==================================================
@app.get("/get_started", response_class=HTMLResponse)
def start_page():
    """Call the page that helps the user to get started."""
    title = "Get started with interro application."
    return title



# ==================================================
#  I N T E R R O
# ==================================================
@app.get("/interro_settings", response_class=HTMLResponse)
def interro_settings(request: Request):
    """Call the page that gets the user settings for one interro."""
    return templates.TemplateResponse(
        "interro_settings.html",
        {
            "request": request,
        }
    )


@app.post("/user-settings")
async def get_user_settings(settings: dict):
    """Acquire the user settings for one interro."""
    global loader
    global test
    loader, test = load_test(
        settings["testType"].lower(),
        settings["numWords"]
    )
    logger.info("User data loaded")
    global flag_data_updated
    flag_data_updated = False
    return JSONResponse(
        content=
        {
            "message": "User settings stored successfully."
        }
    )


def load_test(test_type, words):
    """Load the interroooo!"""
    db_handler = data_handler.MariaDBHandler(test_type, 'container')
    loader_ = interro.Loader(test_type, 0, db_handler)
    loader_.load_tables()
    guesser = views.FastapiGuesser()
    test_ = interro.Test(
        loader_.tables[loader_.test_type + '_voc'],
        words,
        guesser,
        loader_.tables[loader_.test_type + '_perf'],
        loader_.tables[loader_.test_type + '_words_count']
    )
    test_.set_interro_df()
    return loader_, test_


@app.get("/interro_question/{words}/{count}/{score}", response_class=HTMLResponse)
def load_interro_question(
    request: Request,
    words: int,
    count=None,
    score=None,
    ):
    """Call the page that asks the user the meaning of a word"""
    # Instantiation
    try:
        count = int(count)
    except NameError:
        count = 0
    try:
        score = int(score)
    except NameError:
        score = 0
    progress_percent = int(count / int(words) * 100)
    index = test.interro_df.index[count]
    english = test.interro_df.loc[index][0]
    english = english.replace("'", "\'")
    count += 1
    return templates.TemplateResponse(
        "interro_question.html",
        {
            "request": request,
            "numWords": words,
            "count": count,
            "score": score,
            "progressPercent": progress_percent,
            "content_box1": english
        }
    )


@app.get("/interro_answer/{words}/{count}/{score}", response_class=HTMLResponse)
def load_interro_answer(
    request: Request,
    words: int,
    count: int,
    score: int,
    ):
    """
    Call the page that displays the right answer
    Asks the user to tell if his guess was right or wrong.
    """
    count = int(count)
    global test
    index = test.interro_df.index[count - 1]
    english = test.interro_df.loc[index][0]
    french = test.interro_df.loc[index][1]
    english = english.replace("'", "\'")
    french = french.replace("'", "\'")
    progress_percent = int(count / int(words) * 100)
    return templates.TemplateResponse(
        "interro_answer.html",
        {
            "request": request,
            "numWords": words,
            "count": count,
            "score": score,
            "progressPercent": progress_percent,
            "content_box1": english,
            "content_box2": french,
        }
    )


@app.post("/user-answer")
async def get_user_response(data: dict):
    """Acquire the user decision: was his answer right or wrong."""
    global test
    score = data.get('score')
    if data["answer"] == 'Yes':
        score += 1
        test.update_voc_df(True)
    elif data["answer"] == 'No':
        test.update_voc_df(False)
        test.update_faults_df(
            False,
            [
                data.get('english'),
                data.get('french')
            ]
        )
    return JSONResponse(
        content=
        {
            "score": score,
            "message": "User response stored successfully."
        }
    )


@app.get("/propose_rattraps/{words}/{count}/{score}", response_class=HTMLResponse)
def propose_rattraps(
    request: Request,
    words: int,
    count: int,
    score: int,
    ):
    global test
    # Enregistrer les résultats
    global flag_data_updated
    if flag_data_updated is False:
        global loader
        test.compute_success_rate()
        updater = interro.Updater(loader, test)
        updater.update_data()
        logger.info("User data updated.")
        flag_data_updated = True
    else:
        logger.info("User data not updated yet.")
    # Réinitialisation
    new_count = 0
    new_score = 0
    new_words = test.faults_df.shape[0]
    test.interro_df = test.faults_df
    test.faults_df = pd.DataFrame(columns=[['Foreign', 'Native']])
    return templates.TemplateResponse(
        "rattraps_propose.html",
        {
            "request": request,
            "score": score,
            "numWords": words,
            "count": count,
            "newScore": new_score,
            "newWords": new_words,
            "newCount": new_count
        }
    )


@app.get("/interro_end/{words}/{score}", response_class=HTMLResponse)
def end_interro(
    request: Request,
    words: int,
    score: int
    ):
    global flag_data_updated
    if flag_data_updated is False:
        global loader
        global test
        test.compute_success_rate()
        updater = interro.Updater(loader, test)
        updater.update_data()
        logger.info("User data updated.")
    return templates.TemplateResponse(
        "interro_end.html",
        {
            "request": request,
            "score": score,
            "numWords": words
        }
    )



# ==================================================
#  D A T A B A S E
# ==================================================
@app.get("/database", response_class=HTMLResponse)
def data_page(request: Request):
    """Base page for data input by the user."""
    title = "Here you can add words to your database."
    return templates.TemplateResponse(
        "database_add_word.html",
        {
            "request": request,
            "title": title
        }
    )


@app.post("/create-word")
async def create_word(data: dict):
    """Save the word in the database."""
    db_handler = data_handler.MariaDBHandler('version', 'container')
    english = data['english']
    french = data['french']
    if db_handler.create([english, french]) is True:
        message = "Word stored successfully."
    else:
        message = "Error with the storing of the word."
    return JSONResponse(
        content=
        {
            "message": message
        }
    )



# ==================================================
#  D A S H B O A R D
# ==================================================
@app.get("/dashboard", response_class=HTMLResponse)
def graphs_page():
    title = "Here are the graphs that represents your progress."
    return title



# ==================================================
#  S E T T I N G S
# ==================================================
@app.get("/settings", response_class=HTMLResponse)
def settings_page():
    title = "Here you can change your personal settings."
    return title
