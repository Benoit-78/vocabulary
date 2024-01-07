"""
    Main purpose: user local interface, for CLI.
"""

from tkinter import messagebox
from typing import List

from loguru import logger


class CliGuesser():
    """Command Line Interface"""
    def ask_word(self, row: List[str], title: str):
        """Ask a word to the user through a GUI"""
        mot_etranger = row[0]
        text_1 = f"Quelle traduction donnez-vous pour : {mot_etranger}?"
        user_answer = messagebox.showinfo(title=title, message=text_1)
        if user_answer is False:
            logger.error("Interruption by user")
            raise SystemExit

    def get_user_answer(self, row: str, title: str) -> bool:
        """Ask the user to decide if the answer was correct or not."""
        mot_natal = row[1]
        text_2 = f"Voici la traduction correcte : \'{mot_natal}\'. \nAviez-vous la bonne réponse ?"
        word_guessed = messagebox.askyesnocancel(title=title, message=text_2)
        if word_guessed is None:
            logger.error("Interruption by user")
            raise SystemExit
        return word_guessed

    def guess_word(self, row: List[str], i: int, words: int):
        """Given a row, ask a word to the user, and return a boolean."""
        title = f"Word {i}/{words}"
        self.ask_word(row, title)
        word_guessed = self.get_user_answer(row, title)
        return word_guessed
