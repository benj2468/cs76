# Benjamin Cape - 21F - CS76
# PA3
# 10.06.10

from multi_agent_ab import multi_agent_search
from psr_checkers import Board, Move
import random


class PSRMiniMaxGame:
    def __init__(self, depth_limit: int) -> None:
        self.calls = 0
        self.depth_limit = depth_limit

    def call(self, _state):
        self.calls += 1

    def actions(self, state: Board):
        return list(state.legal_moves())

    def result(self, state: Board, action: Move):
        state.push(action)
        return state

    def cut_off(self, state: Board, depth: int):
        return state.is_game_over() or depth >= self.depth_limit

    def utility(self, state: Board):
        outcome = state.outcome()
        if outcome:
            return 1 if outcome == state.turn else 0

        s = 0.0
        for c in state.piece_colors.values():
            if c == state.turn:
                s += (1.0 / len(state.pieces))
            elif c == state.turn.next():
                s -= (0.5 / len(state.pieces))

        return s

    def clean(self, state: Board):
        state.pop()


class PSRAIAgent():
    def __init__(self, depth: int):
        self.depth = depth

    def choose_move(self, board: Board):
        # Don't create a new board, use this one and use the push and pop features
        _val, move = multi_agent_search(PSRMiniMaxGame(self.depth), board,
                                        board.players)
        print("PSR AI recommending move " + str(move))
        return move


class RandomAgent():
    def choose_move(self, board: Board):
        moves = list(board.legal_moves())
        move = random.choice(moves)
        print("Random AI recommending move " + str(move))
        return move