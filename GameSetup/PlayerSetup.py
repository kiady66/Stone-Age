from typing import Dict

from Farmable.Farmable import Resource


class PlayerSetup:
    """
    Object PlayerSetup which represent the setting of the player at the beginning of the game
    """

    def __init__(self,
                 nb_people: int,
                 nb_remaining_people: int,
                 nb_food: int,
                 nb_places_tools: int,
                 nb_food_production: int,
                 nb_points: int):
        """
        Constructor
        :param nb_people: number of people
        :param nb_remaining_people: number of remaining people
        :param nb_food: number of food
        :param nb_places_tools: number of tools places
        :param nb_food_production: number of food production
        :param nb_points: number of points
        """
        self.nb_people = nb_people
        self.nb_remaining_people = nb_remaining_people
        self.nb_food = nb_food
        self.nb_places_tools = nb_places_tools
        self.nb_food_production = nb_food_production
        self.nb_points = nb_points
        self.resource: Dict[Resource, int] = dict()