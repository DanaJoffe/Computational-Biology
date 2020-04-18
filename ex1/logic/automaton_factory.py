from logic.Cell import Cell


def get_neighbors(automaton, row, col):
    if not automaton:
        return None

    number_of_rows = len(automaton)
    number_of_cols = len(automaton[0])

    left_col = (col - 1) % number_of_cols
    right_col = (col + 1) % number_of_cols
    row_below = (row - 1) % number_of_rows
    row_up = (row + 1) % number_of_rows

    neighbors = [
        automaton[row_up][col],

        automaton[row_up][right_col],
        automaton[row][right_col],
        automaton[row_below][right_col],

        automaton[row_below][col],

        automaton[row_below][left_col],
        automaton[row][left_col],
        automaton[row_up][left_col]
    ]

    return neighbors


def set_neighbors(automaton):
    if not automaton:
        return None

    number_of_rows = len(automaton)
    number_of_cols = len(automaton[0])

    for row in range(number_of_rows):
        for col in range(number_of_cols):
            neighbors = get_neighbors(automaton, row, col)
            automaton[row][col].neighbors = neighbors


def create_automaton(number_of_rows, number_of_cols):
    automaton = [[Cell() for _ in range(number_of_cols)] for _ in range(number_of_rows)]

    set_neighbors(automaton)
    return automaton
