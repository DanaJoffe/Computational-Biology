from Observer import Observer
from Subject import Subject
from configuration import EMPTY, SICK


class GameStatistics(Observer, Subject):
    """
    follow the game and calculate statistics.
    """
    def __init__(self, game):
        self.followers = []
        game.attach(self)
        self.cells_amount = game.get_size()
        self.step = None
        self.sick_amount = None
        self.creatures_amount = None

    def update(self, game):
        """
        Receive update from subject.
        """
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

        self.notify()

    def attach(self, observer):
        """
        Attach an observer to the subject.
        """
        self.followers.append(observer)

    def detach(self, observer):
        """
        Detach an observer from the subject.
        """
        self.followers.remove(observer)

    def notify(self):
        """
        Notify all observers about an event.
        """
        for follower in self.followers:
            follower.update(self)

