# PA-4 [21F] [Benjamin Cape] [CSP]

## Running the Code

```
python3 ./circut.py
python3 ./coloring.py
```

This will run tests with and without inference, as well as with and without heuristic. There are puzzles on both tests that should fail, and they successfully do so.

## Extending

To extend the code for a new CSP, simply create a new file: `./<FILE_NAME>.py` and create a new subclass of BinaryCSP. Attempting to run `backtrack_search()` on your newly created object will fail unless you have implemented the `is_consistent()` function, and if you want a full test suit, make sure you implement the `print(assignment)` function as well.

Type hints should help making sure that you get everything right.
