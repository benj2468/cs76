from __future__ import annotations
from enum import Enum
from typing import List
from copy import copy, deepcopy
from itertools import product


class Location(Enum):
    LEFT = 1
    RIGHT = -1


class Action():
    def __init__(self, chickens: int, foxes: int, dest: Location) -> None:
        self.chickens = chickens
        self.foxes = foxes
        self.dest = dest

    def __repr__(self) -> str:
        return f"Action: c:{self.chickens}, f:{self.foxes}, dest:{self.dest}"


class FoxProblem():
    def __init__(self, chickens: int, foxes: int, boat: Location) -> None:
        self.chickens = chickens
        self.foxes = foxes
        self.boat = boat
        self.start_state = self

    def goal_test(self) -> bool:
        return self.chickens == self.foxes == 0 and self.boat == Location.RIGHT

    def get_actions(self) -> List[Action]:
        legal_actions = []
        (max_c, max_f) = (self.start_state.chickens, self.start_state.foxes)
        max_chickens = self.chickens if self.boat == Location.LEFT else max_c - self.chickens
        max_foxes = self.foxes if self.boat == Location.LEFT else max_f - self.foxes
        for (i, j) in product(range(0, min(3, max_chickens + 1)),
                              range(0, min(3, max_foxes + 1))):
            if (i + j > 2) or (i + j < 1):
                continue

            action = Action(i, j, Location(-self.boat.value))

            # Creates a legal next-states
            next = self.transition(action)
            if ((next.chickens >= next.foxes) or next.chickens == 0) and \
            ((max_c - next.chickens) >= (max_f - next.foxes) or next.chickens == max_c):
                legal_actions.append(action)

        return legal_actions

    def get_successors(self) -> List[FoxProblem]:
        states = []
        for action in self.get_actions():
            states.append(self.transition(action))
        return states

    def transition(self, action: Action) -> FoxProblem:
        next = deepcopy(self)
        next.chickens += action.dest.value * action.chickens
        next.foxes += action.dest.value * action.foxes
        next.boat = action.dest
        next.start_state = deepcopy(self.start_state)

        return next

    def __eq__(self, o: FoxProblem) -> bool:
        return self.boat == o.boat and self.chickens == o.chickens and self.foxes == o.foxes

    def __repr__(self) -> str:
        return f"State: c:{self.chickens}, f:{self.foxes}, loc:{self.boat}"

    def __hash__(self) -> int:
        return ((self.chickens * 3) + self.foxes) * self.boat.value