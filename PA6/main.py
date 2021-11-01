# Benjamin Cape
# 21F
# COSC 76: AI
# 11.1.21

from __future__ import annotations
from enum import Enum
from typing import Iterable
from maze import Maze


class Color(Enum):
    Red = 0
    Green = 1
    Yellow = 2
    Blue = 3

    def sense(reading: Color, true_color: Color):
        return 0.88 if reading.value == true_color.value else 0.04

    def __str__(self) -> str:
        if self == Color.Red:
            return '🔴'
        elif self == Color.Green:
            return '🟢'
        elif self == Color.Yellow:
            return '🟡'
        else:
            return '🔵'


class Problem:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def run(self, readings: Iterable[Color]):
        state = Maze.initial_state(self.maze)
        self.maze.print(state)
        for reading in readings:
            state = state.transition(self.maze, reading, Color.sense)
            self.maze.print(state)