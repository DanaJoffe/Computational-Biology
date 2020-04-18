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


def find_empty_cells(automaton, number_of_cells):
    cells = []
    for _ in range(number_of_cells):
        cell = find_empty_cell(automaton)
        cell.set_occupied(True)
        cells.append(cell)
    return cells


def randomly_set_infected_creatures(creatures, number_of_creatures):
    selected_creatures = sample(creatures, number_of_creatures)

    for creature in selected_creatures:
        creature.set_infected(True)


def create_creatures(automaton, number_of_creatures, number_of_infected=1):
    creatures = []
    empty_cells = find_empty_cells(automaton, number_of_creatures)

    for cell in empty_cells:
        c = Creature(cell)
        creatures.append(c)

    randomly_set_infected_creatures(creatures, number_of_infected)

    return creatures
