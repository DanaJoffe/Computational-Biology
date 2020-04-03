from ObserverPattern.Observer import Observer
from graphics.animation import CellAnimation
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox
from configuration import EMPTY, SICK, P, N


# ICON_PLAY =  plt.imread('https://i.stack.imgur.com/ySW6o.png')
# ICON_PAUSE = plt.imread("https://i.stack.imgur.com/tTa3H.png")


class CellAutomatonGameGUI(object):
    """
    GUI to control:
    1. N = # of creatures
    2. P = infection probability
    3. K = quarantine parameter
    4. L = generation (iteration) from which the quarantine applies
    5. animation's speed
    6. pause | play | reset buttons
    """
    def __init__(self, game):
        self.game = game
        self.N = N
        self.P = P
        self.K = None
        self.L = None

    def __set_widgets(self):
        hcolor = None #'0.975'
        axcolor = 'white' # lightgoldenrodyellow
        # [left, bottom, width, height]
        self.p_slider = Slider(plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor),
                          'P', 0.0, 1.0, valinit=self.P)
        self.n_slider = Slider(plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor),
                          'N', 1.0, int(self.game.get_size()/2), valinit=self.N, valstep=1.0)
        y_axis_speed = 0.92
        plt.text(0.80, y_axis_speed, 'speed: ', transform=self.fig.transFigure)
        self.speed_box = plt.text(0.88, y_axis_speed, '', transform=self.fig.transFigure)

        self.speed_up_button = Button(plt.axes([0.94, y_axis_speed, 0.02, 0.03]), '+', hovercolor=hcolor)
        self.speed_down_button = Button(plt.axes([0.96, y_axis_speed, 0.02, 0.03]), '-', hovercolor=hcolor)

        self.play_button = Button(plt.axes([0.8, 0.025, 0.1, 0.04]), 'play', color=axcolor, hovercolor=hcolor)
        # self.play_button = Button(plt.axes([0.8, 0.025, 0.1, 0.04]), '', image=ICON_PLAY)
        self.pause_button = Button(plt.axes([0.69, 0.025, 0.1, 0.04]), 'pause', color=axcolor, hovercolor=hcolor)
        self.reset_button = Button(plt.axes([0.56, 0.025, 0.12, 0.04]), 'reset', color=axcolor, hovercolor=hcolor)

    def __set_p(self, e):
        self.P = self.p_slider.val

    def __set_n(self, e):
        self.N = int(self.n_slider.val)

    def __reset_button_on_click(self, e):
        self.animation.stop()
        self.game.build(self.N, self.P)

    def set_all(self):
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.25, bottom=0.25)
        self.__set_widgets()

        self.p_slider.on_changed(self.__set_p)
        self.n_slider.on_changed(self.__set_n)
        self.reset_button.on_clicked(self.__reset_button_on_click)

        self.stat_displayer = Stat(self.game, self.fig)

    def start(self):
        # game = self.game_factory.create_game(self.N, self.P)
        self.game.build(self.N, self.P)

        self.animation = CellAnimation(self.pause_button, self.play_button, self.speed_up_button,
                                       self.speed_down_button, self.speed_box, self.fig, self.ax)
        self.animation.start(self.game)


class Stat(Observer):
    """
    show the cellular automaton state:
    - # of infected creatures
    - iteration (time)

    todo: calc % of infected creatures for timestep t
    todo: calc infection rate = disease spreading rate
    todo: look for K that enables linear growth and not exponential growth.
    """
    def __init__(self, game, fig, x=0.025, y=0.85):
        game.attach(self)

        x_val_pos = x + 0.07
        plt.text(x, y, 'step: ', transform=fig.transFigure)
        self.step_text = plt.text(x_val_pos, y, '', transform=fig.transFigure)

        plt.text(x, y-0.05, 'sick: ', transform=fig.transFigure)
        self.sick_text = plt.text(x_val_pos, y-0.05, '', transform=fig.transFigure)

        plt.text(x, y - 0.1, '%sick: ', transform=fig.transFigure)
        self.sick_percentage_text = plt.text(x_val_pos, y - 0.1, '', transform=fig.transFigure)

    def update(self, game):
        """
        Receive update from subject.
        """
        board = game.get_board()
        cells_amount = 0
        sick_amount = 0
        creatures_amount = 0
        for row in board:
            for cell in row:
                cells_amount += 1
                if cell != EMPTY:
                    creatures_amount += 1
                    if cell == SICK:
                        sick_amount += 1
        step = game.get_step()
        self.sick_text.set_text(str(sick_amount))
        self.step_text.set_text(str(step))
        self.sick_percentage_text.set_text("{:.1f}".format(sick_amount*100/creatures_amount))





