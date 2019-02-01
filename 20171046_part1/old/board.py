import numpy as np
from config import pos, ROWS, COLUMNS
from elements import Brick
from colorama import init, Fore, Back, Style
from elements import Brick, Cloud, Coin, Lake, Platform
from people import Enemy, BossEnemy
import sys
import os
from random import randint


class Board():
    """Board Class"""

    def __init__(self, height, width):
        assert isinstance(height, int) is True
        assert isinstance(width, int) is True

        self.height = height
        self.width = width
        self._board = np.chararray((height, width), unicode=True)
        self._board[:, :] = " "

        # this stores all the bombs bricks and enemies that spawn
        self._storage = {
            "cloud": [],
            "platform": [],
            "brick": [],
            "lake": [],
            "enemy": [],
            "coin": [],
            "bossenemy": [],
            "bullet": []
        }

        self.player = []

        self.board()

    def addBoard(self, element):
        height, width = element.getSize()
        x, y = element.getCoord()
        self._board[y: y + height,
                    x: x + width] = element.structure

    def clear(self, element):
        height, width = element.getSize()
        x, y = element.getCoord()
        if element.getType() == "lake":
            self._board[y, x:x+width] = "-"
            self._board[y+1, x:x+width] = " "
        else:
            self._board[y: y + height, x: x + width] = " "

    def clearStorage(self, element):
        if element.getType() == "player":
            self.player.remove(element)
        else:
            self._storage[element.getType()].remove(element)

    def addStorage(self, element):
        if element.getType() == "player":
            self.player.append(element)
        elif element not in self._storage[element.getType()]:
            self._storage[element.getType()].append(element)

    def onBoard(self, ch):
        return len(self._storage[ch])

    def board(self):
        # creating the rows
        full_row = np.chararray((2, self.width), unicode=True)
        full_row[:, :] = "$"
        emp_row = np.chararray((2, self.width), unicode=True)
        emp_row[:, :] = " "
        emp_row[:, :2] = emp_row[:, -2:] = "$"
        land_row = np.chararray((1, self.width), unicode=True)
        land_row[:, :] = "-"
        land_row[:, :2] = land_row[:, -2:] = "$"
        # assigning top and bottom
        self._board[:2, :] = self._board[-2:, :] = full_row
        # assigning other rows
        for r in range(2, int(self.height / 2)):
            self._board[(r - 1) * 2: (r * 2), :] = emp_row
        # making land
        self._board[int(3*self.height/4), :] = land_row

    def render(self):
        '''# displaying the board at every frame'''

        temp_board = np.matrix(self._board)
        for row in range(self.height):
            for col in range(self.width):
                sys.stdout.write(Style.BRIGHT + pos(row+3, col+6) +
                                 self._board[row, col])
        del temp_board

    def checkPath(self, element, x, y):
        height, width = element.getSize()
        emp_mat = np.chararray((height, width), unicode=True)
        emp_mat[:, :] = " "

        # mario can land and kill Enemy otherwise get killed by enemy
        if element.getType() == "player":
            for en in self._storage["enemy"]:
                x_en, y_en = en.getCoord()
                if (x, y + 1) == (x_en, y_en) or\
                   (x+1, y + 1) == (x_en, y_en) or\
                   (x, y + 1) == (x_en+1, y_en):
                    self._storage["enemy"].remove(en)
                    en.alive = False
                    en.remove(self)
                    element.scoreboard.scoreUpdate("enemy")
                    sys.stdout.write(pos(ROWS-2, 0) +
                                     str(os.system('aplay mb_touch.wav&')))
                    return True
                if (x+1, y) == (x_en, y_en) or\
                   (x+1, y+1) == (x_en, y_en) or\
                   (x, y) == (x_en+1, y_en) or\
                   (x, y+1) == (x_en+1, y_en):
                    en.alive = False
                    element.scoreboard.lifeUpdate()
                    self._storage["enemy"].remove(en)
                    en.remove(self)
                    sys.stdout.write(pos(ROWS-2, 0) +
                                     str(os.system('aplay mb_die.wav&')))
                    return True

            for cn in self._storage["coin"]:
                x_cn, y_cn = cn.getCoord()
                if (x, y) == (x_cn, y_cn+1) or\
                   (x+1, y+1) == (x_cn, y_cn) or\
                   (x, y) == (x_cn+1, y_cn+1) or\
                   (x, y) == (x_cn+1, y_cn) or\
                   (x+1, y) == (x_cn, y_cn+1) or\
                   (x+1, y) == (x_cn, y_cn) or\
                   (x, y+1) == (x_cn+1, y_cn) or\
                   (x, y+1) == (x_cn, y_cn):
                    self._storage["coin"].remove(cn)
                    cn.remove(self)
                    return True

            for lk in self._storage["lake"]:
                x_lk, y_lk = lk.getCoord()
                if (x, y+1) == (x_lk, y_lk) or\
                   (x+1, y+1) == (x_lk, y_lk) or\
                   (x, y+1) == (x_lk+1, y_lk) or\
                   (x, y+1) == (x_lk+2, y_lk):
                    element.scoreboard.lifeUpdate()
                    self._storage["lake"].remove(lk)
                    lk.remove(self)
                    sys.stdout.write(pos(ROWS-2, 0) +
                                     str(os.system('aplay mb_die.wav&')))
                    return False

        elif element.getType() == "enemy":
                x_pl, y_pl = self.player[0].getCoord()
                if (x_pl+1, y_pl) == (x, y) or\
                   (x_pl+1, y_pl+1) == (x, y) or\
                   (x_pl, y_pl) == (x+1, y) or\
                   (x_pl, y_pl+1) == (x+1, y):
                    element.alive = False
                    element.remove(self)
                    self._storage["enemy"].remove(element)
                    self.player[0].scoreboard.lifeUpdate()
                    sys.stdout.write(pos(ROWS-2, 0) + " ")
                    os.system('aplay mb_die.wav&')
                    return False

        elif element.getType() == "brick":
            for en in self._storage["enemy"]:
                x_en, y_en = en.getCoord()
                if (x+1, y) == (x_en, y_en) or\
                   (x+1, y+1) == (x_en, y_en) or\
                   (x, y) == (x_en+1, y_en) or\
                   (x, y+1) == (x_en+1, y_en):
                    en.moveLeft(self)
                    return True

        elif element.getType() == "bullet":
            if np.all(self._board[y:y+1, x:x+1] != emp_mat):
                ben = self._storage["bossenemy"][0]
                ben.life = ben.life - 1
                element.remove(self)
                self._storage["bullet"].remove(element)
                if ben.life <= 0:
                    ben.alive = False
                    self.player[0].scoreboard.scoreUpdate("bossenemy")
                    self.player[0].scoreboard.showScore("Final Score:: ")
                    self._storage["bossenemy"].remove(ben)
                    ben.remove(self)
                    msg = "You Won!! and still it doesn't matter:-p"
                    sys.stdout.write(Back.RED + pos(ROWS-2, 0) +
                                     msg.center(COLUMNS))
                    exit()
                return False

        if np.all(self._board[y: y + height, x:x + width] == emp_mat):
            return True
        return False

    def moveLeft(self):
        self.player[0].remove(self)
        emp_col = np.chararray((self.height, 1), unicode=True)
        emp_col[:, :] = " "
        emp_col[:2, :] = emp_col[-2:, :] = "$"
        emp_col[int(3*self.height/4), :] = "-"
        for typs in self._storage:
            for ele in self._storage[typs]:
                ele.moveLeft(self)
        self.player[0].show(self)

    def addGame(self, element):
        emp_mat = np.chararray(element.getSize(), unicode=True)
        emp_mat[:, :] = " "
        x, y = element.getCoord()
        height, width = element.getSize()
        if element.getType() == "bossenemy":
            self.addBoard(element)
            self.addStorage(element)
            return True
        elif np.all(self._board[y: y + height, x: x + width] == emp_mat):
            self.addBoard(element)
            self.addStorage(element)
            return True
        elif element.getType() == "lake":
            self.addBoard(element)
            self.addStorage(element)
            return True

        if element.getType() == "bullet":
            element.show(self)
        return False

    def updateEnemys(self):
        for en in self._storage["enemy"]:
            en.move(self)

    def updateBullets(self):
        for bl in self._storage["bullet"]:
            bl.moveRight(self)

    def addMore(self):
        if self.player[0].scoreboard.score > 200 and \
           len(self._storage["bossenemy"]) < 1:
            for typ in self._storage:
                for ele in self._storage[typ]:
                    ele.remove(self)
                    self._storage[typ].remove(ele)
            self.addGame(BossEnemy(self.height, self.width))
            for i in self._storage["bossenemy"]:
                i.show(self)
        elif self.player[0].scoreboard.score < 200:
            for typ in self._storage:
                if len(self._storage[typ]) < 7:
                    rint = randint(0, 15)
                    if rint == 3:
                        if typ == "enemy":
                            self.addGame(Enemy(self.height, self.width))
                        elif typ == "platform":
                            self.addGame(Platform(self.height, self.width))
                        elif typ == "coin":
                            self.addGame(Coin(self.height, self.width))
                        elif typ == "lake":
                            self.addGame(Lake(self.height, self.width))
                        elif typ == "cloud":
                            self.addGame(Cloud(self.height, self.width))
                        elif typ == "brick":
                            self.addGame(Brick(self.height, self.width))
                    elif rint in range(3, 8):
                        if typ == "cloud":
                            self.addGame(Cloud(self.height, self.width))
                        elif typ == "brick":
                            self.addGame(Brick(self.height, self.width))

if __name__ == "__main__":
    b = Board(ROWS-4, COLUMNS-11)
    b.addBoard(Brick())
    b.render()
