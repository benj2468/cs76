# Benjamin Cape
# 21F
# COSC 76: AI
# 11.1.21

import unittest
from markov_model import *
from maze import *


class MarkovModelTest(unittest.TestCase):
    def test_location_neighbors(self):
        self.assertListEqual(
            [Location(4, 6),
             Location(5, 5),
             Location(4, 4),
             Location(3, 5)], list(Location(4, 5).neighbors()))

    def test_board_valid(self):
        b = Board(6, 5, {})
        for i in range(6):
            for j in range(5):
                loc = Location(i, j)
                self.assertTrue(b.is_valid_location(loc))

    def test_board_invalid(self):
        b = Board(6, 5)

        loc = Location(10, 4)
        self.assertFalse(b.is_valid_location(loc))

        loc = Location(-1, 4)
        self.assertFalse(b.is_valid_location(loc))

        loc = Location(2, -1)
        self.assertFalse(b.is_valid_location(loc))

        loc = Location(0, 10)
        self.assertFalse(b.is_valid_location(loc))

    def test_normalize(self):
        state = State({
            tuple(Location(0, 0)): 0.5,
            tuple(Location(0, 1)): 0.5,
            tuple(Location(1, 0)): 0.5
        })
        state.normalize()

        for i in state.expectations.values():
            self.assertEqual(round(i, 2), 0.33)

    def test_transition(self):
        b = Board(
            2, 2, {
                tuple(Location(0, 0)): True,
                tuple(Location(0, 1)): True,
                tuple(Location(1, 0)): False,
                tuple(Location(1, 1)): False,
            })
        state = State({
            tuple(Location(0, 0)): 0.5,
            tuple(Location(0, 1)): 0.5,
            tuple(Location(1, 0)): 0.5,
            tuple(Location(1, 1)): 0.5
        })
        state.normalize()

        sensor_model = lambda x, y: 0.9 if x == y else 0.1

        new = state.transition(b, True, sensor_model)
        self.assertEqual(new.expectations[tuple(Location(0, 0))], 0.45)
        self.assertEqual(new.expectations[tuple(Location(0, 1))], 0.45)
        self.assertEqual(new.expectations[tuple(Location(1, 0))], 0.05)
        self.assertEqual(new.expectations[tuple(Location(1, 1))], 0.05)

        new = new.transition(b, False, sensor_model)
        self.assertEqual(new.expectations[tuple(Location(0, 0))], 0.05)
        self.assertEqual(new.expectations[tuple(Location(0, 1))], 0.05)
        self.assertEqual(new.expectations[tuple(Location(1, 0))], 0.45)
        self.assertEqual(new.expectations[tuple(Location(1, 1))], 0.45)


class MazeTest(unittest.TestCase):
    def test_walls_expectation(self):
        maze = Maze((5, 4), [tuple(Location(1, 1))], {})
        state = maze.initial_state()

        self.assertEqual(state.expectations[tuple(Location(1, 1))], 0)

    def test_non_walls_expectation(self):
        maze = Maze((5, 4), [tuple(Location(1, 1))], {})
        state = maze.initial_state()

        for i in range(5):
            for j in range(4):
                if i == 1 and j == 1:
                    continue
                self.assertNotEqual(state.expectations[tuple(Location(i, j))],
                                    0)


if __name__ == '__main__':
    unittest.main()