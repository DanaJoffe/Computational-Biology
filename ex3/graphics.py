import math
from typing import Mapping
import numpy
from matplotlib import colors
import matplotlib.pyplot as plt
from config import CELL_COLORS

CellState = int
Color = str


def create_cmap(cell_colors: Mapping[CellState, Color]):
    """

    :param cell_colors: maps a number (cell state) to a string color.
    :return:
    """
    cell_states = list(cell_colors.keys())
    # map colors
    cols = [color for _, color in sorted(zip(cell_states, [cell_colors[n] for n in cell_states]))]
    nums = sorted(cell_states)
    bound = nums + [nums[-1] + 1]
    stat = cols
    # create colorMap
    cmap = colors.ListedColormap(stat)
    norm = colors.BoundaryNorm(boundaries=bound, ncolors=cmap.N)
    return cmap, norm


def show_mat(board, cell_size=(10, 10)):
    fig, ax = plt.subplots()
    cmap, norm = create_cmap(CELL_COLORS)
    ax.imshow(board, interpolation='nearest', cmap='gray')#, cmap=cmap)

    ax.set(xticks=[], yticks=[])
    ax.axis('image')

    ax.set_title('The best representation:')

    rows = int(board.shape [0] / cell_size[0])
    columns = int(board.shape [1] / cell_size[1])
    positions = [i + math.ceil(cell_size[0] / 2) for i in range(0, columns * cell_size[0], cell_size[0])]
    labels = [i for i in range(columns)]
    plt.xticks(positions, labels)

    positions = [i + math.ceil(cell_size[1] / 2) for i in range(0, rows * cell_size[1], cell_size[1])]
    labels = [i for i in range(rows)]
    plt.yticks(positions, labels)

    plt.show()




