# Benjamin Cape
# 21F
# COSC 76: AI
# 11.1.21

from __future__ import annotations
from enum import Enum
from typing import Iterable, List, Tuple
from markov_model import Location, State
from maze import Maze


class Color(Enum):
    '''
    Color of each square
    '''
    Red = 0
    Green = 1
    Yellow = 2
    Blue = 3

    def sense(reading: Color, true_color: Color):
        '''
        Used to define the sensor model.
        '''
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
    '''
    Run a maze hidden markov model with different options
    '''
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def run(self, readings: Iterable[Color]):
        state = Maze.initial_state(self.maze)
        self.maze.print(state)

        # Loop over all readings
        for reading in readings:

            # use the State transition, passing in the corrent maze, the reading, and the sensor model
            state = state.transition(self.maze, reading, Color.sense)
            self.maze.print(state)

    def viterbi(self, readings: Iterable[Color]):
        '''
        In addition to finding most likely end-state, also find potential path
        '''
        state = Maze.initial_state(self.maze)
        self.maze.print(state)

        states: List[State] = []
        for reading in readings:
            # use the State transition, passing in the corrent maze, the reading, and the sensor model
            state = state.transition(self.maze, reading, Color.sense)
            states.append(state)

        ## Build best path from best final state recursively back from that state

        i = len(states) - 1
        end = states[i]
        end_location: Tuple[int, Location] = (0, None)
        for loc, exp in end.expectations.items():
            if end_location[0] < exp:
                end_location = (exp, loc)
        end_loc = end_location[1]

        path = [end_loc]
        while i > 0:
            i -= 1
            state = states[i]
            prev: Tuple[int, Location] = (0, None)
            for neighbor in filter(self.maze.is_valid_location,
                                   path[-1].neighbors()):

                if state.expectations[neighbor] > prev[0]:
                    prev = (state.expectations[neighbor], neighbor)
            path.append(prev[1])

        path.reverse()

        for i, loc in enumerate(path):
            self.maze.print(states[i], loc)
