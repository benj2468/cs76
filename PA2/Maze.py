# Benjamin Cape - 21F - CS76
# PA2
# 10.02.10
#
# Partially provided, iterated and added random generation,
# Changed to store locations as 2-tuples rather than a single list

from __future__ import annotations
from typing import List, Set, Tuple
from random import randrange, sample
from itertools import product


class Maze:
    def __init__(self, mazefilename=None, *args, **kwargs):

        self.robotloc: List[Tuple[int, int]] = []

        if not mazefilename:
            self.rand(*args, **kwargs)
            return
        # read the maze file into a list of strings
        f = open(mazefilename)
        lines = []

        for line in f:
            line = line.strip()
            # ignore blank limes
            if len(line) == 0:
                pass
            elif line[0] == "\\":
                # there's only one command, \robot, so assume it is that
                parms = line.split()
                x = int(parms[1])
                y = int(parms[2])
                self.robotloc.append((x, y))
            else:
                lines.append(line)

        f.close()
        self.width = len(lines[0])
        self.height = len(lines)

        self.map = list("".join(lines))

    def index(self, x, y):
        return (self.height - y - 1) * self.width + x

    def robots(self):
        return len(self.robotloc)

    # returns True if the location is a floor
    def is_floor(self, x, y):
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False

        return self.map[self.index(x, y)] == "."

    def has_robot(self, x, y):
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False

        for i in range(0, len(self.robotloc)):
            rx, ry = self.robotloc[i]
            if rx == x and ry == y:
                return True

        return False

    # function called only by __str__ that takes the map and the
    #  robot state, and generates a list of characters in order
    #  that they will need to be printed out in.
    def create_render_list(self):
        renderlist = list(self.map)

        for robot_number, (x, y) in enumerate(self.robotloc):
            renderlist[self.index(x, y)] = robotchar(robot_number)

        return renderlist

    def __str__(self):

        # render robot locations into the map
        renderlist = self.create_render_list()

        # use the renderlist to construct a string, by
        #  adding newlines appropriately
        s = ""
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                s += renderlist[self.index(x, y)]

            s += "\n"

        return s

    def with_goals(self, goals: List[Tuple[int, int]]) -> str:
        # render robot locations into the map
        renderlist = self.create_render_list()

        # use the renderlist to construct a string, by
        #  adding newlines appropriately

        s = ""
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                if (x, y) in goals and (not (x, y) in self.robotloc):
                    s += str(goals.index((x, y)))
                else:
                    s += renderlist[self.index(x, y)]

            s += "\n"

        return s

    def with_potential_robots(self, potential_robots: Set[Tuple[int,
                                                                int]]) -> str:
        # render robot locations into the map
        renderlist = self.create_render_list()

        # use the renderlist to construct a string, by
        #  adding newlines appropriately

        s = ""
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                if (x, y) in potential_robots:
                    s += "X"
                else:
                    s += renderlist[self.index(x, y)]

            s += "\n"

        return s

    # I added this
    def rand(self, max_width: int, max_height: int, robots=None) -> Maze:
        width = randrange(5, max_width)
        height = randrange(5, max_height)
        robots = robots if robots else randrange(1, 4)

        walls = set()

        def is_occupied(x, y) -> bool:
            loc = (x, y)
            return loc in walls or loc in self.robotloc

        for _ in range(robots):
            loc = (randrange(0, width - 1), randrange(0, height - 1))
            while is_occupied(*loc):
                loc = (randrange(0, width - 1), randrange(0, height - 1))

            self.robotloc.append(loc)

        for _ in range(
                randrange(width, max(width + 1, int(width * height / 5)))):
            loc = (randrange(0, width), randrange(0, height))
            while is_occupied(*loc):
                loc = (randrange(0, width), randrange(0, height))

            walls.add(loc)

        self.width = width
        self.height = height

        lines = []
        for i in range(height):
            line = ""
            for j in range(width):
                loc = (j, height - i - 1)
                if loc in walls:
                    line += "#"
                else:
                    line += "."
            lines += line

        self.map = list("".join(lines))

    def rand_goals(self) -> List[Tuple[int, int]]:
        free_spaces = filter(
            lambda loc: (self.is_floor(*loc) and not loc in self.robotloc),
            product(range(0, self.width), range(0, self.height)))
        return sample(list(free_spaces), self.robots())


def robotchar(robot_number):
    return chr(ord("A") + robot_number)


# Some test code

if __name__ == "__main__":
    test_maze1 = Maze("./maze1.maz")
    print(test_maze1)

    test_maze2 = Maze("maze2.maz")
    print(test_maze2)

    test_maze3 = Maze("maze3.maz")
    print(test_maze3)

    print(test_maze3)
    print(test_maze3.robotloc)

    print(test_maze3.is_floor(2, 3))
    print(test_maze3.is_floor(-1, 3))
    print(test_maze3.is_floor(1, 0))

    print(test_maze3.has_robot(1, 0))
