from __future__ import annotations

from typing import TYPE_CHECKING

import Place

if TYPE_CHECKING:
    import random

    from Controller import Controller
    from GameSetup import GameSetup
    from GameSetup.GameBoardSetup import GameBoardSetup

    from UI import View
from enum import Enum
import abc
import random
from Player import AbstractPlayer, HumanPlayer, IAPlayer, DicesRoll
import Action
import typing
from typing import Set, List
from Building.Building import Building, SpecificResourcesBuilding, SumOfDivisorBuilding
from Civilization.Civilization import Civilization
from Place import UpperPartPlace, BuildingPlace, CivilizationPlace, AbstractPlace
from Farmable.Farmable import Resource, Farmable, FarmableWithDivisor


class State(Enum):
    PLACE_MEEPLES = 0
    TAKE_MEEPLES = 1
    FEED_MEEPLES = 2


class SubState(Enum):
    PLACE = 0
    TAKE_OR_lET = 1
    USE_TOOL = 2
    PAY_OR_USE_POINTS = 3
    PAY = 4


class GameData:
    def __init__(self, is_end: bool, turn: int, current_player: str, players: List[AbstractPlayer], state: State,
                 game_board, roll: DicesRoll, debt: int):
        self.debt = debt
        self.roll = roll
        self.is_end = is_end
        self.turn = turn
        self.current_player: str = current_player
        self.state: State = state
        self.players: List[AbstractPlayer] = players
        self.game_board: GameBoard = game_board


class Game:
    def __init__(self, settings: GameSetup, controller: Controller):
        self.view: View = None
        self.rng = random.Random()
        self.settings: GameSetup = settings

        players: Set[AbstractPlayer] = set()
        players.add(HumanPlayer(self, self.settings.player_colors[0], 0, controller))
        for index in range(1, len(self.settings.player_colors)):
            players.add(IAPlayer(self.settings, self.settings.player_colors[index], 0))

        self.players_in_order = [p for p in players if isinstance(p, HumanPlayer)]
        self.players_in_order += players - set(self.players_in_order)
        self.game_board = GameBoard(
            self.rng.sample(settings.set_buildings, len(settings.set_buildings)),
            self.rng.sample(settings.set_civilizations, len(settings.set_civilizations)),
            self.settings.game_board_setup
        )
        self.turns = 1
        self.state: State = None
        self.current_player: AbstractPlayer = self.players_in_order[0]

    def __update_view(self, roll: DicesRoll = None, debt: int = None):
        data = GameData(self.is_end(), self.turns, self.current_player.color, list(self.players_in_order), self.state,
                        self.game_board, roll, debt);
        self.view.update(data)

    def play_IA(self):
        # Loop until every player has no meeple left
        for self.current_player in self.players_in_order:
            if isinstance(self.current_player, HumanPlayer):
                continue
            if self.current_player.get_farmable_count(self.settings.meeple) <= 0:
                continue
            actions = self.__generate_place_actions()
            selected_action = self.current_player.do_action(self.rng, self, actions)
            if selected_action.action_type == Action.ActionType.DO_NOTHING:
                continue
            self.__execute_place_action(selected_action)
            self.view.update()
        self.current_player = self.players_in_order[0]
        evreyone_play = True
        # Si pour tout les joueurs
        for player in self.players_in_order:
            # Si l'un des joueur n'a pas joué
            if player.get_farmable_count(self.settings.meeple) != 0:
                evreyone_play = False
        # Si on a deja placer tout les meeples
        if evreyone_play:
            # On passe a la phase prendre
            self.state = State.TAKE_MEEPLES
        # Sinon
        else:
            # Si le joueur n'a plus de meeple
            if self.current_player.get_farmable_count(self.settings.meeple) <= 0:
                # Alors c'est envors au tour de l'IA
                self.play_IA()

    def run(self):
        while not self.is_end():
            self.__place_meeples_state()
            self.__take_meeples_state()
            self.__feed_meeples_state()
            self.players_in_order.append(self.players_in_order.pop(0))
            self.turns += 1

    def __place_meeples_state(self):
        self.state = State.PLACE_MEEPLES
        # Loop until every player has no meeple left
        while sum([p.get_farmable_count(self.settings.meeple) for p in self.players_in_order]) != 0:
            for self.current_player in self.players_in_order:
                if self.current_player.get_farmable_count(self.settings.meeple) <= 0:
                    continue
                actions = self.__generate_place_actions()
                self.__update_view()
                selected_action = self.current_player.do_action(self.rng, SubState.PLACE, actions)
                if selected_action.action_type == Action.ActionType.DO_NOTHING:
                    continue
                self.__execute_place_action(selected_action)

    def __take_meeples_state(self):
        self.state = State.TAKE_MEEPLES
        for self.current_player in self.players_in_order:
            self.__one_player_take_meeples()

    def __one_player_take_meeples(self):
        actions = self.__generate_take_actions()
        while True:
            self.__update_view()
            selected_action = self.current_player.do_action(self.rng, SubState.TAKE_OR_lET, actions)
            if selected_action.action_type == Action.ActionType.TAKE_MEEPLES:
                self.__execute_take_action(selected_action)
            elif selected_action.action_type == Action.ActionType.LET_ALL_MEEPLES:
                self.__execute_let_all_meeples_action()
            else:
                raise RuntimeError
            actions = self.__generate_take_actions()
            if len(actions) == 1:  # Will always generate let all meeples action
                break

    def __feed_meeples_state(self):
        self.state = State.FEED_MEEPLES
        for self.current_player in self.players_in_order:
            n_meeple = self.current_player.get_farmable_count(self.settings.meeple)
            food_prod = self.current_player.get_farmable_count(self.settings.food_production)
            cost = n_meeple - food_prod
            current_food = self.current_player.get_farmable_count(self.settings.food)
            if current_food < cost:
                self.current_player.set_farmable_count(self.settings.food, 0)
                debt = cost - current_food
                resources = self.current_player.get_resources()
                if sum([resources[r] for r in resources]) < debt:
                    self.current_player.nb_points -= 10
                else:
                    ask_use_resources = [Action.PayResourceOrPointsAction(True),
                                         Action.PayResourceOrPointsAction(False)]
                    self.__update_view(debt=debt)
                    action = self.current_player.do_action(self.rng, SubState.PAY_OR_USE_POINTS, ask_use_resources)
                    if typing.cast(Action.PayResourceOrPointsAction, action).pay_resource:
                        resources_to_pay: typing.Dict[Resource, int] = dict()
                        while debt > 0:
                            cost_actions = self.__generate_pay_actions_from_all_resources()
                            action: Action.PaySingleResourceAction = self.current_player.do_action(self.rng,
                                                                                                   SubState.PAY,
                                                                                                   cost_actions)
                            if action.resource in resources_to_pay:
                                resources_to_pay[action.resource] += 1
                            else:
                                resources_to_pay[action.resource] = 1
                            debt -= 1
                        for reso in resources_to_pay:
                            self.current_player.add_to_farmable_count(reso, -resources_to_pay[reso])
                    else:
                        self.current_player.nb_points -= 10
                self.__update_view()
            else:
                self.current_player.add_to_farmable_count(self.settings.food, -cost)

    def __generate_pay_actions_from_all_resources(self) -> List[Action.PaySingleResourceAction]:
        resources = self.current_player.get_resources()
        return [Action.PaySingleResourceAction(r) for r in resources if resources[r] > 0]

    def __generate_place_actions(self) -> typing.List[Action.Action]:
        assert self.current_player.get_farmable_count(self.settings.meeple) > 0
        actions = []
        for place in self.game_board.places:
            if self.current_player in place.meeples and place.meeples[self.current_player] != 0:
                continue
            if place.name == 'Hut':
                if place.has_place_left() and self.current_player.get_farmable_count(self.settings.meeple) >= 2:
                    actions.append(Action.PlaceMeeplesAction(place, 2))
                continue
            place_left: int = place.get_place_left()
            for n in range(1, place_left + 1):
                if self.current_player.get_farmable_count(self.settings.meeple) >= n:
                    actions.append(Action.PlaceMeeplesAction(place, n))
                else:
                    break
        for place in self.game_board.building_places:
            if place.has_place_left():
                actions.append(Action.PlaceMeeplesAction(place, 1))
        for place in self.game_board.civilization_places:
            if place.has_place_left():
                actions.append(Action.PlaceMeeplesAction(place, 1))
        return actions

    def __generate_take_actions(self) -> typing.List[Action.Action]:
        places = [place for place in self.game_board.get_all_places() if
                  place.has_meeple_from_player(self.current_player)]
        return [Action.TakeMeeplesAction(place) for place in places] + [Action.LetAllMeeplesAction()]

    def is_end(self):
        return sum([len(p.civilizations) for p in self.game_board.civilization_places]) == 0 or sum(
            [len(p.buildings) for p in self.game_board.building_places]) == 0

    def __execute_place_action(self, action: Action.Action):
        assert action.action_type == Action.ActionType.PLACE_MEEPLES
        place_action = typing.cast(Action.PlaceMeeplesAction, action)
        assert place_action.place.has_place_left()
        place_action.place.add_meeples(self.current_player, place_action.nb_meeple)
        self.current_player.add_to_farmable_count(self.settings.meeple, -place_action.nb_meeple)

    def __execute_let_all_meeples_action(self):
        places = [place for place in self.game_board.get_all_places() if
                  place.has_meeple_from_player(self.current_player)]
        for place in places:
            meeples = place.meeples[self.current_player]
            place.set_meeples(self.current_player, 0)
            self.current_player.add_to_farmable_count(self.settings.meeple, meeples)

    def __execute_take_action(self, action: Action.Action):
        assert action.action_type == Action.ActionType.TAKE_MEEPLES
        take_action = typing.cast(Action.TakeMeeplesAction, action)
        n_meeple = take_action.place.meeples[self.current_player]
        take_action.place.set_meeples(self.current_player, 0)
        if isinstance(take_action.place, BuildingPlace):
            self.__manage_building(take_action.place)
        elif isinstance(take_action.place, CivilizationPlace):
            self.__manage_civilization(take_action.place)
        else:
            farmable = self.get_resource_from_place(take_action.place)
            if isinstance(farmable, FarmableWithDivisor):
                roll = DicesRoll(self.rng, n_meeple, farmable.divisor)
                self.__update_view(roll=roll)
                tools = [Action.UseToolAction(n) for n in
                         range(1 + self.current_player.get_farmable_count(list(self.settings.set_tools)[0]))]
                use_tool: Action.UseToolAction = self.current_player.do_action(self.rng, SubState.USE_TOOL, tools)
                roll.tool_bonus = use_tool.nb_tools
                self.__update_view(roll=roll)
            else:
                self.__update_view()
                roll = None
            self.current_player.farm(farmable, n_meeple, roll)
        self.current_player.add_to_farmable_count(self.settings.meeple, n_meeple)

    def get_resource_from_place(self, place: UpperPartPlace) -> Farmable:
        all_resources: Set[Resource] = self.settings.set_resources
        matching_resources = [r for r in all_resources if r.place == place]
        if len(matching_resources) != 0:
            return matching_resources[0]
        elif self.settings.food.place == place:
            return self.settings.food
        elif self.settings.meeple.place == place:
            return self.settings.meeple
        elif self.settings.food_production.place == place:
            return self.settings.food_production
        elif list(self.settings.set_tools)[0].place == place:
            return list(self.settings.set_tools)[0]
        else:
            raise NotImplementedError

    def __manage_building(self, place: BuildingPlace):
        """
        condition de payement
        """
        return
        dict_resources: typing.Dict[Resource, int]
        building: Building = place.buildings[0]
        if isinstance(building, SpecificResourcesBuilding):
            self.current_player.nb_points += 10  # TODO specific cost
        elif isinstance(building, SumOfDivisorBuilding):
            self.current_player.nb_points += sum([dict_resources[r] * r.divisor for r in dict_resources])
        self.current_player.buildings.add(building)
        place.buildings.pop(0)

    def __manage_civilization(self, place):
        pass

    def place_meeple(self, place: Place, nb_meeple: int):
        place.meeples[self.current_player] = nb_meeple


class PlayerIter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def next(self) -> AbstractPlayer:
        pass

    @abc.abstractmethod
    def has_next(self) -> bool:
        pass


class SingleIterationPlayerIter(PlayerIter, abc.ABC):
    def __init__(self, players: List[AbstractPlayer]):
        self.players = list(players)

    def has_next(self):
        return len(self.players) > 0

    def next(self) -> AbstractPlayer:
        return self.players.pop(0)


class EndlessPlayerIter(PlayerIter, abc.ABC):
    def __init__(self, players: List[AbstractPlayer]):
        self.players = list(players)
        self.i = 0

    def has_next(self):
        return True

    def next(self) -> AbstractPlayer:
        player = self.players[self.i]
        self.i += 1
        if self.i == len(self.players):
            self.i = 0
        return player


class GameBoard:
    def __init__(self, buildings: List[Building], civilizations: List[Civilization],
                 game_board_setup: GameBoardSetup):
        self.game_board_setup = game_board_setup
        self.places: Set[UpperPartPlace] = set(game_board_setup.places)
        self.civilization_places: List[CivilizationPlace] = list(game_board_setup.civilization_places)
        self.building_places: List[BuildingPlace] = list(game_board_setup.building_places)
        for place in self.game_board_setup.places:
            place.clear_meeples()
        for place in self.game_board_setup.building_places:
            place.clear_meeples()
            place.clear_buildings()
        for place in self.game_board_setup.civilization_places:
            place.clear_meeples()
            place.clear_civilizations()
        while len(buildings) != 0:
            for place in self.game_board_setup.building_places:
                if len(buildings) == 0:
                    break
                place.buildings.append(buildings.pop())
        while len(civilizations) != 0:
            for place in self.game_board_setup.civilization_places:
                if len(civilizations) == 0:
                    break
                place.civilizations.append(civilizations.pop())

    def get_place(self, name: str) -> UpperPartPlace:
        return [place for place in self.places if place.name == name][0]

    def get_all_places(self) -> List[AbstractPlace]:
        places = list(self.places)
        places += self.building_places
        places += self.civilization_places
        return places

    def get_nb_meeple_in_board(self, player: AbstractPlayer):
        nb_sum = 0
        for place in self.get_all_places():
            if place.meeples.__contains__(player):
                nb_sum += place.meeples[player]
        return nb_sum
