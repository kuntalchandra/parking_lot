from abc import ABCMeta, abstractmethod


class Vehicle(metaclass=ABCMeta):
    @abstractmethod
    def get_registration_number(self) -> str:
        pass

    @abstractmethod
    def get_color(self) -> str:
        pass
