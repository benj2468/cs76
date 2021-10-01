from Maze import Maze
from SensorlessProblem import SensorlessProblem

from astar_search import astar_search


def null_heuristic(state):
    return 0


def test_maze(prob: SensorlessProblem):
    # This will just locate the robot, so this is expected to get a path that is no larger than the manhattan, but it will also be slower becuase it doesn't have a direction
    other = astar_search(prob, prob.options_heuristic)
    print(other)
    other = astar_search(prob, prob.distance_hue)
    print(other)
    # prob.animate_path(other.path)


test_maze3 = Maze("maze3.maz")
test_maze3.robotloc = test_maze3.robotloc[0:1]
sensorless = SensorlessProblem(test_maze3)
test_maze(sensorless)

# You can comment this out if it's not working, sometimes you get a bad graph and you have to restart.
for i in range(5):
    maze = Maze(None, 15, 15, robots=1)
    print(maze)
    prob = SensorlessProblem(maze)
    test_maze(prob)
