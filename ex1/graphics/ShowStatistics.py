from ObserverPattern.Observer import Observer
import matplotlib.pyplot as plt


class ShowStatistics(Observer):
    """
    show the cellular automaton state:
    - # of infected creatures
    - iteration (time-step)
    - % of sick creatures
    """
    def __init__(self, follow, fig, x=0.025, y=0.85):
        follow.attach(self)
        self.cells_amount = None

        x_val_pos = x + 0.07
        plt.text(x, y, 'step: ', transform=fig.transFigure)
        self.step_text = plt.text(x_val_pos, y, '', transform=fig.transFigure)

        plt.text(x, y-0.05, 'sick: ', transform=fig.transFigure)
        self.sick_text = plt.text(x_val_pos, y-0.05, '', transform=fig.transFigure)

        plt.text(x, y - 0.1, '%sick: ', transform=fig.transFigure)
        self.sick_percentage_text = plt.text(x_val_pos, y - 0.1, '', transform=fig.transFigure)

    def update(self, game_stat):
        """ updates shown statistics. the function is called at every game iteration """
        self.sick_text.set_text(str(game_stat.sick_amount))
        self.step_text.set_text(str(game_stat.step))
        self.sick_percentage_text.set_text("{:.1f}".format(game_stat.sick_percentage))
