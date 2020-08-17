from parking_lot.entities.car import Car


class ParkingSlot:
    def __init__(self, available: bool):
        self.car = None
        self.available = available

    @property
    def car(self):
        return self._car

    @car.setter
    def car(self, car: Car):
        self._car = car

    @property
    def available(self):
        return self._available

    @available.setter
    def available(self, available: bool):
        self._available = available
