from SearchSolution import SearchSolution
from heapq import heappush, heappop
from collections import deque
from copy import copy


class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self,
                 state,
                 heuristic,
                 parent=None,
                 transition_cost=0,
                 sync=False):
        self.state = state
        self.parent = parent

        self.heuristic = heuristic
        self.transition_cost = transition_cost

        self.expected_cost = heuristic
        cur = self
        while cur != None:
            # Extension, add cost for length of the path as well...
            if sync:
                self.expected_cost += 1
            self.expected_cost += cur.transition_cost
            cur = cur.parent

    def priority(self):
        return self.expected_cost

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


class PriorityQueue:
    def __init__(self) -> None:
        self.queue = []

    def insert(self, value):
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


def astar_search(search_problem, heuristic_fn, sync=False):
    start_node = AstarNode(search_problem.start_state,
                           heuristic_fn(search_problem.start_state),
                           sync=sync)
    frontier = PriorityQueue()
    frontier.insert(start_node)

    solution = SearchSolution(search_problem,
                              "Astar with heuristic " + heuristic_fn.__name__)

    visited_cost = {}

    def add_visited(node: AstarNode, cost: int):
        visited_cost[node.state.hashed()] = cost

    def check_visited(node: AstarNode, cost: int):
        neighbor = node.state.hashed()
        return (not neighbor in visited_cost) or (
            neighbor in visited_cost and visited_cost[neighbor] > cost)

    def get_visited(node: AstarNode):
        return visited_cost[node.state.hashed()]

    add_visited(start_node, 0)

    while not frontier.is_empty():
        current = frontier.pop()
        solution.nodes_visited += 1

        if current.state.goal_test():
            solution.path = backchain(current)
            solution.cost = get_visited(current)
            return solution

        for (cost, neighbor) in current.state.get_successors():
            tot_cost = get_visited(current) + cost
            next = AstarNode(neighbor,
                             heuristic_fn(neighbor),
                             current,
                             cost,
                             sync=sync)

            if check_visited(next, tot_cost):
                add_visited(next, tot_cost)
                frontier.insert(next)

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
