from collections import deque
from SearchSolution import SearchSolution
from copy import copy, deepcopy


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
        current = to_visit.pop()
        solution.nodes_visited += 1
        for next in current.state.get_successors():
            next = SearchNode(next, current)
            if next.state.goal_test():
                solution.nodes_visited += 1
                return backtracking(solution, next)
            elif not next.state in visited:
                to_visit.append(next)
            visited.add(next.state)
        visited.add(current.state)

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
        sub_solution = dfs_search(search_problem, depth_limit - 1,
                                  SearchNode(next), deepcopy(solution))
        if len(sub_solution.path) > 0:
            return sub_solution
        else:
            solution.nodes_visited = sub_solution.nodes_visited
    # If none of the neighbors found viable paths, then we neglect all we've done and go back
    solution.path = []
    return solution


def ids_search(search_problem, depth_limit=100) -> SearchSolution:
    solution = SearchSolution(search_problem, "IDS")
    for i in range(0, depth_limit):
        sol = dfs_search(search_problem, i, None, deepcopy(solution))
        if len(sol.path) > 0:
            return sol
        else:
            solution.nodes_visited = sol.nodes_visited

    return solution
