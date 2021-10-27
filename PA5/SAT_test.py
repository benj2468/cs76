# Benjamin Cape - 21F - CS76
# PA5
# 10.24.21

from display import display_sudoku_solution
import random, sys
from SAT import SAT
import time

if __name__ == "__main__":
    random.seed(1)

    ## Test invalid

    result = SAT('invalid.cnf').walksat_enhanced()

    assert (result == False)
