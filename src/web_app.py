"""
    Author:
        Benoît DELORME
    Creation date:
        26th August 2023
    Main purpose:
        Vocabulary application in its FastAPI version.
"""

import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

from src import interro
from src import views
from src.data import data_handler
from src.dashboard import feed_dashboard

app = FastAPI()
LANGUAGE = 'english'
test = None
loader = None
flag_data_updated = None


# CSS files
app.mount(
    "/static",
    StaticFiles(directory="src/static"),
    name="static"
)

# HTML files
templates = Jinja2Templates(
    directory="src/templates"
)



# ==================================================
#  W E L C O M E
# ==================================================
@app.get("/", response_class=HTMLResponse)
def welcome_page(request: Request):
    """Call the welcome page"""
    return templates.TemplateResponse(
        "welcome.html",
        {
            "request": request,
        }
    )



@app.get("/root", response_class=HTMLResponse)
def root_page(request: Request):
    """Call the root page"""
    return templates.TemplateResponse(
        "user/root.html",
        {
            "request": request,
        }
    )


@app.get("/help", response_class=HTMLResponse)
def get_help(request: Request):
    """Help!"""
    return templates.TemplateResponse(
        "help.html",
        {
            "request": request,
        }
    )



# ==================================================
#  G E T   S T A R T E D
# ==================================================
@app.get("/about_the_app", response_class=HTMLResponse)
def about_the_app(request: Request):
    """Call the page that helps the user to get started."""
    return templates.TemplateResponse(
        "about_the_app.html",
        {
            "request": request,
        }
    )



# ==================================================
#  I N T E R R O   U S E R
# ==================================================
@app.get("/interro_settings", response_class=HTMLResponse)
def interro_settings(request: Request):
    """Call the page that gets the user settings for one interro."""
    return templates.TemplateResponse(
        "user/interro_settings.html",
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
    db_handler = data_handler.MariaDBHandler(test_type, 'web_local', LANGUAGE)
    loader_ = interro.Loader(0, db_handler)
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
    score=None):
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
        "user/interro_question.html",
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
    score: int):
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
        "user/interro_answer.html",
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
    score: int):
    """Load a page that proposes the user to take a rattraps, or leave the test."""
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
        "user/rattraps_propose.html",
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
    score: int):
    """
    Page that ends the interro with a congratulation message,
    or a blaming message depending on the performances.
    """
    global flag_data_updated
    if flag_data_updated is False:
        global loader
        global test
        test.compute_success_rate()
        updater = interro.Updater(loader, test)
        updater.update_data()
        logger.info("User data updated.")
    return templates.TemplateResponse(
        "user/interro_end.html",
        {
            "request": request,
            "score": score,
            "numWords": words
        }
    )



# ==================================================
# G U E S T
# ==================================================
@app.get("/root_guest", response_class=HTMLResponse)
def root_guest_page(request: Request):
    """
    Call the guest root page.
    The guest only can do some tests, and nothing more.
    - this page must NOT contain pages like settings, add word, ...
    - a guest should not access the 'root' page, even by accident.
    """
    return templates.TemplateResponse(
        "guest/root_guest.html",
        {
            "request": request,
        }
    )


@app.get("/guest_not_allowed", response_class=HTMLResponse)
def guest_not_allowed(request: Request):
    """
    Page used each time a guest tries to access a page he has not access to.
    """
    return templates.TemplateResponse(
        "guest/guest_not_allowed.html",
        {
            "request": request,
        }
    )


@app.get("/interro_settings_guest", response_class=HTMLResponse)
def interro_settings_guest(request: Request):
    """Call the page that gets the user settings for one interro."""
    return templates.TemplateResponse(
        "guest/interro_settings.html",
        {
            "request": request,
        }
    )


@app.post("/user-settings_guest")
async def get_user_settings_guest(settings: dict):
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


def load_test_guest(test_type, words):
    """Load the interroooo!"""
    db_handler = data_handler.MariaDBHandler(test_type, 'web_local', LANGUAGE)
    loader_ = interro.Loader(0, db_handler)
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


@app.get("/interro_question_guest/{words}/{count}/{score}", response_class=HTMLResponse)
def load_interro_question_guest(
    request: Request,
    words: int,
    count=None,
    score=None):
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
        "guest/interro_question.html",
        {
            "request": request,
            "numWords": words,
            "count": count,
            "score": score,
            "progressPercent": progress_percent,
            "content_box1": english
        }
    )


@app.get("/interro_answer_guest/{words}/{count}/{score}", response_class=HTMLResponse)
def load_interro_answer_guest(
    request: Request,
    words: int,
    count: int,
    score: int):
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
        "guest/interro_answer.html",
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


@app.post("/user-answer_guest")
async def get_user_response_guest(data: dict):
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


@app.get("/propose_rattraps_guest/{words}/{count}/{score}", response_class=HTMLResponse)
def propose_rattraps_guest(
    request: Request,
    words: int,
    count: int,
    score: int):
    """Load a page that proposes the user to take a rattraps, or leave the test."""
    global test
    # Enregistrer les résultats
    global flag_data_updated
    if flag_data_updated is False:
        global loader
        test.compute_success_rate()
        updater = interro.Updater(loader, test)
        updater.update_data()
        logger.info("Guest data updated.")
        flag_data_updated = True
    else:
        logger.info("Guest data not updated yet.")
    # Réinitialisation
    new_count = 0
    new_score = 0
    new_words = test.faults_df.shape[0]
    test.interro_df = test.faults_df
    test.faults_df = pd.DataFrame(columns=[['Foreign', 'Native']])
    return templates.TemplateResponse(
        "guest/rattraps_propose.html",
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


@app.get("/interro_end_guest/{words}/{score}", response_class=HTMLResponse)
def end_interro_guest(
    request: Request,
    words: int,
    score: int):
    """
    Page that ends the interro with a congratulation message,
    or a blaming message depending on the performance.
    """
    global flag_data_updated
    if flag_data_updated is False:
        global loader
        global test
        test.compute_success_rate()
        updater = interro.Updater(loader, test)
        updater.update_data()
        logger.info("Guest data updated.")
    return templates.TemplateResponse(
        "guest/interro_end.html",
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
        "user/database_add_word.html",
        {
            "request": request,
            "title": title
        }
    )


@app.post("/create-word")
async def create_word(data: dict):
    """Save the word in the database."""
    db_handler = data_handler.MariaDBHandler('version', 'web_local', LANGUAGE)
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
def graphs_page(request: Request):
    """Load the main page for performances visualization"""
    graphs = feed_dashboard.load_graphs()
    return templates.TemplateResponse(
        "user/dashboard.html",
        {
            "request": request,
            "graph_1": graphs[0],
            "graph_2": graphs[1],
            "graph_3": graphs[2],
            "graph_4": graphs[3],
            "graph_5": graphs[4]
        }
    )



# ==================================================
#  S E T T I N G S
# ==================================================
@app.get("/user_settings", response_class=HTMLResponse)
def settings_page(request: Request):
    """Load the main page for settings."""
    return templates.TemplateResponse(
        "user/settings.html",
        {
            "request": request
        }
    )
