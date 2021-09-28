# CS76 21F - PA-2 Mazeworld [Benjamin Cape]

## Discussion Questions:

1. If there are k robots, how would you represent the state of the system? Hint -- how many numbers are needed to exactly reconstruct the locations of all the robots, if we somehow forgot where all of the robots were? Further hint. Do you need to know anything else to determine exactly what actions are available from this state?

Well, first we will need to know which robot's turn it is to move. This will take one value in the state. We can store each robots location in one value, but that is simply storing 2 log(n)-bit values in a log(n^2)-bit value.

> Not sure how we could recover a robots location with we don't store all of them.

2. Give an upper bound on the number of states in the system, in terms of n and k.

Lets add another value, say we have $n$x$n$ maze, with $k$ robots, and with $r$ barriers. Therefore, we have $n^2 - r$ valid squares for a robot to be on.

$O((n^2-r)*(k+1)) = O(k * (n^2-r))$

This is because each valid square can have $k+1$ different things on it, either one of the $k$ robots, or an empty state

If we don't consider the walls here, we get:

$$O(k*n^2)$$

3. Give a rough estimate on how many of these states represent collisions if the number of wall squares is w, and n is much larger than k.

If we consider $w$ walls, then $O(w * k)$ of those are collisions with the walls.

> Not sure what you mean by n much larger than k

4. If there are not many walls, n is large (say 100x100), and several robots (say 10), do you expect a straightforward breadth-first search on the state space to be computationally feasible for all start and goal pairs? Why or why not?

No, a breadth first search would not be feasible, because it is likely that our solution state is very very far from our start state. We assume that the branching factor for each state is $O(5*k)$, and the depth could be as much as 200, that means our memory/time complexity is $O((5k)^{200})$, that's a huge number. This is incredibly unfeasible. Say we use the metrics from the question, we have time roughly $6.2 x 10^{339}$, that's more calculations clock-cycles then there are possible chess boards.

5. Describe a useful, monotonic heuristic function for this search space. Show that your heuristic is monotonic. See the textbook for a formal definition of monotonic.

A good heuristic function, $h(x)$ for this search space would the be the sum of all the maximum manhattan distances from each robot to a goal state.

For this to be monotonic, we must show:

$$
\forall x,y \text{ s.t. } x \rightarrow_a y; h(x) \leq c(x,a,y) + h(y)
$$

> _Proof_
>
> Fix a robot, r, and consider two states $x$, $y$ where we can reach $y$ by perform the action $a$ on $x$. The first scenario is that $a = NA$, meaning the cost is $0$, in this case $h(x) = h(y)$, satisfying the condition. (We only have to worry about one robot moving, because only one robot can move at each state)
>
> In the other scenarios, $c(x,a,y) = 1$. It is very easy to show though that the move to $y$ can only increase the manhattan distance by at most $2$ (by extending the shorted path manhattan distance from $x$).
>
> $$h(x) \leq c(x,a,y) + h(y) = 1 + h(y) \leq 1 + h(x) + 2 = h(x) + 3$$
> Making the inequality hold.

6. Describe why the 8-puzzle in the book is a special case of this problem. Is the heuristic function you chose a good one for the 8-puzzle?

The 8-puzzle problem is simple the maze problem when $k = n-1$ The heuristic I chose is exactly the heuristic is commonly used for the 8-puzzle.

7. The state space of the 8-puzzle is made of two disjoint sets. Describe how you would modify your program to prove this. (You do not have to implement this.)

> TODO

## Implement and Test

- Implementation is done.

- Random Graphs done

- Need to write tests
