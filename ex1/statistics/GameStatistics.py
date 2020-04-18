from ObserverPattern.Observer import Observer
from ObserverPattern.Subject import Subject
from configuration import EMPTY, SICK


class GameStatistics(Observer, Subject):
    """
    follow the game and calculate statistics.
    informs whoever wants to know about the statistics.
    """
    def __init__(self, game):
        self._followers = []
        game.attach(self)
        self.cells_amount = game.get_size()
        self.step = None
        self.sick_amount = None
        self.creatures_amount = None # N
        self.sick_percentage = None
        self.K = None
        self.L = None
        self.P = None

    def update(self, game):
        """ calculate statistics and inform all followers. the function is called at every game iteration """
        board = game.get_board()
        sick_amount = 0
        creatures_amount = 0
        for row in board:
            for cell in row:
                if cell != EMPTY:
                    creatures_amount += 1
                    if cell == SICK:
                        sick_amount += 1
        self.step = game.get_step()
        self.sick_amount = sick_amount
        self.creatures_amount = creatures_amount
        self.sick_percentage = self.sick_amount*100/self.creatures_amount
        self.P, self.K, self.L = game.get_params()

        self.notify()

    def attach(self, observer):
        """ add game-statistics follower """
        self._followers.append(observer)

    def detach(self, observer):
        """ remove a game-statistics follower"""
        self._followers.remove(observer)

    def notify(self):
        """ inform all followers about the new statistics calculated """
        for follower in self._followers:
            try:
                follower.update(self)
            except:
                self.detach(follower)
