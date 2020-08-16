from parking_lot.entities.car import Car


class ParkingSlot:
    def __init__(self, slot: int, available: bool):
        self.car = None
        self.slot = slot
        self.available = available

    @property
    def car(self):
        return self._car

    @car.setter
    def car(self, car: Car):
        self._car = car

    @property
    def slot(self):
        return self._slot

    @slot.setter
    def slot(self, slot: int):
        self._slot = slot

    @property
    def available(self):
        return self._available

    @available.setter
    def available(self, available: bool):
        self._available = available
