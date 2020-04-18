from random import choices
from ObserverPattern.Observer import Observer


class Creature(Observer):
    def __init__(self, current_cell, is_infected = False):
        self.isInfected = is_infected
        self.currentCell = None
        self.set_current_cell(current_cell)

    def set_current_cell(self, target):
        target.attach(self)
        target.set_occupied(True)
        target.set_is_infected(self.isInfected)
        self.currentCell = target

    def get_current_cell(self):
        return self.currentCell

    def set_infected(self, is_infected):
        self.isInfected = is_infected
        self.get_current_cell().set_is_infected(self.isInfected)

    def move(self, option_cells):
        self.leave_the_current_location()
        target = self.find_next_location(option_cells)
        self.set_current_cell(target)
        self.get_current_cell().set_is_infected(self.isInfected)

    def infect(self, probability, option_cells):
        if self.isInfected:
            infectious = True
            not_infectious = False

            for cell in option_cells:
                if cell.isOccupied and not cell.isInfected:
                    is_infected = choices([infectious, not_infectious], weights=[probability, 1-probability])[0]

                    if is_infected:
                        cell.notify_of_infection()

    def leave_the_current_location(self):
        self.currentCell.detach(self)
        self.currentCell.set_occupied(False)

    def find_next_location(self, option_cells):
        """
        The function finds the cell where the creature will go in the next step.

        If the next cell isOccupied, i.e. there is a creature in the cell already,
        the creature will stay in its current cell
        """
        # find randomly the next cell
        target = choices(option_cells)[0]

        ####################################################
        # ***This code prevents two creatures from being in the same cell.***
        ####################################################
        if target.isOccupied:
            target = self.currentCell
        return target

    def update(self, subject):
        """ implements Observer from ObserverPattern - In case of corona infection """
        if subject == self.currentCell:
            self.set_infected(True)
