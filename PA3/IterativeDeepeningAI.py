# Benjamin Cape - 21F - CS76
# PA3
# 10.06.10

import chess
from AlphaBetaAI import ABPruning
from datetime import datetime

from MinimaxAI import ChessMiniMaxGame


class IterativeDeepeningAI():
    def __init__(self, max_delay_ms: int = 400) -> None:
        self.delay = max_delay_ms

    def choose_move(self, board: chess.Board):
        depth = 1
        best_move = (float('-inf'), None)
        time = 0
        while time < self.delay:
            start = datetime.now()
            game = ChessMiniMaxGame(depth, board.turn)
            val, res = ABPruning().ab_minimax_search(game, board)
            time += (datetime.now() - start).microseconds // 1000
            print(
                f"Iterative Deepening time={time} AI Depth = {depth} discovered best move: {val}, visited = {game.calls}"
            )
            if val > best_move[0]:
                best_move = (val, res)
            if val == 1:
                break
            depth += 1

        return best_move[1]