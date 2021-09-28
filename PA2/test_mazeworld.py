from MazeworldProblem import MazeworldProblem
from Maze import Maze

# from uninformed_search import bfs_search
from astar_search import astar_search, bfs_search


# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0


# Test problems


def test_maze(prob: MazeworldProblem, check_bfs=False):
    print(prob)
    a_res = astar_search(prob, prob.manhattan_heuristic, sync=True)
    print(a_res)
    if check_bfs:
        bfs_res = bfs_search(prob)

        assert (len(bfs_res.path) >= len(a_res.path))
        assert (bfs_res.nodes_visited >= a_res.nodes_visited)
        print("CORRECT. By Proof of BFS correctness")


test_maze3 = Maze("maze3.maz")
test_mp = MazeworldProblem(test_maze3, [(1, 4), (1, 3), (1, 2)])
print(test_mp)
a_res = astar_search(test_mp, test_mp.manhattan_heuristic, sync=True)
print(a_res)

# test_maze(test_mp)

# for i in range(5):
#     rand = Maze(None, 40, 40)
#     prob = MazeworldProblem(rand, rand.rand_goals())
#     test_maze(prob)
