from collections import defaultdict, deque
from typing import Any, Dict, Optional, Set
from enum import Enum
from copy import copy, deepcopy


class VarHeuristic(Enum):
    MRV = "MRV"
    DEGREE_TIEBREAKER = "DEGREE_TIEBREAKER"


class BinaryCSP:
    def __init__(self,
                 variables,
                 constraints,
                 domains,
                 var_h=Optional[VarHeuristic],
                 use_val_h=False) -> None:
        self.variables = variables
        # Change constraints into a map from pairs of variables to pairs of options
        self.constraints = constraints
        self.domains = domains
        self.start_domains = deepcopy(domains)

        self.constraint_graph = defaultdict(lambda: set())
        for (u, v) in constraints:
            self.constraint_graph[u].add(v)
            self.constraint_graph[v].add(u)

        self.var_h = var_h
        self.use_val_h = use_val_h

    def mrv_heuristic(self, assignment, with_degree=False):
        res = (None, float('inf'))
        for v, domain in self.domains.items():
            if v in assignment and assignment[v] != None:
                continue
            if len(domain) < res[1]:
                res = (v, len(domain))
            elif len(domain) == res[1]:
                if with_degree and self.degree_heuristic(
                        v, assignment) > self.degree_heuristic(
                            res[1], assignment):
                    res = (v, len(domain))
        return res[0]

    def degree_heuristic(self, var, assignment):
        degree = 0
        for n in self.constraint_graph[var]:
            if not n in assignment or assignment[n] == None:
                degree += 1

        return degree

    def lcv_heuristic(self, var):
        for val in self.domains[var]:
            count = 0
            for neighbor in self.constraint_graph[var]:
                count += len(self.domains[neighbor])
                if val in self.domains[neighbor]:
                    count -= 1

            yield (val, count)

    def next_variable(self, assignment):
        if self.var_h != None:
            return self.mrv_heuristic(
                assignment, self.var_h == VarHeuristic.DEGREE_TIEBREAKER)
        else:
            for var in self.variables:
                if not var in assignment or assignment[var] == None:
                    return var

    def get_values(self, var, assignment):
        if self.use_val_h:
            return map(lambda a: a[0],
                       sorted(
                           self.lcv_heuristic(var),
                           key=lambda a: a[1],
                       ))
        return self.domains[var]

    def is_complete(self, assignment):
        for var in self.variables:
            if not var in assignment or assignment[var] == None:
                return False

        return True

    def inferences(self, assignment):
        queue = deque(self.constraints.keys())

        inferences = {}
        domains: Dict[Any, Set[Any]] = self.domains

        def remove_inconsistent_values(v, u):
            removed_bool = False
            for x in copy(domains[v]):
                found_consistent = False
                for y in domains[u]:
                    if self.is_consistent(u, y, {v: x}):
                        found_consistent = True
                if not found_consistent:
                    domains[v].remove(x)
                    if len(domains[v]) == 0:
                        return None
                    if len(domains[v]) == 1:
                        n = next(iter(domains[v]))
                        if self.is_consistent(v, n, {
                                **assignment,
                                **inferences
                        }):
                            inferences[v] = n
                    removed_bool = True
            return removed_bool

        while len(queue):
            u, v = queue.pop()
            removed_bool = remove_inconsistent_values(u, v)
            if removed_bool:
                for neighbor in self.constraint_graph[v]:
                    queue.append((v, neighbor))
            elif removed_bool == None:
                return None

        return inferences

    def backtracking_search(self, with_inference=False):
        calls = 0
        return self.backtrack({}, calls, with_inference)

    def backtrack(self, assignment, calls, with_inference):
        if self.is_complete(assignment):
            return (assignment, calls)

        var = self.next_variable(assignment)
        for val in self.get_values(var, assignment):
            calls += 1
            prev_assignment = deepcopy(assignment)
            prev = deepcopy(self)
            if self.is_consistent(var, val, assignment):
                assignment = {**assignment, var: val}
                self.domains[var] = set([val])
                inferences = self.inferences(
                    assignment) if with_inference else {}
                if inferences != None:
                    (result,
                     calls) = self.backtrack({
                         **assignment,
                         **inferences
                     }, calls, with_inference)
                    if result:
                        return (result, calls)
            assignment = prev_assignment
            self = prev

        return (None, calls)

    def print(self, assignment):
        print(assignment)


from datetime import datetime


def test_board(csp: BinaryCSP):
    csp.domains = deepcopy(csp.start_domains)
    print("Without Inference: ")
    start = datetime.now()
    (assign, calls) = csp.backtracking_search()
    print("Running Time: ", (datetime.now() - start).microseconds / 1000, "ms")
    csp.print(assign)
    print("Value checks: ", calls)

    csp.domains = deepcopy(csp.start_domains)
    print("With Inference: ")
    start = datetime.now()
    (assign, calls) = csp.backtracking_search(with_inference=True)
    print("Running Time: ", (datetime.now() - start).microseconds / 1000, "ms")
    csp.print(assign)
    print("Value checks: ", calls)