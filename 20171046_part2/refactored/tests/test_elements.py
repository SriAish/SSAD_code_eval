import pytest
from elements import Cloud
from board import Board
from unittest import TestCase

class CloudTest(TestCase):
    """
    Class to test the Player class
    """
    def setUp(self):
        self.element = Cloud(40,40)
        self.board = Board(40,40)
        self.board.add_game(self.element);
        self.element.is_exist=1

    def test_move_left(self):
        """
        Tests if position changes when function move_left called
        """
        prev_x_current=self.element.get_coord()[0]
        self.element.move_left(self.board)
        self.assertEqual(prev_x_current-1,self.element.get_coord()[0])
