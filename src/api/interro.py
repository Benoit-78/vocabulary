"""
    Creation date:
        23rd February 2024
    Creator:
        B. Delorme
    Main purpose:
        Hosts the functions of interro API.
"""

import ast
from typing import Dict

import pandas as pd
from fastapi.responses import JSONResponse
from loguru import logger

from src.interro import Loader, Interro, PremierTest, Rattrap
from src.api.authentication import get_user_name_from_token
from src.api.database import get_user_databases
from src.data.database_interface import DbQuerier
from src.interro import Updater
from src.views.api import FastapiGuesser


# ------------------ API functions ------------------ #
def get_interro_settings(
        token,
        error_message
    ):
    """
    API function to load the interro settings.
    """
    databases = get_user_databases(token=token)
    db_message = get_error_messages(error_message=error_message)
    settings_dict = {
        'token': token,
        'databases': databases,
        'emptyTableErrorMessage': db_message,
    }
    return settings_dict


def save_interro_settings(
        token,
        params
    ):
    """
    API function to save the interro settings.
    """
    user_name = get_user_name_from_token(token=token)
    logger.info(f"User: {user_name}")
    db_name = params['databaseName']
    test_type = params['testType'].lower()
    test_length = int(params['testLength'])
    try:
        _, premier_test = load_test(
            user_name=user_name,
            db_name=db_name,
            test_type=test_type,
            test_length=test_length
        )
    except ValueError as exc:
        logger.error(exc)
        return JSONResponse(
            content=
            {
                'message': "Empty table",
                'token': token,
                'testLength': test_length
            }
        )
    interro_category = get_interro_category(interro=premier_test)
    response_dict = premier_test.to_dict()
    response_dict['token'] = token
    response_dict['message'] = "Settings saved successfully"
    response_dict['interroCategory'] = interro_category
    response_dict['oldInterroDict'] = get_old_interro_dict(
        interro_dict=response_dict['interroDict']
    )
    response_dict['testScore'] = 0
    response_dict['testCount'] = 0
    response_dict['databaseName'] = db_name
    response_dict['testType'] = test_type
    json_response = JSONResponse(
        content=response_dict
    )
    return json_response


def get_interro_question(
        token,
        params
    ):
    """
    API function to load the interro question.
    """
    test_count = int(params.testCount)
    test_length = int(params.testLength)
    progress_percent = int(test_count / test_length * 100)
    interro_df = decode_dict(params.interroDict)
    test_index = int(params.testIndex)
    foreign_word = interro_df.loc[test_index][0]
    foreign_word = foreign_word.replace("'", "\'")
    test_count += 1
    response_dict = {
        'contentBox1': foreign_word,
        'databaseName': params.databaseName,
        'faultsDict': params.faultsDict,
        'interroCategory': params.interroCategory,
        'interroDict': params.interroDict,
        'message': params.message,
        'oldInterroDict': params.oldInterroDict,
        'progressPercent': progress_percent,
        'testCount': test_count,
        'testIndex': test_index,
        'testLength': test_length,
        'testPerf': params.testPerf,
        'testScore': params.testScore,
        'testType': params.testType,
        'token': token,
    }
    return response_dict


def load_interro_answer(
        token,
        params
    ):
    """
    Load the interro answer.
    """
    test_count = int(params.testCount)
    test_length = int(params.testLength)
    progress_percent = int(test_count / test_length * 100)
    interro_df = decode_dict(params.interroDict)
    test_index = int(params.testIndex)
    foreign = interro_df.loc[test_index][0]
    foreign = foreign.replace("'", "\'")
    native = interro_df.loc[test_index][1]
    native = native.replace("'", "\'")
    response_dict = {
        'contentBox1': foreign,
        'contentBox2': native,
        'databaseName': params.databaseName,
        'faultsDict': params.faultsDict,
        'interroCategory': params.interroCategory,
        'interroDict': params.interroDict,
        'oldInterroDict': params.oldInterroDict,
        'progressPercent': progress_percent,
        'testCount': params.testCount,
        'testIndex': test_index,
        'testLength': test_length,
        'testPerf': params.testPerf,
        'testScore': params.testScore,
        'testType': params.testType,
        'token': token
    }
    return response_dict


def get_user_answer(
        token,
        params
    ):
    """
    Get the user response.
    """
    interro = get_interro(params)
    interro, score = update_interro(interro, params)
    attributes_dict = get_attributes_dict(token, interro, params, score)
    json_response = JSONResponse(
        content=attributes_dict
    )
    return json_response


def end_interro(
        token,
        params
    ):
    """
    End the interro.
    """
    # If the user guesses all words, and there is no rattrap
    if params.interroCategory == 'test':
        interro_df = decode_dict(params.interroDict)
        update_test(params, interro_df, token)
        interro_df = interro_df[['foreign', 'native']]
    # If the user does not guesses all words, and there is a rattrap
    elif params.interroCategory == 'rattrap':
        interro_df = decode_dict(params.oldInterroDict)
    headers, rows = turn_df_into_dict(words_df=interro_df)
    response_dict = {
        'headers': headers,
        'rows': rows,
        'testLength': params.testLength,
        'testScore': params.testScore,
        'token': token,
    }
    return response_dict


def propose_rattrap(
        token,
        params,
    ):
    """
    Propose the rattrap.
    """
    if params.interroCategory == 'test':
        save_result(token, params)
    response_dict = {
        "token": token,
        "databaseName": params.databaseName,
        "faultsDict": params.faultsDict,
        "testIndex": 0,
        "interroCategory": params.interroCategory,
        "interroDict": [],
        "oldInterroDict": params.oldInterroDict,
        "testScore": params.testScore,
        "testLength": len(params.interroDict),
        "testType": params.testType,
    }
    return response_dict


def launch_rattrap(
        token,
        params
    ):
    """
    Load the rattrap!
    """
    old_interro_df = decode_dict(params.oldInterroDict)
    faults_dict = params.faultsDict
    faults_df = get_faults_df(faults_dict)
    guesser = FastapiGuesser()
    rattrap = Rattrap(
        interro_df=faults_df,
        guesser=guesser,
        old_interro_df=old_interro_df
    )
    rattrap.reshuffle_words_table()
    attributes_dict = rattrap.to_dict()
    new_interro_category = get_interro_category(interro=rattrap)
    attributes_dict['testCount'] = 0
    attributes_dict['databaseName'] = params.databaseName
    attributes_dict['interroCategory'] = new_interro_category
    attributes_dict['message'] = "Rattrap created successfully"
    attributes_dict['testScore'] = 0
    attributes_dict['testType'] = params.testType
    attributes_dict['token'] = token
    return JSONResponse(
        content=attributes_dict
    )


# ------------------ Helper functions ------------------ #
def load_test(
        user_name,
        db_name,
        test_type,
        test_length
    ):
    """
    Load the interroooo!
    """
    db_querier = DbQuerier(
        user_name=user_name,
        db_name=db_name,
        test_type=test_type,
    )
    loader = Loader(
        test_length=test_length,
        data_querier=db_querier
    )
    loader.load_tables()
    loader.set_interro_df()
    guesser = FastapiGuesser()
    premier_test = PremierTest(
        interro_df=loader.interro_df,
        test_length=loader.test_length,
        guesser=guesser
    )
    return loader, premier_test


def get_old_interro_dict(interro_dict):
    """
    Get the old interro dict out of the original interro dict.
    """
    while isinstance(interro_dict, str):
        interro_dict = ast.literal_eval(interro_dict)
    old_interro_df = pd.DataFrame(interro_dict)
    old_interro_df = old_interro_df[['foreign', 'native']]
    old_interro_df = old_interro_df.to_json(orient='records')
    return old_interro_df


def get_error_messages(error_message: str):
    """
    Get the error messages from the error message.
    """
    messages = [
        "Empty table",
        "Settings saved successfully",
        ''
    ]
    if error_message == messages[0]:
        result = 'No words in the selected table'
    elif error_message == messages[1]:
        result = ''
    elif error_message == messages[2]:
        result = ''
    else:
        logger.error(f"Error message incorrect: {error_message}")
        logger.error(f"Should be in: {messages}")
        raise ValueError
    return result


def get_interro_category(interro: Interro) -> str:
    """
    Check if the interro object is a premier test or a rattrap.
    """
    if hasattr(interro, 'perf'):
        result = 'test'
    elif hasattr(interro, 'rattrap'):
        result = 'rattrap'
    else:
        logger.error(
            "Unknown interro object, should have either a perf or a rattrap attribute!"
        )
        logger.error(f"Interro object: {type(interro)}")
        raise ValueError
    return result


def turn_df_into_dict(words_df: pd.DataFrame) -> Dict:
    """
    Turn the dataframe into a dictionary.
    """
    headers = list(words_df.columns)
    rows = words_df.values.tolist()
    return headers, rows


def decode_dict(interro_dict):
    """
    Prepare interro_df for words extraction.
    Two times escaping is necessary.
    """
    interro_df = pd.DataFrame(interro_dict)
    if 'creation_date' in interro_df.columns:
        if 'index' in interro_df.columns:
            interro_df = interro_df.set_index('index')
        interro_df.index.name = None
        try:
            interro_df['creation_date'] = pd.to_datetime(interro_df['creation_date'], unit='ms')
            interro_df['creation_date'] = interro_df['creation_date'].dt.strftime('%Y-%m-%d')
        except ValueError:
            pass
    return interro_df


def get_faults_df(faults_dict):
    """
    Empty faults dict can be turned into None on client side.
    """
    if faults_dict in [None, 'None', []]:
        faults_df = pd.DataFrame(columns=['foreign', 'native'])
    else:
        faults_df = decode_dict(faults_dict)
    return faults_df


def get_interro(params):
    """
    Get the interro object.
    """
    interro_df = decode_dict(params.interroDict)
    interro_category = params.interroCategory
    if interro_category == 'test':
        faults_df = get_faults_df(params.faultsDict)
        interro = PremierTest.from_dict({
            'testLength': params.testLength,
            'interroTable': interro_df,
            'faultsTable': faults_df,
            'testIndex': int(params.testIndex),
            'testPerf': params.testPerf
        })
    elif interro_category == 'rattrap':
        guesser = FastapiGuesser()
        old_interro_df = decode_dict(params.oldInterroDict)
        rattrap = Rattrap(
            interro_df=interro_df,
            guesser=guesser,
            old_interro_df=old_interro_df
        )
        rattrap.reshuffle_words_table()
        interro = rattrap
    else:
        logger.error(f"Unknown interro category: {interro_category}")
        raise ValueError
    return interro


def update_interro(interro, params):
    """
    Update the interro object.
    """
    index = int(params.testIndex)
    score = int(params.testScore)
    if params.userAnswer == 'Yes':
        score += 1
        update = True
    elif params.userAnswer == 'No':
        interro_df = decode_dict(params.interroDict)
        update = False
        foreign = interro_df.loc[index][0]
        foreign = foreign.replace("'", "\'")
        native = interro_df.loc[index][1]
        native = native.replace("'", "\'")
        interro.update_faults_df(
            word_guessed=update,
            row=[foreign, native]
        )
    else:
        logger.error(f"Unknown user answer: {params.userAnswer}")
        raise ValueError
    if params.interroCategory == 'test':
        interro.update_interro_df(word_guessed=update)
        count = int(params.testCount)
        if count < int(params.testLength):
            interro.update_index()
    return interro, score


def get_attributes_dict(token, interro, params, score):
    """
    Get the attributes dictionary.

    USed by get_user_answer()
    """
    attributes_dict = interro.to_dict()
    if params.interroCategory != 'test':
        attributes_dict['testIndex'] = 0
    attributes_dict['message'] = "User response stored successfully"
    attributes_dict['token'] = token
    attributes_dict['testCount'] = params.testCount
    attributes_dict['databaseName'] = params.databaseName
    attributes_dict['interroCategory'] = params.interroCategory
    attributes_dict['oldInterroDict'] = str(params.oldInterroDict)
    attributes_dict['testScore'] = score
    attributes_dict['testType'] = params.testType
    return attributes_dict


def save_result(token, params):
    """
    Save the result of the interro.
    """
    interro_df = decode_dict(params.interroDict)
    faults_df = get_faults_df(params.faultsDict)
    premier_test = PremierTest.from_dict({
        'testLength': params.testLength,
        'interroTable': interro_df,
        'faultsTable': faults_df,
        'testIndex': params.testIndex,
        'testPerf': params.testPerf
    })
    premier_test.compute_success_rate()
    # -----
    user_name = get_user_name_from_token(token=token)
    db_querier = DbQuerier(
        user_name=user_name,
        db_name=params.databaseName,
        test_type=params.testType,
    )
    loader = Loader(
        test_length=params.testLength,
        data_querier=db_querier
    )
    loader.load_tables()
    updater = Updater(
        loader=loader,
        interro=premier_test
    )
    updater.update_data()


def update_test(params, interro_df, token):
    """
    Update the test.

    USed by end_interro()
    """
    test_length = params.testLength
    faults_df = get_faults_df(params.faultsDict)
    premier_test = PremierTest.from_dict({
        'faultsTable': faults_df,
        'interroTable': interro_df,
        'testIndex': params.testIndex,
        'testPerf': params.testPerf,
        'testLength': test_length,
    })
    premier_test.compute_success_rate()
    user_name = get_user_name_from_token(token=token)
    db_querier = DbQuerier(
        user_name=user_name,
        db_name=params.databaseName,
        test_type=params.testType,
    )
    loader = Loader(
        test_length=test_length,
        data_querier=db_querier
    )
    loader.load_tables()
    updater = Updater(
        loader=loader,
        interro=premier_test
    )
    updater.update_data()
