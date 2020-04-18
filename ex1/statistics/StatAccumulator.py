from statistics.GamesDataHandler import GamesDataHandler
from ObserverPattern.Observer import Observer


class StatAccumulator(Observer):
    """ save how many sick creatures were at every time step """
    def __init__(self, game_stat, button=None):
        game_stat.attach(self)
        if button:
            button.on_clicked(self.export_data)
        self.sick = []
        self.steps = []
        self.cells = game_stat.cells_amount
        self.N = None
        self.L = None
        self.P = None
        self.K = None

    def reset_data(self, game_stat):
        """ reset all statistics memory from previous game and set parameters as at current game """
        self.N = game_stat.creatures_amount
        self.L = game_stat.L
        self.P = game_stat.P
        self.K = game_stat.K
        self.sick = []
        self.steps = []

    def update(self, game_stat):
        """ accumulate statistics info from current time-step """
        step = game_stat.step
        if step == 0:
            # new game
            self.reset_data(game_stat)
        self.sick.append(game_stat.sick_amount)
        self.steps.append(game_stat.step)

    def export_data(self, e):
        """ write and save all current game's data to external file """
        GamesDataHandler.add(self.__dict__)
