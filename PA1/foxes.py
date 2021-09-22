from FoxProblem import FoxProblem, Location
from uninformed_search import bfs_search, dfs_search, ids_search
from datetime import datetime

# Create a few test problems:
problem331 = FoxProblem(3, 3, Location(1))
problem541 = FoxProblem(5, 4, Location(1))
problem551 = FoxProblem(5, 5, Location(1))

# Run the searches.
#  Each of the search algorithms should return a SearchSolution object,
#  even if the goal was not found. If goal not found, len() of the path
#  in the solution object should be 0.


def stat(method, problem):
    start_time = datetime.now()
    res = method(problem)
    duration = datetime.now() - start_time
    print(res)
    print(f"Time Taken: {duration.microseconds} ms")


stat(dfs_search, problem331)
stat(bfs_search, problem331)
stat(ids_search, problem331)

stat(dfs_search, problem541)
stat(bfs_search, problem541)
stat(ids_search, problem541)

stat(dfs_search, problem551)
stat(bfs_search, problem551)
stat(ids_search, problem551)
