# Benjamin Cape - 21F - CS76
# PA2
# 10.02.10
from __future__ import annotations
from copy import copy, deepcopy
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

    def op(self) -> Move:
        if self.move == Move.North:
            return Move.South
        if self.move == Move.South:
            return Move.North
        if self.move == Move.East:
            return Move.West
        if self.move == Move.West:
            return Move.East
        return Move.NA


ALL_MOVES: List[Move] = [Move.North, Move.South, Move.East, Move.West, Move.NA]


class State:
    def __init__(self, robot_locs: List[Tuple[int, int]]) -> None:
        self.robot_locs = robot_locs

    def hashed(self):
        return f"{self.robot_locs}".__hash__()

    def __str__(self) -> str:
        return f"{self.robot_locs}"


class MazeworldProblem:
    def __init__(self, maze: Maze, goal_locations: List[Tuple[int, int]]):
        self.maze = maze
        self.goal_locations = goal_locations
        self.start_state = State(self.maze.robotloc)

        def manhattan_heuristic(state: State) -> int:
            s = 0
            for ((x, y), (gx, gy)) in zip_longest(state.robot_locs,
                                                  self.goal_locations):
                s += abs(gx - x) + abs(gy - y)
            return s

        self.manhattan_heuristic = manhattan_heuristic

    def transition(self, state: State,
                   actions: List[Action]) -> MazeworldProblem:
        next = deepcopy(state)
        for (i, action) in enumerate(actions):
            dx, dy = action.move.value
            x, y = state.robot_locs[i]
            next.robot_locs[i] = (x + dx, y + dy)

        return next

    def goal_test(self, state: State) -> bool:
        for (rob, goal) in zip_longest(state.robot_locs, self.goal_locations):
            if rob != goal:
                return False
        return True

    def get_successors(
            self, state: State) -> Generator[Tuple[int, MazeworldProblem]]:
        for action in self.legal_actions(state):
            cost = sum(map(lambda x: x.cost(), action))
            yield (cost, self.transition(state, action))

    def legal_actions(self, state: State) -> List[List[Action]]:

        legal_moves = []

        def is_legal(action: Action, rob_loc: Tuple[int, int],
                     past_moves: List[Action]) -> bool:
            dx, dy = action.move.value
            x, y = rob_loc
            nx, ny = x + dx, y + dy

            def has_overlap():
                for i, move in enumerate(past_moves):
                    dx, dy = move.move.value
                    o_x, o_y = state.robot_locs[i]
                    robot_next = (o_x + dx, o_y + dy)
                    if (nx, ny) == robot_next or (
                        (nx, ny) == (o_x, o_y) and move.move == (action.op())):
                        return True
                return False

            return not has_overlap() and self.maze.is_floor(nx, ny)

        def recurse(past_actions: List[Action], robot: int):
            if robot == len(state.robot_locs):
                legal_moves.append(past_actions)
                return
            for move in ALL_MOVES:
                action = Action(move)
                if is_legal(action, state.robot_locs[robot], past_actions):
                    actions = copy(past_actions)
                    actions.append(action)
                    recurse(actions, robot + 1)

        recurse([], 0)

        return legal_moves

    def __str__(self):
        return f"Mazeworld problem: \n{self.maze.with_goals(self.goal_locations)}"

    def hashed(self) -> int:
        return f"Mazeworld problem: \n{self.maze}".__hash__()

    def animate_path(self, path: List[State]):
        maze = self.maze

        for state in path:
            maze.robotloc = state.robot_locs
            s = f"{self.maze.with_goals(self.goal_locations)}"
            print(s)
            sleep(1.0)


if __name__ == "__main__":
    test_maze2 = Maze("maze2.maz")
    test_mp = MazeworldProblem(test_maze2, ((1, 4), (1, 3), (1, 2)))
