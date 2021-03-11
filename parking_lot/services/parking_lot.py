from typing import List
from parking_lot.entities.car import Car
from parking_lot.repositories.car import CarRepository
from parking_lot.repositories.parking_lots import ParkingLotRepository
from parking_lot.exceptions import ParkingLotExistsException, InvalidCommandException, ParkingLotNotExistsException
from parking_lot.entities.parking_slot import ParkingSlot


class ParkingLotService:
    def __init__(self):
        self.slots = {}
        self.slot_ids = []

    def parking_lots(self) -> None:
        parking_lots = ParkingLotRepository()
        lots = parking_lots.get_all()
        print("Parking Lot      Location            Pin Code            Size")
        for lot in lots:
            self.slot_ids.append(lot["id"])
            print("{}           {}              {}          {}".format(lot["name"], lot["location"], lot["pin"], lot["size"]))

    def select_parking_lot(self, lot: int) -> int:
        parking_lots = ParkingLotRepository()
        slot = parking_lots.get_lot(lot)
        if not slot:
            raise ParkingLotNotExistsException("Parking lot doesn't exist or already in use")
        for i in range(1, slot["size"] + 1):
            self.slots[i] = ParkingSlot(available=True)
        print("Parking lot {} with {} slots is ready to use".format(slot["name"], slot["size"]))
        return len(self.slots)

    def parking_lot_exists(self):
        return self.slots

    def park(self, registration_number: str, color: str) -> [int, bool]:
        car_repo = CarRepository()
        if not self.slots:
            raise ParkingLotExistsException("Parking lot doesn't exists")
        for slot_number, parking_slot in self.slots.items():
            if parking_slot.available:
                parking_slot.car = Car(registration_number, color, "", "")
                # TODO: Insert the vehicle. Get the id from there itself

                parking_slot.available = False
                self.slots[slot_number] = parking_slot
                print(self.slots)
                # TODO: Introduce the write query
                print("Allocated slot number: {}".format(slot_number))
                return slot_number
        print("Sorry, parking lot is full")
        return False

    def leave(self, slot: str) -> int:
        if not self.slots:
            raise ParkingLotExistsException("Parking lot doesn't exists")
        slot = int(slot)
        if slot > len(self.slots):
            raise InvalidCommandException("Slot {} is out of range".format(slot))
        if self.slots[slot].available:
            raise InvalidCommandException("Slot {} was never occupied".format(slot))
        self.slots[slot].car = None
        self.slots[slot].available = True
        print("Slot number {} is free".format(slot))
        return slot

    def status(self) -> List[List[str]]:
        if not self.slots:
            raise ParkingLotExistsException("Parking lot doesn't exists")
        print("Slot No. Registration No Colour")
        cars = []
        for slot, details in self.slots.items():
            if not details.available:
                cars.append(
                    [
                        str(slot),
                        details.car.get_registration_number(),
                        details.car.get_color(),
                    ]
                )
        for car in cars:
            print(", ".join(car))
        return cars

    def registration_numbers_for_cars_with_colour(
        self, color: str
    ) -> [List[str], bool]:
        if not self.slots:
            raise ParkingLotExistsException("Parking lot doesn't exists")
        cars = []
        for slot in self.slots.values():
            if not slot.available and slot.car.get_color() == color:
                cars.append(slot.car.get_registration_number())
        if cars:
            print(", ".join(registration_number for registration_number in cars))
            return cars
        print("Not found")
        return False

    def slot_numbers_for_cars_with_colour(self, color: str) -> [List[int], bool]:
        if not self.slots:
            raise ParkingLotExistsException("Parking lot doesn't exists")
        slots = []
        for slot, details in self.slots.items():
            if not details.available and details.car.get_color() == color:
                slots.append(slot)
        if slots:
            print(", ".join(str(slot) for slot in slots))
            return slots
        print("Not found")
        return False

    def slot_number_for_registration_number(
        self, registration_number: str
    ) -> [int, bool]:
        if not self.slots:
            raise ParkingLotExistsException("Parking lot doesn't exists")
        for slot, details in self.slots.items():
            if (
                not details.available
                and details.car.get_registration_number() == registration_number
            ):
                print(slot)
                return slot
        print("Not found")
        return False
