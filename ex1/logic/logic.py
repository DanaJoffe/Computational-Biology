import time

from Cell import Cell
from CellAutomatonGameBase import CellAutomatonGameBase
from Creature import Creature
from random import choices
from random import sample
from graphics.print_board import print_board, SICK, HEALTHY, EMPTY, start_animation


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


def get_board(automaton, creatures):
    # init empty board
    board = [["_" for _ in range(len(automaton[0]))] for _ in range(len(automaton))]
    for row in range(len(board)):
        for col in range(len(board[0])):
            if automaton[row][col].isOccupied:
                for c in creatures:
                    if c.get_current_cell() == automaton[row][col]:
                        if c.isInfected:
                            board[row][col] = SICK
                            break
                        else:
                            board[row][col] = HEALTHY
                            break
            else:
                board[row][col] = EMPTY
    return board


def printBoard(board):
    print("\n\n*******************************************************\n\n")
    for row in range(len(board)):
        for col in range(len(board[0])):
            print(board[row][col], end=",")
        print("")
    print("\n\n*******************************************************\n\n")
    time.sleep(1)


def start_simulation(automaton, creatures, probabilityToInfect):
    af = CellAutomatonGame(automaton, creatures, probabilityToInfect)
    start_animation(af)


class CellAutomatonGame(CellAutomatonGameBase):
    def __init__(self, automaton, creatures, probabilityToInfect):
        self.automaton = automaton
        self.creatures = creatures
        self.probabilityToInfect = probabilityToInfect

        self.steps = 0
        self.board = self.get_board()

    def get_board(self):
        return get_board(self.automaton, self.creatures)

    def get_step(self):
        return self.steps

    def update_board(self):
        self.steps += 1
        # update state
        for creature in self.creatures:
            optionsToInfect = creature.get_current_cell().get_neighbors()
            creature.infect(self.probabilityToInfect, optionsToInfect)

        for creature in self.creatures:
            optionsToMove = creature.get_current_cell().get_neighbors()
            optionsToMove.append(creature.get_current_cell())
            creature.move(optionsToMove)

        # update board with respect to new state
        self.board = self.get_board()


if __name__ == '__main__':
    rows = 10
    cols = 10
    N = 20
    P = 0.5

    cellularAutomaton = init_automaton(rows, cols)
    listOfCreatures = init_creatures(cellularAutomaton, N)

    start_simulation(cellularAutomaton, listOfCreatures, P)
