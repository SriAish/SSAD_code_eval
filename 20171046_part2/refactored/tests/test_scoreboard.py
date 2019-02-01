import pytest
from scoreboard import ScoreBoard
from unittest import TestCase

class ScoreBoardTest(TestCase):
    """
    Class to test the Score Board class
    """
    def setUp(self):
        self.sboard = ScoreBoard()
        self.sboard.is_exist=1

    def test_score_update(self):
        """
        Tests score update
        """
        prev_score = self.sboard.score
        self.sboard.score_update("enemy")
        self.assertEqual(prev_score + 10, self.sboard.score)

    def test_score_update1(self):
        """
        Tests score update
        """
        prev_score = self.sboard.score
        self.sboard.score_update("coin")
        self.assertEqual(prev_score + 5, self.sboard.score)

    def test_score_update2(self):
        """
        Tests score update
        """
        prev_score = self.sboard.score
        self.sboard.score_update("time")
        self.assertEqual(prev_score + 1, self.sboard.score)

    def test_score_update3(self):
        """
        Tests score update
        """
        prev_score = self.sboard.score
        self.sboard.score_update("bossenemy")
        self.assertEqual(prev_score + 100, self.sboard.score)

    def test_life_update(self):
        """
        Tests life update
        """
        prev_life = self.sboard.life
        self.sboard.life_update()
        self.assertEqual(prev_life - 1, self.sboard.life)
