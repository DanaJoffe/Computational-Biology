import time
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib import colors
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


class CellAnimation(object):
    min_tbf = 1
    max_tbf = 500

    def __init__(self, pause_button, play_button, speed_up_button, speed_down_button, speed_box, fig, ax):
        self.time_bt_frames = 250
        self.pause = True
        self.fig, self.ax = fig, ax
        pause_button.on_clicked(self.__pause)
        play_button.on_clicked(self.__start)

        self.speed_box = speed_box
        self.__write_speed()
        speed_up_button.on_clicked(self.__speed_up)
        speed_down_button.on_clicked(self.__speed_down)

    def __write_speed(self):
        speed = int(self.max_tbf + 1 - self.time_bt_frames)
        # self.speed_box.set_val(speed)
        self.speed_box.set_text(str(speed))

    def __speed_up(self, e):
        self.time_bt_frames = max(self.time_bt_frames - 20, self.min_tbf)
        self.animation.event_source.interval = self.time_bt_frames
        self.__write_speed()

    def __speed_down(self, e):
        self.time_bt_frames = min(self.time_bt_frames + 20, self.max_tbf)
        self.animation.event_source.interval = self.time_bt_frames
        self.__write_speed()

    def __pause(self, event):
        # on-click event function
        self.pause = True

    def __start(self, event):
        # on-click event function
        self.pause = False

    def __create_loop(self, game):
        def frame_gen():
            while True:
                if not self.pause:
                    game.update_board()
                yield game

        cmap, norm = create_cmap()
        img = self.ax.matshow(game.get_board(), cmap=cmap, norm=norm)
        # ax.axis('off')

        def init():
            return img,

        def animate(automaton_frame_iter):
            img.set_data(automaton_frame_iter.get_board())
            return img,

        self.animation = animation.FuncAnimation(self.fig, func=animate, frames=frame_gen,
                                                 interval=self.time_bt_frames, init_func=init)
        plt.show()

    def start(self, game):
        self.__create_loop(game)

    def stop(self):
        self.__pause(None)


