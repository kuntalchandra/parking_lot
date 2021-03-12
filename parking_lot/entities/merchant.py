from datetime import datetime


class Merchant:
    def __init__(self, id: int, name: str, registered_at: datetime):
        self.id = id
        self.name = name
        self.registered_at = registered_at

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_registered_at(self):
        return self.registered_at
