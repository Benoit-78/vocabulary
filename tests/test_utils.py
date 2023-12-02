"""
    TEst function for utils module.
"""

import logging
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

REPO_DIR = os.getcwd().split('tests')[0]
sys.path.append(REPO_DIR)
from src import utils
from src.utils import get_os_separator, get_os_type


class TestUtils(unittest.TestCase):
    """Methods that tests functions of utils module."""
    @patch('platform.platform', return_value='Ubuntu')
    def test_get_os_type_error(self, mock_platform):
        """Error should be raised in case of unknown OS."""
        # Arrange
        mock_logger = MagicMock()
        logging.basicConfig(level=logging.ERROR)
        with patch('src.utils.logger', mock_logger):
            # Act
            _ = utils.get_os_type()
        # Assert
        mock_logger.error.assert_called_with("Operating system cannot be identified.")
        mock_logger.warning.assert_called_with("Operating system was arbitrarily set to 'linux'.")
        mock_logger.error.assert_called_once()

    @patch('platform.platform', return_value='Windows-10-10.0.18362-SP0')
    def test_get_os_type_windows(self, mock_platform):
        """Windows should be recognized a valid OS."""
        # Act
        os_type = utils.get_os_type()
        # Assert
        self.assertEqual(os_type, 'Windows')

    @patch('platform.platform', return_value='Linux-4.15.0-65-generic-x86_64-with-Ubuntu-18.04-bionic')
    def test_get_os_type_linux(self, mock_platform):
        """Linux should be recognized a valid OS."""
        # Act
        os_type = utils.get_os_type()
        # Assert
        self.assertEqual(os_type, 'Linux')

    @patch('src.utils.get_os_type', return_value='Windows')
    def test_get_os_separator_windows(self, mock_get_os_type):
        # Act
        result = utils.get_os_separator()
        # Assert
        self.assertEqual(result, '\\')

    @patch('src.utils.get_os_type', return_value='Linux')
    def test_get_os_separator_linux(self, mock_get_os_type):
        # Act
        result = utils.get_os_separator()
        # Assert
        self.assertEqual(result, '/')

    @patch('src.utils.get_os_type', return_value='Mac')
    def test_get_os_separator_mac(self, mock_get_os_type):
        # Act
        result = utils.get_os_separator()
        # Assert
        self.assertEqual(result, '/')

    @patch('src.utils.get_os_type', return_value='Android')
    def test_get_os_separator_android(self, mock_get_os_type):
        # Act
        result = utils.get_os_separator()
        # Assert
        self.assertEqual(result, '/')

    @patch('src.utils.get_os_type', return_value='Unknown')
    def test_get_os_separator_unknown(self, mock_get_os_type):
        with self.assertRaises(NameError):
            # Assert
            utils.get_os_separator()

    def test_complete_columns(self):
        """
        Guarantee that the well_known_words dataframe contains exactly 
        the columns of the output dataframe.
        """
        # Arrange
        df_1 = pd.DataFrame(columns=['col1', 'col2', 'col3'])
        df_2 = pd.DataFrame(columns=['col1', 'col4'])
        # Act
        df_1 = utils.complete_columns(df_1, df_2)
        # Assert
        self.assertIn('col4', df_1)
