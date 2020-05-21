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


def show_mat(board):
    fig, ax = plt.subplots()
    cmap, norm = create_cmap(CELL_COLORS)
    ax.imshow(board, interpolation='nearest')

    ax.set(xticks=[], yticks=[])
    ax.axis('image')
    plt.show()


if __name__ == '__main__':
    with open("Digits_Ex3.txt", 'r') as f:
        board = []
        for row in f:
            if not row.strip() and board:
                board = numpy.array(board)
                show_mat(board)
                board = []
            else:
                board.append([int(n) for n in row.strip()])




