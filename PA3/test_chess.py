# pip3 install python-chess

import chess
from IterativeDeepeningAI import IterativeDeepeningAI
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame

player1 = HumanPlayer()
player2 = RandomAI()
player3 = MinimaxAI(3)
player4 = AlphaBetaAI(5)
player5 = IterativeDeepeningAI()

game = ChessGame(player5, player5)

while not game.is_game_over():
    print(game)
    game.make_move()

#print(hash(str(game.board)))
