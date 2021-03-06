# Benjamin Cape
# CS76 - AI - 21F
# 9.21.21

import unittest
from LossyFoxProblem import FoxProblem, Action, Location


class FoxProblemTest(unittest.TestCase):
    init_state = FoxProblem(3, 3, Location(1), 2)

    def test_init_state(self):
        self.assertEqual(self.init_state.chickens, 3)
        self.assertEqual(self.init_state.foxes, 3)
        self.assertEqual(self.init_state.boat, Location.LEFT)

    def test_valid_states_start(self):
        valid_states = [
            FoxProblem(3, 2, Location.RIGHT, 2),
            FoxProblem(3, 1, Location.RIGHT, 2),
            FoxProblem(0, 3, Location.RIGHT, 0),
            FoxProblem(2, 2, Location.RIGHT, 2),
            FoxProblem(0, 3, Location.RIGHT, 1),
        ]
        self.assertListEqual(self.init_state.get_successors(), valid_states)

    def test_valid_states(self):
        current_state = FoxProblem(2, 2, Location.RIGHT, 2)
        current_state.start_state = FoxProblem(3, 3, Location.LEFT, 2)
        valid_states = [
            FoxProblem(0, 3, Location.LEFT, 0),
            FoxProblem(3, 2, Location.LEFT, 2),
            FoxProblem(3, 3, Location.LEFT, 2),
        ]

        self.assertEqual(current_state.get_successors(), valid_states)

    def test_valid_states2(self):
        current_state = FoxProblem(3, 2, Location.RIGHT, 2)
        current_state.start_state = FoxProblem(3, 3, Location.LEFT, 2)
        valid_states = [
            FoxProblem(3, 3, Location.LEFT, 2),
        ]

        self.assertEqual(current_state.get_successors(), valid_states)

    def test_transition(self):
        action = Action(1, 2, Location.RIGHT)
        self.assertEqual(self.init_state.transition(action),
                         FoxProblem(2, 1, Location.RIGHT))

    def test_goal_test(self):
        goal = FoxProblem(0, 0, Location.RIGHT)
        self.assertTrue(goal.goal_test())

        self.assertFalse(self.init_state.goal_test())


if __name__ == '__main__':
    unittest.main()