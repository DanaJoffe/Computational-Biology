import time
from logic.CellAutomatonGameBase import CellAutomatonGameBase
from configuration import SICK, HEALTHY, EMPTY


class CellAutomatonGame(CellAutomatonGameBase):
    def __init__(self, automaton, creatures, probabilityToInfect):
        self.automaton = automaton
        self.creatures = creatures
        self.probabilityToInfect = probabilityToInfect

        self.steps = 0
        self.board = self.__create_board()

    def __create_board(self):
        automaton = self.automaton
        creatures = self.creatures
        # init empty board
        board = [["_" for _ in range(len(automaton[0]))] for _ in range(len(automaton))]
        for row in range(len(board)):
            for col in range(len(board[0])):
                if automaton[row][col].isOccupied:
                    if automaton[row][col].get_is_infected():
                        board[row][col] = SICK
                        continue
                    else:
                        board[row][col] = HEALTHY
                        continue
                else:
                    board[row][col] = EMPTY
        return board

    def get_board(self):
        return self.board

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
        self.board = self.__create_board()

    def print_automaton(self):
        print("\n\n*******************************************************\n\n")
        for row in range(len(self.automaton)):
            for col in range(len(self.automaton[0])):
                print(self.automaton[row][col], end=",")
            print("")
        print("\n\n*******************************************************\n\n")
        time.sleep(1)
