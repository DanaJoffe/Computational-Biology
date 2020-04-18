from abc import ABC, abstractmethod


class CellAutomatonGameBase(ABC):
    """
    API that defines what info and actions should be available at each game iteration.
    """
    @abstractmethod
    def get_board(self):
        """returns the game board at the current state"""

    @abstractmethod
    def get_step(self):
        """return the iteration number"""

    @abstractmethod
    def update_board(self):
        """apply one game step and change the board"""

    @abstractmethod
    def build(self, N, P, K, L):
        """do initialization"""

    @abstractmethod
    def get_size(self):
        """return amount of cells in the game board"""

    @abstractmethod
    def get_params(self):
        """return game's parameters"""
