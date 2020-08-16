from parking_lot.entities.vehicle import Vehicle


class Car(Vehicle):
    def __init__(self, registration_number: str, color: str):
        self.registration_number = registration_number
        self.color = color

    def get_registration_number(self) -> str:
        return self.registration_number

    def get_color(self) -> str:
        return self.color
