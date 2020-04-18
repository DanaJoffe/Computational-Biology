from ObserverPattern.Subject import Subject


class Cell(Subject):

    def __init__(self):
        self.neighbors = []

        # isOccupied tells if there is a creature on the cell now
        self.isOccupied = False

        # isInfected tells if the creature on the cell is infected.
        self.isInfected = False
        self.observers = []

    def set_neighbors(self, n):
        self.neighbors = n

    def get_neighbors(self):
        return self.neighbors

    def get_is_infected(self):
        return self.isOccupied and self.isInfected

    def set_is_infected(self, isInfected):
        self.isInfected = isInfected

    def is_occupied(self):
        """ the function return if there is a creature on the cell now """
        return self.isOccupied

    def set_occupied(self, isOccupied):
        self.isOccupied = isOccupied

    def notify_of_infection(self):
        self.notify()

    def attach(self, observer):
        """ implements Subject from ObserverPattern - In case of corona infection """
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for o in self.observers:
            o.update(self)
