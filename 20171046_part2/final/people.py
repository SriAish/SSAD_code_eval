""" All Game Characters """

from random import randint
import sys
import numpy as np
from colorama import init, Fore, Style
from config import pos, ROWS, MARGINX, MARGINY
from elements import Bullet
from scoreboard import ScoreBoard
init(autoreset=True)


class Person():
    """Player and enemies inherit from this Class."""
    def __init__(self, y, x):
        self.structure = np.chararray((2, 2))
        self.structure[:, :] = " "
        self._y = y
        self._x = x
        self.fore = Fore.WHITE
        self._type = ""

    def get_size(self):
        """Returns size of matrix"""
        return len(self.structure), len(self.structure.T)

    def get_type(self):
        """Returns type of character"""
        return self._type

    def get_coord(self):
        """Returns coordinates of character"""
        return (self._x, self._y)

    def remove(self, board):
        """Removes character from board"""
        height, width = self.get_size()
        board.clear(self)
        for i in range(height):
            for j in range(width):
                sys.stdout.write(self.fore + pos(self._y+MARGINY+i,
                                                 self._x+MARGINX+j) + str(' '))
        sys.stdout.write(pos(ROWS-2, 0) + " ")

    def show(self, board):
        """Places/shows character on board with new position"""
        board.add_board(self)
        for i in range(self.get_size()[0]):
            for j in range(self.get_size()[1]):
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

    def move(self, move, board):
        """Decides where to move Mario according to key press"""
        if self._jump > 0:
            self.move_up(board)
        elif not self.move_down(board):
            self.on_ground = True

        if move == 'w' and self.on_ground:
            self._jump = 5
            self.on_ground = False
            self.move_up(board)
        elif move == 'a':
            self.move_left(board)
        elif move == 'd':
            self.move_right(board)
        elif move == 's' and board.on_board("bossenemy") > 0:
            board.add_game(Bullet(self._x, self._y))

    def move_left(self, board):
        """Moves Mario to left"""
        self.remove(board)
        if board.check_path(self, self._x-1, self._y):
            self._x = self._x-1
            self.show(board)
            return True
        self.show(board)
        return False

    def move_right(self, board):
        """Moves Mario to right"""
        self.remove(board)
        if board.check_path(self, self._x+1, self._y):
            if self._x < int(board.width/2):
                self._x = self._x + 1
                self.show(board)
            else:
                board.move_left()
        else:
            self.show(board)

    def move_up(self, board):
        """Makes Mario jump"""
        self.remove(board)
        if board.check_path(self, self._x, self._y-1):
            self._jump = self._jump - 1
            self._y = self._y - 1
            board.add_board(self)
            self.show(board)
        else:
            self._jump = 0
            board.add_board(self)
            self.show(board)

    def move_down(self, board):
        """Makes Mario come down faster"""
        self.remove(board)
        if board.check_path(self, self._x, self._y+1):
            self.remove(board)
            self._y = self._y + 1
            board.add_board(self)
            self.show(board)
            return True
        board.add_board(self)
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
        """Decides where to move Enemy"""
        if self.left:
            if not self.move_left(board):
                self.left = False
        elif not self.left:
            if not self.move_right(board):
                self.left = True

    def move_right(self, board):
        """Moves Enemy right"""
        self.remove(board)
        if board.check_path(self, self._x+1, self._y):
            self.remove(board)
            self._x = self._x+1
            self.show(board)
            return True
        if self.alive:
            self.show(board)
            return False
        return False

    def move_left(self, board):
        """Moves Enemy left"""
        self.remove(board)
        if self._x <= 3:
            board.clear_storage(self)
            return False
        if board.check_path(self, self._x-1, self._y):
            self._x = self._x-1
            self.show(board)
            return True
        if self.alive:
            self.show(board)
            return False
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
        self._x = width_s - self.get_size()[0] - 10
        self._y = height_s - self.get_size()[1]
        self.fore = Fore.CYAN
        self.life = 10
        self._type = "bossenemy"

    def move(self, board):
        """Boss enemy doesnt move"""
        pass

    def move_right(self, board):
        """Boss enemy doesnt move right"""
        pass

    def move_left(self, board):
        """Boss enemy doesnt move left"""
        pass
