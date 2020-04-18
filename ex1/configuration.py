import os

EMPTY = 0
HEALTHY = 4
SICK = 23
CELL_STATES = [EMPTY, HEALTHY, SICK]

CELL_COLORS = {EMPTY: 'white',
               HEALTHY: 'lightgreen',
               SICK: 'red'}

rows = 200
cols = 200
N = 2100  # number of creatures
P = 0.5  # infection probability
K = 0  # quarantine parameter
L = None  # generation (iteration) from which the quarantine applies

SPEED = 40  # frames per second

SHOW_LABELS = False
ALLOW_SAVE_DATA = False
SHOW_ONLINE_GRAPH = True

# all data from the games will be saved in DATA_PATH, which is a file named 'data' under statistics directory.
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'statistics', 'data')
