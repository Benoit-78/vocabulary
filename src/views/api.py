"""
    Main purpose:
        User web interfaces.
"""

from typing import List



class FastapiGuesser():
    """
    FastApi UI
    """
    def ask_word(self, row: List[str]):
        """
        Ask a word to the user
        """
        mot_etranger = row[1]
        return mot_etranger

    def return_translation(self, row: List[str]):
        """
        Return translation to the user
        """
        mot_natal = row[2]
        return mot_natal

    # def get_user_answer(self) -> bool:
    #     """
    #     Ask the user to decide if the answer was correct or not.
    #     """
    #     user_answer = "No"
    #     if user_answer == 'Yes':
    #         word_guessed = True
    #     if user_answer == 'No':
    #         word_guessed = False
    #     return word_guessed

    def guess_word(self, row: List[str], i: int, words: int):
        """
        Steps of the user's guessing process.
        """
        self.ask_word(row)
        self.return_translation(row)
        # self.get_user_answer()
        return False
