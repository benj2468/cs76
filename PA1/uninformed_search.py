# Benjamin Cape
# CS76 - AI - 21F
# 9.21.21

from collections import deque
from SearchSolution import SearchSolution
from copy import copy


# you might find a SearchNode class useful to wrap state objects,
#  keep track of current depth for the dfs, and point to parent nodes
class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, parent=None):
        self.parent = parent
        self.state = state


# you might write other helper functions, too. For example,
#  I like to separate out backchaining, and the dfs path checking functions


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

    # This does not add space, because we already store them all within the SearchNode
    # This simply stores the same data in a different place for faster querying, making storage O(2*n) = O(n)
    visited = set()

    while len(to_visit) > 0:
        # Pop left removes things that were added before, since append adds to the right
        current = to_visit.popleft()
        visited.add(current.state)
        solution.nodes_visited += 1

        # Visit all successors
        for next in current.state.get_successors():
            next = SearchNode(next, current)
            solution.nodes_visited += 1

            if next.state.goal_test():

                return backtracking(solution, next)
            elif not next.state in visited:
                # Only add the next state if we haven't already seen it.
                to_visit.append(next)

            visited.add(next.state)

    return solution


# Don't forget that your dfs function should be recursive and do path checking,
#  rather than memoizing (no visited set!) to be memory efficient


# We pass the solution along to each new recursive call to dfs_search
#  so that statistics like number of nodes visited or recursion depth
#  might be recorded
def dfs_search(search_problem,
               depth_limit=100,
               node=None,
               solution=None) -> SearchSolution:
    # if no node object given, create a new search from starting state
    if node == None:
        node = SearchNode(search_problem.start_state)

    if solution == None:
        solution = SearchSolution(search_problem, "DFS")

    # Case for all recursion - add the current state to the path.
    solution.visit(node.state)

    # Base case
    if node.state.goal_test():
        return solution

    # Cut Algorithm short if we reach the depth-limit
    if depth_limit == 0:
        solution.path = []
        return solution

    # Recursive step
    # -------------
    # Loop over each possible next state
    for next in node.state.get_successors():
        # Capture the recurvie solution, which is either a solution, or None
        if next in solution.path:
            continue
        # If it is not None, then we have a solution, and we bubble-up this path without checking the others
        path = copy(solution.path)
        dfs_search(search_problem, depth_limit - 1, SearchNode(next), solution)
        if len(solution.path) > 0:
            return solution
        else:
            solution.path = path
    # If none of the neighbors found viable paths, then we neglect all we've done and go back
    solution.path = []
    return solution


def ids_search(search_problem, depth_limit=100) -> SearchSolution:
    solution = SearchSolution(search_problem, "IDS")
    # Look over all our depths
    for i in range(0, depth_limit):
        dfs_search(search_problem, i, None, solution)
        # If we find a valid solution, terminate by returning
        if len(solution.path) > 0:
            return solution

    return solution
