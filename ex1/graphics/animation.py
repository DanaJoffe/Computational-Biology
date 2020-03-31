import time
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib import colors
from graphics.AutomatonFrame import AutomatonFrame
from configuration import CELL_STATES, CELL_COLORS


def create_cmap():
    # map colors
    cols = [color for _, color in sorted(zip(CELL_STATES, [CELL_COLORS[n] for n in CELL_STATES]))]
    nums = sorted(CELL_STATES)
    bound = nums + [nums[-1] + 1]
    stat = cols

    # create colorMap
    cmap = colors.ListedColormap(stat)
    norm = colors.BoundaryNorm(boundaries=bound, ncolors=cmap.N)
    return cmap, norm


def start_animation(game):
    automaton_frame_iter = AutomatonFrame(game)
    fig, ax = plt.subplots()
    cmap, norm = create_cmap()
    img = ax.matshow(automaton_frame_iter.get_board(), cmap=cmap, norm=norm)
    # ax.axis('off')

    def init():
        return img,

    def animate(automaton_frame_iter):
        img.set_data(automaton_frame_iter.get_board())
        return img,

    ani = animation.FuncAnimation(fig, func=animate,  frames=automaton_frame_iter, interval=500, init_func=init)
    plt.show()


def print_board(game):
    """
    for debugging only.
    """
    af = AutomatonFrame(game)
    cmap, norm = create_cmap()

    for iter in af:
        board = iter.board()
        print("\n\n*******************************************************\n\n")
        for row in range(len(board)):
            for col in range(len(board[0])):
                print(board[row][col], end=",")
            print("")
        print("\n\n*******************************************************\n\n")

        plt.matshow(np.array(board), cmap=cmap, norm=norm)
        plt.show()
        time.sleep(1)

