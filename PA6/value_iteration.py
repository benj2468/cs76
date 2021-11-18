from __future__ import annotations
from collections import defaultdict
from typing import List, Tuple


class Node():
    def __init__(self, label: str, reward: int):
        self.label = label
        self.reward = reward
        self.actions = defaultdict(lambda: [])

    def add_action(self, ty: int, action: Action):
        self.actions[ty].append(action)


class Action():
    def __init__(self,
                 prob: float,
                 destination: Node,
                 reward: int = None) -> None:
        self.prob = prob
        self.dest = destination
        self.reward = reward if reward != None else self.dest.reward


def value_iteration_pre(nodes: List[Node], discount: float, iters: int):
    table = [[0] * len(nodes)]
    for i in range(iters):
        prev = table[-1]
        new = []
        for node in nodes:
            m = float('-inf')
            for a in node.actions:
                s = node.reward
                for prob_action in node.actions[a]:
                    v_prev = prev[nodes.index(prob_action.dest)]
                    s += prob_action.prob * (discount * v_prev)
                m = max(m, s)
            new.append(m)
        table.append(new)
    return table


def value_iteration_post(nodes: List[Node], discount: float, iters: int):
    table = [[(0, None)] * len(nodes)]
    for i in range(iters):
        prev = table[-1]
        new = []
        for node in nodes:
            m = (float('-inf'), None)
            for a in node.actions:
                s = 0
                for prob_action in node.actions[a]:
                    v_prev = prev[nodes.index(prob_action.dest)]
                    s += prob_action.prob * (prob_action.dest.reward +
                                             discount * v_prev[0])
                if s > m[0]:
                    m = (s, a)
            new.append(m)
        table.append(new)
    return table


def q_learning(alpha: float, gamma: float,
               observations: List[Tuple[int, int, int, int]]):
    table = defaultdict(lambda: defaultdict(lambda: 0))
    for (s, a, s2, r) in observations:
        m = float('-inf')
        for u in table[s2]:
            m = max(m, table[s2][u])
        if m == float('-inf'):
            m = 0
        table[s][a] = (1 - alpha) * (table[s][a]) + alpha * (r + gamma * (m))
    return table


Ok = Node('OK', 2)
Danger = Node('Danger', -1)
Caught = Node('Caught', -5)

Ok.add_action(0, Action(0.5, Ok))
Ok.add_action(0, Action(0.5, Danger))
Ok.add_action(1, Action(.2, Caught))
Ok.add_action(1, Action(.8, Ok))

Danger.add_action(0, Action(0.4, Ok))
Danger.add_action(0, Action(0.3, Danger))
Danger.add_action(0, Action(0.3, Caught))
Danger.add_action(1, Action(.25, Ok))
Danger.add_action(1, Action(.2, Danger))
Danger.add_action(1, Action(.55, Caught))

Caught.add_action(0, Action(.3, Caught))
Caught.add_action(0, Action(.7, Danger))
Caught.add_action(1, Action(.3, Ok))
Caught.add_action(1, Action(.7, Caught))

for i in range(100):
    print(value_iteration_post([Ok, Danger, Caught], 0.9, i)[-1])

# print(
#     q_learning(0.5, 1, [('x', 'r', 'y', 2), ('z', 'l', 'y', 2),
#                         ('y', 'r', 'z', -2), ('x', 'r', 'y', 4)]))
