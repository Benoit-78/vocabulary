"""
    Creation date:
        9th May 2024
    Creator:
        B. Delorme
    Main purpose:
        Hosts the functions of common router.
"""

from fastapi.responses import JSONResponse

from src.data.csv_interface import MenuReader


def change_language(data: dict) -> JSONResponse:
    """
    Change the language of the user interface.
    """
    menu_reader = MenuReader(current_page=data.get('path'))
    translations_dict = menu_reader.get_translations_dict()
    json_response = JSONResponse(
        content={
            'translations_dict': translations_dict
        }
    )
    return json_response
