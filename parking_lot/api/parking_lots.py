from fastapi import APIRouter, Depends

from parking_lot.api.dependencies import (
    get_parking_lot_service,
)
from parking_lot.api.schemas import (
    CreateParkingLotRequest,
    ParkingLotListResponse,
    ParkingLotResponse,
)
from parking_lot.services.parking_lots import (
    ParkingLotService,
)


router = APIRouter(prefix="/parking-lots", tags=["parking-lots"])


# POST /parking-lots
# Creates the initial parking lot and its configured spaces.
@router.post("", response_model=ParkingLotResponse, status_code=201)
def create_parking_lot(
    request: CreateParkingLotRequest,
    service: ParkingLotService = Depends(
        get_parking_lot_service
    ),
) -> ParkingLotResponse:
    parking_lot = service.create_parking_lot(
        name=request.name,
        small_space_count=request.small_space_count,
        medium_space_count=request.medium_space_count,
        large_space_count=request.large_space_count,
        hourly_rate=request.hourly_rate,
    )
    return ParkingLotResponse.model_validate(parking_lot)


# GET /parking-lots/{parking_lot_id}
# Returns the requested parking lot or 404 when it does not exist.
@router.get(
    "/{parking_lot_id}",
    response_model=ParkingLotResponse,
)
def get_parking_lot(
    parking_lot_id: int,
    service: ParkingLotService = Depends(
        get_parking_lot_service
    ),
) -> ParkingLotResponse:
    parking_lot = service.get_parking_lot(parking_lot_id)
    return ParkingLotResponse.model_validate(parking_lot)


# GET /parking-lots
# Lists the parking lots currently managed by the application.
@router.get("", response_model=ParkingLotListResponse)
def list_parking_lots(
    service: ParkingLotService = Depends(
        get_parking_lot_service
    ),
) -> ParkingLotListResponse:
    parking_lots = service.list_parking_lots()

    return ParkingLotListResponse(
        parking_lots=[
            ParkingLotResponse.model_validate(parking_lot)
            for parking_lot in parking_lots
        ]
    )