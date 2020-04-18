from ObserverPattern.Observer import Observer
import matplotlib.pyplot as plt


class OnlineGraph(Observer):
    """ draws an online graph of sick percentage over time steps """
    def __init__(self, game_stat):
        game_stat.attach(self)
        self.sick_per_timestep = []
        self.steps = []

        self.fig, self.ax = plt.subplots(figsize=(4,4))
        plt.gcf().subplots_adjust(bottom=0.14, left=0.2)

        self.title = 'sickness spread speed'
        self.ylabel = '% infected'
        self.xlabel = 'step'

        self.line, = self.ax.plot(self.steps, self.sick_per_timestep)

    def reset_graph(self):
        """ delete the graph and reset scale """
        self.sick_per_timestep = []
        self.steps = []
        self.ax.clear()
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.set_title(self.title)

    def update(self, game_stat):
        """ updates the graph according to the current data. the function is called at every game iteration """
        step = game_stat.step
        if step == 0:
            # new game
            self.reset_graph()

        self.sick_per_timestep.append(game_stat.sick_percentage)
        self.steps.append(game_stat.step)

        self.line.set_ydata(self.sick_per_timestep)
        self.line.set_xdata(self.steps)

        self.line.remove()
        self.line, = self.ax.plot(self.steps, self.sick_per_timestep, color='blue')
        self.fig.canvas.draw()
