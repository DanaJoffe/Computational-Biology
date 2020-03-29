import time

from Cell import Cell
from Creature import Creature
from random import choices
from random import sample


def get_neighbors(automaton, row, col):
    if not automaton:
        return None

    numberOfRows = len(automaton)
    numberOfCols = len(automaton[0])

    leftCol = (col - 1) % numberOfCols
    rightCol = (col + 1) % numberOfCols
    rowBelow = (row - 1) % numberOfRows
    rowUp = (row + 1) % numberOfRows

    neighbors = [
        automaton[rowUp][rightCol],
        automaton[row][rightCol],
        automaton[rowBelow][rightCol],
        automaton[rowUp][col],
        automaton[rowBelow][col],
        automaton[rowBelow][leftCol],
        automaton[row][leftCol],
        automaton[rowUp][leftCol]
    ]

    return neighbors


def set_neighbors(automaton):
    if not automaton:
        return None

    numberOfRows = len(automaton)
    numberOfCols = len(automaton[0])

    for row in range(numberOfRows):
        for col in range(numberOfCols):
            neighbors = get_neighbors(automaton, row, col)
            automaton[row][col].neighbors = neighbors


def find_empty_cell(automaton):
    cell = None
    while cell is None:
        # select cell randomly
        cell = choices(choices(automaton)[0])[0]
        if cell.is_occupied():
            cell = None
    return cell


def create_creatures(automaton, numberOfCreatures):
    creatures = []
    for _ in range(numberOfCreatures):
        cell = find_empty_cell(automaton)
        cell.set_occupied(True)
        c = Creature(cell)
        creatures.append(c)
    return creatures


def set_infected_creatures(creatures, numberOfCreatures=1):
    selectedCretures = sample(creatures, numberOfCreatures)

    for creature in selectedCretures:
        creature.set_infected(True)


def init_automaton(numberOfRows, numberOfCols):
    automaton = [[Cell() for _ in range(numberOfCols)] for _ in range(numberOfRows)]

    set_neighbors(automaton)
    return automaton


def init_creatures(automaton, numberOfCreatures):
    creatures = create_creatures(automaton, numberOfCreatures)
    set_infected_creatures(creatures)

    return creatures


def printBoard(automaton, creatures):
    print("\n\n*******************************************************\n\n")
    for row in range(len(automaton)):
        for col in range(len(automaton[0])):
            if automaton[row][col].isOccupied:
                for c in creatures:
                    if c.get_current_cell() == automaton[row][col]:
                        if c.isInfected:
                            print("@", end=",")
                            break
                        else:
                            print("#", end=",")
                            break
                else:
                    print("&", end=",")

            else:
                print("_", end=",")
        print("")
    print("\n\n*******************************************************\n\n")
    time.sleep(1)



def start_simulation(automaton, creatures, probabilityToInfect):
    stop = False
    while not stop:
        for creature in creatures:
            optionsToInfect = creature.get_current_cell().get_neighbors()
            creature.infect(probabilityToInfect, optionsToInfect)

        for creature in creatures:
            optionsToMove = creature.get_current_cell().get_neighbors()
            optionsToMove.append(creature.get_current_cell())
            creature.move(optionsToMove)

        printBoard(automaton, creatures)


if __name__ == '__main__':
    rows = 10
    cols = 10
    N = 20
    P = 0.5

    cellularAutomaton = init_automaton(rows, cols)
    listOfCreatures = init_creatures(cellularAutomaton, N)

    start_simulation(cellularAutomaton, listOfCreatures, P)
