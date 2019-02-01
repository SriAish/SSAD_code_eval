from colorama import Back, Fore, Style
from config import MARGINX, MARGINY, ROWS, COLUMNS
from config import pos
import sys


class ScoreBoard():
    """Score Class"""
    def __init__(self):
        self.life = 3
        self.score = 0

    def scoreUpdate(self, type):
        if type == "enemy":
            self.score = self.score + 10
        elif type == "coin":
            self.score = self.score + 5
        elif type == "time":
            self.score = self.score + 1
        elif type == "bossenemy":
            self.score = self.score + 100

    def lifeUpdate(self):
        self.life = self.life - 1
        if self.life <= 0:
            self.showScore()
            sys.stdout.write(Back.RED + pos(ROWS-2, 0) +
                             "Bro you dead".center(COLUMNS))
            exit()

    def showScore(self, fin=""):
        disp = fin + "Score: " + str(self.score) + "     Lives: " +\
               str(self.life)
        sys.stdout.write(Back.YELLOW + Style.BRIGHT + pos(ROWS-3, 0) +
                         disp.center(COLUMNS))
