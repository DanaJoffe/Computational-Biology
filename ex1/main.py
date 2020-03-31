from graphics.animation import start_animation
from logic.AutomatopnFactory import create_automaton
from logic.CreaturesFactory import create_creatures
from logic.CellAutomatonGame import CellAutomatonGame


def start_simulation(automaton, creatures, probabilityToInfect):
    af = CellAutomatonGame(automaton, creatures, probabilityToInfect)
    start_animation(af)

if __name__ == '__main__':
    rows = 10
    cols = 10
    N = 5
    P = 0.5

    cellularAutomaton = create_automaton(rows, cols)
    listOfCreatures = create_creatures(cellularAutomaton, N)

    start_simulation(cellularAutomaton, listOfCreatures, P)