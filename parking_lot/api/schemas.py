from datetime import datetime
from parking_lot.domain.models import (
    ParkingSpaceSize,
    TicketState,
)
from pydantic import BaseModel, ConfigDict, Field


class CreateParkingLotRequest(BaseModel):
    name: str = Field(min_length=1)
    small_space_count: int = Field(ge=0)
    medium_space_count: int = Field(ge=0)
    large_space_count: int = Field(ge=0)
    hourly_rate: int = Field(gt=0)


class ParkingLotResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    hourly_rate: int
    small_space_count: int
    medium_space_count: int
    large_space_count: int


class ParkingLotListResponse(BaseModel):
    parking_lots: list[ParkingLotResponse]


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail

class ParkVehicleRequest(BaseModel):
    registration_number: str = Field(min_length=1)


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    parking_lot_id: int
    registration_number: str
    space_number: int
    space_size: ParkingSpaceSize
    parked_at: datetime
    exited_at: datetime | None
    billed_hours: int | None
    hourly_rate: int
    total_cost: int | None
    state: TicketState

class AvailableSpacesResponse(BaseModel):
    small: int
    medium: int
    large: int


class AvailabilityResponse(BaseModel):
    parking_lot_id: int
    available: AvailableSpacesResponse
    total_available: int


class OccupiedSpaceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    space_number: int
    space_size: ParkingSpaceSize
    registration_number: str
    ticket_id: int
    parked_at: datetime


class ParkingSpaceListResponse(BaseModel):
    spaces: list[OccupiedSpaceResponse]


class TicketListResponse(BaseModel):
    tickets: list[TicketResponse]