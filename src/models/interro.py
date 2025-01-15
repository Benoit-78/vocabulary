"""
    Creation date:
        12 January 2025
    Main purpose:
        Provide with pydantic models for interro API.
"""

import ast
from typing import Optional

from loguru import logger
from pydantic import BaseModel



class Params(BaseModel):
    """
    Standard arguments for interro API.
    """
    # Mandatory
    databaseName: str
    faultsDict: dict
    testIndex: int
    interroCategory: str
    interroDict: dict
    oldInterroDict: dict
    testScore: int
    testLength: int
    testType: str
    # Optional
    userAnswer: Optional[str]=None
    contentBox1: Optional[str]=None
    contentBox2: Optional[str]=None
    testCount: Optional[int]=None
    message: Optional[str]=''
    testPerf: Optional[int]=None

    @classmethod
    def from_query_params(cls, params: dict):
        """
        Convert query params to a Params BaseModel object.
        """
        for dict_name in ['interroDict', 'oldInterroDict', 'faultsDict']:
            while isinstance(params[dict_name], str):
                params[dict_name] = ast.literal_eval(params[dict_name])
        logger.debug(f"Query params: \n{params}")
        return cls(**params)
