import time
from Subject import Subject
from automaton_factory import create_automaton
from creatures_factory import create_creatures
from logic.CellAutomatonGameBase import CellAutomatonGameBase
from configuration import SICK, HEALTHY, EMPTY


class CellAutomatonGame(CellAutomatonGameBase, Subject):

    def __init__(self, rows=20, columns=20):
        self.followers = []
        self.rows, self.cols = rows, columns
        self.automaton = None
        self.creatures = None
        self.probabilityToInfect = None
        self.steps = None
        self.board = None

    def build(self, N, P, K=0, L=None):
        self.automaton = create_automaton(self.rows, self.cols)
        self.creatures = create_creatures(self.automaton, N)
        self.probabilityToInfect = P
        self.steps = 0
        self.board = self.__create_board()
        self.notify()

    def __create_board(self):
        automaton = self.automaton
        creatures = self.creatures
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
        self.notify()

    def print_automaton(self):
        print("\n\n*******************************************************\n\n")
        for row in range(len(self.automaton)):
            for col in range(len(self.automaton[0])):
                print(self.automaton[row][col], end=",")
            print("")
        print("\n\n*******************************************************\n\n")
        time.sleep(1)

    def attach(self, observer):
        """
        Attach an observer to the subject.
        """
        self.followers.append(observer)

    def detach(self, observer):
        """
        Detach an observer from the subject.
        """
        self.followers.remove(observer)

    def notify(self):
        """
        Notify all observers about an event.
        """
        for f in self.followers:
            f.update(self)

