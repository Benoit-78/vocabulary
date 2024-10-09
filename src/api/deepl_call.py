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

API_KEY = os.getenv("DEEPL_API_KEY")

deepl.http_client.max_network_retries = 3

translator = deepl.Translator(API_KEY)


# ----- Text words
try:
    result = translator.translate_text(
        "Hello",
        source_lang='EN',
        target_lang='FR',
        formality='less',
        context='aggressive'
        # split_sentences='on'
    )
    print(result.text)
except deepl.exceptions.DeepLException as exc:
    logger.error(exc)


def translate_documents(input_path: str, output_path: str):
    """
    Sending a whole document to DeepL is costly in tokens.
    Better is to decompose the document content as a list of words.
    """
    input_path = 'data/deepl_in.xlsx'
    output_path = 'data/deepl_out_less.xlsx'
    logger.debug("Before document translation")
    try:
        translator.translate_document_from_filepath(
            input_path,
            output_path,
            target_lang="FR",
            formality="less"
        )
        # Alternatively you can use translate_document() with file IO objects
        # with open(input_path, "rb") as in_file, open(output_path, "wb") as out_file:
        #     translator.translate_document(
        #         in_file,
        #         out_file,
        #         target_lang="DE",
        #         formality="more"
        #     )
    except deepl.DocumentTranslationException as error:
        # The document_handle property contains the document handle that may be used to
        # later retrieve the document from the server, or contact DeepL support.
        doc_id = error.document_handle.id
        doc_key = error.document_handle.key
        logger.error(f"Error after uploading ${error}, id: ${doc_id} key: ${doc_key}")
    except deepl.DeepLException as error:
        # Errors during upload raise a DeepLException
        logger.error(error)
    logger.debug("After document translation")
