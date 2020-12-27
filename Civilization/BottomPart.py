import abc
from abc import ABC
from enum import Enum


class BottomPart(metaclass=abc.ABCMeta):
    """
    Object BottomPart which represent the bottom the civilization card
    """

    @abc.abstractmethod
    def execute_reward(self):
        raise NotImplementedError


class Items(BottomPart, ABC):
    """
    Object Items which represent the names of items
    Children of Class BottomPart
    """

    def __init__(self, name: str):
        """
        Constructor of Items
        :param name: name of items
        """
        self.name = name

    def execute_reward(self):
        raise NotImplementedError


class MultiplierPoints(BottomPart, ABC):
    """
    Object MultiplierPoints which represent the multiplier value
    Children of Class BottomPart
    """

    def __init__(self, number: int, multipliable):
        """
        Constructor of MultiplierPoints
        :param number: number of points
        :param multipliable: numbeer of multiplier
        """
        if not isinstance(multipliable, Multipliable):
            raise TypeError('multipliable must be an instance of Multipliable Enum')
        self.number = number
        self.multipliable = multipliable

    def execute_reward(self):
        raise NotImplementedError


class Multipliable(Enum):
    """
    Enumeration
    """
    AGRICULTURE = 1
    BUILDING = 2
    TOOL = 3
    MEEPLES = 4
