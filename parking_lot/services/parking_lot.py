from typing import List

from parking_lot.entities.car import Car
from parking_lot.exceptions import ParkingLotExistsException, InvalidCommandException
from parking_lot.entities.parking_slot import ParkingSlot


class ParkingLotService:
    def __init__(self):
        self.slots = {}

    def create_parking_lot(self, slots: str) -> int:
        slots = int(slots)
        if self.slots:
            raise ParkingLotExistsException("Parking lot already exists")
        for i in range(1, slots + 1):
            self.slots[i] = ParkingSlot(available=True)
        print("Created a parking lot with {} slots".format(slots))
        return len(self.slots)

    def parking_lot_exists(self):
        return self.slots

    def park(self, registration_number: str, color: str) -> [int, bool]:
        if not self.slots:
            raise ParkingLotExistsException("Parking lot doesn't exists")
        for slot_number, parking_slot in self.slots.items():
            if parking_slot.available:
                parking_slot.car = Car(registration_number, color)
                parking_slot.available = False
                self.slots[slot_number] = parking_slot
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

    def status(self) -> List[str]:
        if not self.slots:
            raise ParkingLotExistsException("Parking lot doesn't exists")
        cars = ["Slot No. Registration No Colour"]
        for slot, details in self.slots.items():
            if not details.available:
                cars.append([slot, details.car.get_registration_number(), details.car.get_color()])
        for car in cars:
            print(car)
        return cars

    def registration_numbers_for_cars_with_colour(self, color: str) -> None:
        if not self.slots:
            raise ParkingLotExistsException("Parking lot doesn't exists")
        cars = []
        for slot in self.slots.values():
            if slot.car.get_color() == color:
                cars.append(slot.car.get_registration_number())
        if cars:
            print(", ".join(registration_number for registration_number in cars))
            return
        print("Not found")

    def slot_numbers_for_cars_with_colour(self, color: str) -> None:
        if not self.slots:
            raise ParkingLotExistsException("Parking lot doesn't exists")
        slots = []
        for slot, details in self.slots.items():
            if details.car.get_color() == color:
                slots.append(slot)
        if slots:
            print(", ".join(str(slot) for slot in slots))
            return
        print("Not found")

    def slot_number_for_registration_number(self, registration_number: str) -> None:
        if not self.slots:
            raise ParkingLotExistsException("Parking lot doesn't exists")
        for slot, details in self.slots.items():
            if (
                not details.available
                and details.car.get_registration_number() == registration_number
            ):
                print(slot)
                return
        print("Not found")
