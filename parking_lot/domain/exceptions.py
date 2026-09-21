class ParkingLotError(Exception):
    """Base exception for expected parking-lot failures."""


class InvalidParkingLotConfigurationError(ParkingLotError):
    """Raised when parking-lot configuration is invalid."""


class ParkingLotAlreadyExistsError(ParkingLotError):
    """Raised when the initial parking lot already exists."""


class ParkingLotNotFoundError(ParkingLotError):
    """Raised when a requested parking lot does not exist."""