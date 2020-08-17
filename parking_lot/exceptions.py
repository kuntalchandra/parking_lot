class ParkingLotException(Exception):
    pass


class InvalidCommandException(ParkingLotException):
    def __init__(self, msg, **identifiers):
        super().__init__(msg)
        self.identifiers = identifiers


class ParkingLotExistsException(ParkingLotException):
    def __init__(self, msg, **identifiers):
        super().__init__(msg)
        self.identifiers = identifiers
