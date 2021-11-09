# [PA-6] Hidden Markov Model - Benjamin Cape

# Description

> How do your implemented algorithms work? What design decisions did you make? How you laid out the problems? In particular, for this specific assignment, explain your model precisely, and explain exactly how you compute each new distribution of possible states.

- How do your <a id="implementation"></a>implemented algorithms work?

My algorithm(Problem), takes a maze and a list of observations to determine where we are on the grid. It loops over each observation(reading) and updates the state based on that observation. We first create a new state, with empty expectations, and the current reading. We use the reading to print out the next process nicely in the console. We then loop over each location, find all of it's neighbors, and sum the probabilities of all the neighbors into the current location - this accounts for the **conjunction over the possible moves from all the neighbors**. The next step is to consider the **disjunction over the sensor reading**, this is accomplished by multiplying the transition model by the sensor model for each location given the proper reading correctness. The final step is **normalizing** all the probabilities such that we retain constant 100% likelihood for all outcomes.

- What design decisions did you make?

I decided to take, once again, and object oriented approach to split out functionality into respective entities. The `markov_model.py` files is generic, over any board with data at each location. The `maze.py` file contains all the maze related specific functionality, and the `main.py` file specifies the specific problem with the colors. I chose this to make it as generic as possible. I considered splitting the `markov_chain` even to allow for any generic markov chain, rather than board specific, but didn't seem necessary.

- How did you lay out the problems?

See above.

- In particular, for this specific assignment, explain your model precisely, and explain how you compute each new distribution of possible states.

The model is a hashmap of expectations for locations on a board. Each location is given a probability (expectation) that the robot is in that location. Therefore, updating probabilities is very fast and efficient, and clear. We can update probabilities in O(n) time by looping over each location. See [Implementation](#implementation) for information on how we compute the new distribution of possible states.

# Evaluation

> Do your implemented algorithms actually work? How well? If it doesn’t work, can you tell why not? What partial successes did you have that deserve partial credit? Include a comparison of running time results using different heuristics and inference.

- Do your implemented algorithms actually work? How well?

Yes, in fact they seem to work very well. After running a various randomly generated mazes, the robot is generally very good at localizing itself.

- What partial successes did you have that deserve partial credit?

I believe that I deserve full credit.

- Include a comparison of running time results using different heuristics and inference.

There are no heuristics for this assignment, nor is there any inference. But here is an evaluation of state determination based on some randomly generated maps:

```
-------- State (Read: None) ---------
        0               1              2               3               4
4:      🔵0.05          🔵0.05          🟡0.05          #               🔴0.05
3:      🔴0.05          🔵0.05          🟢0.05          🟡0.05          🔵0.05
2:      🔵0.05          #               #               🔵0.05          🔵0.05
1:      🔴0.05          🟢0.05          🟡0.05          🟢0.05          🔵0.05
0:      #               🔴0.05          #               🔵0.05          🟡0.05
-------- State (Read: 🟢) ---------
        0               1               2               3               4
4:      🔵0.007         🔵0.011         🟡0.007         #               🔴0.004
3:      🔴0.011         🔵0.011         🟢0.241         🟡0.011         🔵0.011
2:      🔵0.007         #               #               🔵0.011         🔵0.011
1:      🔴0.007         🟢0.241         🟡0.007         🟢0.321         🔵0.011
0:      #               🔴0.004         #               🔵0.007         🟡0.007
-------- State (Read: 🔴) ---------
        0               1               2               3               4
4:      🔵0.001         🔵0.002         🟡0.016         #               🔴0.029
3:      🔴0.034         🔵0.017         🟢0.002         🟡0.017         🔵0.002
2:      🔵0.002         #               #               🔵0.022         🔵0.002
1:      🔴0.344         🟢0.002         🟡0.036         🟢0.002         🔵0.021
0:      #               🔴0.349         #               🔵0.021         🟡0.001
-------- State (Read: 🔵) ---------
        0               1               2               3               4
4:      🔵0.041         🔵0.039         🟡0.002         #               🔴0.002
3:      🔴0.001         🔵0.063         🟢0.003         🟡0.003         🔵0.055
2:      🔵0.45          #               #               🔵0.043         🔵0.05
1:      🔴0.001         🟢0.039         🟡0.001         🟢0.005         🔵0.006
0:      #               🔴0.001         #               🔵0.005         🟡0.002
```

This one shows very well that with a proper path from (1,1) -> (1,0) -> (2,0) that is G, R, B and no other such path, we are placed INCREDIBLY likely at location (2,0) and very unlikely at the remaining locations of the board.

# Discussion

1. What is the state transition model?

The state transition model is adding up all of the neighboring state's probabilities, because we assume uniform provability that the robot moves in any direction, so summing up is essentially saying, we were either in neighbor 1, 2 3 or 4 (max being 4 for 4 neighbors).

2. What is the sensor model?

The sensor model is multiplying the retrieved probability from summing the neighboring state probabilities with the probability that our reading was correct given the actual color of the square. I.e. if we just read a RED, and the square we are on is in fact red, then we multiply by 0.88, whereas for all other colors we would multiply by 0.04

3. How do you implement the filtering algorithm, given that there are several possible values for the state variable (the state variable is not boolean).

The filtering algorithm is simply keeping track of the previous state, and rather than re-computing everything on each transition, using the previous state to calculate the new state. That is described above, but simply put we create a new board, fill in initial probabilities given the transition model, and then update those probabilities with the sensor model.

# Extra Credit

I implemented a viterbi algorithm that backtracks from the final state to find the best path.

This is visible with the following output from a random generated path and map. The `⭐` indicates where the robot thinks it is.

```
-------- State (Read: None) ---------
        0               1               2               3               4
4:      🔴0.05          🔵0.05          🔵0.05          🟢0.05          🟡0.05
3:      #               #               #               🔵0.05          🔴0.05
2:      #               🔴0.05          🟡0.05          🔴0.05          🔴0.05
1:      🟡0.05          🟡0.05          🟢0.05          🔵0.05          #
0:      🔴0.05          🟡0.05          🟡0.05          🔴0.05          🔵0.05
-------- State (Read: 🟢) ---------
        0               1               2               3               4
4:      🔴0.014         🔵0.014         🔵0.014         ⭐🟢0.314        🟡0.014
3:      #               #               #               🔵0.014         🔴0.014
2:      #               🔴0.014         🟡0.014         🔴0.014         🔴0.014
1:      🟡0.014         🟡0.014         🟢0.314         🔵0.014         #
0:      🔴0.014         🟡0.014         🟡0.014         🔴0.014         🔵0.014
-------- State (Read: 🟢) ---------
        0               1               2               3               4
4:      🔴0.003         🔵0.003         🔵0.02          🟢0.438         🟡0.02
3:      #               #               #               ⭐🔵0.02        🔴0.003
2:      #               🔴0.003         🟡0.02          🔴0.003         🔴0.003
1:      🟡0.003         🟡0.02          🟢0.07          🔵0.02          #
0:      🔴0.003         🟡0.003         🟡0.02          🔴0.003         🔵0.003
-------- State (Read: 🔴) ---------
        0               1               2               3               4
4:      🔴0.026         🔵0.003         🔵0.045         🟢0.046         🟡0.045
3:      #               #               #               🔵0.043         🔴0.095
2:      #               🔴0.095         🟡0.009         ⭐🔴0.129       🔴0.026
1:      🟡0.003         🟡0.007         🟢0.007         🔵0.009         #
0:      🔴0.026         🟡0.004         🟡0.009         🔴0.095         🔵0.001
-------- State (Read: 🟡) ---------
        0               1               2               3               4
4:      🔴0.003         🔵0.003         🔵0.006         🟢0.007         🟡0.209
3:      #               #               #               🔵0.013         🔴0.009
2:      #               🔴0.008         ⭐🟡0.217       🔴0.004         🔴0.011
1:      🟡0.035         🟡0.099         🟢0.001         🔵0.01          #
0:      🔴0.002         🟡0.042         🟡0.105         🔴0.005         🔵0.004
-------- State (Read: 🟢) ---------
        0               1               2               3               4
4:      🔴0.001         🔵0.001         🔵0.001         🟢0.277         🟡0.023
3:      #               #               #              🔵0.002         🔴0.013
2:      #               🔴0.018         🟡0.012         🔴0.013         🔴0.002
1:      🟡0.009         🟡0.005         ⭐🟢0.507       🔵0.001         #
0:      🔴0.004         🟡0.013         🟡0.008         🔴0.007         🔵0.001
```
