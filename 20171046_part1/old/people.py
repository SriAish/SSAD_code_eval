from config import pos, COLUMNS, ROWS, get_input, MARGINX, MARGINY
from random import randint
import numpy as np
import sys
import os
from elements import Bullet
from scoreboard import ScoreBoard
from colorama import init, Back, Fore, Style
init(autoreset=True)


class Person():
    """Player and enemies inherit from this Class."""
    def __init__(self, y, x):
        self.structure = np.chararray((2, 2))
        self.structure[:, :] = " "
        self._y = y
        self._x = x
        self.fore = Fore.WHITE

    def getSize(self):
        return self.structure.shape

    def getType(self):
        return self._type

    def getCoord(self):
        return (self._x, self._y)

    def remove(self, board):
        height, width = self.getSize()
        board.clear(self)
        for i in range(height):
            for j in range(width):
                sys.stdout.write(self.fore + pos(self._y+MARGINY+i,
                                 self._x+MARGINX+j) + str(' '))
        sys.stdout.write(pos(ROWS-2, 0) + " ")

    def show(self, board):
        board.addBoard(self)
        for i in range(self.getSize()[0]):
            for j in range(self.getSize()[1]):
                sys.stdout.write(self.fore + Style.BRIGHT +
                                 pos(self._y+MARGINY+i, self._x+MARGINX+j) +
                                 self.structure[i, j])
        sys.stdout.write(pos(ROWS-2, 0) + " ")


class Mario(Person):
    """Mario Class."""
    def __init__(self, width_s, height_s):
        super(Mario, self).__init__(int(3*height_s/4)-2, int(width_s/2))
        self.structure = np.matrix([['o', 'o'],
                                    [']', '[']])
        self._jump = 0
        self.on_ground = True
        self._type = "player"
        self.scoreboard = ScoreBoard()

    def atCenter(self):
        if self._x < int(board.width/2):
            return False
        return True

    def move(self, move, board):
        if self._jump > 0:
            self.moveUp(board)
        elif not self.moveDown(board):
                self.on_ground = True

        if move == 'w' and self.on_ground:
            self._jump = 5
            self.on_ground = False
            self.moveUp(board)
        elif move == 'a':
            self.moveLeft(board)
        elif move == 'd':
            self.moveRight(board)
        elif move == 's' and board.onBoard("bossenemy") > 0:
            board.addGame(Bullet(self._x, self._y))

    def moveLeft(self, board):
        self.remove(board)
        if board.checkPath(self, self._x-1, self._y):
            self._x = self._x-1
            self.show(board)
            return True
        self.show(board)
        return False

    def moveRight(self, board):
        self.remove(board)
        if board.checkPath(self, self._x+1, self._y):
            if self._x < int(board.width/2):
                self._x = self._x + 1
                self.show(board)
            else:
                board.moveLeft()
        else:
            self.show(board)

    def moveUp(self, board):
        self.remove(board)
        if board.checkPath(self, self._x, self._y-1):
            self._jump = self._jump - 1
            self._y = self._y - 1
            board.addBoard(self)
            self.show(board)
        else:
            self._jump = 0
            board.addBoard(self)
            self.show(board)

    def moveDown(self, board):
        self.remove(board)
        if board.checkPath(self, self._x, self._y+1):
            self.remove(board)
            self._y = self._y + 1
            board.addBoard(self)
            self.show(board)
            return True
        board.addBoard(self)
        self.show(board)
        return False


class Enemy(Person):
    """Enemy Class."""
    def __init__(self, height_s, width_s):
        super(Enemy, self).__init__(int(3*height_s/4)-2, randint(0, width_s-3))
        self.structure = np.matrix([['^', '^'],
                                    ['e', 'e']])
        self._jump = 0
        self.left = True
        self._type = "enemy"
        self.fore = Fore.RED
        self.alive = True

    def move(self, board):
        if self.left:
            if not self.moveLeft(board):
                self.left = False
        elif not self.left:
            if not self.moveRight(board):
                self.left = True

    def moveRight(self, board):
        self.remove(board)
        if board.checkPath(self, self._x+1, self._y):
            self.remove(board)
            self._x = self._x+1
            self.show(board)
            return True
        elif self.alive:
            self.show(board)
            return False

    def moveLeft(self, board):
        self.remove(board)
        if self._x <= 3:
            board.clearStorage(self)
            return False
        elif board.checkPath(self, self._x-1, self._y):
            self._x = self._x-1
            self.show(board)
            return True
        elif self.alive:
            self.show(board)
            return False


class BossEnemy(Enemy):
    """BossEnemy class"""
    def __init__(self, height_s, width_s):
        super(BossEnemy, self).__init__(height_s, width_s)
        self.structure = np.matrix([['\\', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                                    ' ', ' ', ' ', ' ', '/', ' '],
                                    [' ', ')', '\\', ' ', ' ', ' ', ' ',
                                    ' ', ' ', ' ', ' ', '/', '(', ' '],
                                    ['_', '_', '_', '\\', ' ', ' ', ',',
                                    ',', ' ', ' ', '/', '_', '_', '_'],
                                    [' ', ')', ' ', '/', '\\', ' ', '/',
                                    '\\', ' ', '/', '\\', ' ', '(', ' '],
                                    [' ', ')', ' ', '/', '\\', ' ', '/',
                                    '\\', ' ', '/', '\\', ' ', '(', ' '],
                                    [' ', ' ', ' ', ' ', ' ', '\\', ' ',
                                    ' ', '/', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', 'w', ',',
                                    ',', 'w', ' ', ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', '`', '8', '|',
                                    '|', '8', "'", ' ', ' ', ' ', ' '],
                                    [' ', ' ', ' ', ' ', ' ', ' ', '{',
                                    '(', ' ', ' ', ' ', ' ', ' ', ' ']])
        self._x = width_s - self.getSize()[0] - 10
        self._y = height_s - self.getSize()[1]
        self.fore = Fore.CYAN
        self.life = 10
        self._type = "bossenemy"

    def move(self):
        pass
