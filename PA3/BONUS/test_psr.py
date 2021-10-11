# Benjamin Cape - 21F - CS76
# PA3
# 10.06.10

from psr_ai import PSRAIAgent, RandomAgent
from psr_game import PSRGame
from time import sleep

red = RandomAgent()
yellow = PSRAIAgent(3)
blue = PSRAIAgent(2)

# The aim of this game is to eliminate one other player.
# Blue has to eliminate red,
# red has to eliminate yellow
# yellow has to eliminate blue.

game = PSRGame(red, yellow, blue)

while not game.is_game_over():
    print(game)
    game.make_move()
    sleep(0.2)
