# Benjamin Cape - 21F - CS76
# PA4
# 10.13.10

from typing import List
from csp import BinaryCSP, VarHeuristic, test_board, ValHeuristic


class Coloring(BinaryCSP):
    def __init__(self, variables: List[str], colors: int, constraints,
                 **kwargs) -> None:

        domains = {}
        for v in variables:
            domains[v] = set(c for c in range(colors))
        self.colors = colors

        constraints_dict = {}
        for const in constraints:
            constraints_dict[const] = "NotEqual"

        super().__init__(variables, constraints_dict, domains, **kwargs)

    def print(self, assignment, **kwargs):
        solution = []
        solution.append(f"Variables: {self.variables}")
        solution.append(f"Colors: {self.colors}")
        solution.append(f"Assignment: {assignment}")

        super().print(solution, **kwargs)

    def is_consistent(self, var, val, assignment) -> bool:
        for neighbor in self.constraint_graph[var]:
            if neighbor in assignment and assignment[neighbor] == val:
                return False

        return True


coloring_problem = Coloring(
    ['WA', 'OR', 'CA', 'ID', 'MT', "BC", "WY"],
    3,
    [("WA", "BC"), ("WA", "ID"), ("WA", "OR"), ("OR", "ID"), ("OR", "CA"),
     ("ID", "MT"), ("ID", "WY"), ("BC", "ID"), ("BC", "MT"), ("MT", "WY")],
)
test_board(coloring_problem)

coloring_problem = Coloring(['WA', 'OR', 'CA', 'ID', 'MT', "BC", "WY"],
                            3, [("WA", "BC"), ("WA", "ID"), ("WA", "OR"),
                                ("OR", "ID"), ("OR", "CA"), ("ID", "MT"),
                                ("ID", "WY"), ("BC", "ID"), ("BC", "MT"),
                                ("MT", "WY")],
                            var_h=VarHeuristic.DEGREE_TIEBREAKER)
test_board(coloring_problem)

coloring_problem = Coloring(['WA', 'OR', 'CA', 'ID', 'MT', "BC", "WY"],
                            3, [("WA", "BC"), ("WA", "ID"), ("WA", "OR"),
                                ("OR", "ID"), ("OR", "CA"), ("ID", "MT"),
                                ("ID", "WY"), ("BC", "ID"), ("BC", "MT"),
                                ("MT", "WY")],
                            var_h=VarHeuristic.DEGREE_TIEBREAKER,
                            val_h=ValHeuristic.LCV)
test_board(coloring_problem)

coloring_problem = Coloring(['WA', 'OR', 'CA', 'ID', 'MT', "BC", "WY"],
                            2, [("WA", "BC"), ("WA", "ID"), ("WA", "OR"),
                                ("OR", "ID"), ("OR", "CA"), ("ID", "MT"),
                                ("ID", "WY"), ("BC", "ID"), ("BC", "MT"),
                                ("MT", "WY")],
                            var_h=VarHeuristic.DEGREE_TIEBREAKER,
                            val_h=ValHeuristic.LCV)
test_board(coloring_problem)
