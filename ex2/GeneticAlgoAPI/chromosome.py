import random
from abc import ABC, abstractmethod
"""
a chromosome implementation shouldn't inherit from Chromosome class, but from it's subclasses.
"""


class IndexedObject(ABC, object):
    """ an object that can be accessed and changes via indexes"""
    @abstractmethod
    def __getitem__(self, k):
        """  """
        raise NotImplemented

    @abstractmethod
    def __setitem__(self, key, value):
        """  """
        raise NotImplemented

    @abstractmethod
    def __len__(self):
        """  """
        raise NotImplemented


class Chromosome(IndexedObject, ABC):
    fitness = None
    genome = None

    def set_fitness_score(self, score):
        self.fitness = score

    def get_fitness(self):
        return self.fitness

    def __repr__(self):
        fitness = self.get_fitness()
        if fitness:
            return "({}) {}".format(str(fitness), str(self))
        return str(self)

    def __copy__(self):
        class_type = self.__class__
        instance = class_type()
        instance.genome = self.genome.copy()
        return instance


class ListChromosomeBase(Chromosome, ABC):
    """ chromosome that have a list as inner representation """
    def __init__(self, length):
        """ initialize random bit list """
        num = random.randint(0, 2 ** length - 1)
        bit_string = bin(num)[2:]
        bit_string = '0' * (length - len(bit_string)) + bit_string
        bit_list = [int(num) for num in list(bit_string)]
        self.genome = bit_list

    def __getitem__(self, k):
        return self.genome.__getitem__(k)

    def __setitem__(self, key, value):
        self.genome.__setitem__(key, value)

    def __len__(self):
        return self.genome.__len__()

    def __str__(self):
        return ','.join(str(v) for v in self.genome)
