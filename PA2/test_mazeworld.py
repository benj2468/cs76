# Benjamin Cape - 21F - CS76
# PA2
# 10.02.10

from MazeworldProblem import MazeworldProblem
from Maze import Maze

from astar_search import astar_search


def test_maze(prob: MazeworldProblem):
    print(prob)
    a_res = astar_search(prob, prob.manhattan_heuristic)
    print("First: ", a_res)
    # Animate the path is you wish!
    # prob.animate_path(a_res.path)
    return a_res


test_maze3 = Maze("maze3.maz")
test_3_1 = MazeworldProblem(test_maze3, [(1, 4), (1, 3), (1, 2)])
test_maze(test_3_1)

for i in range(3):
    rand = Maze(None, 60, 60)
    goals = rand.rand_goals()
    prob = MazeworldProblem(rand, goals)
    test_maze(prob)
