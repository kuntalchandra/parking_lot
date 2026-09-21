from dataclasses import dataclass
from enum import StrEnum


class ParkingSpaceSize(StrEnum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"


class VehicleSize(StrEnum):
    # Additional vehicle sizes are deferred.
    SMALL = "SMALL"


@dataclass(frozen=True, slots=True)
class ParkingLot:
    id: int
    name: str
    hourly_rate: int
    small_space_count: int
    medium_space_count: int
    large_space_count: int


@dataclass(frozen=True, slots=True)
class ParkingSpace:
    id: int
    parking_lot_id: int
    space_number: int
    size: ParkingSpaceSize