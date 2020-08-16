from parking_lot.entities.parking_slot import ParkingSlot


class ParkingLotService:
    def __init__(self):
        self.slots = {}

    def create_parking_lot(self, slots: str) -> None:
        slots = int(slots)
        if self.slots:
            raise Exception("Parking lot already exists")
        for i in range(1, slots + 1):
            self.slots[i] = ParkingSlot(slot=i, available=True)
        print("Created a parking lot with {} slots".format(slots))

    def park(self, registraion_number: str, color: str):
        pass

    def leave(self, slot: str):
        slot = int(slot)
        pass

    def status(self) -> None:
        pass

    def slot_numbers_for_cars_with_colour(self, color: str) -> None:
        pass

    def slot_number_for_registration_number(self, registration_number: str) -> None:
        pass
