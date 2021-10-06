from psr_checkers import PSRMiniMax
from PSRGame import PSRGame

red = PSRMiniMax(2)
yellow = PSRMiniMax(2)
blue = PSRMiniMax(4)

game = PSRGame(red, yellow, blue)

while not game.is_game_over():
    print(game)
    game.make_move()

#print(hash(str(game.board)))
