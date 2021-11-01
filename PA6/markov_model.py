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

    def __iter__(self):
        yield self.x
        yield self.y

    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y

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


Expectation = Mapping[Tuple[int, int], float]


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
        next = State(defaultdict(lambda: 0), reading)
        for loc in prev.expectations:
            neighbors = list(
                filter(board.is_valid_location,
                       Location(*loc).neighbors()))
            for neighbor in neighbors:
                next.expectations[tuple(neighbor)] += (prev.expectations[loc] /
                                                       len(neighbors))
        for loc in next.expectations:
            next.expectations[loc] *= sensor_model(reading,
                                                   board.location_data[loc])
        next.normalize()
        return next