import abc
import string
from abc import ABC
from typing import Set, cast, Dict

from numpy.core.defchararray import isnumeric

import Controller
import Place
from Game.Game import State, GameData
from Place import AbstractPlace
from Player import AbstractPlayer


class View(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def update(self, game: GameData):
        pass


class TextUI(View, ABC):
    def __init__(self, places: Set[AbstractPlace], controller: Controller):
        super().__init__()
        self.controller: Controller = controller
        self.places_map = {}
        for place in places:
            if isinstance(place, Place.UpperPartPlace):
                self.places_map[cast(Place.UpperPartPlace, place).name] = place
            elif isinstance(place, Place.BuildingPlace):
                self.places_map['B' + str(cast(Place.BuildingPlace, place).ordinal)] = place
            elif isinstance(place, Place.CivilizationPlace):
                self.places_map['C' + str(cast(Place.BuildingPlace, place).ordinal)] = place
            else:
                raise RuntimeError
        controller.on_place_event_action = self.get_place_with_n
        controller.on_take_event_action = lambda: self.place_for_take_selected
        controller.on_use_tool_event_action = self.ask_use_tool
        controller.let_meeple_event_action = self.ask_let_meeple
        controller.choose_between_lose_points_or_resources_event_action = self.ask_use_resources_or_points
        controller.on_pay_resource_event_action = self.ask_pay_resource

    def get_place_with_n(self):
        while True:
            text = input()
            split = text.split(' ')
            if len(split) < 2:
                continue
            name = ' '.join(split[:len(split) - 1])
            val = split[len(split) - 1]
            if not isnumeric(val) or name not in self.places_map:
                continue
            return self.places_map[name], int(val)

    def ask_let_meeple(self):
        while True:
            text = input()
            if text == 'laisser':
                self.place_for_take_selected = None
                return True
            if text not in self.places_map:
                continue
            self.place_for_take_selected = self.places_map[text]
            return False

    @staticmethod
    def ask_use_tool():
        print('Entrez le nombre d\'outils à utiliser')
        while True:
            text = input()
            if not isnumeric(text) or int(text) < 0:
                continue
            return int(text)
    @staticmethod
    def ask_use_resources_or_points():
        print('Payer vos dettes avec des resources ou des points ? Entrez "Oui" pour utiliser des resources.')
        return input() == 'Oui'

    @staticmethod
    def ask_pay_resource():
        print('Choisissez une ressource pour payer parmi les ressources que vous avez')
        return input()

    def update(self, data: GameData):
        if data.roll is not None:
            roll = data.roll
            res = roll.result
            tool_b = str(roll.tool_bonus)
            div = str(roll.divisor)
            gain = str(roll.compute_resource_gain())
            print(f'({res} + {tool_b}) / {div} = {gain}')
        else:
            self.print_data(data)

    def print_data(self, data: GameData):
        if data.is_end:
            print('Fin du jeu')
        else:
            print('Tour ' + str(data.turn))
            print('Zones :')
            print('  Normales :')
            for place in data.game_board.places:
                print('    ' + place.name + ' -> ' + str_player_int_dict(place.meeples))
            print('  Buildings :')
            for place in data.game_board.building_places:
                print('    Building ' + str(place.ordinal) + ' -> ' + str_player_int_dict(place.meeples))
            print('  Civilizations :')
            for place in data.game_board.civilization_places:
                print('    Civilization ' + str(place.ordinal) + ' -> ' + str_player_int_dict(place.meeples))
            print('Joueurs :')
            for p in data.players:
                print('  ' + str(p) + ':')
                print('    Points: ' + str(p.nb_points))
                print('    Stacks')
                print('      ' + str({str(s) + ': ' + str(p.stacks[s]) for s in p.stacks}))
            print('Joueurs dans l\'ordre :')
            for p in data.players:
                print(str(p))
            print('C\'est le tour du joueur ' + str(data.current_player))
            if data.state == State.PLACE_MEEPLES:
                print('Sélectionnez une zone et un nombre de meeples')
            elif data.state == State.TAKE_MEEPLES:
                print('Sélectionnez une zone pour prendre des meeples ou entrez "laisser"')
            else:
                if data.debt is not None:
                    print(f'{data.current_player} a {data.debt} de dette')


def str_player_int_dict(d: Dict[AbstractPlayer, int]):
    return str({str(p) + ': ' + str(d[p]) for p in d})
