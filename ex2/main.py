import numpy
from GeneticAlgoAPI.chromosome import ListChromosomeBase
from GeneticAlgoAPI.crossover_strategy import SinglePointCrossover
from GeneticAlgoAPI.fitness_function import MistakesBasedFitnessFunc
from GeneticAlgoAPI.genetic_algorithm import GeneticAlgorithm, ApplyElitism
from GeneticAlgoAPI.mutation_strategy import BinaryMutation
from GeneticAlgoAPI.selection_strategy import RouletteWheelSelection
from config import MUTATION_RATE, CROSSOVER_RATE, POPULATION_SIZE, ELITISM
from graphics import show_mat
from run_ga import build_and_run


def calc_collisions(board):
    values = {i for row in board for i in row}
    collisions = {num: set() for num in values}
    for i in range(0, len(board)):
        for j in range(1, len(board[0]) - 1):
            center = board[i][j]
            right = board[i][j + 1]
            left = board[i][j - 1]
            if center != right:
                collisions[min(center, right)].add(max(center, right))
            if center != left:
                collisions[min(center, left)].add(max(center, left))

            # if not last row:
            if i < len(board) - 1:
                down = board[i + 1][j]
                if center != down:
                    collisions[min(center, down)].add(max(center, down))
    return collisions


with open("shape", 'r') as f:
    init_board = [[int(j.strip()) for j in [i.strip() for i in row.split(' ')] if j] for row in f]
collisions = calc_collisions(init_board)


class MapPaintChromosome(ListChromosomeBase):
    def __init__(self):
        super().__init__(24)
        # 4 colors
        # 2 bits to represent a color
        # 12 blocks

    def get_num_to_color(self):
        num_to_color = {}
        for shape_num, i in enumerate(range(0, len(self), 2)):
            g1, g2 = self[i:i + 2]
            color = int(''.join(map(str, [g1, g2])), 2)
            num_to_color[shape_num+1] = color
        return num_to_color

    def to_matrix(self):
        board = numpy.array(init_board)
        num_to_color = self.get_num_to_color()
        m = max(num_to_color) + 1
        for k, v in num_to_color.items():
            board[board == k] = m + v
        board = board - m
        return board


class MapPaintGA(RouletteWheelSelection, SinglePointCrossover, BinaryMutation, ApplyElitism,
                 MistakesBasedFitnessFunc, GeneticAlgorithm):
    def __init__(self, elitism=ELITISM,
                 mutation_rate=MUTATION_RATE,
                 crossover_rate=CROSSOVER_RATE,
                 population_size=POPULATION_SIZE):
        super().__init__()
        self.elitism = elitism
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population_size = population_size

    def calc_mistakes(self, chromosome):
        num_to_color = chromosome.get_num_to_color()
        errors = sum([1 for k, vals in collisions.items()
                      for v in vals
                      if num_to_color[k] == num_to_color[v]])
        return errors


def main():
    mutation_rate = MUTATION_RATE
    crossover_rate = CROSSOVER_RATE
    population_size = POPULATION_SIZE
    elitism_count = ELITISM

    time, chromo, gen = build_and_run(mutation_rate, crossover_rate, population_size, elitism_count,
                                      MapPaintGA, MapPaintChromosome)
    print("run for {:.2f} {} and {} generations".format(time, "seconds", gen+1))
    show_mat(chromo.to_matrix())


if __name__ == '__main__':
    main()
