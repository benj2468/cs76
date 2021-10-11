# Benjamin Cape - 21F - CS76
# PA3
# 10.06.10

import chess
from IterativeDeepeningAI import IterativeDeepeningAI
from RandomAI import RandomAI, FirstMoveAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame
from time import sleep

# player1 = HumanPlayer()
# player2 = RandomAI()

player1 = RandomAI()
# player1 = FirstMoveAI()
player2 = AlphaBetaAI(3, "Alice")

# player1 = MinimaxAI(4)
# player2 = MinimaxAI(3)

game = ChessGame(player2, player1)
while not game.is_game_over():
    game.make_move()
    print(game)
    # sleep(0.1)

print(player2.pruner.total_visited)
print(game.board.outcome())