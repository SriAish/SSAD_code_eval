import pytest
from people import Mario
from board import Board
from unittest import TestCase

class MarioTest(TestCase):
    """
    Class to test the Player class
    """
    def setUp(self):
        self.player=Mario(40,40)
        self.board = Board(40,40)
        self.board.add_game(self.player);
        self.player.is_exist=1

    def test_move_left(self):
        """
        Tests if position changes when function move_left called
        """
        prev_x_current=self.player.get_coord()[0]
        self.player.move_left(self.board)
        self.assertEqual(prev_x_current-1,self.player.get_coord()[0])

    def test_move_right(self):
        """
        Tests if position changes when function move_right called
        """
        prev_x_current=self.player.get_coord()[0]
        self.player.move_right(self.board)
        self.assertEqual(prev_x_current,self.player.get_coord()[0])

    def test_move_up(self):
        """
        Tests if position changes when function move_right called
        """
        prev_y_current=self.player.get_coord()[1]
        self.player.move_up(self.board)
        self.assertEqual(prev_y_current-1,self.player.get_coord()[1])

    def test_move_down(self):
        """
        Tests if position changes when function move_right called
        """
        prev_y_current=self.player.get_coord()[1]
        self.player.move_down(self.board)
        self.assertEqual(prev_y_current,self.player.get_coord()[1])

    def test_move(self):
        """
        Tests if position changes when function move called
        """
        prev_x_current=self.player.get_coord()[0]
        self.player.move('a', self.board)
        self.assertEqual(prev_x_current-1,self.player.get_coord()[0])

    def test_move1(self):
        """
        Tests if position changes when function move called
        """
        prev_x_current=self.player.get_coord()[0]
        self.player.move('d', self.board)
        self.assertEqual(prev_x_current,self.player.get_coord()[0])
