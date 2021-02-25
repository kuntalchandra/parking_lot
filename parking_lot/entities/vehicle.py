from abc import ABCMeta, abstractmethod


class Vehicle(metaclass=ABCMeta):
    @abstractmethod
    def get_registration_number(self) -> str:
        pass

    @abstractmethod
    def get_color(self) -> str:
        pass

    # TODO: TypeError: Can't instantiate abstract class Car with abstract methods in_at, out_at
    """
    @abstractmethod
    def in_at(self) -> str:
        pass

    @abstractmethod
    def out_at(self) -> str:
        pass
    """
