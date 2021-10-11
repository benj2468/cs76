# Benjamin Cape - 21F - CS76
# PA3
# 10.06.10

from datetime import datetime
from random import shuffle
import chess


def minimax_search(game, state):
    game.call(state)
    value, move = max_value(game, state, depth=0)
    return (value, move)


def max_value(game, state, depth=0):
    game.call(state)
    if game.cut_off(state, depth):
        return game.utility(state), None

    v = None
    move = None
    for action in game.actions(state):
        v2, _a2 = min_value(game, game.result(state, action), depth + 1)
        if not v or v2 > v:
            v, move = v2, action
        game.clean(state)
    return v, move


def min_value(game, state, depth):
    game.call(state)
    if game.cut_off(state, depth):
        return game.utility(state), None

    v = None
    move = None
    for action in game.actions(state):
        v2, _a2 = max_value(game, game.result(state, action), depth + 1)
        if not v or v2 < v:
            v, move = v2, action
        game.clean(state)
    return v, move


class ChessMiniMaxGame:
    def __init__(self,
                 depth_limit: int,
                 top_color: chess.Color,
                 reordering=False) -> None:
        self.calls = 0
        self.top_color = top_color
        self.depth_limit = depth_limit
        self.reordering = reordering

    def call(self, _state):
        self.calls += 1

    def actions(self, state: chess.Board):
        def check_utility(action):
            state.push(action)
            util = self.utility(state)
            state.pop()
            return util

        if self.reordering:
            actions = sorted(
                state.legal_moves,
                key=check_utility,
            )

            actions.sort(key=check_utility,
                         reverse=self.top_color == state.turn)
            return actions
        else:
            return state.legal_moves

    def result(self, state: chess.Board, action: chess.Move):
        state.push(action)
        return state

    def cut_off(self, state: chess.Board, depth: int):
        return state.is_game_over() or depth > self.depth_limit

    def utility(self, state: chess.Board):
        outcome = state.outcome()
        if outcome:
            # For terminal states
            return 1 if outcome.winner == self.top_color else -1

        ## Calculate utility for non-terminal states
        MAX_SCORE = 8 * 1 + 2 * 11 + 9
        scores = {
            chess.PAWN: 1,
            chess.ROOK: 5,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.QUEEN: 9,
        }

        s = 0.0
        for piece_type, weight in scores.items():
            s += weight * len(state.pieces(piece_type, self.top_color))
            s -= weight * len(state.pieces(piece_type, not self.top_color))

        return s / MAX_SCORE

    def clean(self, state: chess.Board):
        state.pop()


class MinimaxAI():
    def __init__(self, depth: int):
        self.depth = depth

    def choose_move(self, board: chess.Board):
        # Don't create a new board, use this one and use the push and pop features
        start = datetime.now()
        game = ChessMiniMaxGame(self.depth, board.turn)
        val, res = minimax_search(game, board)
        dur = datetime.now() - start

        print(
            f"Minimax visited {game.calls} nodes, with depth: {game.depth_limit}, in {dur.microseconds / 1000 }ms, best move value: {val}"
        )
        return res
