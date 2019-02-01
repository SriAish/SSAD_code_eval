from config import pos, get_input, MARGINX, MARGINY, ROWS
from random import randint
import numpy as np
import sys
from colorama import Back
from colorama import init, Back, Fore, Style
init(autoreset=True)


class Element():
    """Common Element Class."""
    def __init__(self, y, x):
        self._y = y
        self._x = x
        self.fore = Fore.WHITE

    def getSize(self):
        return self.structure.shape

    def update(self):
        self.remove()
        if self._x <= 2:
            return True
        else:
            self._x = self._x-1
            return False

    def moveLeft(self, board):
        self.remove(board)
        if self._x <= 3:
            board.clearStorage(self)
        else:
            board.checkPath(self, self._x-1, self._y)
            self._x = self._x-1
            self.show(board)

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
        height, width = self.getSize()
        board.addBoard(self)
        for i in range(self.getSize()[0]):
            for j in range(self.getSize()[1]):
                sys.stdout.write(self.fore + Style.BRIGHT +
                                 pos(self._y+MARGINY+i, self._x+MARGINX+j) +
                                 self.structure[i, j])
        sys.stdout.write(pos(ROWS-2, 0) + " ")


class Cloud(Element):
    """Cloud Class."""
    def __init__(self, height_s, width_s, x=None):
        if x is None:
            x = width_s - 5

        super(Cloud, self).__init__(randint(2, int(height_s/4)-2), x)
        self.structure = np.matrix([[' ', '@', ' '],
                                    ['@', '@', '@'],
                                    [' ', '@', ' ']])
        self._type = "cloud"
        self.fore = Fore.BLUE


class Brick(Element):
    """Brick Class."""
    def __init__(self, height_s, width_s, x=None):
        if x is None:
            x = width_s - 4

        super(Brick, self).__init__(int(3*height_s/4)-2, x)
        self.structure = np.matrix([['#', '#'],
                                    ['#', '#']])
        self._type = "brick"
        self.fore = Fore.GREEN


class Coin(Element):
    """Coin Class."""
    def __init__(self, height_s, width_s, x=None):

        if x is None:
            x = width_s - 4

        super(Coin, self).__init__(randint(int(height_s/4),
                                   int(2*height_s/3)), x)
        self.structure = np.matrix([['0', '0'],
                                    ['0', '0']])
        self._type = "coin"
        self.fore = Fore.YELLOW


class Lake(Element):
    """Lake Class."""
    def __init__(self, height_s, width_s):
        super(Lake, self).__init__(int(3*height_s/4), width_s - 5)
        self.structure = np.matrix([['~', '~', '~'],
                                    [' ', '~', ' ']])
        self.fore = Fore.BLUE
        self._type = "lake"

    def remove(self, board):
        height, width = self.getSize()
        board.clear(self)
        for i in range(height):
            for j in range(width):
                if i == 0:
                    sys.stdout.write(Style.BRIGHT + pos(self._y+MARGINY+i,
                                                        self._x+MARGINX+j) +
                                     str('-'))
                else:
                    sys.stdout.write(pos(self._y+MARGINY+i,
                                         self._x+MARGINX+j) + str(' '))
        sys.stdout.write(pos(ROWS-2, 0) + " ")


class Platform(Element):
    """Platform Class."""
    def __init__(self, height_s, width_s):
        super(Platform, self).__init__(randint(int(height_s/4)+2,
                                               int(3*height_s/4)-4),
                                       width_s - 6)
        self.structure = np.matrix([['^', '^', '^', '^'],
                                    ['^', '^', '^', '^']])
        self._type = "platform"
        self.fore = Fore.GREEN


class Bullet(Element):
    """Bullet Class."""
    def __init__(self, x, y):
        super(Bullet, self).__init__(y, x+2)
        self.structure = np.matrix([['=']])
        self.fore = Fore.CYAN
        self._type = "bullet"

    def moveRight(self, board):
        self.remove(board)
        if self._x >= board.width-4:
            board.clearStorage(self)
        else:
            board.checkPath(self, self._x+1, self._y)
            self._x = self._x+2
            self.show(board)
