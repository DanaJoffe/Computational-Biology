import math
import random
from copy import copy
from typing import Type, List
import numpy as np
from SOM_API.content import Content
from SOM_API.net import GridNet, Net
from animation import CellAnimation, GUIanimation
from graphics import show_mat


def parse_digits():
    all_digits = []
    with open("Digits_Ex3.txt", 'r') as f:
        board = []
        for row in f:
            if not row.strip() and board:
                board = np.array(board)
                all_digits.append(board)
                board = []
            else:
                board.append([int(n) for n in row.strip()])
    return all_digits


def visualize_dataset():
    all_digits = parse_digits()
    comb = np.concatenate([np.concatenate(all_digits[i:i+10], axis=1)
                           for i in range(0, 100, 10)], axis=0)
    show_mat(comb)


# def check():
#     class Number(Content):
#         def __init__(self, n=0):
#             self.n = n#random.randint(0, 1)
#
#         def __str__(self):
#             return str(self.n)
#
#     net = GridNet(6, 6)
#     net.init(Number)
#     print(net)
#     while 1:
#         i, j = [int(inp.strip()) for inp in input().split(',')]
#         curr_layer = net.get_cell(i, j)
#         curr_layer.set_content(Number(1))
#         print(net)
#
#         next_layer = curr_layer.next_layer()
#         while next_layer:
#             curr_layer.set_content(Number(0))
#             curr_layer = next_layer
#             curr_layer.set_content(Number(1))
#             print(net)
#             next_layer = curr_layer.next_layer()
#         curr_layer.set_content(Number(0))
#         print(net)


# def show_net(net):
#     """ domain specific """
#     contents = [c.content.get_mat() for c in net.get_cells()]
#     comb = np.concatenate([np.concatenate(contents[i:i + net.columns], axis=1)
#                            for i in range(0, net.rows * net.columns, net.rows)], axis=0)
#     show_mat(comb)


""" CODE """


class BinNumMat(Content):
    def __init__(self, mat=None):
        self.r = 10
        self.c = 10
        self.n = mat if mat is not None else [[random.uniform(0, 1) for _ in range(self.c)] for _ in range(self.r)]
        self.n = np.array(self.n)

    def __str__(self):
        ret = ""
        for row in self.n:
            ret += ''.join([str(c) for c in row]) + '\n'
        return ret

    def get_mat(self):
        # return np.array(self.n)
        return self.n

    def dist_from(self, other: "BinNumMat"):
        """
        returns the distance between self & other = amount of mismatches

        calculates distance by sum squared distances of all features
        """
        return sum((self.n[i][j] - other.n[i][j]) ** 2 for i in range(self.r) for j in range(self.c))

    def approach_other(self, other: "BinNumMat", learn_func):
        for i in range(self.r):
            for j in range(self.c):
                error = other.n[i][j] - self.n[i][j]
                self.n[i][j] += learn_func(error)


class DomainNet(GridNet):
    def get_repr(self):
        contents = [c.content.get_mat() for c in self.get_cells()]
        comb = np.concatenate([np.concatenate(contents[i:i + self.columns], axis=1)
                               for i in range(0, self.rows * self.columns, self.columns)], axis=0)
        return comb


class SOM(object):
    def __init__(self, net: Net, examples: List[Content], content_class: Type[Content], epochs=math.inf):
        self._epochs = epochs
        self._net = net
        self._net.init(content_class)
        self.x = examples
        self._init_examples = copy(examples)
        self.board = self._net.get_repr()
        self.epoch = 0
        self.set_params()

    def set_params(self, learning_rate=None, h_func=None, layers_affected=1.0, calc_amendment_func=None, epochs=None,
                   shuffle_examples_each_epoch=True):
        self._h = h_func if h_func else lambda layer, time: 0.5 ** layer
        self._lr = learning_rate if learning_rate else lambda time: 0.4
        self._layers_affected = layers_affected
        self._calc_amendment_func = calc_amendment_func if calc_amendment_func else self._get_learn_func
        self.shuffle = shuffle_examples_each_epoch
        if epochs:
            self._epochs = epochs

    def _get_learn_func(self, layer, lr=None, h=None, time=None):
        """
        default implementation for amendment creation

        time is ignored
        """
        lr = lr or self._lr
        h = h or self._h
        time = time or self.epoch

        def learn_func(error):
            return lr(time) * h(layer, time) * error

        return learn_func

    def _train(self, xi):
        cells = self._net.get_cells()
        errors = [c.content.dist_from(xi) for c in cells]
        indx = np.argmin(errors)
        # get representative
        layer = cells[indx]
        l = 0
        while layer:
            if l > self._layers_affected:
                break
            # get layer closer to xi
            lf = self._calc_amendment_func(l, lr=self._lr, h=self._h, time=self.epoch)
            for cell in layer:
                cell.content.approach_other(xi, lf)
            layer = layer.next_layer()
            l += 1

    def test(self):
        """
        for each example get representation coordinates

        :return the location of example's representations & the grade (sum of distances)
        """
        cells = self._net.get_cells()
        locations = []
        grade = 0
        for xi in self._init_examples:
            distances = [c.content.dist_from(xi) for c in cells]
            indx = np.argmin(distances)
            grade += distances[indx]
            cell = cells[indx]
            i, j = self._net.get_cell_location(cell)
            locations.append((i, j))
        return grade, locations


    @property
    def epochs(self):
        return self._epochs

    def run_epoch_generator(self):
        """ run a hole epoch and yield a board after each example """
        if self.epoch >= self._epochs:
            return self._net.get_repr()
        self.epoch += 1
        if self.shuffle:
            random.shuffle(self.x)
        for xi in self.x:
            self._train(xi)
            self.board = self._net.get_repr()
            yield self.board

    def run_epoch(self):
        self.epoch += 1
        if self.shuffle:
            random.shuffle(self.x)
        for xi in self.x:
            self._train(xi)
            self.board = self._net.get_repr()

    def __str__(self):
        return str(self._net)


def run_som(som):
    """ plot the board every epoch """
    for epoch in range(min(som.epochs, 1000)):
        som.run_epoch()
        show_mat(som.board)


def animate_som(som):
    c = GUIanimation(som)
    c.start()


def main():
    # todo: change params, try to be time-dependent

    # parameters
    rows, columns = 6,6
    layers_affected = 1  # for no layer-limitation put 'math.inf'
    epochs = math.inf
    learning_rate = lambda time: 0.4
    h_func = lambda layer, time: 0.5 ** layer  # 60%
    calc_amendment_func = lambda layer, lr, h, time: lambda error: lr(time) * h(layer, time) * error

    s = SOM(DomainNet(rows, columns), [BinNumMat(e) for e in parse_digits()], BinNumMat)

    s.set_params(learning_rate=learning_rate,
                 h_func=h_func,
                 layers_affected=layers_affected,
                 calc_amendment_func=calc_amendment_func,
                 epochs=epochs,
                 shuffle_examples_each_epoch=True)

    # run_som(s)
    animate_som(s)


if __name__ == '__main__':
    # visualize_dataset()
    main()

