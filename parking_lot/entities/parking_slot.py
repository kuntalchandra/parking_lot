from parking_lot.entities.car import Car
from parking_lot.entities.merchant import Merchant
from parking_lot.entities.parking_lot import ParkingLot


class ParkingSlot:
    def __init__(self, available: bool, parking_lot: ParkingLot):
        self.merchant = None
        self.parking_lot = parking_lot
        self.car = None
        self.available = available

    def set_merchant(self, merchant: Merchant) -> None:
        self.merchant = merchant

    def get_merchant(self) -> Merchant:
        return self.merchant

    def get_parking_lot(self) -> ParkingLot:
        return self.parking_lot

    def set_car(self, car: Car) -> None:
        self.car = car

    def get_car(self) -> Car:
        return self.car

    def set_available(self, available: bool) -> None:
        self.available = available

    def get_available(self) -> bool:
        return self.available
