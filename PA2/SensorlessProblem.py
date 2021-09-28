from __future__ import annotations
from copy import deepcopy

from Maze import Maze
from time import sleep
from typing import Generator, List, Tuple
from itertools import product
from enum import Enum


class Action(Enum):
    North = (0, 1)
    South = (0, -1)
    East = (1, 0)
    West = (-1, 0)


ALL_ACTIONS = [Action.North, Action.South, Action.East, Action.West]


class SensorlessProblem:

    ## You write the good stuff here:

    def __init__(self, maze: Maze, goal: Tuple[int, int]):
        self.maze = maze
        self.goal = goal

        self.options = set()
        for loc in product(range(self.maze.width), range(self.maze.height)):
            if self.maze.is_floor(*loc):
                self.options.add(loc)

        self.start_state = self
        self.previous_mode = None

        def manhattan_heuristic(state: SensorlessProblem) -> int:
            s = 0
            gx, gy = state.goal
            for x, y in state.options:
                s += abs(gx - x) + abs(gy - y)
            return s

        self.manhattan_heuristic = manhattan_heuristic

    def goal_test(self):
        return len(self.options) == 1

    def transition(self, action: Action) -> SensorlessProblem:
        next = deepcopy(self)
        new_options = set()
        dx, dy = action.value

        for x, y in self.options:
            new = (x + dx, y + dy)
            new_options.add(new if self.maze.is_floor(*new) else (x, y))

        next.options = new_options
        next.previous_mode = action
        return next

    def get_successors(self) -> Generator[Tuple[int, SensorlessProblem]]:
        for action in ALL_ACTIONS:
            yield (0, self.transition(action))

    def __str__(self):
        return f"Blind robot problem: \nMove:{self.previous_mode} \n{self.maze.with_potential_robots(self.options)}"

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def hashed(self):
        return f"{self.maze}{self.options}".__hash__()

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state.maze.robotloc)

        for state in path:
            print(str(state))
            sleep(1.0)


## A bit of test code

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_problem = SensorlessProblem(test_maze3)
