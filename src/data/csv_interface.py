"""
    Creator:
        B. DELORME
    Main purpose:
        Provide with all methods necessary to interact with csv files.
"""

from typing import Dict

import pandas as pd
from loguru import logger

from src.utils.system_i import get_os_separator



class DataHandler():
    """
    Provide with all methods necessary to interact with csv files.
    """
    def __init__(self, test_type: str):
        self.test_type = test_type
        self.os_sep = get_os_separator()
        self.paths: Dict[str, str] = {}
        self.tables: Dict[str, pd.DataFrame] = {}

    def set_paths(self):
        """
        List paths to data csv.
        """
        self.paths[self.test_type + '_voc'] = self.os_sep.join(
            [r'.', 'data', self.test_type + '_voc.csv']
        )
        self.paths[self.test_type + '_perf'] = self.os_sep.join(
            [r'.', 'data', self.test_type + '_perf.csv']
        )
        self.paths[self.test_type + '_word_cnt'] = self.os_sep.join(
            [r'.', 'data', self.test_type + '_words_count.csv']
        )
        if self.test_type == 'version':
            self.paths['output'] = self.os_sep.join(['.', 'data', 'theme_voc.csv'])
        elif self.test_type == 'theme':
            self.paths['output'] = self.os_sep.join(['.', 'data', 'archives.csv'])
        else:
            logger.error(f"Wrong test_type argument: {self.test_type}")
            raise SystemExit

    def set_tables(self):
        """
        Load the different tables necessary to the app.
        """
        self.set_paths()
        self.tables[self.test_type + '_voc'] = pd.read_csv(
            self.paths[self.test_type + '_voc'],
            sep=';',
            encoding='utf-8'
        )
        self.tables[self.test_type + '_perf'] = pd.read_csv(
            self.paths[self.test_type + '_perf'],
            sep=';',
            encoding='utf-8'
        )
        self.tables[self.test_type + '_word_cnt'] = pd.read_csv(
            self.paths[self.test_type + '_word_cnt'],
            sep=';',
            encoding='utf-8'
        )
        self.tables['output'] = pd.read_csv(
            self.paths['output'],
            sep=';',
            encoding='utf-8'
        )

    def get_paths(self) -> Dict[str, str]:
        """
        Return the paths
        """
        self.set_paths()
        return self.paths

    def get_tables(self) -> Dict[str, pd.DataFrame]:
        """
        Load the tables
        """
        self.set_tables()
        return self.tables

    def save_table(self, table_name: str, table: pd.DataFrame):
        """
        Save given table.
        """
        self.set_paths()
        table.to_csv(
            self.paths[table_name],
            index=False,
            sep=';',
            encoding='utf-8'
        )



class MenuReader():
    """
    Provide with all methods necessary to interact with csv files.
    """
    def __init__(self, current_page: str):
        self.os_sep = get_os_separator()
        self.path = ''
        self.page = current_page.split('/')[1] + '.html'

    def set_path(self):
        """
        Define the path to the menu csv file.
        """
        self.path = self.os_sep.join([
            r'.',
            'data',
            'menus.csv'
        ])

    def get_translations_dict(self) -> Dict[str, Dict[str, str]]:
        """
        Load the tables
        """
        self.set_path()
        menus_df = pd.read_csv(self.path, sep=';', encoding='utf-8')
        menus_df = menus_df[menus_df['page']==self.page]
        translations_dict = {}
        for _, row in menus_df.iterrows():
            original_text = str(row['standard'])
            translated_text_fo = str(row['foreign'])
            translated_text_na = str(row['native'])
            translations_dict[original_text] = {
                'fo': translated_text_fo,
                'na': translated_text_na
            }
        return translations_dict
