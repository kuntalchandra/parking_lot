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