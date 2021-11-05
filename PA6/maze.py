# Benjamin Cape
# 21F
# COSC 76: AI
# 11.1.21

from __future__ import annotations
from typing import Any, Mapping, Set, Tuple
from random import sample

from markov_model import *


class Maze(Board):
    def __init__(self, size: Tuple[int, int], walls: Set[Location],
                 data: Mapping[Location, Any]) -> None:

        self.walls = walls

        super().__init__(size[0], size[1], data)

    def initial_state(maze: Maze) -> State:
        open_locations = (maze.width * maze.height) - len(maze.walls)
        expectations = defaultdict(None)
        for i in range(maze.width):
            for j in range(maze.height):
                if Location(i, j) in maze.walls:
                    expectation = 0
                else:
                    expectation = 1.0 / open_locations
                expectations[Location(i, j)] = expectation
        return State(expectations)

    def is_valid_location(self, loc: Location) -> bool:
        return super().is_valid_location(loc) and not loc in self.walls

    def print(self, state: State, expected_loc: Location = None):
        lines = []
        for i in range(self.width):
            line = f'{i}:\t'
            for j in range(self.height):
                loc = Location(i, j)

                if loc in self.walls:
                    line += "#\t\t"
                else:
                    if expected_loc and expected_loc == loc:
                        line += '⭐'
                    line += str(self.location_data[loc]) + str(
                        state.expectations[loc].__round__(3)) + '\t\t'
            lines.append(line)
        header = '\t\t'.join(map(str, list(range(0, self.width))))
        lines.append(f"\t{header}")
        lines.reverse()

        print(f"-------- State (Read: {state.reading}) ---------")
        print('\n'.join(lines))

    def __str__(self) -> str:
        lines = []
        for i in range(self.width):
            line = f'{i}:\t'
            for j in range(self.height):
                if Location(i, j) in self.walls:
                    line += "# "
                else:
                    line += str(self.location_data[Location(i, j)]) + ' '
            lines.append(line)
        lines.append(f"\t{' '.join(map(str, list(range(0, self.width))))}")
        lines.reverse()

        return '\n'.join(lines)

    def random(w, h, walls, data_domain) -> Maze:
        colors = {}
        for i in range(w):
            for j in range(h):
                loc = Location(i, j)
                color = sample(data_domain, 1)[0]
                colors[loc] = color

        walls = sample(list(colors), walls) if walls > 0 else []

        return Maze((w, h), walls, colors)