from copy import deepcopy
from typing import List
from csp import BinaryCSP, VarHeuristic, test_board
from datetime import datetime


class Coloring(BinaryCSP):
    def __init__(self,
                 variables: List[str],
                 colors: int,
                 constraints,
                 var_h: VarHeuristic = None,
                 use_val_h=False) -> None:

        domains = {}
        for v in variables:
            domains[v] = set(c for c in range(colors))

        constraints_dict = {}
        for const in constraints:
            constraints_dict[const] = "NotEqual"

        super().__init__(variables, constraints_dict, domains, var_h,
                         use_val_h)

        self.var_heuristic = VarHeuristic
        self.val_heuristic = use_val_h

    def is_consistent(self, var, val, assignment) -> bool:
        for neighbor in self.constraint_graph[var]:
            if neighbor in assignment and assignment[neighbor] == val:
                return False

        return True


coloring_problem = Coloring(['WA', 'OR', 'CA', 'ID', 'MT', "BC", "WY"],
                            3, [("WA", "BC"), ("WA", "ID"), ("WA", "OR"),
                                ("OR", "ID"), ("OR", "CA"), ("ID", "MT"),
                                ("ID", "WY"), ("BC", "ID"), ("BC", "MT"),
                                ("MT", "WY")],
                            var_h=VarHeuristic.DEGREE_TIEBREAKER,
                            use_val_h=True)

test_board(coloring_problem)
