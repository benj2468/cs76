# Benjamin Cape
# CS76 - AI - 21F
# 9.21.21

import unittest
from FoxProblem import Location
from uninformed_search import bfs_search, dfs_search
from FoxProblem import FoxProblem


class SearchTest(unittest.TestCase):
    init_state = FoxProblem(3, 3, Location(1))

    def test_bfs(self):
        solution = bfs_search(self.init_state)
        self.assertEqual(solution.nodes_visited, 14)
        self.assertEqual(len(solution.path), 12)

    def test_dfs(self):
        solution = dfs_search(self.init_state)
        self.assertEqual(solution.nodes_visited, 13)
        self.assertEqual(len(solution.path), 12)


if __name__ == '__main__':
    unittest.main()