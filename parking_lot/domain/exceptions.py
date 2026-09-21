class ParkingLotError(Exception):
    """Base exception for expected parking-lot failures."""


class InvalidParkingLotConfigurationError(ParkingLotError):
    """Raised when parking-lot configuration is invalid."""


class ParkingLotAlreadyExistsError(ParkingLotError):
    """Raised when the initial parking lot already exists."""


class ParkingLotNotFoundError(ParkingLotError):
    """Raised when a requested parking lot does not exist."""

class InvalidRegistrationNumberError(ParkingLotError):
    """Raised when a registration number is invalid."""


class VehicleAlreadyParkedError(ParkingLotError):
    """Raised when a vehicle already has a PARKED ticket."""


class ParkingLotFullError(ParkingLotError):
    """Raised when no compatible parking space is available."""

class InvalidParkingDurationError(ParkingLotError):
    """Raised when exit time precedes parking time."""


class ParkingTicketNotFoundError(ParkingLotError):
    """Raised when a requested parking ticket does not exist."""


class ParkingTicketAlreadyExitedError(ParkingLotError):
    """Raised when an EXITED ticket is used again."""