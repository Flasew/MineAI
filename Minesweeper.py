"""
A complete minesweeper game with difficulty setting
"""

import random
import time
import numpy as np
from itertools import product, starmap

OPEN = 100  # square is touched/revealed
HIDDEN = 101  # square is untouched
FLAGGED = 102  # square is flagged by player
DEATH_MINE = 103 # square of mine that was triggered
MISFLAGGED = 104 # square not mine that was flagged

DIFF_BEGINNER = {'width': 8, 'height': 8, 'num_mines': 10, 'desc': 'BEGINNER'}
DIFF_INTERMED = {'width': 16, 'height': 16, 'num_mines': 40, 'desc': 'INTERMEDIATE'}
DIFF_EXPERT = {'width': 30, 'height': 16, 'num_mines': 99, 'desc': 'EXPERT'}

