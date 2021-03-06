#import chess
import random
from time import sleep
import chess


class RandomAI():
    def __init__(self):
        pass

    def choose_move(self, board: chess.Board):
        moves = list(board.legal_moves)
        move = random.choice(moves)
        print("Random AI recommending move " + str(move))
        return move


class FirstMoveAI():
    def __init__(self):
        pass

    def choose_move(self, board: chess.Board):
        moves = list(board.legal_moves)
        move = moves[0]
        print("FirstMove AI recommending move " + str(move))
        return move