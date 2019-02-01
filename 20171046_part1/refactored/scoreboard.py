"""Scoreboard Module"""

import sys
from colorama import Back, Style
from config import ROWS, COLUMNS, pos


class ScoreBoard():
    """Score Class"""
    def __init__(self):
        self.life = 3
        self.score = 0

    def score_update(self, typ):
        """Updating score"""
        if typ == "enemy":
            self.score = self.score + 10
        elif typ == "coin":
            self.score = self.score + 5
        elif typ == "time":
            self.score = self.score + 1
        elif typ == "bossenemy":
            self.score = self.score + 100

    def life_update(self):
        """Updating lives"""
        self.life = self.life - 1
        if self.life <= 0:
            self.show_score()
            sys.stdout.write(Back.RED + pos(ROWS-2, 0) +
                             "Bro you dead".center(COLUMNS))
            exit()

    def show_score(self, fin=""):
        """Show score"""
        disp = fin + "Score: " + str(self.score) + "     Lives: " +\
               str(self.life)
        sys.stdout.write(Back.YELLOW + Style.BRIGHT + pos(ROWS-3, 0) +
                         disp.center(COLUMNS))
