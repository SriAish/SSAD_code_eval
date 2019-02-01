import pytest
from board import Board
from people import Mario
from elements import Cloud
from unittest import TestCase

class ScoreBoardTest(TestCase):
    """
    Class to test the Score Board class
    """
    def setUp(self):
        self.board = Board(40, 40)
        self.board.is_exist=1

    def test_add_board(self):
        """
        Add element to board
        """
        self.board.add_game(Mario(40, 40))
        self.assertEqual(len(self.board.player), 1)

    def test_add_board1(self):
        """
        Add element to board
        """
        self.board.add_game(Cloud(40, 40))
        self.assertEqual(self.board.on_board("cloud"), 1)
