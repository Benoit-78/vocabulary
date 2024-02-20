"""
    Creator:
        B.Delorme
    Creation date:
        9th December 2023
    Main purpose:
        Test function for utils module.
"""

import logging
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src.utils import data



class TestUtils(unittest.TestCase):
    """
    Methods that tests functions of data module.
    """
    def test_complete_columns(self):
        """
        Guarantee that the well_known_words dataframe contains exactly 
        the columns of the output dataframe.
        """
        # Arrange
        df_1 = pd.DataFrame(columns=['col1', 'col2', 'col3'])
        df_2 = pd.DataFrame(columns=['col1', 'col4'])
        # Act
        df_1 = data.complete_columns(df_1, df_2)
        # Assert
        self.assertIn('col4', df_1)
