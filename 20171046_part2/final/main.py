""" Game Engine Module """

from random import randint
import os
import sys
from colorama import init, Back, Style
from board import Board
from config import ROWS, COLUMNS, MARGINX, MARGINY, get_input, pos
from elements import Brick, Cloud
from people import Mario, Enemy
init(autoreset=True)


def main():
    """ Game Engine """
    os.system('tput reset')
    screen_height, screen_width = ROWS-2*MARGINY, COLUMNS-2*MARGINX
    board = Board(screen_height, screen_width)

    board.add_game(Enemy(screen_height, screen_width))
    board.add_game(Mario(screen_width, screen_height))

    i = 8

    while i:
        board.add_game(Brick(screen_height, screen_width, randint(4,
                                                                  screen_width-5)))
        i = i - 1

    i = 5

    while i:
        board.add_game(Cloud(screen_height, screen_width, randint(4,
                                                                  screen_width-6)))
        i = i - 1

    sys.stdout.write(Style.BRIGHT + Back.YELLOW + pos(2, 0) +
                     "SUPER MARIO".center(COLUMNS))

    board.render()

    game_on = True
    char = " "

    while game_on:
        board.player[0].scoreboard.show_score()
        board.player[0].move(char, board)
        board.update_enemys()
        board.update_bullets()
        if char == 'q':
            sys.stdout.write(Back.RED + pos(ROWS-2, 0) +
                             "We got a quitter".center(COLUMNS))
            game_on = False
        char = get_input()
        board.add_more()
        board.player[0].scoreboard.score_update("time")

if __name__ == "__main__":
    main()
