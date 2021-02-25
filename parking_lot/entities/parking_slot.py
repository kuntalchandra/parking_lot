from parking_lot.entities.car import Car
from parking_lot.entities.merchant import Merchant
from parking_lot.entities.parking_lot import ParkingLot


class ParkingSlot:
    def __init__(self, available: bool):
        self.merchant = None
        self.parking_lot = None
        self.car = None
        self.available = available

    @property
    def merchant(self):
        return self._merchant

    @merchant.setter
    def merchant(self, merchant: Merchant):
        self._merchant = merchant

    @property
    def parking_lot(self):
        return self._parking_lot

    @parking_lot.setter
    def parking_lot(self, parking_lot: ParkingLot):
        self._parking_lot = parking_lot

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
