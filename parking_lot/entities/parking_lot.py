from datetime import datetime


class ParkingLot:
    def __init__(self, id: int, name: str, area: str, pin_code: int, is_available: bool, start_date: datetime, slot_count: int):
        # TODO: Parking Lot is a read-only entity in the prototype. Revisit for the getters and setters
        self.id = id
        self.name = name
        self.area = area
        self.pin_code = pin_code
        self.is_available = is_available
        self.start_date = start_date
        self.slot_count = slot_count

    def get_id(self) -> int:
        return self.id

