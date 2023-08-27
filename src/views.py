"""
    Main purpose: user interface.
"""

from tkinter import messagebox
from typing import List


class CliGuesser():
    """View in MVC pattern."""
    def ask_word(self, title: str, row: List[str]):
        """Ask a word to the user through a GUI"""
        mot_etranger = row[0]
        text_1 = f"Quelle traduction donnez-vous pour : {mot_etranger}?"
        user_answer = messagebox.showinfo(title=title, message=text_1)
        if user_answer is False:
            print("# ERROR: Interruption by user")
            raise SystemExit

    def check_word(self, title: str, row: str) -> bool:
        """Ask the user to decide if the answer was correct or not."""
        mot_natal = row[1]
        text_2 = f"Voici la traduction correcte : \'{mot_natal}\'. \nAviez-vous la bonne réponse ?"
        word_guessed = messagebox.askyesnocancel(title=title, message=text_2)
        if word_guessed is None:
            print("# ERROR: Interruption by user")
            raise SystemExit
        return word_guessed

    def guess_word(self, row: List[str], title: str):
        """Given an index, ask a word to the user, and return a boolean."""
        self.ask_word(title, row)
        word_guessed = self.check_word(title, row)
        return word_guessed
