# Benjamin Cape
# 21F
# COSC 76: AI
# 11.1.21

from main import *
from random import randint
import sys

WIDTH = '-w'
HEIGHT = '-h'
OBSTACLES = '-o'
LENGTH = '-l'

params = {}
params_in = sys.argv[1:]
for i in range(0, len(params_in), 2):
    params[params_in[i]] = int(params_in[i + 1])

maze = Maze.random(params[WIDTH], params[HEIGHT], params[OBSTACLES],
                   list(map(Color, range(0, 4))))
readings = (Color(randint(0, 4)) for _ in range(LENGTH))

Problem(maze).run(readings)
