# Benjamin Cape - 21F - CS76
# PA4
# 10.13.10

from typing import List
from csp import BinaryCSP, VarHeuristic, test_board, ValHeuristic


class CircutPiece():
    def __init__(self, letter, width, height) -> None:
        self.letter = letter
        self.height = height
        self.width = width

    def realize(self, start):
        points = []
        (x, y) = start
        points.append(start)
        for dx in range(self.width):
            for dy in range(self.height):
                points.append((x + dx, y + dy))
        return points

    def size(self):
        return self.height * self.width

    def __str__(self) -> str:
        return f"({self.width}, {self.height})"

    def __add__(self, point):
        (x, y) = point
        return (x + self.width, y + self.height)

    def __hash__(self) -> int:
        return (self.letter, self.height, self.width).__hash__()


def doOverlap(l1, r1, l2, r2):

    # To check if either rectangle is actually a line
    # For example  :  l1 ={-1,0}  r1={1,1}  l2={0,-1}  r2={0,1}
    if (l1[0] == r1[0] or l1[1] == r1[1] or l2[0] == r2[0] or l2[1] == r2[1]):
        # the line cannot have positive overlap
        return False
    # If one rectangle is on left side of other
    if (l1[0] >= r2[0] or l2[0] >= r1[0]):
        return False
    # If one rectangle is above other
    if (r1[1] >= l2[1] or r2[1] >= l1[1]):
        return False

    return True


def do_overlap(piece1: CircutPiece, start1, piece2: CircutPiece, start2):
    # This can most def be done faster
    realized1 = set(piece1.realize(start1))
    realized2 = set(piece2.realize(start2))
    return not realized1.isdisjoint(realized2)


class CircutLayout(BinaryCSP):
    def __init__(self, height: int, width: int, pieces: List[CircutPiece],
                 **kwargs) -> None:

        variables = range(0, len(pieces))
        self.height = height
        self.width = width

        self.variable_map = {}
        for i, var in enumerate(pieces):
            self.variable_map[i] = var

        constraints = {}
        domains = {}
        for piece in variables:
            for piece2 in variables:
                if piece != piece2:
                    constraints[(piece, piece2)] = "NonOverlapping"

            domains[piece] = set()
            for i in range(width - self.variable_map[piece].width + 1):
                for j in range(height - self.variable_map[piece].height + 1):
                    domains[piece].add((i, j))

        super().__init__(variables, constraints, domains, **kwargs)

    def print(self, assignment, **kwargs) -> str:

        solution = []
        solution.append(
            f"Variables: {', '.join(map(lambda x: str(x), self.variable_map.values()))}"
        )

        if not assignment:
            res = ["None"]
        else:
            realized = {}
            for i in self.variables:
                piece = self.variable_map[i]
                if not i in assignment:
                    continue
                for r in piece.realize(assignment[i]):
                    realized[r] = piece

            res = []
            for j in range(self.height - 1, -1, -1):
                line = ""
                for i in range(self.width):
                    if (i, j) in realized:
                        line += realized[(i, j)].letter
                    else:
                        line += "."

                res.append(line)

        solution.append(f"Assignment: ")
        for line in res:
            solution.append(f"  {line}")

        super().print(solution, **kwargs)

    def is_consistent(self, var, val, assignment):
        for i in assignment.keys():
            piece = self.variable_map[i]
            if do_overlap(self.variable_map[var], val, piece, assignment[i]):
                return False
        return True


# circut = CircutLayout(3,
#                       10, [
#                           CircutPiece("a", 3, 1),
#                           CircutPiece("a", 3, 1),
#                           CircutPiece("b", 5, 1),
#                           CircutPiece("b", 5, 1),
#                           CircutPiece("c", 2, 1),
#                           CircutPiece("c", 2, 1),
#                           CircutPiece("c", 2, 1),
#                           CircutPiece("d", 7, 1)
#                       ],
#                       var_h=VarHeuristic.DEGREE_TIEBREAKER,
#                       val_h=ValHeuristic.LCV)
# test_board(circut)

# circut = CircutLayout(3,
#                       10, [
#                           CircutPiece("a", 3, 1),
#                           CircutPiece("a", 3, 1),
#                           CircutPiece("b", 5, 1),
#                           CircutPiece("b", 5, 1),
#                           CircutPiece("c", 2, 1),
#                           CircutPiece("c", 2, 1),
#                           CircutPiece("c", 2, 1),
#                           CircutPiece("d", 7, 1)
#                       ],
#                       var_h=VarHeuristic.DEGREE_TIEBREAKER)
# test_board(circut)

circut = CircutLayout(3,
                      13, [
                          CircutPiece("b", 5, 1),
                          CircutPiece("b", 9, 1),
                          CircutPiece("c", 2, 1),
                          CircutPiece("c", 2, 1),
                          CircutPiece("c", 2, 1),
                          CircutPiece("d", 8, 1),
                          CircutPiece("a", 3, 4)
                      ],
                      var_h=VarHeuristic.DEGREE_TIEBREAKER,
                      val_h=ValHeuristic.LCV)

test_board(circut)