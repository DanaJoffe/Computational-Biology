from abc import abstractmethod, ABC


class Content(ABC):
    @abstractmethod
    def __str__(self):
        raise NotImplemented

    @abstractmethod
    def dist_from(self, other: "Content") -> float:
        """ returns the distance between self & other """
        raise NotImplemented

    @abstractmethod
    def approach_other(self, other: "Content", learn_func):
        """ get self closer to other """
        raise NotImplemented
