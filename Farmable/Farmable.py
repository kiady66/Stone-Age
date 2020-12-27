import abc
from abc import ABC


class Farmable(metaclass=abc.ABCMeta):
    """
    Object Farmable which represent the different farmable
    """
    def __init__(self, number: int, place):
        """
        Constructor Class Building
        :param number: number of farmable
        :param place: place allocated to farmable
        """
        self.number = number
        self.place = place

    @abc.abstractmethod
    def farm(self, n_meeple: int, roll) -> int:
        """
        Have the returned value if we farm the object with n n_meeple
        :param n_meeple: number of meeple that are in the place
        :param roll: result of dice 
        """
        raise NotImplementedError


class FarmableWithDivisor(Farmable, metaclass=abc.ABCMeta):
    """
    Object FarmableWithDivisor which represent different farmable with divisor
    Children of Class Building
    """
    def __init__(self, number: int, place, divisor: int):
        """
        Constructor Class Building
        :param number: number of farmable
        :param place: place allocated to farmable
        :param divisor: farmable divisor number
        """
        super().__init__(number, place)
        self.divisor = divisor

    def farm(self, n_meeple: int, roll) -> int:
        """
        Have the returned value if we farm the object with n n_meeple
        :param n_meeple: number of meeple that are in the place
        :param roll: result of dice 
        """
        return roll.compute_sum_result() // self.divisor


class Food(FarmableWithDivisor, ABC):
    """
    Object Food which represent the different food with farmable divisor
    """
    def __init__(self, number: int, place, divisor: int):
        """
        Constructor Class Food
        :param number: number of food
        :param place: place allocated to food
        :param divisor: food divisor number
        """
        super().__init__(number, place, divisor)

    def __str__(self):
        """
        Return string (Food)
        """
        return 'Food'


class Resource(FarmableWithDivisor, ABC):
    """
    Object Resource which represent the different resource with farmable divisor
    """
    def __init__(self, name: str, number: int, place, divisor: int):
        """
        Constructor Class Resource
        :param name: name of resource
        :param number: number of resource
        :param place: place allocated to resource
        :param divisor: food divisor resource
        """
        super().__init__(number, place, divisor)
        self.name = name

    def __str__(self):
        """
        Return the name in string 
        """
        return self.name.capitalize()


class Tool(Farmable, ABC):
    """
    Object Tool which represent the different tool farmable
    """
    def __init__(self, value: int, number: int, place):
        """
        Constructor Class Resource
        :param value: value of tool
        :param number: number of tool
        :param place: place allocated to tool
        """
        super().__init__(number, place)
        self.value = value

    def farm(self, n_meeple: int, roll) -> int:
        """
        Have the returned value if we farm the object with n n_meeple
        :param n_meeple: number of meeple that are in the place
        :param roll: result of dice 
        """
        return 1

    def __str__(self):
        """
        Return string (Tool)
        """
        return 'Tool'


class Meeple(Farmable, ABC):
    """
    Object Meeple which represent the different meeple farmable
    """
    def __init__(self, number: int, place):
        """
        Constructor Class Resource
        :param number: number of meeple
        :param place: place allocated to meeple
        """
        super().__init__(number, place)

    def farm(self, n_meeple: int, roll) -> int:
        """
        Have the returned value if we farm the object with n n_meeple
        :param n_meeple: number of meeple that are in the place
        :param roll: result of dice 
        """
        if n_meeple == 2:
            return 1
        else:
            return 0

    def __str__(self):
        """
        Return string (Meeple)
        """
        return 'Meeple'


class FoodProduction(Farmable, ABC):
    """
    Object FoodProduction which represent the different food production farmable
    """
    def __init__(self, number: int, place):
        """
        Constructor Class FoodProduction
        :param number: number of meeple
        :param place: place allocated to meeple
        """
        super().__init__(number, place)

    def farm(self, n_meeple: int, roll) -> int:
        """
        Have the returned value if we farm the object with n n_meeple
        :param n_meeple: number of meeple that are in the place
        :param roll: result of dice 
        """
        return 1

    def __str__(self):
        """
        Return string (FoodProduction)
        """
        return 'FoodProduction'
