from board import Board
from config import ROWS, COLUMNS, MARGINX, MARGINY, get_input, pos
from random import randint
from elements import Brick, Cloud
from people import Mario, Enemy
import os
import sys
from colorama import init, Fore, Back, Style
init(autoreset=True)


def main():
    os.system('tput reset')
    screen_height, screen_width = ROWS-2*MARGINY, COLUMNS-2*MARGINX
    board = Board(screen_height, screen_width)

    board.addGame(Enemy(screen_height, screen_width))
    board.addGame(Mario(screen_width, screen_height))

    for i in range(8):
        board.addGame(Brick(screen_height, screen_width, randint(4,
                      screen_width-5)))

    for i in range(5):
        board.addGame(Cloud(screen_height, screen_width, randint(4,
                      screen_width-6)))

    sys.stdout.write(Style.BRIGHT + Back.YELLOW + pos(2, 0) +
                     "SUPER MARIO".center(COLUMNS))

    board.render()

    game_on = True
    a = " "

    while game_on:
        board.player[0].scoreboard.showScore()
        board.player[0].move(a, board)
        board.updateEnemys()
        board.updateBullets()
        if a == 'q':
            sys.stdout.write(Back.RED + pos(ROWS-2, 0) +
                             "We got a quitter".center(COLUMNS))
            game_on = False
        a = get_input()
        board.addMore()
        board.player[0].scoreboard.scoreUpdate("time")

if __name__ == "__main__":
    main()
