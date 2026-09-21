from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class ParkingSpaceSize(StrEnum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"


class VehicleSize(StrEnum):
    SMALL = "SMALL"


class TicketState(StrEnum):
    PARKED = "PARKED"
    EXITED = "EXITED"


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


@dataclass(frozen=True, slots=True)
class ParkingTicket:
    id: int
    parking_lot_id: int
    parking_space_id: int
    space_number: int
    space_size: ParkingSpaceSize
    registration_number: str
    parked_at: datetime
    exited_at: datetime | None
    billed_hours: int | None
    hourly_rate: int
    total_cost: int | None
    state: TicketState

@dataclass(frozen=True, slots=True)
class ParkingAvailability:
    parking_lot_id: int
    small: int
    medium: int
    large: int

    @property
    def total(self) -> int:
        return self.small + self.medium + self.large


@dataclass(frozen=True, slots=True)
class OccupiedSpace:
    space_number: int
    space_size: ParkingSpaceSize
    registration_number: str
    ticket_id: int
    parked_at: datetime