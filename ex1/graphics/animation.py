import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
from configuration import CELL_STATES, CELL_COLORS, SPEED, SHOW_LABELS


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
    """ manages the automaton animation """
    min_speed = 1
    max_speed = 40

    def __init__(self, pause_button, play_button, speed_up_button, speed_down_button, speed_box, fig, ax):
        self.speed_step = 1
        self.speed = SPEED
        self.pause = True
        self.fig, self.ax = fig, ax
        pause_button.on_clicked(self.__pause)
        play_button.on_clicked(self.__start)

        self.speed_box = speed_box
        self.__write_speed()
        speed_up_button.on_clicked(self.__speed_up)
        speed_down_button.on_clicked(self.__speed_down)

    def __write_speed(self):
        """ update visible speed value on the gui """
        self.speed_box.set_text(str(self.speed))

    def __speed_up(self, e):
        """ on-click event function: increase animation's speed """
        self.speed = min(self.speed + self.speed_step, self.max_speed)
        time_bt_frames = 1e3/self.speed
        self.animation.event_source.interval = time_bt_frames
        self.__write_speed()

    def __speed_down(self, e):
        """ on-click event function: decrease animation's speed """
        self.speed = max(self.speed - self.speed_step, self.min_speed)
        time_bt_frames = 1e3 / self.speed
        self.animation.event_source.interval = time_bt_frames
        self.__write_speed()

    def __pause(self, e):
        """ on-click event function: pause animation """
        self.pause = True

    def __start(self, event):
        """ on-click event function: resume animation """
        self.pause = False

    def __create_loop(self, game):
        """ create animation's loop"""
        def frame_gen():
            """ generator function: generates every frame in the game """
            while True:
                if not self.pause:
                    game.update_board()
                yield game

        cmap, norm = create_cmap()
        img = self.ax.matshow(game.get_board(), cmap=cmap, norm=norm, aspect='auto')
        # turn off tick labels
        if not SHOW_LABELS:
            self.ax.axes.get_xaxis().set_ticks([])
            self.ax.axes.get_yaxis().set_ticks([])

        def init():
            return img,

        def animate(automaton_frame_iter):
            img.set_data(automaton_frame_iter.get_board())
            return img,

        self.animation = animation.FuncAnimation(self.fig, func=animate, frames=frame_gen,
                                                 interval=1e3 / self.speed, init_func=init)
        plt.show()

    def start(self, game):
        """ start animation's loop """
        self.__create_loop(game)

    def stop(self):
        """ pause animation """
        self.__pause(None)
