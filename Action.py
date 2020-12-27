import abc
from abc import ABC
from enum import Enum
from typing import Dict

from Farmable.Farmable import Resource


class ActionType(Enum):
    """
    Object ActionType which represent the type of action
    """

    PLACE_MEEPLES = 0
    TAKE_MEEPLES = 1
    LET_ALL_MEEPLES = 2
    PAY_SINGLE_RESOURCE_COST = 3
    PAY_RESOURCE_OR_POINTS = 4
    USE_TOOL = 5
    DO_NOTHING = 6


class Action(metaclass=abc.ABCMeta):
    """
    Object Action which represent all the possible actions
    """

    def __init__(self, action_type: ActionType):
        """
        Constructor of Action
        :param action_type: type of action
        """
        self.action_type = action_type


class PlaceMeeplesAction(Action, ABC):
    """
    Object PlaceMeeplesAction which represent the action to place meeple
    Children of Action
    """

    def __init__(self, place, nb_meeple: int):
        """
        Constructor of PlaceMeeplesAction
        :param place: place of meeple
        :param nb_meeple: number of meeple
        """
        super().__init__(ActionType.PLACE_MEEPLES)
        self.place = place
        self.nb_meeple = nb_meeple

    def __str__(self):
        return 'Place ' + str(self.nb_meeple) + ' meeples in ' + self.place.name


class LetAllMeeplesAction(Action, ABC):
    """
    Object LetAllMeeplesAction
    Children of Action
    """

    def __init__(self):
        super().__init__(ActionType.LET_ALL_MEEPLES)

    def __str__(self):
        return 'Let all meeples'


class DoNothingAction(Action, ABC):
    """
    Object DoNothingAction
    Children of Action
    """

    def __init__(self):
        """
        Constructor of DoNothingAction
        """
        super().__init__(ActionType.DO_NOTHING)

    def __str__(self):
        return 'Do nothing'


class TakeMeeplesAction(Action, ABC):
    """
    Object TakeMeeplesAction which represent the action to take meeple
    Children of Action
    """

    def __init__(self, place):
        """
        Constructor of TakeMeeplesAction
        :param place: place of meeple
        """
        super().__init__(ActionType.TAKE_MEEPLES)
        self.place = place


class PayResourceOrPointsAction(Action, ABC):
    """
    Object PayResourceOrPointsAction which represent the action to pay resource or points
    Children of Action
    """

    def __init__(self, pay_resource: bool):
        """
        Constructor of PayResourceOrPointsAction
        :param pay_resource: pay resource
        """
        super().__init__(ActionType.PAY_RESOURCE_OR_POINTS)
        self.pay_resource = pay_resource

    def __str__(self):
        return 'Pay resource :' + str(self.pay_resource)

class PaySingleResourceAction(Action, ABC):
    """
    Object PaySingleResourceAction which represent the action to pay a single resource
    Children to Action
    """

    def __init__(self, resource: Resource):
        """
        Constructor of PaySingleResourceAction
        :param resource: type of resource
        """
        super().__init__(ActionType.PAY_SINGLE_RESOURCE_COST)
        self.resource = resource

    def __str__(self):
        return 'Pay ' + str(self.resource)


class UseToolAction(Action, ABC):
    """
    Object UseToolAction which represent the action to use a tool
    Children of Action
    """

    def __init__(self, nb_tools: int):
        """
        Constructor to UseToolAction
        :param nb_tools: number of tools
        """
        super().__init__(ActionType.USE_TOOL)
        self.nb_tools = nb_tools

    def __str__(self):
        return 'Use tools level ' + str(self.nb_tools)
