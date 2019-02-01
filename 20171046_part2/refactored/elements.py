""" All Game Elements """

from random import randint
import sys
from colorama import init, Fore, Style
import numpy as np
from config import pos, MARGINX, MARGINY, ROWS
init(autoreset=True)


class Element():
    """Common Element Class."""
    def __init__(self, y, x):
        self._y = y
        self._x = x
        self.fore = Fore.WHITE
        self.structure = np.matrix([])
        self._type = ""

    def get_size(self):
        """Returns size of matrix"""
        return len(self.structure), len(self.structure.T)

    def move_left(self, board):
        """Moves the element to the left"""
        self.remove(board)
        if self._x <= 3:
            board.clear_storage(self)
        else:
            board.check_path(self, self._x-1, self._y)
            self._x = self._x-1
            self.show(board)

    def get_type(self):
        """Returns type of element"""
        return self._type

    def get_coord(self):
        """Returns coordinates of element"""
        return (self._x, self._y)

    def remove(self, board):
        """Removes element from board"""
        height, width = self.get_size()
        board.clear(self)
        for i in range(height):
            for j in range(width):
                sys.stdout.write(self.fore + pos(self._y+MARGINY+i,
                                                 self._x+MARGINX+j) + str(' '))
        sys.stdout.write(pos(ROWS-2, 0) + " ")

    def show(self, board):
        """Places/shows updated element on board"""
        board.add_board(self)
        for i in range(self.get_size()[0]):
            for j in range(self.get_size()[1]):
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
        """Removes lake from board"""
        height, width = self.get_size()
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

    def move_right(self, board):
        """Moves the element to the right"""
        self.remove(board)
        if self._x >= board.width-4:
            board.clear_storage(self)
        else:
            board.check_path(self, self._x+1, self._y)
            self._x = self._x+2
            self.show(board)
