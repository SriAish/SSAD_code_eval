import pytest
from people import Enemy
from board import Board
from unittest import TestCase

class EnemyTest(TestCase):
    """
    Class to test the Player class
    """
    def setUp(self):
        self.player=Enemy(30,30)
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
        self.assertEqual(prev_x_current+1,self.player.get_coord()[0])

    def test_move(self):
        """
        Tests if position changes when function move called
        """
        prev_x_current=self.player.get_coord()[0]
        self.player.move(self.board)
        self.assertEqual(prev_x_current-1,self.player.get_coord()[0])
