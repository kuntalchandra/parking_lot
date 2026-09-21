from fastapi import APIRouter, Depends

from parking_lot.api.dependencies import get_parking_service
from parking_lot.api.schemas import (
    ParkVehicleRequest,
    TicketResponse,
)
from parking_lot.services.parking import ParkingService


router = APIRouter(
    prefix="/parking-lots/{parking_lot_id}/tickets",
    tags=["parking-tickets"],
)


# POST /parking-lots/{parking_lot_id}/tickets
# Allocates the nearest compatible space and issues a PARKED ticket.
@router.post("", response_model=TicketResponse, status_code=201)
def park_vehicle(
    parking_lot_id: int,
    request: ParkVehicleRequest,
    service: ParkingService = Depends(get_parking_service),
) -> TicketResponse:
    ticket = service.park_vehicle(
        parking_lot_id=parking_lot_id,
        registration_number=request.registration_number,
    )
    return TicketResponse.model_validate(ticket)