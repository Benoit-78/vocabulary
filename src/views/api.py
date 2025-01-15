"""
    Main purpose:
        User web interfaces.
"""

from typing import List



class FastapiGuesser():
    """
    FastApi UI
    """
    def ask_word(self, row: List[str]) -> str:
        """
        Ask a word to the user
        """
        mot_etranger = row[1]
        return mot_etranger

    def return_translation(self, row: List[str]) -> str:
        """
        Return translation to the user
        """
        mot_natal = row[2]
        return mot_natal

    def guess_word(self, row: List[str], words: int) -> bool:
        """
        Steps of the user's guessing process.
        """
        self.ask_word(row)
        self.return_translation(row)
        return False
