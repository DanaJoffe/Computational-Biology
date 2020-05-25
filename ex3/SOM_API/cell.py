from typing import List, Iterable, Optional, Set

from SOM_API.content import Content


class Layer(object):
    def __init__(self, layer_cells: Iterable["Cell"], inside_cells=None):
        self.inside_cells = set(inside_cells) if inside_cells else set()
        self.layer_cells: Set[Cell] = set(layer_cells)

    def __iter__(self):
        return self.layer_cells.__iter__()

    def next_layer(self) -> Optional["Layer"]:
        """ return next layer """
        next_layer_cells = {n for c in self.layer_cells for n in c.neighbors} - self.inside_cells - self.layer_cells
        inside_cells = self.layer_cells
        return Layer(next_layer_cells, inside_cells) if next_layer_cells else None

    def set_content(self, content):
        for cell in self.layer_cells:
            cell.set_content(content)


class Cell(Layer):
    def __init__(self, content: Content):
        super().__init__([self])
        self._content = content
        self._neighbors: List[Cell] = []

    def add_neighbor(self, n: "Cell"):
        self._neighbors.append(n)
        return self

    @property
    def content(self):
        return self._content

    @property
    def neighbors(self) -> List["Cell"]:
        return self._neighbors

    def __str__(self):
        return self._content.__str__()

    def set_content(self, content):
        self._content = content
