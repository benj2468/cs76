# Benjamin Cape - 21F - CS76
# PA3
# 10.06.10

from datetime import datetime
import chess
from MinimaxAI import ChessMiniMaxGame
from MinimaxAI import minimax_search


class ABPruning:
    def __init__(self) -> None:
        self.table = {}
        self.total_visited = 0

    def hash(self, state):
        return str(str(state) + "\n" + str(state.turn)).__hash__()

    def ab_minimax_search(self, game, state):
        value, move = self.ab_max_value(game, state)
        self.total_visited += game.calls
        return (value, move)

    def ab_max_value(self,
                     game,
                     state,
                     depth=0,
                     alpha=float('-inf'),
                     beta=float('inf')):

        if game.cut_off(state, depth):
            return game.utility(state), None

        if self.hash(state) in self.table:
            return self.table[self.hash(state)]
        game.call(state)

        v = None
        move = None
        for action in game.actions(state):
            v2, a2 = self.ab_min_value(game, game.result(state, action),
                                       depth + 1, alpha, beta)
            if not v or v2 > v:
                v, move = v2, action
            if v >= beta:
                game.clean(state)
                return v, action
            alpha = max(alpha, v)
            game.clean(state)
        self.table[self.hash(state)] = (v, move)
        return v, move

    def ab_min_value(self,
                     game,
                     state,
                     depth=0,
                     alpha=float('-inf'),
                     beta=float('inf')):

        if game.cut_off(state, depth):
            return game.utility(state), None
        if self.hash(state) in self.table:
            return self.table[self.hash(state)]

        game.call(state)

        v = None
        move = None
        for action in game.actions(state):
            v2, a2 = self.ab_max_value(game, game.result(state, action),
                                       depth + 1, alpha, beta)
            if not v or v2 < v:
                v, move = v2, action
            if v <= alpha:
                game.clean(state)
                return v, action
            beta = min(beta, v)
            game.clean(state)
        self.table[self.hash(state)] = (v, move)
        return v, move


class AlphaBetaAI():
    def __init__(self, depth: int, name: str):
        self.depth = depth
        self.name = name
        self.pruner = ABPruning()
        pass

    def choose_move(self, board: chess.Board):
        game = ChessMiniMaxGame(self.depth, board.turn)
        start = datetime.now()
        val, res = self.pruner.ab_minimax_search(game, board)
        dur = datetime.now() - start
        print(
            f"{self.name}: A/B Pruning Visited: {game.calls} nodes, with depth: {game.depth_limit}, in {dur.microseconds / 1000}ms, best move value: {val}"
        )
        return res