"""
    Creation date:
        13th July 2024
    Creator:
        Benoît DELORME
    Main purpose:
        Call the Deepl API to provide translation to user's inputs
"""

import os

import deepl
from loguru import logger

API_KEY: str = os.environ["DEEPL_API_KEY"]
deepl.http_client.max_network_retries = 3
translator = deepl.Translator(API_KEY)


def translate_documents(input_path: str, output_path: str):
    """
    Sending a whole document to DeepL is costly in tokens.
    Better is to decompose the document content as a list of words.
    """
    input_path = 'data/deepl_in.xlsx'
    output_path = 'data/deepl_out_less.xlsx'
    try:
        translator.translate_document_from_filepath(
            input_path,
            output_path,
            target_lang="FR",
            formality="less"
        )
    except deepl.DocumentTranslationException as error:
        logger.error(f"Error after uploading ${error}")
    except deepl.DeepLException as error:
        logger.error(f"Error has occurred: {error}")
    logger.debug("After document translation")
