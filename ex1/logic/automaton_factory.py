from logic.Cell import Cell


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


def create_automaton(numberOfRows, numberOfCols):
    automaton = [[Cell() for _ in range(numberOfCols)] for _ in range(numberOfRows)]

    set_neighbors(automaton)
    return automaton
