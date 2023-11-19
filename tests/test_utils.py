"""
    TEst function for utils module.
"""

import unittest
import sys
import logging
from unittest.mock import patch, MagicMock

sys.path.append('..\\')
from src import utils


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

    @patch(
        'platform.platform',
        return_value='Linux-4.15.0-65-generic-x86_64-with-Ubuntu-18.04-bionic'
    )
    def test_get_os_type_linux(self, mock_platform):
        """Linux should be recognized a valid OS."""
        # Act
        os_type = utils.get_os_type()
        # Assert
        self.assertEqual(os_type, 'Linux')

    def test_set_os_separator(self):
        """Separator should be OS-specific"""
        # Arrange
        os_type = utils.get_os_type()
        # Happy paths
        os_sep = utils.get_os_separator()
        if os_type == 'Windows':
            self.assertEqual(os_sep, '\\')
        elif os_type in ['Linux', 'Android', 'Mac']:
            self.assertEqual(os_sep, '/')
        # Sad paths
