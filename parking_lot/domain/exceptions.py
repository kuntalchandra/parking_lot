class ParkingLotError(Exception):
    """Base exception for expected parking-lot failures."""


class ParkingLotAlreadyExistsError(ParkingLotError):
    """Raised when the initial parking lot already exists."""