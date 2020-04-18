from graphics.ShowStatistics import ShowStatistics
from statistics.GameStatistics import GameStatistics
from graphics.OnlineGraph import OnlineGraph
from statistics.StatAccumulator import StatAccumulator
from graphics.animation import CellAnimation
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from configuration import P, N, K, L, ALLOW_SAVE_DATA, SHOW_ONLINE_GRAPH


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
        self.K = K
        self.L = L

        # future members
        self.fig, self.ax = None, None
        self.animation = None

    def __set_widgets(self):
        """ set all sliders and buttons that are in the gui's responsibility """
        hcolor = None
        axcolor = 'white'
        slider_x_loc = 0.25
        slider_y_loc = 0.2
        slider_width = 0.6
        slider_hight = 0.021
        gap = slider_hight + 0.01

        # [left, bottom, width, height]
        # parameters sliders
        self.n_slider = Slider(plt.axes([slider_x_loc, slider_y_loc, slider_width, slider_hight],
                                        facecolor=axcolor), 'N', 1.0, int(self.game.get_size()/2), valinit=self.N,
                               valstep=1.0, valfmt='%0.0f')
        self.p_slider = Slider(plt.axes([slider_x_loc, slider_y_loc-gap, slider_width, slider_hight],
                                        facecolor=axcolor), 'P', 0.0, 1.0, valinit=self.P)
        self.k_slider_loc = plt.axes([slider_x_loc, slider_y_loc-2*gap, slider_width, slider_hight], facecolor=axcolor)
        self.k_slider = Slider(self.k_slider_loc, 'K', 1.0, 8.0, valinit=self.K, valstep=1.0, valfmt='%0.0f')
        self.k_slider_loc.set_visible(False)
        self.l_slider_loc = self.fig.add_axes([slider_x_loc, slider_y_loc - 3 * gap, slider_width, slider_hight],
                                              facecolor=axcolor)
        self.l_slider = Slider(self.l_slider_loc, 'L', 0.0, 1000.0, valinit=0, valstep=20.0, valfmt='%0.0f')
        self.l_slider_loc.set_visible(False)

        # quarantine option menu
        self.right_menu_x_loc = 0.025
        self.options_button = CheckButtons(plt.axes([self.right_menu_x_loc, slider_y_loc - 4 * gap, 0.18, 0.15]),
                                           ['apply\nquarantine'])
        self.get_stat_button = None
        if ALLOW_SAVE_DATA:
            self.get_stat_button = Button(plt.axes([self.right_menu_x_loc, slider_y_loc +15*gap, 0.12, 0.04]),
                                      'save data', color=axcolor, hovercolor=hcolor)

        # control animation's speed
        y_axis_speed = 0.92
        plt.text(0.80, y_axis_speed, 'speed: ', transform=self.fig.transFigure)
        self.speed_box = plt.text(0.88, y_axis_speed, '', transform=self.fig.transFigure)
        self.speed_up_button = Button(plt.axes([0.94, y_axis_speed, 0.02, 0.03]), '+', hovercolor=hcolor)
        self.speed_down_button = Button(plt.axes([0.96, y_axis_speed, 0.02, 0.03]), '-', hovercolor=hcolor)

        # control animation buttons
        self.play_button = Button(plt.axes([0.8, 0.025, 0.1, 0.04]), 'play', color=axcolor, hovercolor=hcolor)
        self.pause_button = Button(plt.axes([0.69, 0.025, 0.1, 0.04]), 'pause', color=axcolor, hovercolor=hcolor)
        self.reset_button = Button(plt.axes([0.56, 0.025, 0.12, 0.04]), 'reset', color=axcolor, hovercolor=hcolor)

    def __set_p(self, e):
        """ on-click function: change P slider value """
        self.P = self.p_slider.val

    def __set_n(self, e):
        """ on-click function: change N slider value """
        self.N = int(self.n_slider.val)

    def __set_k(self, e):
        """ on-click function: change K slider value """
        check = self.options_button.get_status()[0]
        self.k_slider_loc.set_visible(check)
        self.k_slider.set_active(check)
        self.K = int(self.k_slider.val) if check else 0

    def __set_l(self, e):
        """ on-click function: change L slider value """
        check = self.options_button.get_status()[0]
        self.l_slider_loc.set_visible(check)
        self.l_slider.set_active(check)
        self.L = int(self.l_slider.val) if check else None

    def __reset_button_on_click(self, e):
        """ on-click function: pause and reset the game with current parameters """
        self.animation.stop()
        self.game.build(self.N, self.P, self.K, self.L)

    def set_all(self):
        """ create gui's visible elements and attach them to event-functions """
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.25, bottom=0.25)
        self.__set_widgets()

        self.p_slider.on_changed(self.__set_p)
        self.n_slider.on_changed(self.__set_n)
        self.k_slider.on_changed(self.__set_k)
        self.l_slider.on_changed(self.__set_l)

        self.options_button.on_clicked(self.__set_l)
        self.options_button.on_clicked(self.__set_k)
        self.reset_button.on_clicked(self.__reset_button_on_click)

    def start(self):
        """ create all entities and start the animation """
        # calculate game's statistics for each time step
        gs = GameStatistics(self.game)
        # follow statistics
        ShowStatistics(gs, self.fig, x=self.right_menu_x_loc)
        StatAccumulator(gs, self.get_stat_button)
        if SHOW_ONLINE_GRAPH:
            OnlineGraph(gs)

        self.game.build(self.N, self.P, self.K, self.L)
        self.animation = CellAnimation(self.pause_button, self.play_button, self.speed_up_button,
                                       self.speed_down_button, self.speed_box, self.fig, self.ax)
        self.animation.start(self.game)
