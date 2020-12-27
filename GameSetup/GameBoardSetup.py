from typing import Set, List

from Place import UpperPartPlace, CivilizationPlace, BuildingPlace


class GameBoardSetup:
    """
    Object GameBoardSetup which represent the parameters of the gameboard
    """

    def __init__(self, max_nb_food_production: int, nb_points_when_do_not_feed: int,
                 places: Set[UpperPartPlace], civilization_places: List[CivilizationPlace],
                 building_places: List[BuildingPlace]):
        """
        Constructor of GameBoardSetup
        :param max_nb_food_production: maximum of food production
        :param nb_points_when_do_not_feed: number of points when do not feed
        :param places: places of gameboard
        :param civilization_places: civilization place of gameboard
        :param building_places: building place of gameboard
        """
        self.max_nb_food_production = max_nb_food_production
        self.nb_points_when_do_not_feed = nb_points_when_do_not_feed
        self.places: Set[UpperPartPlace] = places
        self.civilization_places: List[CivilizationPlace] = civilization_places
        self.building_places: List[BuildingPlace] = building_places
