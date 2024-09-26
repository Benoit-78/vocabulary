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

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src.utils import system



class TestUtils(unittest.TestCase):
    """
    Methods that tests functions of utils module.
    """
    @patch('platform.platform', return_value='Ubuntu')
    def test_get_os_type_error(self, mock_platform):
        """
        Error should be raised in case of unknown system.
        """
        # Arrange
        mock_logger = MagicMock()
        logging.basicConfig(level=logging.ERROR)
        with patch('src.utils.system.logger', mock_logger):
            # Act
            _ = system.get_os_type()
        # Assert
        mock_logger.error.assert_called_with("Operating system cannot be identified.")
        mock_logger.warning.assert_called_with("Operating system was arbitrarily set to 'linux'.")
        mock_logger.error.assert_called_once()

    @patch('platform.platform', return_value='Windows-10-10.0.18362-SP0')
    def test_get_os_type_windows(self, mock_platform):
        """
        Windows should be recognized a valid os.
        """
        # Act
        os_type = system.get_os_type()
        # Assert
        self.assertEqual(os_type, 'Windows')

    @patch('platform.platform', return_value='Linux-4.15.0-65-generic-x86_64-with-Ubuntu-18.04-bionic')
    def test_get_os_type_linux(self, mock_platform):
        """
        Linux should be recognized a valid os.
        """
        # Act
        os_type = system.get_os_type()
        # Assert
        self.assertEqual(os_type, 'Linux')

    @patch('src.utils.system.get_os_type', return_value='Windows')
    def test_get_os_separator_windows(self, mock_get_os_type):
        # Act
        result = system.get_os_separator()
        # Assert
        self.assertEqual(result, '\\')

    @patch('src.utils.system.get_os_type', return_value='Linux')
    def test_get_os_separator_linux(self, mock_get_os_type):
        # Act
        result = system.get_os_separator()
        # Assert
        self.assertEqual(result, '/')

    @patch('src.utils.system.get_os_type', return_value='Mac')
    def test_get_os_separator_mac(self, mock_get_os_type):
        # Act
        result = system.get_os_separator()
        # Assert
        self.assertEqual(result, '/')

    @patch('src.utils.system.get_os_type', return_value='Android')
    def test_get_os_separator_android(self, mock_get_os_type):
        # Act
        result = system.get_os_separator()
        # Assert
        self.assertEqual(result, '/')

    @patch('src.utils.system.get_os_type', return_value='Unknown')
    def test_get_os_separator_unknown(self, mock_get_os_type):
        with self.assertRaises(NameError):
            # Assert
            system.get_os_separator()
