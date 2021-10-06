from typing import List


class TreeNode:
    def __init__(self, children=[], val=None) -> None:
        self.children = children
        self.val = val
        if self.val != None:
            self.expected_val = val
        else:
            self.expected_val = 0
            for child in self.children:
                self.expected_val += child.expected_val / len(self.children)


a = TreeNode([TreeNode(val=3), TreeNode(val=12), TreeNode(val=8)])
b = TreeNode([TreeNode(val=2), TreeNode(val=4), TreeNode(val=6)])
c = TreeNode([TreeNode(val=14), TreeNode(val=5), TreeNode(val=2)])
root = TreeNode([a, b, c])

TreeActions = ['LEFT', 'RIGHT']

## Example from SA3

h = TreeNode([TreeNode(val=-2), TreeNode(val=4)])
i = TreeNode([TreeNode(val=6), TreeNode(val=-8)])
l = TreeNode([TreeNode(val=-3), TreeNode(val=-1)])
m = TreeNode([TreeNode(val=7), TreeNode(val=-5)])

d = TreeNode([h, i])
c = TreeNode([l, m])

b = TreeNode([d, c])

n = TreeNode([TreeNode(val=2), TreeNode(val=-4)])
o = TreeNode([TreeNode(val=-6), TreeNode(val=8)])
p = TreeNode([TreeNode(val=3), TreeNode(val=1)])
q = TreeNode([TreeNode(val=-7), TreeNode(val=5)])

f = TreeNode([n, o])
g = TreeNode([p, q])

c = TreeNode([f, g])

a = TreeNode([b, c])


class TestGame:
    def __init__(self, depth) -> None:
        self.alpha = float('-inf')
        self.beta = float('inf')
        self.calls = []
        self.terminals_reached = []
        self.depth = depth

    def call(self, state):
        self.calls.append(state)

    def actions(self, state):
        for i in range(len(state.children)):
            yield i

    def result(self, state, action):
        return state.children[action]

    def utility(self, state):
        return state.expected_val

    def cut_off(self, state, depth):
        return depth >= self.depth or state.val != None

    def clean(self, *args):
        pass


# Testing Codes
from AlphaBetaAI import ab_minimax_search
from MinimaxAI import minimax_search

game = TestGame(depth=100)
value, move = ab_minimax_search(game, a)
print(f"Results from alpha-beta minimax: {value}, {move}")
for state in game.calls:
    print(state.val)


def tester(depth1, depth2):
    game = TestGame(depth=depth1)
    value, move = ab_minimax_search(game, root)
    print(f"Results from alpha-beta minimax: {value}, {move}")

    game2 = TestGame(depth=depth2)
    value2, move2 = minimax_search(game2, root)
    print(f"Results from minimax: {value2}, {move2}")

    if depth1 == depth2:
        assert (value == value2)
        assert (len(game.calls) <= len(game2.calls))

    assert (move == move2)


tester(1, 1)
tester(2, 2)
tester(2, 3)
tester(5, 1)
