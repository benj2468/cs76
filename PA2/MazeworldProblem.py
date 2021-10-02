# Benjamin Cape - 21F - CS76
# PA2
# 10.02.10

from __future__ import annotations
from copy import deepcopy
from Maze import Maze
from time import sleep
from enum import Enum
from itertools import zip_longest
from typing import Generator, List, Tuple


class Move(Enum):
    North = (0, 1)
    South = (0, -1)
    East = (1, 0)
    West = (-1, 0)
    NA = (0, 0)


class Action:
    def __init__(self, move: Move) -> None:
        self.move = move

    def cost(self) -> int:
        return 0 if self.move == Move.NA else 1

    def __str__(self) -> str:
        return f"{self.move}"


ALL_MOVES: List[Move] = [Move.North, Move.South, Move.East, Move.West, Move.NA]


class State:
    def __init__(self, robot: int, robot_locs: List[Tuple[int, int]]) -> None:
        self.robot = robot
        self.robot_locs = robot_locs

    def hashed(self):
        return (self.robot, f"{self.robot_locs}").__hash__()

    def __str__(self) -> str:
        return f"Turn: {self.robot}, locations: {self.robot_locs}"


class MazeworldProblem:
    def __init__(self, maze: Maze, goal_locations: List[Tuple[int, int]]):
        self.maze = maze
        self.goal_locations = goal_locations
        self.start_state = State(0, self.maze.robotloc)

        def manhattan_heuristic(state: State) -> int:
            s = 0
            for ((x, y), (gx, gy)) in zip_longest(state.robot_locs,
                                                  self.goal_locations):
                s += abs(gx - x) + abs(gy - y)
            return s

        self.manhattan_heuristic = manhattan_heuristic

    def transition(self, state: State, action: Action) -> MazeworldProblem:
        next = deepcopy(state)
        dx, dy = action.move.value
        x, y = state.robot_locs[state.robot]
        next.robot_locs[state.robot] = (x + dx, y + dy)

        next.robot = (state.robot + 1) % len(state.robot_locs)

        return next

    def goal_test(self, state: State) -> bool:
        for (rob, goal) in zip_longest(state.robot_locs, self.goal_locations):
            if rob != goal:
                return False
        return True

    def get_successors(
            self, state: State) -> Generator[Tuple[int, MazeworldProblem]]:
        for action in self.legal_actions(state):
            yield (action.cost(), self.transition(state, action))

    def legal_actions(self, state: State) -> Generator[Action]:
        x, y = state.robot_locs[state.robot]

        def is_legal(action: Action) -> bool:
            dx, dy = action.move.value
            nx, ny = x + dx, y + dy
            return ((not (nx, ny) in state.robot_locs)
                    and self.maze.is_floor(nx, ny)) or action.move == Move.NA

        for move in ALL_MOVES:
            action = Action(move)
            if is_legal(action):
                yield action

    def __str__(self):
        return f"Mazeworld problem: \n{self.maze.with_goals(self.goal_locations)}"

    def hashed(self) -> int:
        return f"Mazeworld problem: \n{self.maze}".__hash__()

    # given a sequence of states (including robot turn), modify the maze and print it out.
    #  (Be careful, this does modify the maze!)
    def animate_path(self, path: List[State]):
        # reset the robot locations in the maze
        maze = self.maze

        for state in path:
            maze.robotloc = state.robot_locs
            s = f"Turn: {state.robot}\n{self.maze.with_goals(self.goal_locations)}"
            print(s)
            sleep(1.0)


if __name__ == "__main__":
    test_maze2 = Maze("maze2.maz")
    test_mp = MazeworldProblem(test_maze2, ((1, 4), (1, 3), (1, 2)))
