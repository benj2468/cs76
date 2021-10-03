# Benjamin Cape - 21F - CS76
# PA2
# 10.02.10

from SearchSolution import SearchSolution
from heapq import heappush, heappop
from collections import deque
from copy import copy


class AstarNode:
    def __init__(self, state, heuristic, parent=None, tot_cost=0):
        self.state = state
        self.parent = parent

        self.expected_cost = tot_cost + heuristic
        self.removed = False

    def priority(self):
        return self.expected_cost

    def remove(self):
        self.removed = True

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


class PriorityQueue:
    def __init__(self) -> None:
        self.queue = []
        self.visited = {}

    def add_visited(self, node: AstarNode, cost: int):
        self.visited[node.state.hashed()] = (cost, node)

    def get_visited(self, node: AstarNode):
        return self.visited[node.state.hashed()][0]

    def insert(self, value, cost):
        state = value.state.hashed()
        if not state in self.visited:
            self.add_visited(value, cost)
            heappush(self.queue, value)
        elif self.visited[state][0] > cost:
            self.visited[state][1].remove()
            self.add_visited(value, cost)
            heappush(self.queue, value)

    def pop(self):
        res = heappop(self.queue)
        while res.removed:
            res = heappop(self.queue)
        return res

    def is_empty(self):
        return len(self.queue) == 0


def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result


def astar_search(search_problem, heuristic_fn):
    start_node = AstarNode(search_problem.start_state,
                           heuristic_fn(search_problem.start_state))
    frontier = PriorityQueue()

    solution = SearchSolution(search_problem,
                              "Astar with heuristic " + heuristic_fn.__name__)

    frontier.insert(start_node, 0)

    while not frontier.is_empty():
        current = frontier.pop()

        solution.nodes_visited += 1
        if search_problem.goal_test(current.state):
            solution.path = backchain(current)
            solution.cost = frontier.get_visited(current)
            return solution

        for (cost, neighbor) in search_problem.get_successors(current.state):
            tot_cost = frontier.get_visited(current) + cost
            next = AstarNode(neighbor, heuristic_fn(neighbor), current,
                             tot_cost)

            frontier.insert(next, tot_cost)

    solution.cost = float("inf")
    return solution
