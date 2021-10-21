# Benjamin Cape - 21F - CS76
# PA4
# 10.13.10

from typing import List
from main import BinaryCSP, VarHeuristic, test_board, ValHeuristic


class Point:
    '''
    A point is name up of an x and y coordinate
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, comp):
        return Point(self.x + comp.width, self.y + comp.height)

    def __str__(self):
        return f"({self.x}, {self.y})"


class CircutComponent:
    def __init__(self, d_start: Point, width: int, height: int):
        '''
        A circut compoint is a rectangular component that together with others can be built into tetris components

        THe d_start is the delta from the starting point of the circut piece
        '''
        self.start = d_start
        self.width = width
        self.height = height

    def realize(self, start):
        '''
        Given some starting point (bottom left), get all points in this component
        '''
        points = []
        start = Point(start.x + self.start.x, start.y + self.start.y)
        for i in range(self.width):
            for j in range(self.height):
                points.append(Point(start.x + i, start.y + j))
        return points


class CircutPiece():
    '''
    A circut piece is a tetris piece. The letter is used to describe it in printing. The order of the components doesn't matter
    '''
    def __init__(self, letter, components: List[CircutComponent]) -> None:
        self.letter = letter
        self.components = components

        self.width_sub = 0
        self.width = 0
        self.height_sub = 0
        self.height = 0

        for comp in components:
            self.height = max(self.height, comp.start.y + comp.height)
            self.width = max(self.width, comp.start.x + comp.width)

            self.height_sub = min(self.height, comp.start.y)
            self.width_sub = min(self.width, comp.start.x)

    def realize(self, start):
        '''
        Given a starting point for the piece, calculate all points
        '''
        points = []
        for component in self.components:
            comp_points = component.realize(start)
            points.extend(comp_points)
        return points

    def size(self):
        '''
        maximum size, greatest height and greatest width
        '''
        return self.height * self.width

    def __str__(self) -> str:
        return f"({self.width}, {self.height})"

    def __hash__(self) -> int:
        return (self.letter, self.height, self.width).__hash__()


def do_overlap(piece1: CircutPiece, start1, piece2: CircutPiece, start2):
    '''
    Given two pieces and their respective starting places, determine if they are disjoint or not.
    '''
    p1 = set(map(lambda x: str(x), piece1.realize(Point(*start1))))
    p2 = set(map(lambda x: str(x), piece2.realize(Point(*start2))))

    return not p1.isdisjoint(p2)


class CircutLayout(BinaryCSP):
    '''
    A CSP for solving the tetris layout problem
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
            for i in range(abs(self.variable_map[piece].width_sub),
                           width - self.variable_map[piece].width + 1):
                for j in range(abs(self.variable_map[piece].height_sub),
                               height - self.variable_map[piece].height + 1):
                    domains[piece].add((i, j))

        super().__init__(variables, constraints, domains, **kwargs)

    def print(self, assignment, **kwargs) -> str:
        '''
        Print the board with a specific assignment
        '''
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
                for r in piece.realize(Point(*assignment[i])):
                    realized[(r.x, r.y)] = piece
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

circut = CircutLayout(
    3,
    10, [
        CircutPiece("a", [CircutComponent(Point(0, 0), 3, 1)]),
        CircutPiece("b", [CircutComponent(Point(0, 0), 3, 1)]),
        CircutPiece("c", [
            CircutComponent(Point(0, 0), 5, 1),
            CircutComponent(Point(-1, 0), 1, 2)
        ]),
        CircutPiece("d", [CircutComponent(Point(0, 0), 1, 2)]),
        CircutPiece("e", [CircutComponent(Point(0, 0), 3, 2)]),
        CircutPiece("f", [
            CircutComponent(Point(0, 0), 2, 1),
            CircutComponent(Point(1, -1), 1, 1)
        ]),
        CircutPiece("g", [
            CircutComponent(Point(0, 0), 2, 1),
            CircutComponent(Point(1, -2), 1, 2)
        ]),
    ],
    var_h=VarHeuristic.DEGREE_TIEBREAKER,
    val_h=ValHeuristic.LCV)

test_board(circut)