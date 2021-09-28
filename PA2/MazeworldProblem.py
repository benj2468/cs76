from __future__ import annotations
from copy import deepcopy
from Maze import Maze, robotchar
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


class MazeworldProblem:

    ## you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze: Maze, goal_locations: List[Tuple[int, int]]):
        self.maze = maze
        self.goal_locations = goal_locations
        self.robot = 0
        self.start_state = self

        def manhattan_heuristic(state: MazeworldProblem) -> int:
            s = 0
            for ((x, y), (gx, gy)) in zip_longest(state.maze.robotloc,
                                                  self.goal_locations):
                s += abs(gx - x) + abs(gy - y)
            return s

        self.manhattan_heuristic = manhattan_heuristic

    def transition(self, action: Action) -> MazeworldProblem:
        next = deepcopy(self)
        dx, dy = action.move.value
        x, y = next.maze.robotloc[self.robot]
        next.maze.robotloc[self.robot] = (x + dx, y + dy)

        next.robot = (next.robot + 1) % next.maze.robots()

        return next

    def goal_test(self) -> bool:
        for (rob, goal) in zip_longest(self.maze.robotloc,
                                       self.goal_locations):
            if rob != goal:
                return False
        return True

    def get_successors(self) -> Generator[Tuple[int, MazeworldProblem]]:
        for action in self.legal_actions():
            yield (action.cost(), self.transition(action))

    def legal_actions(self) -> Generator[Action]:
        x, y = self.maze.robotloc[self.robot]

        def is_legal(action: Action) -> bool:
            dx, dy = action.move.value
            nx, ny = x + dx, y + dy
            return nx >= 0 and ny >= 0 and nx < self.maze.width and ny < self.maze.height and (
                not self.maze.is_occupied(nx, ny) or action.move == Move.NA)

        for move in ALL_MOVES:
            action = Action(move)
            if is_legal(action):
                yield action

    def __str__(self):
        return f"Mazeworld problem: \nTurn: {robotchar(self.robot)}\n{self.maze.with_goals(self.goal_locations)}"

    def hashed(self) -> int:
        return f"Mazeworld problem: \nTurn: {robotchar(self.robot)}\n{self.maze}".__hash__(
        )

    # given a sequence of states (including robot turn), modify the maze and print it out.
    #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state.maze.robotloc)

        for state in path:
            print(str(state))
            sleep(0.5)


## A bit of test code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze2 = Maze("maze2.maz")
    test_mp = MazeworldProblem(test_maze2, ((1, 4), (1, 3), (1, 2)))
