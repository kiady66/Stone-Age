import abc
from abc import ABC
from typing import Set

from Farmable.Farmable import Resource


class UpperPart(metaclass=abc.ABCMeta):
    """
    Object UpperPart which represent the top the civilization card
    """

    @abc.abstractmethod
    def execute_reward(self):
        raise NotImplementedError


class ItemsDice(UpperPart, ABC):
    """
    Object ItemsDice which represent the dice with the resource
    Children of UpperPart
    """

    def __init__(self):
        self.resources_order: Set[Resource] = set()

    def execute_reward(self):
        raise NotImplementedError


class ResourceReward(UpperPart, ABC):
    """
    Object ResourceReward which represent the resource reward
    Children of UpperPart
    """

    def __init__(self, resource: Resource, numbers: int):
        """
        Constructor of ResourceReward
        :param resource: name of resource reward
        :param numbers: number of resource
        """
        self.resource = resource
        self.numbers = numbers

    def execute_reward(self):
        raise NotImplementedError


class ResourceDiceRoll(UpperPart, ABC):
    """
    Object ResourceDiceRoll which represent the dice roll with resource
    Children of UpperPart
    """

    def __init__(self, resource: Resource, number_dice: int):
        """
        Constructor of ResourceDiceRoll
        :param resource: name of resource
        :param number_dice: number on one side of the dice
        """
        self.resource = resource
        self.number_dice = number_dice

    def execute_reward(self):
        raise NotImplementedError


class Point(UpperPart, ABC):
    """
    Object Point which represent the point
    Children of UpperPart
    """

    def __init__(self, numbers: int):
        """
        Constructor of Point
        :param numbers: number of points
        """
        self.numbers = numbers

    def execute_reward(self):
        raise NotImplementedError


class NewTool(UpperPart, ABC):
    """
    Object NewTool which represent the tool
    Children of UpperPart
    """

    def __init__(self, numbers: int):
        """
        Constructor of NewTool
        :param numbers: number of tool points
        """
        self.numbers = numbers

    def execute_reward(self):
        raise NotImplementedError


class AdditionalFood(UpperPart, ABC):
    """
    Object AdditionalFood which represent the additional of food
    Children of UpperPart
    """

    def __init__(self, numbers: int):
        """
        Constructor of AdditionalFood
        :param numbers: number of food points
        """
        self.numbers = numbers

    def execute_reward(self):
        raise NotImplementedError


class AdditionalAgriculture(UpperPart, ABC):
    """
    Object AdditionalAgriculture which represent the additional of food
    Children of UpperPart
    """

    def __init__(self, numbers: int):
        """
        Constructor of AdditionalAgriculture
        :param numbers: number of food level
        """
        self.numbers = numbers

    def execute_reward(self):
        raise NotImplementedError


class AdditionalCard(UpperPart, ABC):
    """
    Object AdditionalCard which represent the card additional
    Children of UpperPart
    """

    def __init__(self, numbers: int):
        """
        Constructor of AdditionalCard
        :param numbers: number of card
        """
        self.numbers = numbers

    def execute_reward(self):
        raise NotImplementedError


class ToolsUnique(UpperPart, ABC):
    """
    Object ToolsUnique which represent a tool where you can use it only on time
    Children of UpperPart
    """

    def __init__(self, numbers: int):
        """
        Constructor of ToolsUnique
        :param numbers: number of tool points
        """
        self.numbers = numbers

    def execute_reward(self):
        raise NotImplementedError


class SelectedResource(UpperPart, ABC):
    """
    Object SelectedResource which represent the resource that the player can take
    Children of UpperPart
    """

    def __init__(self, numbers: int):
        """
        Constructor of SelectedResource
        :param numbers: number of resources
        """
        self.numbers = numbers

    def execute_reward(self):
        raise NotImplementedError
