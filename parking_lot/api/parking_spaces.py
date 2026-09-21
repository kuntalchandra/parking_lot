from fastapi import APIRouter, Depends, HTTPException, Query

from parking_lot.api.dependencies import (
    get_parking_query_service,
)
from parking_lot.api.schemas import (
    AvailabilityResponse,
    AvailableSpacesResponse,
    OccupiedSpaceResponse,
    ParkingSpaceListResponse,
)
from parking_lot.services.queries import ParkingQueryService


router = APIRouter(
    prefix="/parking-lots/{parking_lot_id}",
    tags=["parking-spaces"],
)


# GET /parking-lots/{parking_lot_id}/availability
# Returns currently available space counts by size.
@router.get(
    "/availability",
    response_model=AvailabilityResponse,
)
def get_availability(
    parking_lot_id: int,
    service: ParkingQueryService = Depends(
        get_parking_query_service
    ),
) -> AvailabilityResponse:
    availability = service.get_availability(parking_lot_id)

    return AvailabilityResponse(
        parking_lot_id=availability.parking_lot_id,
        available=AvailableSpacesResponse(
            small=availability.small,
            medium=availability.medium,
            large=availability.large,
        ),
        total_available=availability.total,
    )


# GET /parking-lots/{parking_lot_id}/spaces?occupied=true
# Returns currently occupied spaces ordered by space number.
@router.get(
    "/spaces",
    response_model=ParkingSpaceListResponse,
)
def list_occupied_spaces(
    parking_lot_id: int,
    occupied: bool = Query(default=True),
    service: ParkingQueryService = Depends(
        get_parking_query_service
    ),
) -> ParkingSpaceListResponse:
    if not occupied:
        raise HTTPException(
            status_code=422,
            detail=(
                "Only occupied=true is supported by this endpoint"
            ),
        )
    spaces = service.list_occupied_spaces(parking_lot_id)

    return ParkingSpaceListResponse(
        spaces=[
            OccupiedSpaceResponse.model_validate(space)
            for space in spaces
        ]
    )