from __future__ import annotations

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Controller import Controller

from abc import ABC
from random import Random
from typing import Dict, Set, List

import Action
from Building.Building import Building
from Civilization.Civilization import Civilization
from Farmable.Farmable import Farmable, Resource
from GameSetup.GameSetup import GameSetup


class DicesRoll:
    """
    Object DicesRoll which represent the dice
    """

    def __init__(self, rng: Random, n_meeple: int, divisor: int):
        """
        Constructor DicesRoll
        :param rng: random
        :param n_meeple: number of meeple
        :param divisor: divisor of place
        """
        self.divisor = divisor
        self.result = [rng.randint(0, 6) for _ in range(n_meeple)]
        self.tool_bonus = 0

    def compute_sum_result(self):
        """
        :return: result of dice with tool bonus
        """
        return sum(self.result) + self.tool_bonus

    def compute_resource_gain(self):
        """
        :return: result of dice divised by the resource divisor
        """
        return self.compute_sum_result() // self.divisor


class AbstractPlayer(metaclass=abc.ABCMeta):
    """
    Object AbstractPlayer which represent the player
    """

    def __init__(self, settings: GameSetup, color: str, nb_points: int):
        """
        Constructor AbstractPlayer
        :param settings: game setup of player
        :param color: color of player
        :param nb_points: point number of player
        """
        self.settings = settings
        self.color = color
        self.nb_points = nb_points
        self.stacks: Dict[Farmable, int] = dict(settings.player_setup.resource)
        self.stacks[settings.food] = settings.player_setup.nb_food
        for tool in settings.set_tools:
            self.stacks[tool] = 0
        self.stacks[settings.meeple] = settings.player_setup.nb_people
        self.stacks[settings.food_production] = settings.player_setup.nb_food_production
        self.buildings: Set[Building] = set()
        self.civilization: Set[Civilization] = set()

    def get_farmable_count(self, farmable: Farmable) -> int:
        """
        Give the farmable number of player
        :param farmable: farmable to count
        :return: farmable number of player
        """
        if farmable in self.stacks:
            return self.stacks[farmable]
        return 0

    def set_farmable_count(self, farmable: Farmable, value: int):
        """
        set dictionary, assigned the number of farmable
        :param farmable: farmable to count
        :param value: value of farmable
        """
        self.stacks[farmable] = value

    def add_to_farmable_count(self, farmable: Farmable, value: int):
        """
        add farmable to dictionary
        :param farmable: farmable to count
        :param value: value of farmable
        """
        count = self.get_farmable_count(farmable)
        self.stacks[farmable] = count + value

    def farm(self, farmable: Farmable, n_meeple: int, roll: DicesRoll):
        """
        enable farm the ressource        
        :parm farmable: farmable
        :parm n_meeple: number of meeple
        :parm roll: dice roll
        """
        self.stacks[farmable] += farmable.farm(n_meeple, roll)

    def get_resources(self) -> Dict[Resource, int]:
        return {r: self.stacks[r] for r in self.stacks if isinstance(r, Resource)}

    @abc.abstractmethod
    def do_action(self, rng: Random, state, possible_actions: List[Action.Action]):
        """
        Do action
        """
        pass

    def __hash__(self):
        return self.color.__hash__()

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.color == other.color

    def __str__(self):
        return self.color


class HumanPlayer(AbstractPlayer, ABC):
    """
    Object HumanPlayer which represent the human player
    """

    def __init__(self, game, color: str, nb_points: int, controller: Controller):
        """
        Constructor HumanPlayer
        :param game: game of player
        :param color: color of player
        :param nb_points: point number of player
        :param controller: controller of player
        """
        super().__init__(game.settings, color, nb_points)
        self.game = game
        self.controller = controller

    def do_action(self, rng: Random, state, possible_actions: List[Action.Action]):
        """
        Do action
        :param rng: random
        :param state: state at time of action
        :param possible_actions: list of possible actions
        :returns: action
        """
        action: Action.Action = None
        while action is None:
            from Game.Game import SubState
            if state == SubState.PLACE:
                action = self.controller.on_place_event(possible_actions)
            elif state == SubState.TAKE_OR_lET:
                action = self.controller.let_meeple_event(possible_actions)
                if action is None:
                    action = self.controller.on_take_event(possible_actions)
            elif state == SubState.USE_TOOL:
                action = self.controller.on_use_tool_event(possible_actions)
            elif state == SubState.PAY_OR_USE_POINTS:
                action = self.controller.choose_between_lose_points_or_resources_event(possible_actions)
            elif state == SubState.PAY:
                action = self.controller.on_pay_resource_event(possible_actions)
        return action

    def __str__(self):
        """
        :return: string Human + color
        """
        return '<Human: ' + self.color + '>'


class IAPlayer(AbstractPlayer, ABC):
    """
    Object IAPlayer which represent the artificial intelligence player
    """

    def __init__(self, settings: GameSetup, color: str, nb_points: int):
        """
        Constructor IAPlayer
        :param settings: game setup of player
        :param color: color of player
        :param nb_points: point number of player
        """
        super().__init__(settings, color, nb_points)

    def do_action(self, rng: Random, state, possible_actions: List[Action.Action]):
        """
        Do action
        :param rng: random
        :param state: state at time of action
        :param possible_actions: list of possible actions
        :returns: action
        """
        index = rng.randint(0, len(possible_actions) - 1)
        print('IA ' + self.color + ' a joué : ' + str(possible_actions[index]))
        return possible_actions[index]

    def __str__(self):
        """
        :return: string IA + color
        """
        return '<IA: ' + self.color + '>'
