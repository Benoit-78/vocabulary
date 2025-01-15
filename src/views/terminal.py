"""
    Main purpose: user local interface, for CLI.
"""

import argparse
import sys

from tkinter import messagebox
from typing import List

from loguru import logger



class CliUser():
    """
    User who launchs the app through the CLI.
    """
    def __init__(self):
        self.settings = None

    def parse_arguments(self, arg: List[str]):
        """
        Parse command line argument.
        """
        another_parser = argparse.ArgumentParser()
        another_parser.add_argument("-t", "--type", type=str)
        another_parser.add_argument("-l", "--test_length", type=int)
        another_parser.add_argument("-r", "--rattrap", type=int)
        if '-t' not in arg:
            arg.append('-t')
            arg.append('version')
        if '-l' not in arg:
            arg.append('-l')
            arg.append('10')
        if '-r' not in arg:
            arg.append('-r')
            arg.append('2')
        self.settings = another_parser.parse_args(arg)

    def get_settings(self):
        """
        Check the kind of interro, version or theme.
        """
        self.parse_arguments(sys.argv[1:])
        cond_1 = not self.settings.type
        cond_2 = not self.settings.test_length
        cond_3 = not self.settings.rattrap
        if cond_1 or cond_2 or cond_3:
            message = ' '.join([
                "Please give",
                "-t <test type>, ",
                "-l <test length> and ",
                "-r <number of rattrap>"
            ])
            logger.error(message)
            raise SystemExit
        if self.settings.type not in ['version', 'theme']:
            logger.error("Test type must be either version or theme")
            raise SystemExit
        if self.settings.rattrap < -1:
            logger.error("Number of rattrap must be greater than -1.")
            raise SystemExit
        if self.settings.test_length < 1:
            logger.error("Test length must be greater than 0.")
            raise SystemExit



class CliGuesser():
    """
    Command Line Interface
    """
    def ask_word(self, row: List[str], title: str):
        """
        Ask a word to the user through a GUI
        """
        mot_etranger = row[0]
        text_1 = f"Quelle traduction donnez-vous pour : {mot_etranger}?"
        user_answer = messagebox.showinfo(title=title, message=text_1)
        if user_answer is False:
            logger.error("Interruption by user")
            raise SystemExit

    def get_user_answer(self, row: List[str], title: str) -> bool:
        """
        Ask the user to decide if the answer was correct or not.
        """
        mot_natal = row[1]
        text_2 = f"Voici la traduction correcte : \'{mot_natal}\'. \nAviez-vous la bonne réponse ?"
        word_guessed = messagebox.askyesnocancel(title=title, message=text_2)
        if word_guessed is None:
            logger.error("Interruption by user")
            raise SystemExit
        return word_guessed

    def guess_word(self, row: List[str], i: int, words: int) -> bool:
        """
        Given a row, ask a word to the user, and return a boolean.
        """
        title = f"Word {i}/{words}"
        self.ask_word(row, title)
        word_guessed = self.get_user_answer(
            row=row,
            title=title
        )
        return word_guessed
