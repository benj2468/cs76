from Maze import Maze
from SensorlessProblem import SensorlessProblem

from astar_search import astar_search


def null_heuristic(state):
    return 0


def test_maze(prob: SensorlessProblem):
    a_res = astar_search(prob, prob.manhattan_heuristic)
    print(a_res)


test_maze3 = Maze("maze3.maz")
test_maze3.robotloc = test_maze3.robotloc[0:1]
sensorless = SensorlessProblem(test_maze3, (1, 4))
test_maze(sensorless)

# You can comment this out if it's not working, sometimes you get a bad graph and you have to restart.
for i in range(5):
    maze = Maze(None, 15, 15, robots=1)
    goal = maze.rand_goals()[0]
    print(maze.with_goals([goal]))
    prob = SensorlessProblem(maze, goal)
    test_maze(prob)
