"""
    Creation date:
        9th May 2024
    Creator:
        B. Delorme
    Main purpose:
        Hosts the functions of common router.
"""

import os
import sys

from fastapi.responses import JSONResponse
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.data.csv_interface import MenuReader


def change_language(data):
    """
    Change the language of the user interface.
    """
    menu_reader = MenuReader(data.get('path'))
    translations_dict = menu_reader.get_translations_dict()
    json_response = JSONResponse(
        content={
            'translations_dict': translations_dict
        }
    )
    return json_response