from fastapi import APIRouter, Depends

from parking_lot.api.schemas import (
    ParkVehicleRequest,
    TicketResponse,
)
from parking_lot.api.dependencies import (
    get_exit_service,
    get_parking_service,
)
from parking_lot.services.exit import ExitService
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

# POST /parking-lots/{parking_lot_id}/tickets/{ticket_id}/exit
# Closes a PARKED ticket, calculates its cost and releases its space.
@router.post(
    "/{ticket_id}/exit",
    response_model=TicketResponse,
)
def exit_vehicle(
    parking_lot_id: int,
    ticket_id: int,
    service: ExitService = Depends(get_exit_service),
) -> TicketResponse:
    ticket = service.exit_vehicle(
        parking_lot_id=parking_lot_id,
        ticket_id=ticket_id,
    )
    return TicketResponse.model_validate(ticket)