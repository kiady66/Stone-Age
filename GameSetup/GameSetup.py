from typing import Set

from Building.Building import Building
from Civilization import Civilization
from Farmable.Farmable import Food, Resource, Tool, Meeple, FoodProduction
from GameSetup.GameBoardSetup import GameBoardSetup
from GameSetup.PlayerSetup import PlayerSetup


class GameSetup:
    """
    Object GameSetup which represent the settings of the game
    """

    def __init__(self,
                 name: str,
                 min_player: int,
                 max_player: int,
                 food: Food,
                 player_setup: PlayerSetup,
                 game_board_setup,
                 meeple: Meeple,
                 food_production: FoodProduction):
        """
        Constructor of GameSetup
        :param name: name of the game
        :param min_player: minimum of player on the game
        :param max_player: maximum of player on the game
        :param food: food of game
        :param player_setup: parameters of player
        :param game_board_setup: parameters of gameboard
        :param meeple: meeple of game
        :param food_production: production of food
        """
        self.game_name = name
        self.min_player = min_player
        self.max_player = max_player
        self.player_colors: str[4] = []
        self.set_resources: Set[Resource] = set()
        self.set_tools: Set[Tool] = set()
        self.set_civilizations: Set[Civilization] = set()
        self.set_buildings: Set[Building] = set()
        self.food = food
        self.player_setup = player_setup
        self.game_board_setup: GameBoardSetup = game_board_setup
        self.meeple: Meeple = meeple
        self.food_production: FoodProduction = food_production
