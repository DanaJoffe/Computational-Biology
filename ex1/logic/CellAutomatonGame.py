import time
from ObserverPattern.Subject import Subject
from logic.automaton_factory import create_automaton
from logic.creatures_factory import create_creatures
from logic.CellAutomatonGameBase import CellAutomatonGameBase
from configuration import SICK, HEALTHY, EMPTY


class CellAutomatonGame(CellAutomatonGameBase, Subject):

    def __init__(self, rows=200, columns=200):
        self.followers = []
        self.rows, self.cols = rows, columns
        self.automaton = None
        self.creatures = None
        self.probabilityToInfect = None
        self.steps = None
        self.board = None
        self.numberOfCreaturesInIsolation = None
        self.number_of_steps_to_take_action = None

    def build(self, N, P, K=0, L=0):
        self.automaton = create_automaton(self.rows, self.cols)
        self.creatures = create_creatures(self.automaton, N)
        self.probabilityToInfect = P
        self.numberOfCreaturesInIsolation = K
        self.number_of_steps_to_take_action = L

        self.is_isolation_activated = False
        self.steps = 0
        self.__create_board()
        self.notify()

    def __create_board(self):
        automaton = self.automaton
        # init empty board
        if not self.board:
            self.board = [["_" for _ in range(len(automaton[0]))] for _ in range(len(automaton))]

        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if automaton[row][col].isOccupied:
                    if automaton[row][col].get_is_infected():
                        self.board[row][col] = SICK
                        continue
                    else:
                        self.board[row][col] = HEALTHY
                        continue
                else:
                    self.board[row][col] = EMPTY

    def get_board(self):
        return self.board

    def get_step(self):
        return self.steps

    def get_size(self):
        return self.rows * self.cols

    def get_params(self):
        """ returns P, K, L"""
        return self.probabilityToInfect, self.numberOfCreaturesInIsolation, self.number_of_steps_to_take_action

    def update_board(self):
        self.steps += 1
        if self.number_of_steps_to_take_action != None and self.steps >= self.number_of_steps_to_take_action:
            self.take_action()
        # update state
        for creature in self.creatures:
            options_to_infect = creature.get_current_cell().get_neighbors()

            # subtract the creatures in isolation from the relevant options
            if self.is_isolation_activated:
                options_to_infect = options_to_infect[self.numberOfCreaturesInIsolation:]

            creature.infect(self.probabilityToInfect, options_to_infect)

        for creature in self.creatures:
            options_to_move = creature.get_current_cell().get_neighbors()
            options_to_move.append(creature.get_current_cell())
            creature.move(options_to_move)

        # update board with respect to new state
        self.__create_board()
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

    def take_action(self):
        self.is_isolation_activated = True
