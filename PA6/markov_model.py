# Benjamin Cape
# 21F
# COSC 76: AI
# 11.1.21

from __future__ import annotations
from collections import defaultdict
from types import FunctionType
from typing import Any, Iterator, Mapping, Set, Tuple


class Location:
    '''
    Describe a location by type
    '''
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y

    def __hash__(self) -> int:
        return (self.x, self.y).__hash__()

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def neighbors(self) -> Iterator[Location]:
        '''
        Find all the neighbors of a location
        '''
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            yield Location(self.x + dx, self.y + dy)


class Board(object):
    '''
    Generic class for a board with data at each location
    '''
    def __init__(self,
                 width: int,
                 height: int,
                 location_data: Mapping[Location, Any] = {}) -> None:
        self.width = width
        self.height = height

        self.location_data = location_data

    def is_valid_location(self, loc: Location) -> bool:
        return 0 <= loc.x < self.width and 0 <= loc.y < self.height


Expectation = Mapping[Location, float]


class State:
    def __init__(self, expectations: Expectation, reading: Any = None) -> None:
        self.expectations = expectations
        self.reading = reading

    def __iter__(self):
        for loc in self.expectations:
            yield loc

    def normalize(self):
        tot = 0
        for loc in self:
            tot += self.expectations[loc]
        for loc in self:
            self.expectations[loc] = self.expectations[loc] / tot

    def transition(prev, board: Board, reading: Any,
                   sensor_model: FunctionType) -> State:
        next = State({}, reading)
        for loc in prev.expectations:
            transition = 0
            for neighbor in loc.neighbors():
                if board.is_valid_location(neighbor):
                    transition += 0.25 * prev.expectations[neighbor]
                else:
                    transition += 0.25 * prev.expectations[loc]
            next.expectations[loc] = transition
        for loc in next.expectations:
            next.expectations[loc] *= sensor_model(reading,
                                                   board.location_data[loc])
        next.normalize()
        return next
