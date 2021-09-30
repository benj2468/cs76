from SearchSolution import SearchSolution
from heapq import heappush, heappop
from collections import deque
from copy import copy


class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, tot_cost=0):
        self.state = state
        self.parent = parent

        self.expected_cost = tot_cost + heuristic
        self.marked = False

    def priority(self):
        return self.expected_cost

    def mark(self):
        self.marked = True

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


class PriorityQueue:
    def __init__(self) -> None:
        self.queue = []
        self.visited = {}

    def add_visited(self, node: AstarNode, cost: int):
        self.visited[node.state.hashed()] = cost

    def check_visited(self, node: AstarNode, cost: int):
        neighbor = node.state.hashed()
        return (not neighbor in self.visited) or (
            neighbor in self.visited and self.visited[neighbor] > cost)

    def get_visited(self, node: AstarNode):
        return self.visited[node.state.hashed()]

    def insert(self, value, cost):
        if self.check_visited(value, cost):
            self.add_visited(value, cost)
            heappush(self.queue, value)

    def pop(self):
        return heappop(self.queue)

    def is_empty(self):
        return len(self.queue) == 0


# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
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


# OLD CODE
class SearchNode:
    def __init__(self, state, parent=None):
        self.parent = parent
        self.state = state


def backtracking(solution, search_node: SearchNode) -> SearchSolution:
    '''Bubble up from a search_node until parent is None (i.e. start node) and add all to the path of the solution'''
    while search_node.parent:
        solution.path.append(search_node.state)
        search_node = search_node.parent
    solution.path.append(search_node.state)
    return solution


def bfs_search(search_problem, node=None) -> SearchSolution:
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "BFS")
    to_visit = deque()
    to_visit.append(node)

    visited = set()
    visited.add(node.state)

    while len(to_visit) > 0:
        current = to_visit.popleft()
        solution.nodes_visited += 1

        for (_, next) in current.state.get_successors():
            next = SearchNode(next, current)

            if next.state.goal_test():
                return backtracking(solution, next)
            elif not next.state in visited:
                to_visit.append(next)

            visited.add(next.state)

    return solution
