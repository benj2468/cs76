from __future__ import annotations
from copy import deepcopy

from Maze import Maze
from time import sleep
from typing import Generator, List, Set, Tuple
from itertools import product
from enum import Enum


class Action(Enum):
    North = (0, 1)
    South = (0, -1)
    East = (1, 0)
    West = (-1, 0)


ALL_ACTIONS = [Action.North, Action.South, Action.East, Action.West]


class State:
    def __init__(self,
                 options: Set[Tuple[int, int]],
                 previous_move=None) -> None:
        self.previous_move = previous_move
        self.options = options

    def hashed(self):
        return f"{self.options}".__hash__()


class SensorlessProblem:

    ## You write the good stuff here:

    def __init__(self, maze: Maze, goal: Tuple[int, int]):
        self.maze = maze
        self.goal = goal

        options = set()
        for loc in product(range(self.maze.width), range(self.maze.height)):
            if self.maze.is_floor(*loc):
                options.add(loc)

        self.start_state = State(options)

        def manhattan_heuristic(state: State) -> int:
            s = 0
            gx, gy = self.goal
            for x, y in state.options:
                s += abs(gx - x) + abs(gy - y)
            return s

        self.manhattan_heuristic = manhattan_heuristic

    def goal_test(self, state: State):
        return len(state.options) == 1

    def transition(self, state: State, action: Action) -> SensorlessProblem:
        next = deepcopy(state)
        new_options = set()
        dx, dy = action.value

        for x, y in state.options:
            new = (x + dx, y + dy)
            new_options.add(new if self.maze.is_floor(*new) else (x, y))

        next.options = new_options
        next.previous_move = action
        return next

    def get_successors(
            self, state: State) -> Generator[Tuple[int, SensorlessProblem]]:
        for action in ALL_ACTIONS:
            yield (1, self.transition(state, action))

    def __str__(self):
        return f"Blind robot problem: \n{self.maze}"

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path: List[State]):
        # reset the robot locations in the maze

        for state in path:
            s = f"Move: {state.previous_move} \n{self.maze.with_potential_robots(state.options)}"
            print(s)
            sleep(1.0)


## A bit of test code

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_problem = SensorlessProblem(test_maze3)
