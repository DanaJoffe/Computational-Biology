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
