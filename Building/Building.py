from typing import Dict

from Farmable.Farmable import Resource


class Building:
    """
    Object Building which represent the different building
    """

    def __init__(self, building_type: str, nb_copy: int):
        """
        Constructor Class Building
        :param building_type: type of building
        :param nb_copy: number of copy
        """
        self.building_type = building_type
        self.nb_copy = nb_copy


class SumOfDivisorBuilding(Building):
    def __init__(self, building_type: str, nb_copy: int):
        super().__init__(building_type, nb_copy)


class OneToSevenResourcesBuilding(SumOfDivisorBuilding):
    """
    Object OneToSevenResourcesBuilding which represent the number resources of the building
    Children of Class Building
    """

    def __init__(self, building_type: str, nb_copy: int, nb_min_resources: int, nb_max_resources: int):
        """
        Constructor Class OneToSevenResourcesBuilding
        :param building_type: type of building
        :param nb_copy: number of copy
        :param nb_min_resources: number minimum of resources
        :param nb_max_resources: number maximum of resources
        """
        super().__init__(building_type, nb_copy)
        self.nb_min_resources = nb_min_resources
        self.nb_max_resources = nb_max_resources


class SelectedResourcesBuilding(SumOfDivisorBuilding):
    """
    Object SelectedResourcesBuilding which represent the different kinds of resources
    Children of Class Building
    """

    def __init__(self, building_type: str, nb_copy: int, nb_resources: int, nb_kinds: int):
        """
        Constructor Class SelectedResourcesBuilding
        :param building_type: type of building
        :param nb_copy: number of copy
        :param nb_resources: number of resources
        :param nb_kinds: number of different kinds
        """
        super().__init__(building_type, nb_copy)
        self.nb_resources = nb_resources
        self.nb_kinds = nb_kinds


class SpecificResourcesBuilding(Building):
    """
    Object SpecificResourcesBuilding which represent the specific resources of building
    Children of Class Building
    """

    def __init__(self, building_type: str, nb_copy: int):
        """
        Constructor Class SpecificResourcesBuilding
        :param building_type: type of building
        :param nb_copy: number of copy
        """
        super().__init__(building_type, nb_copy)
        self.resources_required: Dict[Resource, int] = dict()
