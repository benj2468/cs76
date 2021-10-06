# Benjamin Cape - 21F - CS76
# PA3
# 10.06.10

from enum import Enum
from re import sub
from typing import List, Optional, Tuple

from AlphaBetaAI import ab_minimax_search


class Color(Enum):
    Red = 0
    Yellow = 1
    Blue = 2

    def next(self):
        return Color((self.value + 1) % 3)

    def prev(self):
        return Color((self.value - 1) % 3)

    def __str__(self) -> str:
        if self == Color.Red:
            return "🔴"
        elif self == Color.Blue:
            return "🔵"
        elif self == Color.Yellow:
            return "🟡"


COLORS = [Color.Red, Color.Yellow, Color.Blue]

Coordinate = Tuple[int, int]


class Move:
    def __init__(self, src: Coordinate, dst: Coordinate) -> None:
        self.src = src
        self.dst = dst

    def __str__(self) -> str:
        return f"src: {self.src}, dest: {self.dst}"


class Jump(Move):
    def __init__(self, src: Coordinate, dst: Coordinate,
                 jumped: List[Coordinate]) -> None:
        self.jumped = jumped
        super().__init__(src, dst)

    def __str__(self) -> str:
        return f"src: {self.src}, dest: {self.dst}, jumped: {self.jumped}"


class Board:
    def __init__(self) -> None:
        self.turn = Color.Blue

        self.moves = []

        self.pieces = set()
        self.piece_colors = {}

        yellow_start = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 1), (1, 2),
                        (1, 3), (1, 4), (2, 2), (2, 3), (2, 4)]
        blue_start = [(4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2), (6, 0),
                      (6, 1), (6, 2), (7, 0), (7, 1), (8, 0)]
        red_start = [(4, 6), (4, 7), (4, 8), (5, 5), (5, 6), (5, 7), (6, 4),
                     (6, 5), (6, 6), (7, 4), (7, 5), (8, 4)]

        for loc in yellow_start:
            self.pieces.add(loc)
            self.piece_colors[loc] = Color.Yellow
        for loc in blue_start:
            self.pieces.add(loc)
            self.piece_colors[loc] = Color.Blue
        for loc in red_start:
            self.pieces.add(loc)
            self.piece_colors[loc] = Color.Red

    def check(self, loc: Coordinate) -> bool:
        x, y = loc
        return 0 <= x <= 8 and 0 <= y <= 8 - abs(x - 4)

    def neighbor_locs(self, loc):

        res = []

        def check(*loc):
            if self.check(loc):
                res.append(loc)

        x, y = loc

        check(x, y - 1)
        check(x, y + 1)

        if x == 4:
            check(x + 1, y - 1)
            check(x + 1, y)
            check(x - 1, y - 1)
            check(x - 1, y)

        if x < 4:
            check(x + 1, y + 1)
            check(x + 1, y)
            check(x - 1, y - 1)
            check(x - 1, y)

        if x > 4:
            check(x + 1, y)
            check(x - 1, y)
            check(x + 1, y - 1)
            check(x - 1, y + 1)

        return res

    def _corner_next(self, prev: Coordinate,
                     loc: Coordinate) -> Optional[Coordinate]:
        corners = {
            (0, 0): [(0, 1), (1, 0)],
            (4, 0): [(3, 0), (5, 0)],
            (8, 0): [(7, 0), (8, 1)],
            (8, 4): [(8, 3), (7, 5)],
            (4, 8): [(3, 7), (5, 7)],
            (0, 4): [(0, 3), (1, 5)]
        }

        if loc in corners:
            (op1, op2) = corners[loc]
            if op2 == prev:
                return op1
            if op1 == prev:
                return op2

    def _on_path(self, a: Coordinate, b: Coordinate) -> Coordinate:
        x, y = a
        nx, ny = b
        dx, dy = nx - x, ny - y

        next = (nx + dx, ny +
                dy) if nx != 4 or nx == ny == 4 else (nx + dx, ny -
                                                      1 if ny == y else ny)
        if self.check(next):
            return next
        else:
            return self._corner_next(a, b)

    def legal_moves(self):
        for loc in self.pieces:
            if self.piece_colors[loc] == self.turn:

                def jump(path: List[Coordinate]) -> List[List[Coordinate]]:
                    last = path[-1]
                    if last in self.pieces or not last:
                        return []

                    jumps = [path]

                    for neighbor in self.neighbor_locs(last):
                        if neighbor == path[-2]:
                            continue
                        if neighbor in self.pieces:
                            for sub_jump in jump(path + [neighbor]):
                                jumps.append(sub_jump)

                    return jumps

                ## Check moves to immediate neighbors
                for neighbor in self.neighbor_locs(loc):
                    if not neighbor in self.pieces:
                        yield Move(loc, neighbor)
                    else:
                        for jmp in jump(
                            [loc, neighbor,
                             self._on_path(loc, neighbor)]):
                            yield Jump(jmp[0], jmp[-1], jmp[1:-1:2])

    def push(self, move: Move):
        self.moves.append(move)

        self.pieces.remove(move.src)
        del self.piece_colors[move.src]
        self.pieces.add(move.dst)
        self.piece_colors[move.dst] = self.turn

        if isinstance(move, Jump):
            for jumped in move.jumped:
                if self.piece_colors[jumped] == self.turn.next():
                    self.pieces.remove(jumped)
                    del self.piece_colors[jumped]

        self.turn = self.turn.next()

    def pop(self):
        move = self.moves.pop(-1)
        self.turn = self.turn.prev()

        self.pieces.remove(move.dst)
        del self.piece_colors[move.dst]
        self.pieces.add(move.src)
        self.piece_colors[move.src] = self.turn

        if isinstance(move, Jump):
            for jumped in move.jumped:
                if not jumped in self.pieces:
                    self.pieces.add(jumped)
                    self.piece_colors[jumped] = self.turn.next()

    def outcome(self):
        count = [0, 0, 0]
        for color in self.piece_colors.values():
            count[color.value] += 1

        for color in COLORS:
            if count[color.value] == 3:
                return color

    def is_game_over(self):
        return bool(self.outcome())

    def __str__(self) -> str:
        res = ""

        order = [[(4, 0)], [(3, 0), (5, 0)], [(2, 0), (4, 1), (6, 0)],
                 [(1, 0), (3, 1), (5, 1), (7, 0)],
                 [(0, 0), (2, 1), (4, 2), (6, 1), (8, 0)],
                 [(1, 1), (3, 2), (5, 2), (7, 1)],
                 [(0, 1), (2, 2), (4, 3), (6, 2), (8, 1)],
                 [
                     (1, 2),
                     (3, 3),
                     (5, 3),
                     (7, 2),
                 ], [(0, 2), (2, 3), (4, 4), (6, 3), (8, 2)],
                 [(1, 3), (3, 4), (5, 4), (7, 3)],
                 [(0, 3), (2, 4), (4, 5), (6, 4), (8, 3)],
                 [(1, 4), (3, 5), (5, 5), (7, 4)],
                 [(0, 4), (2, 5), (4, 6), (6, 5), (8, 4)],
                 [(1, 5), (3, 6), (5, 6), (7, 5)], [(2, 6), (4, 7), (6, 6)],
                 [(3, 7), (5, 7)], [(4, 8)]]

        for row in order:
            first = row[0]
            res += " " * first[0] * 3
            for elem in row:
                if elem in self.pieces:
                    res += str(self.piece_colors[elem]) + "    "
                else:
                    res += "-     "
            res += '\n'
        return res


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


class PSRMiniMax():
    def __init__(self, depth: int):
        self.depth = depth

    def choose_move(self, board: Board):
        # Don't create a new board, use this one and use the push and pop features
        _val, res = ab_minimax_search(PSRMiniMaxGame(self.depth), board)
        return res


board = Board()
for move in board.legal_moves():
    board.push(move)
    print(board)
    board.pop()