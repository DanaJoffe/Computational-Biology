import math
import matplotlib.pyplot as plt
import numpy
from matplotlib import animation
from matplotlib.widgets import Button


class CellAnimation(object):
    def __init__(self, som, cell_size=(10, 10)):
        """

        :param som: SOM object
        :param cell_size: size of a single cell in som's board.
        """
        self.som = som

        self.resolution = cell_size
        self.board = som.board
        self.rows = len(self.board)
        self.columns = len(self.board[0])

        fig, ax = plt.subplots()
        self.fig, self.ax = fig, ax

        self.img = self.ax.matshow(self.board, interpolation='nearest', cmap='gray')
        self.ax.set(xticks=[], yticks=[])
        if self.resolution:
            positions = [i + math.ceil(self.resolution[0] / 2) for i in range(0, self.columns, self.resolution[0])]
            labels = [i for i in range(int(self.columns / self.resolution[0]))]
            # self.ax.set_xticklabels(str(i) for i in labels)
            plt.xticks(positions, labels)
            positions = [i + math.ceil(self.resolution[1] / 2) for i in range(0, self.rows, self.resolution[1])]
            labels = [i for i in range(int(self.rows / self.resolution[1]))]
            # self.ax.set_yticklabels(positions, labels)
            plt.yticks(positions, labels)
        # self.ax.set(xticks=[], yticks=[])
        # if self.resolution:
        #     l =  [i for i in range(self.columns)]
        #     self.ax.set_xticklabels([''] + [str(i) for i in range(int(self.columns / self.resolution[1]))], ha='center')
        #     self.ax.set_yticklabels([''] + [str(i) for i in range(int(self.rows/self.resolution[0]))], ha='center', ma='center')

    def frame_gen(self):
        """ generator function: generates every frame in the game """
        prev = self.som.epoch
        for board in self.som.run_epoch_generator():
            # board, time = self.som.run_epoch()
            if prev != self.som.epoch:
                prev = self.som.epoch
                print(f"epoch {self.som.epoch}")
            yield board

    def __create_loop(self):
        """ create animation's loop"""
        img = self.img

        def init():
            return img,

        def animate(ignore):
            img.set_data(self.som.board)
            return img,

        self.animation = animation.FuncAnimation(self.fig, func=animate, frames=self.frame_gen,
                                                 interval=5, init_func=init)
        plt.show()

    def start(self):
        """ start animation's loop """
        self.__create_loop()


class GUIanimation(CellAnimation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.resolution = None

        # GUI items
        self.pause = True
        hcolor = None
        axcolor = 'white'
        # [left, bottom, width, height]
        self.play_button = Button(plt.axes([0.8, 0.025, 0.1, 0.04]), 'play', color=axcolor, hovercolor=hcolor)
        self.pause_button = Button(plt.axes([0.69, 0.025, 0.1, 0.04]), 'pause', color=axcolor, hovercolor=hcolor)
        self.pause_button.on_clicked(self.__pause)
        self.play_button.on_clicked(self.__start)

        plt.text(0.80, 0.92, 'epoch: ', transform=self.fig.transFigure)
        self.speed_box = plt.text(0.88, 0.92, '', transform=self.fig.transFigure)

    def __pause(self, e):
        """ on-click event function: pause animation """
        self.pause = True
        print(self.som.test())

    def __start(self, event):
        """ on-click event function: resume animation """
        self.pause = False

    def frame_gen(self):
        """ generator function: generates every frame in the game """
        iter = self.som.run_epoch_generator()
        prev = self.som.epoch
        while True:
            if not self.pause:
                self.board = iter.__next__()
            if prev != self.som.epoch:
                prev = self.som.epoch
                self.speed_box.set_text(str(self.som.epoch))
                # print(f"epoch {self.som.epoch}")
            yield self.board

