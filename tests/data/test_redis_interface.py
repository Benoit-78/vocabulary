"""
    Creator:
        B.Delorme
    Creation date:
        20th April 2024
    Main purpose:
        Test script for 
"""

import os
import pickle
import sys
import unittest
from unittest.mock import MagicMock

# from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.data import redis_interface



class TestRedisInterface(unittest.TestCase):
    def setUp(self):
        """
        Create a mock Redis connection
        """
        self.mock_redis_db = MagicMock()
        self.test_object = {
            'question': 'What is the answer to life, the universe, and everything?',
            'answer': 42
        }
        self.loader_object = {
            'name': 'TestLoader',
            'load': 'TestLoader loaded'
        }

    def test_save_interro_in_redis(self):
        """
        Should save a test object in redis database.
        """
        # ----- ARRANGE
        token = 'test_token'
        interro_category = 'mock_category'
        # ----- ACT
        redis_interface.save_interro_in_redis(
            interro=self.test_object,
            token=token,
            interro_category=interro_category,
            redis_db=self.mock_redis_db
        )
        # ----- ASSERT
        self.mock_redis_db.set.assert_called_once_with(
            'test_token_mock_category',
            pickle.dumps(self.test_object)
        )

    def test_load_interro_from_redis(self):
        """
        Should load a test object from redis database.
        """
        # ----- ARRANGE
        token = 'test_token'
        interro_category = 'mock_category'
        pickled_test_object = pickle.dumps(self.test_object)
        self.mock_redis_db.get.return_value = pickled_test_object
        # ----- ACT
        result = redis_interface.load_interro_from_redis(
            token=token,
            interro_category=interro_category,
            redis_db=self.mock_redis_db
        )
        # ----- ASSERT
        self.assertEqual(result, self.test_object)
        self.mock_redis_db.get.assert_called_once_with('test_token_mock_category')

    def test_save_loader_in_redis(self):
        """
        Should save a loader object in redis database.
        """
        # ----- ARRANGE
        token = 'test_token'
        # ----- ACT
        redis_interface.save_loader_in_redis(
            self.loader_object,
            token,
            redis_db=self.mock_redis_db
        )
        # ----- ASSERT
        self.mock_redis_db.set.assert_called_once_with(
            token + '_loader',
            pickle.dumps(self.loader_object)
        )

    def test_load_loader_from_redis(self):
        """
        Should load a loader object from redis database.
        """
        # ----- ARRANGE
        token = 'test_token'
        pickled_loader_object = pickle.dumps(self.loader_object)
        self.mock_redis_db.get.return_value = pickled_loader_object
        # ----- ACT
        result = redis_interface.load_loader_from_redis(
            token,
            redis_db=self.mock_redis_db
        )
        # ----- ASSERT
        self.assertEqual(result, self.loader_object)
