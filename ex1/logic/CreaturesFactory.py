from logic.Creature import Creature
from random import choices
from random import sample


def find_empty_cell(automaton):
    cell = None
    while cell is None:
        # select cell randomly
        cell = choices(choices(automaton)[0])[0]
        if cell.is_occupied():
            cell = None
    return cell


def find_empty_cells(automaton, numberOfCells):
    cells = []
    for _ in range(numberOfCells):
        cell = find_empty_cell(automaton)
        cell.set_occupied(True)
        cells.append(cell)
    return cells


def randomly_set_infected_creatures(creatures, numberOfCreatures):
    selectedCretures = sample(creatures, numberOfCreatures)

    for creature in selectedCretures:
        creature.set_infected(True)


def create_creatures(automaton, numberOfCreatures, numberOfInfected = 1):
    creatures = []
    emptyCells = find_empty_cells(automaton, numberOfCreatures)

    for cell in emptyCells:
        c = Creature(cell)
        creatures.append(c)

    randomly_set_infected_creatures(creatures, numberOfInfected)

    return creatures
