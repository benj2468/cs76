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


def test_game(player1, player2):
    game = ChessGame(player1, player2)
    while not game.is_game_over():
        game.make_move()
        # You can toggle this if you actually want to see the game
        print(game)
        # sleep(0.1)

    print(game.board.outcome())


# Each of these were tests that I ran

print("ITERATIVE DEEPENING")
test_game(RandomAI(), IterativeDeepeningAI())

print("MINIMAX")
test_game(RandomAI(), MinimaxAI(2))

print("AB Pruner")
test_game(RandomAI(), AlphaBetaAI(4, "Bob"))

print("AB 2 vs. AB 4")
test_game(AlphaBetaAI(2, "Alice"), AlphaBetaAI(4, "Bob"))

print("AB vs. Iterative Deepening")
test_game(AlphaBetaAI(4, "Alice"), IterativeDeepeningAI())
