"""
    Creation date:
        16th December 2023
    Main purpose:

"""

import os
import sys
from abc import ABC, abstractmethod

import pandas as pd
import plotly.express as px
import plotly.io as pio
from loguru import logger

APP_DIR = 'vocabulary'
APP_PATH = os.getcwd().split(APP_DIR)[0] + APP_DIR
sys.path.append(APP_PATH)
from src.data.data_handler import MariaDBHandler



class Graph(ABC):
    """Abstract class for creating and saving user-specific graphs."""
    def __init__(self, db_handler):
        """Constructor should get a database handler, such as MariaDBHandler"""
        self.db_handler = db_handler
        self.data = pd.DataFrame()

    @abstractmethod
    def set_data(self):
        """Fetch the data that will feed the graph."""

    @abstractmethod
    def create(self):
        """
        Display the data in a graph
        and return this graph as an html file.
        """



class Graph1(Graph):
    """
    Graph that represents the success rate of each word
    in function of the number of times it has been asked.
    """
    def set_data(self):
        """See abstract method description"""
        tables = self.db_handler.get_tables()
        voc_table_name = list(tables.keys())[0]
        logger.debug(f"voc_table_name: {voc_table_name}")
        voc_table = tables[voc_table_name]
        logger.debug(f"voc_table head: \n{voc_table.head()}")
        self.data = voc_table[[
            self.db_handler.language_1.lower(),
            'nb',
            'taux'
        ]]

    def correct_data(self):
        """Correct imprecisions or errors in the data"""
        logger.debug(self.data.head())
        self.data = self.data[self.data['taux']<=100]
        self.data = self.data[self.data['taux']>=-100]

    def create(self):
        """See abstract method description"""
        self.set_data()
        self.correct_data()
        logger.debug(f"\n{self.data.head()}")
        fig = px.scatter(
            x=list(self.data['nb']),
            y=list(self.data['taux']),
            labels={
                'x': 'Count',
                'y': 'Success rate'
            },
            title='Graph 1'
        )
        graph_html = pio.to_html(fig, full_html=False)
        return graph_html



def load_graphs():
    """Load the user's graphs"""
    html_graphs = []
    # Version
    data_handler = MariaDBHandler(test_type='version', mode='web_local', language_1='english')
    graph_1 = Graph1(data_handler)
    graph_1_html = graph_1.create()
    html_graphs.append(graph_1_html)
    return html_graphs
