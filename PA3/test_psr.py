# Benjamin Cape - 21F - CS76
# PA3
# 10.06.10

from psr_checkers import PSRAgent
from PSRGame import PSRGame
from time import sleep

red = PSRAgent(1)
yellow = PSRAgent(1)
blue = PSRAgent(3)

game = PSRGame(red, yellow, blue)

while not game.is_game_over():
    print(game)
    game.make_move()
    sleep(0.2)
