from Maze import Maze
from SensorlessProblem import SensorlessProblem

from astar_search import astar_search


def null_heuristic(state):
    return 0


test_maze3 = Maze("maze4.maz")
sensorless = SensorlessProblem(test_maze3, (1, 4))
man_res = astar_search(sensorless, sensorless.manhattan_heuristic, sync=True)
print(man_res)
