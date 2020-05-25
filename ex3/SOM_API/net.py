import math
from abc import ABC, abstractmethod
from typing import Type

from SOM_API.cell import Cell
from SOM_API.content import Content


class Net(ABC):
    def __init__(self, cells_amount):
        self.cells_amount = cells_amount
        self.cells = None

    @abstractmethod
    def init(self, domain_content: Type[Content]):
        raise NotImplemented

    @abstractmethod
    def get_repr(self):
        """ returns the representation of the net """
        raise NotImplemented

    @abstractmethod
    def get_cells(self):
        raise NotImplemented

    @abstractmethod
    def get_cell_location(self, cell):
        raise NotImplemented


class GridNet(Net):
    def __init__(self, rows, columns):
        super().__init__(rows * columns)
        self.rows = rows
        self.columns = columns
        self.cells_locations = {}

    def init(self, domain_content: Type[Content]):
        self.cells = [[Cell(domain_content()) for _ in range(self.columns)] for _ in range(self.rows)]
        # set neighbors
        for r in range(0, self.rows):
            for c in range(0, self.columns):
                center = self.cells[r][c]
                self.cells_locations[center] = (r, c)
                surr = []
                if r < self.rows-1:
                    surr.append(self.cells[r+1][c])  # down
                if c < self.columns-1:
                    surr.append(self.cells[r][c+1])  # right
                if r < self.rows-1 and c < self.columns-1:
                    surr.append(self.cells[r + 1][c + 1])  # downright
                for cell in surr:
                    center.add_neighbor(cell)
                    cell.add_neighbor(center)

        for r in range(0, self.rows-1):
            for c in range(1, self.columns):
                center = self.cells[r][c]
                self.cells_locations[center] = (r, c)
                downleft = self.cells[r + 1][c - 1]
                center.add_neighbor(downleft)
                downleft.add_neighbor(center)

    def __str__(self):
        ret = ""
        for row in self.cells:
            ret += ', '.join([str(c) for c in row]) + '\n'
        return ret

    def get_cell(self, i, j):
        return self.cells[i][j]

    def get_cell_location(self, cell):
        return self.cells_locations[cell]

    def get_cells(self):
        return [c for row in self.cells for c in row]
