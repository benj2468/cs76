# Benjamin Cape - 21F - CS76
# PA4
# 10.13.10

from math import degrees
from typing import List
from main import BinaryCSP, VarHeuristic, test_board, ValHeuristic


class Coloring(BinaryCSP):
    '''
    A definition for a CSP for solving any sort of coloring

    colors: # of colors we are allowed to use
    Constraints: Which variables must have different colors
    '''
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
        '''
        Means for printing the assignment
        '''
        solution = []
        solution.append(f"Variables: {self.variables}")
        solution.append(f"Colors: {self.colors}")
        solution.append(f"Assignment: {assignment}")

        super().print(solution, **kwargs)

    def is_consistent(self, var, val, assignment) -> bool:
        '''
        Determine if the new var:val is consistent with the assignment
        '''
        for neighbor in self.constraint_graph[var]:
            if neighbor in assignment and assignment[neighbor] == val:
                return False

        return True


# Testing

usa = {
    'AK': [],
    'AL': ['MS', 'TN', 'GA', 'FL'],
    'AR': ['MO', 'TN', 'MS', 'LA', 'TX', 'OK'],
    'AZ': ['CA', 'NV', 'UT', 'CO', 'NM'],
    'CA': ['OR', 'NV', 'AZ'],
    'CO': ['WY', 'NE', 'KS', 'OK', 'NM', 'AZ', 'UT'],
    'CT': ['NY', 'MA', 'RI'],
    'DC': ['MD', 'VA'],
    'DE': ['MD', 'PA', 'NJ'],
    'FL': ['AL', 'GA'],
    'GA': ['FL', 'AL', 'TN', 'NC', 'SC'],
    'HI': [],
    'IA': ['MN', 'WI', 'IL', 'MO', 'NE', 'SD'],
    'ID': ['MT', 'WY', 'UT', 'NV', 'OR', 'WA'],
    'IL': ['IN', 'KY', 'MO', 'IA', 'WI'],
    'IN': ['MI', 'OH', 'KY', 'IL'],
    'KS': ['NE', 'MO', 'OK', 'CO'],
    'KY': ['IN', 'OH', 'WV', 'VA', 'TN', 'MO', 'IL'],
    'LA': ['TX', 'AR', 'MS'],
    'MA': ['RI', 'CT', 'NY', 'NH', 'VT'],
    'MD': ['VA', 'WV', 'PA', 'DC', 'DE'],
    'ME': ['NH'],
    'MI': ['WI', 'IN', 'OH'],
    'MN': ['WI', 'IA', 'SD', 'ND'],
    'MO': ['IA', 'IL', 'KY', 'TN', 'AR', 'OK', 'KS', 'NE'],
    'MS': ['LA', 'AR', 'TN', 'AL'],
    'MT': ['ND', 'SD', 'WY', 'ID'],
    'NC': ['VA', 'TN', 'GA', 'SC'],
    'ND': ['MN', 'SD', 'MT'],
    'NE': ['SD', 'IA', 'MO', 'KS', 'CO', 'WY'],
    'NH': ['VT', 'ME', 'MA'],
    'NJ': ['DE', 'PA', 'NY'],
    'NM': ['AZ', 'UT', 'CO', 'OK', 'TX'],
    'NV': ['ID', 'UT', 'AZ', 'CA', 'OR'],
    'NY': ['NJ', 'PA', 'VT', 'MA', 'CT'],
    'OH': ['PA', 'WV', 'KY', 'IN', 'MI'],
    'OK': ['KS', 'MO', 'AR', 'TX', 'NM', 'CO'],
    'OR': ['CA', 'NV', 'ID', 'WA'],
    'PA': ['NY', 'NJ', 'DE', 'MD', 'WV', 'OH'],
    'RI': ['CT', 'MA'],
    'SC': ['GA', 'NC'],
    'SD': ['ND', 'MN', 'IA', 'NE', 'WY', 'MT'],
    'TN': ['KY', 'VA', 'NC', 'GA', 'AL', 'MS', 'AR', 'MO'],
    'TX': ['NM', 'OK', 'AR', 'LA'],
    'UT': ['ID', 'WY', 'CO', 'NM', 'AZ', 'NV'],
    'VA': ['NC', 'TN', 'KY', 'WV', 'MD', 'DC'],
    'VT': ['NY', 'NH', 'MA'],
    'WA': ['ID', 'OR'],
    'WI': ['MI', 'MN', 'IA', 'IL'],
    'WV': ['OH', 'PA', 'MD', 'VA', 'KY'],
    'WY': ['MT', 'SD', 'NE', 'CO', 'UT', 'ID'],
}

constraints = set()
for st in list(usa):
    for st2 in usa[st]:
        constraint = (min(st, st2), max(st, st2))
        constraints.add(constraint)

coloring_problem = Coloring(list(usa),
                            5,
                            list(constraints),
                            var_h=VarHeuristic.DEGREE_TIEBREAKER,
                            val_h=ValHeuristic.LCV)
test_board(coloring_problem)

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
