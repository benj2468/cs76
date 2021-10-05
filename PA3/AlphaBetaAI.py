import chess
from MinimaxAI import ChessMiniMaxGame
from MinimaxAI import minimax_search


def ab_minimax_search(game, state):
    value, move = ab_max_value(game, state)
    return (value, move)


def ab_max_value(game, state, depth=0, alpha=float('-inf'), beta=float('inf')):
    game.call(state)
    if game.cut_off(state, depth):
        return game.utility(state), None

    v = None
    move = None
    for action in game.actions(state):
        v2, a2 = ab_min_value(game, game.result(state, action), depth + 1,
                              alpha, beta)
        if not v or v2 > v:
            v, move = v2, action
        if v >= beta:
            game.clean(state)
            return v, action
        alpha = max(alpha, v)
        game.clean(state)
    return v, move


def ab_min_value(game, state, depth=0, alpha=float('-inf'), beta=float('inf')):
    game.call(state)
    if game.cut_off(state, depth):
        return game.utility(state), None

    v = None
    move = None
    for action in game.actions(state):
        v2, a2 = ab_max_value(game, game.result(state, action), depth + 1,
                              alpha, beta)
        if not v or v2 < v:
            v, move = v2, action
        if v <= alpha:
            game.clean(state)
            return v, action
        beta = min(beta, v)
        game.clean(state)
    return v, move


class AlphaBetaAI():
    def __init__(self, depth: int):
        self.depth = depth
        pass

    def choose_move(self, board: chess.Board):
        _val, res = ab_minimax_search(ChessMiniMaxGame(self.depth), board)
        return res