import chess
from AlphaBetaAI import ab_minimax_search
from datetime import datetime

from MinimaxAI import ChessMiniMaxGame


class IterativeDeepeningAI():
    def __init__(self, max_delay_ms: int = 500) -> None:
        self.delay = max_delay_ms

        pass

    def choose_move(self, board: chess.Board):
        depth = 1
        best_move = (float('inf'), None)
        time = 0
        while time < self.delay:
            start = datetime.now()
            val, res = ab_minimax_search(ChessMiniMaxGame(depth), board)
            time = (datetime.now() - start).microseconds // 1000
            if val > best_move[0]:
                best_move = (val, res)
            depth += 1
        return res