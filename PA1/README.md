# CS76 21F - PA-1 Chicken and Foxes [Benjamin Cape]

## Description

My algorithms work relatively simply. BFS follows standard BFS protocol. Using a queue to add nodes in the FIFO order, so that we search breadth before depth. In order to make sure that we do not go in loops, i.e. make the same move again and re-check it, I keep a set of visited nodes. While this might appear to double our space, our space is still linear with the possible number of nodes in the graph (i.e. the states) therefore this does not increase our asymptotic space bound.

For DFS we make some small alterations to the standard DFS. First, we use path-processing, making our DFS recursive. This means that as we traverse down one path, we do keep in memory the data stores on other paths, or the data that will be apart of future paths. The recursive nature makes sure of this, since each recursive step only knows about the path that had lead to it. The next thing we've added is depth-throttling. This means, we only traverse down a certain depth, and cut short if we reach that depth. This allows for iterative DFS. If we reach out depth-limit, and we have not yet found our goal, then we report a failure (i.e. path is empty). In the recursive step we follow DFS standard protocol, iterating through neighbors, if a neighbor is already in our path we ignore it (since we don't want to waste time/go into an infinite loop) and recursively calling DFS on each neighbor with a limit of one less than the current step. With the result from the recursive call, we check if the solution was valid (i.e. the path is not empty) if valid, we return it, otherwise we update our visited notes (since we did visit each node in the sub-part) and we continue onto the next neighbor. At the end, if we've made it through all the neighbors and have no valid path, then we set out path to empty, and we return our solution.

IDS search is incredibly simple, iterating over the range and calling DFS with the depth limit $i$. If we succeed, then we terminate, if non of the iterative calls succeed then we return our empty solution with all the visited nodes from the each call (since we do visit nodes multiple times)

## Evaluation

Yes, my implemented algorithms work. And I like to believe that they work particularly well. In my BFS I've added a bit of space to make the runtime faster. In DFS, since our path is a list, searching that list to see if we've already visited a node takes some time, making that an inefficiency of the algorithm. Otherwise, my solutions are strong. the BFS and the IDS always find paths of the same length, which is expected because they are optimal, and my DFS gets a sub-optimal solution though not much less strong.

## Discussions

1. States are either legal, or not legal. First, give an upper bound on the number of states, without considering legality of states. (Hint -- 331 is one state. 231 another, although illegal. Keep counting.) Describe how you got this number.

There are three options for how to represent chickens, $1,2,3$, similartly three options for how to represent foxes $1,2,3$, and two ways to represent the location of the boat `LEFT`, `RIGHT` thus we have a total of $3 * 3 * 2 = 18$ states.

[PDF](<./PC1 Graphic.pdf>) representation of the first state, it's actions, following states, and all those states actions

2. Does path-checking depth-first search save significant memory with respect to breadth-first search? Draw an example of a graph where path-checking DFS takes much more run-time than breadth-first search; include in your report and discuss.

Path-checking Depth First search does save significant memory with respect to BFS. This is because with PC-DFS, at any given point we only have $O(m)$ space in memory, $m$ being the length of the maximum path in the graph. Rather, with BFS, would could have to store the entire graph in memory, as we expand an entire level (depth) before we move onto the next level.

[PDF](<./PC1 DISC 2.pdf>) illustrates a graph where DFS takes much more run-time than BFS. This graph is small, so the order is insignificant, but in general, a graph that has the goal node close to the top, but not necessarily the first to get expanded by DFS would take much longer. A thought to solve this problem is, rather than using lexicographical order, randomizing the order ot he neighbors that you expand.

3. Does memoizing DFS save significant memory with respect to breadth-first search? Why or why not? As a reminder, there are two styles of depth-first search on a graph. One style, memoizing keeps track of all states that have been visited in some sort of data structure, and makes sure the DFS never visits the same state twice.

It does not, because BFS does this already. In order for BFS to work, we need to keep track of all the nodes that we have already seen, either in a backtracking data-structure, such as `SearchNode` or in some set, such as `visited` (I use both for speed of querying, and to use SearchNode).

4. [Iterative Deepening Search] On a graph, would it make sense to use path-checking DFS, or would you prefer memoizing DFS in your iterative deepening search? Consider both time and memory aspects. (Hint. If it's not better than BFS, just use BFS.)

It makes more sense to use memoizing DFS, or BFS with depth-limiting. Why? Well if we use PC-DFS, then each time we increment our depth, since we don't keep track of everything we've seen, only the current path, we'd need to re-check everything again. Rather, if we use memoizing DFS then we don't need to re-check everything that we've already seen.

Using Memoizing DFS with IDS is essentially the same as BFS, since in iteration 0 we check everything at distance 0 from the start (just the start), then in iteration 1 we check all at distance 1. Then at iteration 2 we check all at distance 2 etc. This is the same as BFS, so it's much simpler to use BFS. And this makes sense. You use IDS when you suspect that your goal is close to the root, so as to net get bogged down by DFS's deep-depth-first component. This is the same reason to use BFS.

## Tests

See [FoxProblem_test](./FoxProblem_test.py) to see tests on my Fox game state/action implementation.

See [search_test](./search_test.py) for tests on the search problems.
