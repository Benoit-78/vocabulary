"""
    Author:
        Benoît DELORME
    Creation date:
        26th August 2023
    Main purpose:
        Vocabulary application in its FastAPI version.
"""

import json
import os
import sys

import pandas as pd
from fastapi import FastAPI, Query, Depends, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, JSONResponse
# from fastapi.session import Session
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src import interro, views
from src.dashboard import feed_dashboard
from src.data import data_handler, users

app = FastAPI(
    title="vocabulary",
    docs_url="/docs",
    redoc_url=None,
    servers=[{"url": "https://www.vocabulary-app.com"}],
)
GUEST_USER_NAME = 'guest'
GUEST_DB_NAME = 'vocabulary'
test = None
loader = None
flag_data_updated = None
cred_checker = users.CredChecker()

with open('conf/hum.json', 'r') as json_file:
    HUM = json.load(json_file)

with open('conf/data.json', 'r') as json_file:
    DATA = json.load(json_file)

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



# ==================================================
#  W E L C O M E   P A G E
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


@app.get("/sign-in", response_class=HTMLResponse)
def sign_in(request: Request):
    """Call the sign-in page"""
    return templates.TemplateResponse(
        "user/sign_in.html",
        {
            "request": request
        }
    )


@app.get("/create-account", response_class=HTMLResponse)
def sign_in(request: Request):
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
def about_the_app(request: Request):
    """Call the page that helps the user to get started."""
    return templates.TemplateResponse(
        "about_the_app.html",
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
#  U S E R   S P A C E
# ==================================================
@app.post("/create-user-account")
async def create_account(request: Request, creds: dict):
    """
    Create the user account if the given user name does not exist yet.
    """
    # A lot of things to do
    user_account = users.UserAccount(creds['input_name'], creds['input_password'])
    result = user_account.create_account()
    if result == 1:
        return JSONResponse(
            content=
            {
                "message": "User name not available.",
                "userName": user_account.user_name
            }
        )
    elif result == 0:
        return JSONResponse(
            content=
            {
                "message": "User account created successfully",
                "userName": user_account.user_name,
                "userPassword": user_account.user_password
            }
        )


@app.post("/authenticate-user")
async def authenticate(creds: dict):
    """
    Acquire the user settings for one interro.
    """
    global cred_checker
    cred_checker.check_credentials(
        creds['input_name'],
        creds['input_password']
    )
    return JSONResponse(
        content={
            "message": "User credentials validated successfully",
            "userName": creds['input_name'],
            "userPassword": creds['input_password']
        }
    )


@app.get("/user-space", response_class=HTMLResponse)
def user_main_page(
    request: Request,
    query: str = Query(None, alias="userName")
    ):
    """
    Call the base page of user space
    """
    user_name = query.split('?')[0]
    user_password = query.split('?')[1].split('=')[1]
    if user_name:
        cred_checker.check_credentials(user_name, user_password)
    else:
        logger.error("No user name found in cookies.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No user name found in cookies."
        )
    return templates.TemplateResponse(
        "user/user_space.html",
        {
            "request": request,
            "userName": user_name,
            "userPassword": user_password
        }
    )


@app.get("/sign-out/{user_name}", response_class=HTMLResponse)
def sign_out(request: Request):
    """
    Deconnect the user and return to the welcome page.
    """
    cred_checker = users.CredChecker()
    return templates.TemplateResponse(
        "welcome.html",
        {
            "request": request
        }
    )


# ==================================================
#  I N T E R R O   U S E R
# ==================================================
@app.post("/check-connection-to-database/{user_name}/{db_name}")
async def check_db_connection(settings: dict, user_name, db_name):
    """
    Acquire the database chosen by the user.
    """
    db_handler = data_handler.DbDefiner('localhost', user_name)
    connection, cursor = db_handler.get_db_cursor(db_name)
    return JSONResponse(
        content=
        {
            "message": "Connection to database established successfully.",
        }
    )


@app.get("/interro-settings", response_class=HTMLResponse)
def interro_settings(
    request: Request,
    query: str = Query(None, alias="userName")
    ):
    """Call the page that gets the user settings for one interro."""
    # Authenticate user
    user_name = query.split('?')[0]
    user_password = query.split('?')[1].split('=')[1]
    if user_name:
        cred_checker.check_credentials(user_name, user_password)
    else:
        logger.error("User name not found.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User name not found."
        )
    # Load settings page
    return templates.TemplateResponse(
        "user/interro_settings.html",
        {
            "request": request,
            "userName": user_name,
            "userPassword": user_password
        }
    )


@app.post("/save-interro-settings/{user_name}/{db_name}}")
async def save_interro_settings(settings: dict, user_name, db_name):
    """Acquire the user settings for one interro."""
    global loader
    global test
    password = 'mais_quel_est_le_password'
    loader, test = load_test(
        user_name,
        db_name,
        settings["testType"].lower(),
        settings["numWords"],
        password
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


def load_test(user_name, db_name, test_type, test_length, password):
    """Load the interroooo!"""
    db_handler = data_handler.DbManipulator(
        host='localhost',
        user_name=user_name,
        db_name=db_name,
        test_type=test_type,
    )
    db_handler.check_test_type(test_type)
    loader_ = interro.Loader(0, db_handler)
    loader_.load_tables(password)
    guesser = views.FastapiGuesser()
    logger.debug(f"Table names: {loader_.tables.keys()}")
    test_ = interro.Test(
        loader_.tables[loader_.test_type + '_voc'],
        test_length,
        guesser,
        loader_.tables[loader_.test_type + '_perf'],
        loader_.tables[loader_.test_type + '_words_count']
    )
    logger.debug(f"Test created: {test_}")
    test_.set_interro_df()
    return loader_, test_


@app.get("/interro-question/{user_name}/{words}/{count}/{score}", response_class=HTMLResponse)
def load_interro_question(
    request: Request,
    user_name,
    words: int,
    count=None,
    score=None):
    """Call the page that asks the user the meaning of a word"""
    cred_checker.check_credentials(user_name)
    global test
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
            "userName": user_name,
            "numWords": words,
            "count": count,
            "score": score,
            "progressPercent": progress_percent,
            "content_box1": english
        }
    )


@app.get("/interro-answer/{user_name}/{words}/{count}/{score}", response_class=HTMLResponse)
def load_interro_answer(
    request: Request,
    user_name,
    words: int,
    count: int,
    score: int):
    """
    Call the page that displays the right answer
    Asks the user to tell if his guess was right or wrong.
    """
    cred_checker.check_credentials(user_name)
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
            "userName": user_name,
            "numWords": words,
            "count": count,
            "score": score,
            "progressPercent": progress_percent,
            "content_box1": english,
            "content_box2": french,
        }
    )


@app.post("/user-answer/{user_name}")
async def get_user_response(data: dict, user_name):
    """Acquire the user decision: was his answer right or wrong."""
    cred_checker.check_credentials(user_name)
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


@app.get("/propose-rattraps/{user_name}/{words}/{count}/{score}", response_class=HTMLResponse)
def propose_rattraps(
    request: Request,
    user_name,
    words: int,
    count: int,
    score: int):
    """Load a page that proposes the user to take a rattraps, or leave the test."""
    cred_checker.check_credentials(user_name)
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
            "userName": user_name,
            "score": score,
            "numWords": words,
            "count": count,
            "newScore": new_score,
            "newWords": new_words,
            "newCount": new_count
        }
    )


@app.get("/interro-end/{user_name}/{words}/{score}", response_class=HTMLResponse)
def end_interro(
    request: Request,
    user_name,
    words: int,
    score: int):
    """
    Page that ends the interro with a congratulation message,
    or a blaming message depending on the performances.
    """
    cred_checker.check_credentials(user_name)
    # Execution
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
            "numWords": words,
            "userName": user_name
        }
    )



# ==================================================
# G U E S T
# ==================================================
# The guest is able to do some tests, but nothing more.
#     - this page should NOT contain pages like settings, add word, ...
#     - a guest should not access the 'root' page, even by accident.
@app.get("/guest-not-allowed", response_class=HTMLResponse)
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


@app.get("/interro-settings-guest", response_class=HTMLResponse)
def interro_settings_guest(request: Request):
    """Call the page that gets the user settings for one interro."""
    return templates.TemplateResponse(
        "guest/interro_settings.html",
        {
            "request": request,
        }
    )


@app.post("/interro-settings-guest")
async def save_interro_settings_guest(settings: dict):
    """Acquire the user settings for one interro."""
    global loader
    global test
    loader, test = load_test(
        user_name='guest',
        db_name=HUM['user']['guest']['databases'][0],
        test_type=settings["testType"].lower(),
        test_length=settings["numWords"],
        password=HUM['user']['guest']['OK']
    )
    logger.info("User data loaded")
    global flag_data_updated
    flag_data_updated = False
    return JSONResponse(
        content=
        {
            "message": "Guest user settings stored successfully."
        }
    )


@app.get("/interro-question-guest/{words}/{count}/{score}", response_class=HTMLResponse)
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
    global test
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


@app.get("/interro-answer-guest/{words}/{count}/{score}", response_class=HTMLResponse)
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


@app.post("/user-answer-guest")
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


@app.get("/propose-rattraps-guest/{words}/{count}/{score}", response_class=HTMLResponse)
def propose_rattraps_guest(
    request: Request,
    words: int,
    count: int,
    score: int):
    """
    Load a page that proposes the user to take a rattraps, or leave the test.
    """
    global test
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


@app.get("/interro-end-guest/{words}/{score}", response_class=HTMLResponse)
def end_interro_guest(
    request: Request,
    words: int,
    score: int):
    """
    Page that ends the interro with a congratulation message,
    or a blaming message depending on the performance.
    """
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
@app.get("/user-databases", response_class=HTMLResponse)
def user_databases(
    request: Request,
    query: str = Query(None, alias="userName")
    ):
    """
    Call the base page of user databases.
    """
    # Authenticate user
    user_name = query.split('?')[0]
    user_password = query.split('?')[1].split('=')[1]
    if user_name:
        cred_checker.check_credentials(user_name, user_password)
    else:
        logger.error("User name not found.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User name not found."
        )
    # Launch database creation page
    return templates.TemplateResponse(
        "user/databases.html",
        {
            "request": request,
            "userName": user_name,
            "userPassword": user_password
        }
    )


@app.post("/create-database")
async def create_database(data: dict):
    """Save the word in the database."""
    # Authenticate user
    user_name = data['usr']
    user_password = data['pwd']
    cred_checker = users.CredChecker()
    cred_checker.check_credentials(user_name, user_password)
    # Create database
    db_name = data['db_name']
    user_account = users.UserAccount(user_name, user_password)
    result = user_account.create_database(db_name)
    if result == 1:
        return JSONResponse(
            content=
            {
                "message": "Database name not available.",
                "databaseName": db_name
            }
        )
    elif result == 0:
        return JSONResponse(
            content=
            {
                "message": "Database created successfully.",
                "userName": user_account.user_name,
                "userPassword": user_account.user_password
            }
        )


@app.get("/fill_database", response_class=HTMLResponse)
def data_page(
    request: Request,
    query: str = Query(None, alias="userName")
    ):
    """
    Base page for data input by the user.
    """
    # Authenticate user
    user_name = query.split('?')[0]
    user_password = query.split('?')[1].split('=')[1]
    db_name = query.split('?')[2].split('=')[1]
    if user_name:
        cred_checker.check_credentials(user_name, user_password)
    else:
        logger.error("User name not found.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User name not found."
        )
    # Load database page
    title = "Here you can add words to your database."
    return templates.TemplateResponse(
        "user/fill_database.html",
        {
            "request": request,
            "title": title,
            "userName": user_name,
            "userPassword": user_password,
            "databaseName": db_name
        }
    )


@app.post("/create-word")
async def create_word(data: dict):
    """Save the word in the database."""
    # Authenticate user
    user_name = data['usr']
    user_password = data['pwd']
    cred_checker = users.CredChecker()
    cred_checker.check_credentials(user_name, user_password)
    # Add the word
    db_name = data['db_name']
    user_account = users.UserAccount(user_name, user_password)
    result = user_account.insert_word(db_name, data['foreign'], data['native'])
    if result == 1:
        return JSONResponse(content={"message": "Error with the word creation."})
    elif result == 0:
        return JSONResponse(content={"message": "Word created successfully."})



# ==================================================
#  D A S H B O A R D
# ==================================================
@app.get("/dashboard/{user_name}", response_class=HTMLResponse)
def graphs_page(request: Request, user_name):
    """Load the main page for performances visualization"""
    cred_checker.check_credentials(user_name)
    graphs = feed_dashboard.load_graphs()
    return templates.TemplateResponse(
        "user/dashboard.html",
        {
            "request": request,
            "graph_1": graphs[0],
            "graph_2": graphs[1],
            "graph_3": graphs[2],
            "graph_4": graphs[3],
            "graph_5": graphs[4],
            "userName": user_name
        }
    )



# ==================================================
#  S E T T I N G S
# ==================================================
@app.get("/user-settings/{user_name}", response_class=HTMLResponse)
def settings_page(request: Request, user_name):
    """Load the main page for settings."""
    cred_checker.check_credentials(user_name)
    return templates.TemplateResponse(
        "user/settings.html",
        {
            "request": request,
            "userName": user_name
        }
    )
