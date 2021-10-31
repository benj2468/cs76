# Benjamin Cape - 21F - CS76
# PA5
# 10.24.21

from display import display_sudoku_solution
import random, sys
from SAT import SAT
from SAT_BONUS import SAT as SAT3
import time

if __name__ == "__main__":
    random.seed(1)

    puzzle_name = str(sys.argv[1][:-4])
    sol_filename = puzzle_name + ".sol"

    sat = SAT(sys.argv[1])

    print('SAT Stats:', sat.stats())

    t = time.time()
    result = sat.walksat_enhanced()

    print(f"Enhanced Walksat", time.time() - t)
    print("Enhanced walksat: ", result)

    if result[1]:
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)

    t = time.time()
    random.seed(1)
    result = sat.walksat()
    print("walksat: ", time.time() - t)
    print("walksat: ", result)

    t = time.time()
    random.seed(1)
    result = sat.gsat()
    print("gsat: ", time.time() - t)
    print("gsat: ", result)

    sat3 = SAT3(sys.argv[1])
    result = sat3.dpll_backtracking()
    if result[1]:

        sat3.write_solution("_" + sol_filename)
        display_sudoku_solution("_" + sol_filename)
        sat3.delete_solution("_" + sol_filename)