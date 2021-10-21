# Benjamin Cape - 21F - CS76
# PA4
# 10.13.10

from typing import List
from main import BinaryCSP, VarHeuristic, test_board, ValHeuristic


class Point:
    '''
    A point consists of an x and y coordinate
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y


class CircutPiece():
    '''
    A circut piece is a rectangular piece. The letter is used to describe it in printing.
    '''
    def __init__(self, letter, width, height) -> None:
        self.letter = letter
        self.height = height
        self.width = width

    def realize(self, start):
        '''
        Given a starting point for the piece, calculate all points
        '''
        points = []
        (x, y) = start
        points.append(start)
        for dx in range(self.width):
            for dy in range(self.height):
                points.append((x + dx, y + dy))
        return points

    def size(self):
        '''
        maximum size, greatest height and greatest width
        '''
        return self.height * self.width

    def __str__(self) -> str:
        return f"({self.width}, {self.height})"

    def __radd__(self, point):
        (x, y) = point
        return (x + self.width, y + self.height)

    def __hash__(self) -> int:
        return (self.letter, self.height, self.width).__hash__()

    def as_points(self, bot_left):
        (x, y) = bot_left
        return (Point(x, y + self.height), Point(x + self.width, y))


# I did not write this. Credit: https://www.geeksforgeeks.org/find-two-rectangles-overlap/
# Returns true if two rectangles(l1, r1)
# and (l2, r2) overlap
def doOverlap(l1, r1, l2, r2):

    # To check if either rectangle is actually a line
    # For example  :  l1 ={-1,0}  r1={1,1}  l2={0,-1}  r2={0,1}

    if (l1.x == r1.x or l1.y == r1.y or l2.x == r2.x or l2.y == r2.y):
        # the line cannot have positive overlap
        return False

    # If one rectangle is on left side of other
    if (l1.x >= r2.x or l2.x >= r1.x):
        return False

    # If one rectangle is above other
    if (r1.y >= l2.y or r2.y >= l1.y):
        return False

    return True


def do_overlap(piece1: CircutPiece, start1, piece2: CircutPiece, start2):
    '''
    Given two pieces and their respective starting places, determine if they are disjoint or not.
    '''
    return doOverlap(*piece1.as_points(start1), *piece2.as_points(start2))


class CircutLayout(BinaryCSP):
    '''
    A CSP for solving the rectangular circut layout problem
    '''
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
        '''
        Determine if the new var:val is consistent with the assignment
        '''
        for i in assignment.keys():
            piece = self.variable_map[i]
            if do_overlap(self.variable_map[var], val, piece, assignment[i]):
                return False
        return True


# Testing

circut = CircutLayout(3, 10, [
    CircutPiece("a", 3, 1),
    CircutPiece("a", 3, 1),
    CircutPiece("b", 5, 1),
    CircutPiece("b", 5, 1),
    CircutPiece("c", 2, 1),
    CircutPiece("c", 2, 1),
    CircutPiece("c", 2, 1),
    CircutPiece("d", 7, 1)
])
test_board(circut)

circut = CircutLayout(3,
                      13, [
                          CircutPiece("a", 3, 1),
                          CircutPiece("a", 3, 1),
                          CircutPiece("b", 5, 1),
                          CircutPiece("b", 5, 1),
                          CircutPiece("c", 2, 1),
                          CircutPiece("c", 2, 1),
                          CircutPiece("c", 2, 1),
                          CircutPiece("d", 7, 1)
                      ],
                      var_h=VarHeuristic.MRV,
                      val_h=ValHeuristic.LCV)

test_board(circut)

circut = CircutLayout(3,
                      10, [
                          CircutPiece("a", 3, 1),
                          CircutPiece("a", 3, 1),
                          CircutPiece("b", 5, 1),
                          CircutPiece("b", 5, 1),
                          CircutPiece("c", 2, 1),
                          CircutPiece("c", 2, 1),
                          CircutPiece("c", 2, 1),
                          CircutPiece("d", 7, 1)
                      ],
                      var_h=VarHeuristic.DEGREE_TIEBREAKER,
                      val_h=ValHeuristic.LCV)
test_board(circut)