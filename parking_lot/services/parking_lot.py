from collections import OrderedDict
from parking_lot.entities.car import Car
from parking_lot.exceptions import ParkingLotExistsException, InvalidCommandException
from parking_lot.entities.parking_slot import ParkingSlot


class ParkingLotService:
    def __init__(self):
        self.slots = OrderedDict()

    def create_parking_lot(self, slots: str) -> None:
        slots = int(slots)
        if self.slots:
            raise ParkingLotExistsException("Parking lot already exists")
        for i in range(1, slots + 1):
            self.slots[i] = ParkingSlot(available=True)
        print("Created a parking lot with {} slots".format(slots))

    def parking_lot_exists(self):
        return self.slots

    def park(self, registration_number: str, color: str):
        if not self.slots:
            raise ParkingLotExistsException("Parking lot doesn't exists")
        for slot_number, parking_slot in self.slots.items():
            if parking_slot.available:
                parking_slot.car = Car(registration_number, color)
                parking_slot.available = False
                self.slots[slot_number] = parking_slot
                print("Allocated slot number: {}".format(slot_number))
                return
        print("Sorry, parking lot is full")

    def leave(self, slot: str):
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

    def status(self) -> None:
        if not self.slots:
            raise ParkingLotExistsException("Parking lot doesn't exists")
        print("Slot No.     Registration No     Colour")
        for slot, details in self.slots.items():
            if not details.available:
                print(
                    "{}       {}      {}".format(
                        slot,
                        details.car.get_registration_number(),
                        details.car.get_color(),
                    )
                )

    def slot_numbers_for_cars_with_colour(self, color: str) -> None:
        if not self.slots:
            raise ParkingLotExistsException("Parking lot doesn't exists")
        pass

    def slot_number_for_registration_number(self, registration_number: str) -> None:
        if not self.slots:
            raise ParkingLotExistsException("Parking lot doesn't exists")
        pass

    def registration_numbers_for_cars_with_colour(self, color: str) -> None:
        if not self.slots:
            raise ParkingLotExistsException("Parking lot doesn't exists")
        pass
