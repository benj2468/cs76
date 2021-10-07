# Benjamin Cape - 21F - CS76
# PA3
# 10.06.10

from psr_ai import PSRAIAgent
from psr_game import PSRGame
from time import sleep

red = PSRAIAgent(1)
yellow = PSRAIAgent(1)
blue = PSRAIAgent(3)

game = PSRGame(red, yellow, blue)

while not game.is_game_over():
    print(game)
    game.make_move()
    sleep(0.2)
