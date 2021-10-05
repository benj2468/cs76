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
    def __init__(self, depth_limit: int) -> None:
        self.calls = 0
        self.depth_limit = depth_limit

    def call(self, _state):
        self.calls += 1

    def actions(self, state: chess.Board):
        return list(state.legal_moves)

    def result(self, state: chess.Board, action: chess.Move):
        state.push(action)
        return state

    def cut_off(self, state: chess.Board, depth: int):
        return state.is_game_over() or depth >= self.depth_limit

    def utility(self, state: chess.Board):
        outcome = state.outcome()
        if outcome:
            return 1 if outcome.winner else 0

        ## Calculate utility for non-terminal states
        ## This evaluation function needs to be described in my document
        MAX_SCORE = 16 * 21
        scores = {
            chess.PAWN: 1,
            chess.ROOK: 5,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.QUEEN: 9,
        }

        s = 0.0
        for piece_type, weight in scores.items():
            s += (weight / MAX_SCORE) * len(
                state.pieces(piece_type, state.turn))

        return s

    def clean(self, state: chess.Board):
        state.pop()


class MinimaxAI():
    def __init__(self, depth: int):
        self.depth = depth

    def choose_move(self, board: chess.Board):
        # Don't create a new board, use this one and use the push and pop features
        _val, res = minimax_search(ChessMiniMaxGame(self.depth), board)
        return res
