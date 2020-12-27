from __future__ import annotations

import abc
from abc import ABC
from typing import Dict, List
from typing import TYPE_CHECKING

from Building.Building import Building
from Civilization.Civilization import Civilization

if TYPE_CHECKING:
    from Player import AbstractPlayer


class AbstractPlace(metaclass=abc.ABCMeta):
    """
    Object AbstractPlace which represent the place
    """

    def __init__(self, name: str, nb_place: int):
        """
        Constructor AbstractPlace
        :param name: name of place
        :param nb_place: number of place
        """
        self.name = name
        self.nb_place = nb_place
        self.meeples: Dict[AbstractPlayer, int] = dict()

    def clear_meeples(self):
        """
        Clear dictionary meeples
        """
        self.meeples = dict()

    def set_meeples(self, player: AbstractPlayer, n: int):
        """
        set dictionary meeples
        :param player: player who owns the meeple
        :param n: number of mepples
        """
        self.meeples[player] = n

    def add_meeples(self, player: AbstractPlayer, n: int):
        """
        add meeple to dictionary
        :param player: player who owns the meeple
        :param n: number of meeple
        """
        if player in self.meeples:
            self.meeples[player] += n
        else:
            self.set_meeples(player, n)

    def has_meeple_from_player(self, player: AbstractPlayer) -> bool:
        """
        if the player have meeples
        :param player: player who owns the meeple
        """
        if player in self.meeples:
            return self.meeples[player] > 0
        return False

    def get_place_left(self) -> int:
        """
        Give the number of place if there are that possible spaces
        :return: number of place - sum of meeples
        """
        if self.nb_place == -1:
            return 999
        sum_meeples = 0
        for n in self.meeples.values():
            sum_meeples += n
        return self.nb_place - sum_meeples

    def has_place_left(self) -> bool:
        """
        If the place have enough space
        """
        return self.get_place_left() > 0


class BuildingPlace(AbstractPlace, ABC):
    """
    Object BuildingPlace
    Children of AbstractPlace
    """

    def __init__(self, name: str, nb_place: int, nb_player: int, nb_stacks: int, ordinal: int,
                 nb_building_per_stack: int):
        """
        Constructor of BuildingPlace
        :param name: name of palce
        :param nb_place: number of place
        :param nb_player: number of player
        :param nb_stacks: number of stack
        :param ordinal: ordinal of BuildingPlace
        :param nb_building_per_stack: number of building per stack
        """
        super().__init__(name, nb_place)
        self.ordinal = ordinal
        self.nb_player = nb_player
        self.nb_stacks = nb_stacks
        self.nb_building_per_stack = nb_building_per_stack
        self.buildings: List[Building] = []

    def clear_buildings(self):
        """
        Clear dictionary building
        """
        self.buildings = []


class CivilizationPlace(AbstractPlace, ABC):
    """
    Object CivilizationPlace
    Children of AbstractPlace
    """

    def __init__(self, name: str, nb_place: int, ordinal: int, nb_resource: int):
        """
        Constructor of CivilizationPlace
        :param name: name of place
        :param nb_place: number of place
        :param ordinal: ordinal of CivilizationPlace
        :param nb_resource: number of resource
        """
        super().__init__(name, nb_place)
        self.ordinal = ordinal
        self.nb_resource = nb_resource
        self.civilizations: List[Civilization] = []

    def clear_civilizations(self):
        """
        Clear dictionary civilization
        """
        self.civilizations = []


class UpperPartPlace(AbstractPlace, ABC):
    """
    Object UpperPartPlace
    Children of AbstractPlace
    """

    def __init__(self, name: str, nb_place: int):
        """
        Constructor of UpperPartPlace
        :param name: name of place
        :param nb_place: number of place
        """
        super().__init__(name, nb_place)
