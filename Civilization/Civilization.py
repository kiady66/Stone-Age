from Civilization.BottomPart import BottomPart
from Civilization.UpperPart import UpperPart


class Civilization:
    """
    Object Civilization which represent the Civilization card
    """

    def __init__(self, nb_copy: int, upper_part: UpperPart, bottom_part: BottomPart):
        """
        Constructor Class Civilization
        :param nb_copy: number of copy
        :param upper_part:
        :param bottom_part:
        """
        self.nb_copy = nb_copy
        self.upper_part = upper_part
        self.bottom_part = bottom_part
