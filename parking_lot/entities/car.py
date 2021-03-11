from parking_lot.entities.vehicle import Vehicle


class Car(Vehicle):
    def __init__(self, registration_number: str, color: str, in_at: str, out_at: str, id: int = None):
        self.id = id
        self.registration_number = registration_number
        self.color = color
        self.in_at = in_at
        self.out_at = out_at

    def get_registration_number(self) -> str:
        return self.registration_number

    def get_color(self) -> str:
        return self.color

    def get_in_at(self) -> str:
        return self.in_at

    def get_out_at(self) -> str:
        return self.out_at

    def get_id(self) -> int:
        return self.id

    def set_id(self, id: int) -> None:
        self.id = id
        return
