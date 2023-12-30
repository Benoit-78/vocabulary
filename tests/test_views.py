"""
    Creation date:
        27th December 2023
    Main purpose:
        
"""

import os
import sys
import unittest
from unittest.mock import patch

REPO_DIR = os.getcwd().split('tests')[0]
sys.path.append(REPO_DIR)
from src import views



