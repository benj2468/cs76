# Benjamin Cape - 21F - CS76
# PA5
# 10.24.21

import random, sys
from SAT import SAT
from CNF import Satisfied
import time

if __name__ == "__main__":
    random.seed(1)

    ## Test invalid

    result = SAT('invalid.cnf').walksat_enhanced()

    assert (result == (1, None))

    ## Test sub-functions
    cnf = SAT('tester.cnf').cnf

    assert (cnf.is_satisfied([None, None]) == False)

    assert (cnf.satisfied([None, None]) == Satisfied.Unknown)

    assert (cnf.count_satisfied([True, None]) == 1)

    assert (cnf.get_satisfied([True, True]).union(
        cnf.unsatisfied_clauses([True, True])) == set(cnf.sentences))

    assert (cnf.count_satisfied_diff(cnf.get_satisfied([True, True]),
                                     [True, True], 1) == 1)

    assert (cnf.count_satisfied_diff(cnf.get_satisfied([True, True]),
                                     [True, True], 0) == 1)
