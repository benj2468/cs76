# Benjamin Cape - 21F - CS76
# PA4
# 10.13.10

from collections import defaultdict, deque
from typing import Any, Dict, List, Mapping, Optional, Set, Tuple
from enum import Enum
from copy import copy, deepcopy


class VarHeuristic(Enum):
    '''
    Enum for specifying variable selection heuristic
    '''
    MRV = "MRV"
    DEGREE_TIEBREAKER = "DEGREE_TIEBREAKER"


class ValHeuristic(Enum):
    '''
    Enum for specifying value selection heuristic
    '''
    LCV = "LCV"


class BinaryCSP:
    '''
    Base object for describing any binary CSP
    '''
    def __init__(self,
                 variables: List[int],
                 constraints: Mapping[Tuple[int, int], str],
                 domains: Mapping[int, Set[int]],
                 var_h: Optional[VarHeuristic] = None,
                 val_h: Optional[ValHeuristic] = None) -> None:
        self.variables = variables
        self.constraints = constraints
        self.domains = domains
        self.start_domains = deepcopy(domains)

        self.default_assignment = {}

        self.constraint_graph = defaultdict(lambda: set())
        for (u, v) in constraints:
            self.constraint_graph[u].add(v)
            self.constraint_graph[v].add(u)

        self.var_h = var_h
        self.val_h = val_h

    def assign_one(self, var, val, assignment):
        '''
        Given a variable and a value, add it to the assignment
        '''
        for neighbor in copy(self.constraint_graph[var]):
            if neighbor in assignment:
                # Once we make the assignments we can remove the constraints - this will speed up inference dramatically
                self.constraint_graph[neighbor].remove(var)
                self.constraint_graph[var].remove(neighbor)
                if (var, neighbor) in self.constraints:
                    del self.constraints[(var, neighbor)]
                if (neighbor, var) in self.constraints:
                    del self.constraints[(neighbor, var)]
        # Make the assignment
        return {**assignment, var: val}

    def assign_many(self, inferences, assignment):
        '''
        Given many different, valid, assignments, make all of them.
        '''
        new = {**assignment}
        for k, v in inferences:
            new = self.assign_one(k, v, new)
        return new

    def is_assigned(self, var, assignment):
        '''
        Check if 
        '''
        return var in assignment and assignment[var] != None

    def mrv_heuristic(self, assignment, with_degree=False):
        '''
        Minimum Remaining Values - take value with smallest domain, might use degree heuristic as a tie breaker 
        '''
        res = (None, float('inf'))
        for v, domain in self.domains.items():
            # Don't consider assigned variables
            if self.is_assigned(v, assignment):
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
        '''
        Degree heuristic - take the variable that has the fewest contraints with other variables.
        '''
        degree = 0
        for n in self.constraint_graph[var]:
            if not self.is_assigned(n, assignment):
                degree += 1

        return degree

    def lcv_heuristic(self, var):
        '''
        Least Constraining variable heuristic - take variable that restricts the least other variables domains
        '''
        for val in self.domains[var]:
            count = 0
            for neighbor in self.constraint_graph[var]:
                count += len(self.domains[neighbor])
                if val in self.domains[neighbor]:
                    count -= 1

            yield (val, count)

    def next_variable(self, assignment):
        '''
        Get the next variable to search, given an existing assignment - will potentially use heuristic
        '''
        if self.var_h in [VarHeuristic.DEGREE_TIEBREAKER, VarHeuristic.MRV]:
            return self.mrv_heuristic(
                assignment, self.var_h == VarHeuristic.DEGREE_TIEBREAKER)
        elif self.var_h == None:
            for var in self.variables:
                if not self.is_assigned(var, assignment):
                    return var
        else:
            return self.var_h(assignment)

    def get_values(self, var, assignment):
        '''
        Get the values of the specific variable, given an existing assignment - will potentially use heuristic
        '''
        if self.val_h == ValHeuristic.LCV:
            return map(
                lambda a: a[0],
                sorted(self.lcv_heuristic(var),
                       key=lambda a: a[1],
                       reverse=True))
        elif self.val_h == None:
            return self.domains[var]
        else:
            return self.val_h(var, assignment)

    def is_complete(self, assignment):
        '''
        Check if the assignment is complete
        '''
        for var in self.variables:
            if not self.is_assigned(var, assignment):
                return False

        return True

    def has_consistent(self, var, val, other_var):
        '''
        Check if there is a way to make other_var consistent with the assignment of val to var.
        '''
        for y in self.domains[other_var]:
            if self.is_consistent(
                    other_var, y,
                    self.assign_one(var, val, self.default_assignment)):
                return True
        return False

    def inferences(self, var, val, assignment):
        '''
        Make inferences provided a value to start with, and an assignment to add to.

        This will edit self
        '''
        # Start only with the ones that are imediatly changed, this will grow as we make more restrictions to domains
        queue = deque(self.constraints)

        inferences = self.default_assignment
        domains: Dict[Any, Set[Any]] = self.domains

        # Remove inconsistent values from the domains
        def remove_inconsistent_values(v, u):
            removed_bool = False
            for x in copy(domains[v]):
                found_consistent = self.has_consistent(v, x, u)
                if not found_consistent:
                    domains[v].remove(x)
                    # If we make the domain empty, we know we failed, so return None.
                    if len(domains[v]) == 0:
                        return None
                    # If we get only one, making the assignment
                    if len(domains[v]) == 1:
                        n = next(iter(domains[v]))
                        with_inferences = self.assign_many(
                            inferences, assignment)
                        if self.is_consistent(v, n, with_inferences):
                            self.assign_one(v, n, inferences)
                    removed_bool = True
            return removed_bool

        while len(queue):
            u, v = queue.pop()
            removed_bool = remove_inconsistent_values(u, v)
            if removed_bool:
                # if we removed some variables, add all the neighbors of v to the queue so that we recheck them too
                for neighbor in self.constraint_graph[v]:
                    queue.append((v, neighbor))
            elif removed_bool == None:
                # If we got none, that means this failed, so we return None and bubble up
                return None

        return inferences

    def backtracking_search(self, with_inference=False):
        '''
        Function actually called to initiate the backtracking search
        '''
        calls = 0
        return self.backtrack(self.default_assignment, calls, with_inference)

    def backtrack(self, assignment, calls, with_inference):
        '''
        Backtracking algorithm that searched for a valid assignment of the variables.
        '''
        if self.is_complete(assignment):
            return (assignment, calls)

        var = self.next_variable(assignment)
        for val in self.get_values(var, assignment):
            calls += 1
            # Deep copy self so that if we fail, we get back to the state at this point in the tree.
            prev = deepcopy(self)
            if self.is_consistent(var, val, assignment):
                sub_assignment = self.assign_one(var, val, assignment)
                # After making an assignment, set the domain to just that variable
                self.domains[var] = set([val])
                inferences = self.inferences(
                    var, val, sub_assignment
                ) if with_inference else self.default_assignment
                if inferences != None:
                    # If we didn't fail with the inference, i.e. retrieved {} or {...} then we continue down the DFS tree
                    # returns calls so we keep track of ALL the calls
                    (result, calls) = self.backtrack(
                        self.assign_many(inferences, sub_assignment), calls,
                        with_inference)
                    if result:
                        return (result, calls)
            self = prev

        return (None, calls)

    def print(self, data: List[str], calls: int = None, time=None):
        '''
        Print the CSP with the provided previous data
        '''
        data.append(f"Variable Heuristic: {self.var_h}")
        data.append(f"Value Heuristic: {self.val_h}")
        if time:
            data.append(f"Time Taken: {time.microseconds / 1000} ms")
        if calls != None:
            data.append(f"Values Checked: {calls}")
        data = "\n|- ".join(data)
        print(f"""
|-----
|- Solution:
|-
|- {data}
|-----
""")


from datetime import datetime


def test_board(csp: BinaryCSP):
    csp.domains = deepcopy(csp.start_domains)
    print("With Inference: ")
    start = datetime.now()
    (assign, calls) = csp.backtracking_search(with_inference=True)
    csp.print(assign, time=(datetime.now() - start), calls=calls)

    csp.domains = deepcopy(csp.start_domains)
    print("Without Inference: ")
    start = datetime.now()
    (assign, calls) = csp.backtracking_search()
    csp.print(assign, time=(datetime.now() - start), calls=calls)
