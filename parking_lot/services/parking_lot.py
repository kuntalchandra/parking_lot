from parking_lot.entities.parking_slot import ParkingSlot


class ParkingLotService:
    def __init__(self):
        self.slots = {}

    def create_parking_lot(self, slots) -> None:
        slots = int(slots)
        if self.slots:
            raise Exception("Parking lot already exists")
        for i in range(1, slots + 1):
            self.slots[i] = ParkingSlot(slot=i, available=True)
        print("Created a parking lot with {} slots".format(slots))

    def status(self) -> None:
        pass
