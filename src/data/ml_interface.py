"""
    Creation date:
        5th May 2024
    Creator:
        B.Delorme
    Main purpose:
        
"""
# import os
import pickle
# import sys

from abc import ABC, abstractmethod

# REPO_NAME = 'vocabulary'
# REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
# if REPO_DIR not in sys.path:
#     sys.path.append(REPO_DIR)



class MLHandler(ABC):
    """
    Class that defines the interface between the app and the Machine Learning models.

    Mish-mash between dev and MLOps.
    """
    def __init__(self, user_name, db_name):
        self.user_name = user_name
        self.db_name = db_name

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def predict(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def delete(self):
        pass
