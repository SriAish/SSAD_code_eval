"""Board Module"""

from random import randint
import sys
import os
from colorama import Back, Style
import numpy as np
from config import pos, ROWS, COLUMNS
from elements import Brick, Cloud, Coin, Lake, Platform
from people import Enemy, BossEnemy


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

    def add_board(self, element):
        """Add element to board"""
        height, width = element.get_size()
        x_coord, y_coord = element.get_coord()
        self._board[y_coord: y_coord + height,
                    x_coord: x_coord + width] = element.structure

    def clear(self, element):
        """Clear whole board"""
        height, width = element.get_size()
        x_coord, y_coord = element.get_coord()
        if element.get_type() == "lake":
            self._board[y_coord, x_coord:x_coord+width] = "-"
            self._board[y_coord+1, x_coord:x_coord+width] = " "
        else:
            self._board[y_coord: y_coord + height, x_coord: x_coord + width] = " "

    def clear_storage(self, element):
        """Clear element from storage"""
        if element.get_type() == "player":
            self.player.remove(element)
        else:
            self._storage[element.get_type()].remove(element)

    def add_storage(self, element):
        """Add element to storage"""
        if element.get_type() == "player":
            self.player.append(element)
        elif element not in self._storage[element.get_type()]:
            self._storage[element.get_type()].append(element)

    def on_board(self, char):
        """Check if something exists on board or not"""
        return len(self._storage[char])

    def board(self):
        """Initially showing the board"""
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
        for r_val in range(2, int(self.height / 2)):
            self._board[(r_val - 1) * 2: (r_val * 2), :] = emp_row
        # making land
        self._board[int(3*self.height/4), :] = land_row

    def render(self):
        """Displaying the board at every frame"""

        temp_board = np.matrix(self._board)
        for row in range(self.height):
            for col in range(self.width):
                sys.stdout.write(Style.BRIGHT + pos(row+3, col+6) +
                                 self._board[row, col])
        del temp_board

    def check_path(self, element, x_coord, y_coord):
        """Checking wether all elements can move and the result"""

        height, width = element.get_size()
        emp_mat = np.chararray((height, width), unicode=True)
        emp_mat[:, :] = " "

        # mario can land and kill Enemy otherwise get killed by enemy
        if element.get_type() == "player":
            for enem in self._storage["enemy"]:
                x_en, y_en = enem.get_coord()
                if (x_coord, y_coord + 1) == (x_en, y_en) or\
                   (x_coord+1, y_coord + 1) == (x_en, y_en) or\
                   (x_coord, y_coord + 1) == (x_en+1, y_en):
                    self._storage["enemy"].remove(enem)
                    enem.alive = False
                    enem.remove(self)
                    element.scoreboard.score_update("enemy")
                    sys.stdout.write(pos(ROWS-2, 0) +
                                     str(os.system('aplay mb_touch.wav&')))
                    return True

                if (x_coord+1, y_coord) == (x_en, y_en) or\
                   (x_coord+1, y_coord+1) == (x_en, y_en) or\
                   (x_coord, y_coord) == (x_en+1, y_en) or\
                   (x_coord, y_coord+1) == (x_en+1, y_en):
                    enem.alive = False
                    element.scoreboard.life_update()
                    self._storage["enemy"].remove(enem)
                    enem.remove(self)
                    sys.stdout.write(pos(ROWS-2, 0) +
                                     str(os.system('aplay mb_die.wav&')))
                    return True

            for coi in self._storage["coin"]:
                x_en, y_en = coi.get_coord()
                if (x_coord, y_coord) == (x_en, y_en+1) or\
                   (x_coord+1, y_coord+1) == (x_en, y_en) or\
                   (x_coord, y_coord) == (x_en+1, y_en+1) or\
                   (x_coord, y_coord) == (x_en+1, y_en) or\
                   (x_coord+1, y_coord) == (x_en, y_en+1) or\
                   (x_coord+1, y_coord) == (x_en, y_en) or\
                   (x_coord, y_coord+1) == (x_en+1, y_en) or\
                   (x_coord, y_coord+1) == (x_en, y_en):
                    self._storage["coin"].remove(coi)
                    coi.remove(self)
                    return True

            for lak in self._storage["lake"]:
                x_en, y_en = lak.get_coord()
                if (x_coord, y_coord+1) == (x_en, y_en) or\
                   (x_coord+1, y_coord+1) == (x_en, y_en) or\
                   (x_coord, y_coord+1) == (x_en+1, y_en) or\
                   (x_coord, y_coord+1) == (x_en+2, y_en):
                    element.scoreboard.life_update()
                    self._storage["lake"].remove(lak)
                    lak.remove(self)
                    sys.stdout.write(pos(ROWS-2, 0) +
                                     str(os.system('aplay mb_die.wav&')))
                    return False

        elif element.get_type() == "enemy":
            if self.player:
                x_en, y_en = self.player[0].get_coord()
                if (x_en+1, y_en) == (x_coord, y_coord) or\
                   (x_en+1, y_en+1) == (x_coord, y_coord) or\
                   (x_en, y_en) == (x_coord+1, y_coord) or\
                   (x_en, y_en+1) == (x_coord+1, y_coord):
                    element.alive = False
                    element.remove(self)
                    self._storage["enemy"].remove(element)
                    self.player[0].scoreboard.life_update()
                    sys.stdout.write(pos(ROWS-2, 0) + " ")
                    os.system('aplay mb_die.wav&')
                    return False

        elif element.get_type() == "brick":
            for enem in self._storage["enemy"]:
                x_en, y_en = enem.get_coord()
                if (x_coord+1, y_coord) == (x_en, y_en) or\
                   (x_coord+1, y_coord+1) == (x_en, y_en) or\
                   (x_coord, y_coord) == (x_en+1, y_en) or\
                   (x_coord, y_coord+1) == (x_en+1, y_en):
                    enem.move_left(self)
                    return True

        elif element.get_type() == "bullet":
            if np.all(self._board[y_coord:y_coord+1, x_coord:x_coord+1] != emp_mat):
                ben = self._storage["bossenemy"][0]
                ben.life = ben.life - 1
                element.remove(self)
                self._storage["bullet"].remove(element)
                if ben.life <= 0:
                    ben.alive = False
                    self.player[0].scoreboard.score_update("bossenemy")
                    self.player[0].scoreboard.show_score("Final Score:: ")
                    self._storage["bossenemy"].remove(ben)
                    ben.remove(self)
                    msg = "You Won!! and still it doesn't matter:-p"
                    sys.stdout.write(Back.RED + pos(ROWS-2, 0) +
                                     msg.center(COLUMNS))
                    exit()
                return False

        if np.all(self._board[y_coord: y_coord + height, x_coord:x_coord + width] == emp_mat):
            return True
        return False

    def move_left(self):
        """Move everything left"""
        self.player[0].remove(self)
        emp_col = np.chararray((self.height, 1), unicode=True)
        emp_col[:, :] = " "
        emp_col[:2, :] = emp_col[-2:, :] = "$"
        emp_col[int(3*self.height/4), :] = "-"
        for typs in self._storage:
            for ele in self._storage[typs]:
                ele.move_left(self)
        self.player[0].show(self)

    def add_game(self, element):
        """Add elements to game"""
        emp_mat = np.chararray(element.get_size(), unicode=True)
        emp_mat[:, :] = " "
        x_coord, y_coord = element.get_coord()
        height, width = element.get_size()
        if element.get_type() == "bossenemy":
            self.add_board(element)
            self.add_storage(element)
            return True

        if np.all(self._board[y_coord: y_coord + height, x_coord: x_coord + width] == emp_mat):
            self.add_board(element)
            self.add_storage(element)
            return True

        if element.get_type() == "lake":
            self.add_board(element)
            self.add_storage(element)
            return True

        if element.get_type() == "bullet":
            element.show(self)
        return False

    def update_enemys(self):
        """Update enemy"""
        for enem in self._storage["enemy"]:
            enem.move(self)

    def update_bullets(self):
        """Update bullets"""
        for bull in self._storage["bullet"]:
            bull.move_right(self)

    def add_more(self):
        """Add more elements"""
        if self.player[0].scoreboard.score > 200 and \
           len(self._storage["bossenemy"]) < 1:
            for typ in self._storage:
                for ele in self._storage[typ]:
                    ele.remove(self)
                    self._storage[typ].remove(ele)
            self.add_game(BossEnemy(self.height, self.width))
            for i in self._storage["bossenemy"]:
                i.show(self)
        elif self.player[0].scoreboard.score < 200:
            for typ in self._storage:
                if len(self._storage[typ]) < 7:
                    rint = randint(0, 15)
                    if rint == 3:
                        if typ == "enemy":
                            self.add_game(Enemy(self.height, self.width))
                        elif typ == "platform":
                            self.add_game(Platform(self.height, self.width))
                        elif typ == "coin":
                            self.add_game(Coin(self.height, self.width))
                        elif typ == "lake":
                            self.add_game(Lake(self.height, self.width))
                        elif typ == "cloud":
                            self.add_game(Cloud(self.height, self.width))
                        elif typ == "brick":
                            self.add_game(Brick(self.height, self.width))
                    elif rint in range(3, 8):
                        if typ == "cloud":
                            self.add_game(Cloud(self.height, self.width))
                        elif typ == "brick":
                            self.add_game(Brick(self.height, self.width))

if __name__ == "__main__":
    BOARD = Board(ROWS-4, COLUMNS-11)
    BOARD.render()
