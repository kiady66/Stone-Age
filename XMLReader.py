import xml.etree.ElementTree
from typing import Set, List

from Building.Building import Building, OneToSevenResourcesBuilding, SelectedResourcesBuilding, \
    SpecificResourcesBuilding
from Civilization.BottomPart import Items, BottomPart, MultiplierPoints, Multipliable
from Civilization.Civilization import Civilization
from Civilization.UpperPart import UpperPart, ItemsDice, AdditionalFood, ResourceReward, ResourceDiceRoll, NewTool, \
    AdditionalAgriculture, AdditionalCard, ToolsUnique, SelectedResource, Point
from Farmable.Farmable import Food, Meeple, FoodProduction
from Farmable.Farmable import Resource
from Farmable.Farmable import Tool
from GameSetup.GameBoardSetup import GameBoardSetup
from GameSetup.GameSetup import GameSetup
from GameSetup.PlayerSetup import PlayerSetup
from Place import CivilizationPlace, BuildingPlace, UpperPartPlace


class XMLReader:
    """
    read the XML file and initialize the variables.
    @author: Therry
    """
    class OnlyXMLReader:
        """
        Singleton class
        """
        def __init__(self, arg: str):
            """
            Constructor of Singleton
            :param arg: XML file path
            """
            self.path_xml = arg

    def __init__(self, path_xml: str):
        """
        Constructor of XMLReader
        :param path_xml: XML file path
        """
        if not XMLReader.instance:
            XMLReader.instance = XMLReader.OnlyXMLReader(path_xml)
        else:
            self.instance.path_xml = path_xml

    instance = None
    resource = None
    meeple = None

    @classmethod
    def get_resource(cls, name: str) -> Resource:
        """
        get the resources get the resource by name
        :param name: name of the reource
        """
        for res in cls.resource:
            if res.name == name:
                return res

    @classmethod
    def read(cls) -> GameSetup:
        """
        function which reads the XML file and initializes the variables
        """
        tree = xml.etree.ElementTree.parse(cls.instance.path_xml)
        root = tree.getroot()
        type(root)

        game_name: str = root.find('game_name').text
        min_players: int = int(root.find('n_min_players').text)
        max_players: int = int(root.find('n_max_players').text)

        # GameBoard
        xml_game_board = root.find('game_board')
        # GameBoard - GameBoardSetup - Place
        building_nb_place = 0
        civilization_nb_place = 0
        set_place: Set[UpperPartPlace] = set()
        for places in xml_game_board.find('places'):
            if places.find('n_places').text is not None:
                nb_place = int(places.find('n_places').text)
            else:
                nb_place = -1
            if places.find('name').text == 'Building':
                building_nb_place = nb_place
            elif places.find('name').text == 'Civilization':
                civilization_nb_place = nb_place
            else:
                set_place.add(UpperPartPlace(places.find('name').text, nb_place))
        # GameBoard - GameBoardSetup - CivilizationPlace        
        civilization_places: List[CivilizationPlace] = []
        for civilizationPlaces in xml_game_board.find('civilization_places'):
            civilization_places.append(
                CivilizationPlace('Civilization', civilization_nb_place, int(civilizationPlaces.find('ordinal').text),
                                  int(civilizationPlaces.find('n_resource_cost').text)))
        # GameBoard - GameBoardSetup - BuildingPlace
        building_places: List[BuildingPlace] = []
        i = 0
        for buildingPlaces in xml_game_board.find('building_places'):
            building_places.append(
                BuildingPlace('Building', building_nb_place, int(buildingPlaces.find('n_players').text),
                              int(buildingPlaces.find('n_stacks').text),
                              i,
                              int(buildingPlaces.find('n_buildings_per_stack').text)))
            i += 1
        # GameBoard - GameBoardSetup
        game_bord_set = GameBoardSetup(int(xml_game_board.find('max_n_food_production').text),
                                       int(xml_game_board.find('n_points_when_do_not_feed').text),
                                       set_place,
                                       civilization_places,
                                       building_places)

        # Resources
        set_resources: Set[Resource] = set()
        for resource in root.find('resources'):
            place_for_res = [place for place in game_bord_set.places if place.name == resource.find('place').text][0]
            set_resources.add(Resource(resource.find('name').text,
                                       int(resource.find('number').text),
                                       place_for_res,
                                       int(resource.find('divisor').text)))
        cls.resource = set_resources

        place_for_res = [place for place in game_bord_set.places if place.name == 'Hut'][0]
        cls.meeple = Meeple(-1, place_for_res)
        place_for_res = [place for place in game_bord_set.places if place.name == 'Field'][0]
        cls.food_level = FoodProduction(-1, place_for_res)
        # Tools
        set_tools: Set[Tool] = set()
        """Place for make tools, here where place name contains 'Tool' """
        place_for_tool: UpperPartPlace = [place for place in game_bord_set.places if 'Tool' in place.name][0]
        for tool in root.find('tools'):
            set_tools.add(Tool(int(tool.find('value').text),
                               int(tool.find('number').text),
                               place_for_tool))

        # Building
        set_buildings: Set[Building] = set()
        for building in root.find('buildings'):
            if '1 to 7 resources' in building.find('building_type').text:
                set_buildings.add(OneToSevenResourcesBuilding(building.find('building_type').text,
                                                              int(building.find('n_copies').text),
                                                              int(building.find('n_min_resources').text),
                                                              int(building.find('n_max_resources').text)))
            elif 'Selected resources' in building.find('building_type').text:
                set_buildings.add(SelectedResourcesBuilding(building.find('building_type').text,
                                                            int(building.find('n_copies').text),
                                                            int(building.find('n_resources').text),
                                                            int(building.find('n_kinds').text)))
            elif 'Specific resources' in building.find('building_type').text:
                specific_res = SpecificResourcesBuilding(building.find('building_type').text,
                                                         int(building.find('n_copies').text))
                for resBuild in building.find('resources_required'):
                    specific_res.resources_required[cls.get_resource(resBuild.find('resource').text)] = int(
                        resBuild.find('n_resources').text)
            else:
                raise NotImplementedError

        # Food
        xml_food = root.find('food')
        place_for_food = [place for place in game_bord_set.places if place.name == xml_food.find('place').text][0]
        food = Food(int(xml_food.find('number').text),
                    place_for_food,
                    int(xml_food.find('divisor').text))

        # Player setup
        xmlp_setup = root.find('player_setup')
        player_set = PlayerSetup(int(xmlp_setup.find('n_people').text),
                                 int(xmlp_setup.find('n_remaining_people').text),
                                 int(xmlp_setup.find('n_food').text),
                                 int(xmlp_setup.find('n_places_tools').text),
                                 int(xmlp_setup.find('n_food_production').text),
                                 int(xmlp_setup.find('n_points').text))
        # Player setup - Resource
        for resource in xmlp_setup.find('resources'):
            player_set.resource[cls.get_resource(resource.find('resource').text)] = int(
                resource.find('n_resources').text)

        # Civilisation
        set_civilisations: Set[Civilization] = set()
        for civilization in root.find('civilizations'):
            upper_part_xml = civilization.find('upper_part')
            upper_part: UpperPart
            if 'Items for dice' in upper_part_xml.find('civilization_type').text:
                upper_part = ItemsDice()
            elif 'Food' in upper_part_xml.find('civilization_type').text:
                upper_part = AdditionalFood(int(upper_part_xml.find('n_food').text))
            elif 'Resource with die roll' in upper_part_xml.find('civilization_type').text:
                resource = cls.get_resource(upper_part_xml.find('resource').find('resource').text)
                upper_part = ResourceDiceRoll(resource, int(upper_part_xml.find('resource').find('n_dice').text))
            elif 'Resource' in upper_part_xml.find('civilization_type').text:
                resource = cls.get_resource(upper_part_xml.find('resource').find('resource').text)
                upper_part = ResourceReward(resource, int(upper_part_xml.find('resource').find('n_resources').text))
            elif 'New tool' in upper_part_xml.find('civilization_type').text:
                upper_part = NewTool(int(upper_part_xml.find('n_tools').text))
            elif 'Additional food production' in upper_part_xml.find('civilization_type').text:
                upper_part = AdditionalAgriculture(int(upper_part_xml.find('n_food_production').text))
            elif 'Additional card' in upper_part_xml.find('civilization_type').text:
                upper_part = AdditionalCard(int(upper_part_xml.find('n_cards').text))
            elif 'Tool for unique use' in upper_part_xml.find('civilization_type').text:
                upper_part = ToolsUnique(int(upper_part_xml.find('n_tools_for_unique_use').text))
            elif '2 resources of the player’s choice' in upper_part_xml.find('civilization_type').text:
                upper_part = SelectedResource(int(upper_part_xml.find('n_resources').text))
            elif 'Points' in upper_part_xml.find('civilization_type').text:
                upper_part = Point(int(upper_part_xml.find('n_points').text))
            else:
                raise NotImplementedError
            bottom_part_xml = civilization.find('bottom_part')
            bottom_part: BottomPart
            if bottom_part_xml.find('green_background') is not None:
                bottom_part = Items(bottom_part_xml.find('green_background').text)
            elif bottom_part_xml.find('n_hut_builders') is not None:
                bottom_part = MultiplierPoints(int(bottom_part_xml.find('n_hut_builders').text), Multipliable.BUILDING)
            elif bottom_part_xml.find('n_tool_makers') is not None:
                bottom_part = MultiplierPoints(int(bottom_part_xml.find('n_tool_makers').text), Multipliable.TOOL)
            elif bottom_part_xml.find('n_farmers') is not None:
                bottom_part = MultiplierPoints(int(bottom_part_xml.find('n_farmers').text), Multipliable.AGRICULTURE)
            elif bottom_part_xml.find('n_shamen') is not None:
                bottom_part = MultiplierPoints(int(bottom_part_xml.find('n_shamen').text), Multipliable.MEEPLES)
            else:
                raise NotImplementedError
            set_civilisations.add(Civilization(int(root.find('n_min_players').text), upper_part, bottom_part))

        # GameSetup
        game: GameSetup = GameSetup(game_name, min_players, max_players, food, player_set, game_bord_set, cls.meeple,
                                    cls.food_level)
        for color in root.iter('player_color'):
            game.player_colors += [color.text]
        game.set_resources = set_resources
        game.set_tools = set_tools
        game.set_buildings = set_buildings
        game.set_civilizations = set_civilisations

        return game
