from random import choices

from ObserverPattern.Observer import Observer
from ObserverPattern.Subject import Subject


class Creature(Observer):
    def __init__(self, currentCell, isInfected = False):
        self.isInfected = isInfected
        self.currentCell = None
        self.set_current_cell(currentCell)


    def set_current_cell(self, target):
        target.attach(self)
        target.set_occupied(True)
        target.set_is_infected(self.isInfected)
        self.currentCell = target


    def get_current_cell(self):
        return self.currentCell

    def set_infected(self, isInfected):
        self.isInfected = isInfected
        self.get_current_cell().set_is_infected(self.isInfected)

    def move(self, optionCells):
        self.leave_the_current_location()
        target = self.find_next_location(optionCells)
        self.set_current_cell(target)
        self.get_current_cell().set_is_infected(self.isInfected)


    def infect(self, probability, optionCells):
        if self.isInfected:
            infectious = True
            notInfectious = False

            for cell in optionCells:
                if cell.isOccupied and not cell.isInfected:
                    isInfected = choices([infectious, notInfectious], weights=[probability, 1-probability])[0]

                    if isInfected:
                        cell.notify_of_infection()

    def leave_the_current_location(self):
        self.currentCell.detach(self)
        self.currentCell.set_occupied(False)

    def find_next_location(self, optionCells):
        target = choices(optionCells)[0]
        if target.isOccupied:
            target = self.currentCell
        return target

    # Implements Observer from ObserverPattern - In case of corona infection
    def update(self, subject):
        if subject == self.currentCell:
            self.set_infected(True)
