# CS76 21F - PA-3 Chess [Benjamin Cape]

## Description

### How do your implemented algorithms work? What design decisions did you make?

My implemented algorithms work exactly as the psuedocode is provided in the textbook/from the slides.

I implemented alpha beta pruning minimax with the same game structure as a normal minimax. So, any game that you write that can be passed into an alpha-beta pruning search, can also be used in a regular minimax search. I found this particularly helpful when testing the speed of alpha-beta with respect to normal minimax.

The iterative deepening algorithm is also interesting, in that it takes a time value as a toggle, and deepens as long as the previous search took less than the required time.

The only other algorithm that I introduced which is of substance is the evaluation function. Which I will talk about in the discussion question.

## Evaluation

### Do your implemented algorithms actually work? How well? If it doesn’t work, can you tell why not? What partial successes did you have that deserve partial credit?

Yes, my algorithms for search work very well. The alpha beta pruning performs very well as compared to the regular minimax, allowing us to search much deeper into the search tree.

## Discussion

1. (minimax and cutoff test) Vary maximum depth to get a feeling of the speed of the algorithm. Also, have the program print the number of calls it made to minimax as well as the maximum depth. Record your observations in your document.

```
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R
----------------
a b c d e f g h

White to move

Minimax visited 422 nodes, with depth: 2, in 11.893ms
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . N
P P P P P P P P
R N B Q K B . R
----------------
a b c d e f g h

Black to move

Minimax visited 207805 nodes, with depth: 4, in 526.411ms
```

It is clear that the deeper the depth, the more nodes we visit. Also, clearly observable by the time here, it takes MUCH longer if our depth is higher. This is because our branching factor is VERY high, so each added depth increases our search results exponentially.

2. (evaluation function) Describe the evaluation function used and vary the allowed depth, and discuss in your document the results.

My evaluation function is simple. It assigns a score to each piece:

```
scores = {
    chess.PAWN: 1,
    chess.ROOK: 5,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.QUEEN: 9,
}
```

There also is a maximum score: 8 + 2 \* (5 + 3 + 3) + 9 = 39

Then, a linear sum of the frequency of each root color, and the score for the piece, minus the same value for the not root color pieces followed by normalization over the maximum possible score provides us a number $[-1,1]$ that indicates a score for a particular individual.

If the root wins, they get a score of 1, if they lose, they get a score of -1.

From the start state, even with a deep depth-limit (5):

```
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R
----------------
a b c d e f g h


Minimax visited 5072214 nodes, with depth: 5, in 893.37ms, best move value: 1.0
```

We know this makes sense, because there IS a way to keep all of your pieces with $5$ moves in a game of chess.

3. (alpha-beta) Record your observations on move-reordering in your document.

With Ordering:

```
Alice: A/B Pruning Visited: 1604 nodes, with depth: 4, in 453.011ms, best move value: 0.02564102564102564
Alice: A/B Pruning-with move-reordering Visited: 1578 nodes, with depth: 4, in 104.193ms, best move value: 0.02564102564102564
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . N
P P P P P P P P
R N B Q K B . R
----------------
a b c d e f g h

Black to move

Random AI recommending move g7g5
r n b q k b n r
p p p p p p . p
. . . . . . . .
. . . . . . p .
. . . . . . . .
. . . . . . . N
P P P P P P P P
R N B Q K B . R
----------------
a b c d e f g h

White to move

Alice: A/B Pruning Visited: 4128 nodes, with depth: 4, in 854.096ms, best move value: 0.02564102564102564
Alice: A/B Pruning-with move-reordering Visited: 3435 nodes, with depth: 4, in 310.701ms, best move value: 0.02564102564102564
r n b q k b n r
p p p p p p . p
. . . . . . . .
. . . . . . N .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B . R
----------------
a b c d e f g h

Black to move

Random AI recommending move d7d5
r n b q k b n r
p p p . p p . p
. . . . . . . .
. . . p . . N .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B . R
----------------
a b c d e f g h

White to move

Alice: A/B Pruning Visited: 5902 nodes, with depth: 4, in 235.327ms, best move value: 0.05128205128205128
Alice: A/B Pruning-with move-reordering Visited: 3619 nodes, with depth: 4, in 631.857ms, best move value: 0.05128205128205128
r n b q k b n r
p p p . p p . p
. . . . . . . .
. . . p . . . .
. . . . . . . .
. . . . . N . .
P P P P P P P P
R N B Q K B . R
----------------
a b c d e f g h

Black to move

Random AI recommending move a7a5
r n b q k b n r
. p p . p p . p
. . . . . . . .
p . . p . . . .
. . . . . . . .
. . . . . N . .
P P P P P P P P
R N B Q K B . R
----------------
a b c d e f g h

White to move

Alice: A/B Pruning Visited: 7879 nodes, with depth: 4, in 621.131ms, best move value: 0.05128205128205128
Alice: A/B Pruning-with move-reordering Visited: 5736 nodes, with depth: 4, in 423.603ms, best move value: 0.05128205128205128
r n b q k b n r
. p p . p p . p
. . . . . . . .
p . . p . . . .
. . . . . . . .
. . . . . N . .
P P P P P P P P
R N B Q K B R .
----------------
a b c d e f g h

Black to move

Random AI recommending move b7b5
r n b q k b n r
. . p . p p . p
. . . . . . . .
p p . p . . . .
. . . . . . . .
. . . . . N . .
P P P P P P P P
R N B Q K B R .
----------------
a b c d e f g h
```

We see that performing move-reordering saves us some moves, and in fact also saves us some time! When we re-order we are able to prune sooner, and therefore visit fewer nodes, but ultimately get the same expected outcome.

4. (iterative deepening) Verify that for some start states, best_move changes (and hopefully improves) as deeper levels are searched. Discuss the observations in your document.

I made it such that iterative deepening takes a time as a parameter. It will search for search for at most that amount of time (actually a bit more, but after it takes this much time it won't start another deepening). We also stop if we ever reach a score of 1.

For the chess starting state, an alpha-beta pruner can get the following 2 different result:

```
Alpha Beta Pruning Visited: 17528 nodes, with depth: 5, in 510.486ms, best move value: 0.02564102564102564
----
Alpha Beta Pruning Visited: 1516 nodes, with depth: 4, in 56.544ms, best move value: 0.0
```

By searching one depth further, we get a slightly better outcome. Strange though, if we search one depth further, to 6, we get a negative payout. I think this makes sense though, since with a depth of 5, there is always a way for the opponent to capture at least one of your pieces.

```
White to move

Iterative Deepening time=2 AI Depth = 1 discovered best move: 0.5897435897435898, visited = 20
Iterative Deepening time=29 AI Depth = 2 discovered best move: 0.5897435897435898, visited = 97
Iterative Deepening time=98 AI Depth = 3 discovered best move: 0.5897435897435898, visited = 735
Iterative Deepening time=504 AI Depth = 4 discovered best move: 0.6153846153846154, visited = 2578
. . . . . k . r
. . . . p . p p
. . . . . n . .
. . . p . p . .
. . . . . . . .
. . N . . . . .
P P P P P P P P
R . B Q K B . R
----------------
a b c d e f g h
```

Here is an example of where searching another depth gives us a better score, might be the same move, but at least we are surer of it.

```
White to move

Iterative Deepening time=3 AI Depth = 1 discovered best move: 0.5897435897435898, visited = 31
Iterative Deepening time=86 AI Depth = 2 discovered best move: 0.6153846153846154, visited = 199
Iterative Deepening time=197 AI Depth = 3 discovered best move: 0.5897435897435898, visited = 1511
Iterative Deepening time=229 AI Depth = 4 discovered best move: 0.6153846153846154, visited = 7801
Iterative Deepening time=831 AI Depth = 5 discovered best move: 0.6153846153846154, visited = 46579
```

Here is an example of it fluctuation. This is possible because it might look like a great move in the short-run, but on the next turn we lose a piece. But maybe that's OK because we take an opponents piece after that. Remember that all of these scores are estimates based on pieces on the board, they are not true values for winning/losing.

## Extra Credit

For extra credit I have implemented the rock-paper-scissors checkers game created by Professor Bjoern. In order to accomplish this, I have implemented multi-agent maximization as well.

I have also implemented a transposition table. This works by hashing a state, and the depth at which we search for it. So if we want to search for the same depth again we can just use to lookup table.

```
Alice: A/B Pruning Visited: 507 nodes, with depth: 3, in 51.165ms, best move value: 0.8717948717948718
Alice: A/B Pruning without table Visited: 581 nodes, with depth: 3, in 61.191ms, best move value: 0.8717948717948718
. . . . . k . .
. . . . . . . .
p . . . . . p N
P . p . . . . .
P p . . . . . p
. . . . . . . .
. . P P P P P P
R N B Q K B . R
----------------
a b c d e f g h

Black to move

Random AI recommending move f8e8
. . . . k . . .
. . . . . . . .
p . . . . . p N
P . p . . . . .
P p . . . . . p
. . . . . . . .
. . P P P P P P
R N B Q K B . R
----------------
a b c d e f g h

White to move

Alice: A/B Pruning Visited: 0 nodes, with depth: 3, in 0.08ms, best move value: 0.8717948717948718
Alice: A/B Pruning without table Visited: 778 nodes, with depth: 3, in 83.021ms, best move value: 0.8974358974358975
. . . . k . . .
. . . . . . . .
p . . . . . p N
P . p . . . . .
P p . . . . . p
. . . . P . . .
. . P P . P P P
R N B Q K B . R
----------------
a b c d e f g h
```

For some moves of the RandomAI, ones that lead us to perform very similar moves, or moves we have already done we can see the difference in time and nodes visited with the table and without the table. We don't count nodes as visited if we can simply look them up in the table.
