from collections.abc import Iterator
from sqlite3 import Connection

from fastapi import Depends, Request

from parking_lot.database import connect_database
from parking_lot.domain.allocation import (
    DefaultSpaceAllocationPolicy,
)
from parking_lot.domain.clock import SystemClock
from parking_lot.domain.pricing import (
    FixedHourlyPricingPolicy,
)
from parking_lot.services.exit import ExitService
from parking_lot.repositories.parking_spaces import (
    ParkingSpaceRepository,
)
from parking_lot.repositories.parking_tickets import (
    ParkingTicketRepository,
)
from parking_lot.services.parking import ParkingService
from parking_lot.repositories.parking_lots import (
    ParkingLotRepository,
)
from parking_lot.services.parking_lots import (
    ParkingLotService,
)


def get_connection(request: Request) -> Iterator[Connection]:
    connection = connect_database(
        request.app.state.database_path
    )

    try:
        yield connection
    finally:
        connection.close()


def get_parking_lot_service(
    connection: Connection = Depends(get_connection),
) -> ParkingLotService:
    repository = ParkingLotRepository(connection)
    return ParkingLotService(repository)

def get_parking_service(
    connection: Connection = Depends(get_connection),
) -> ParkingService:
    return ParkingService(
        connection=connection,
        parking_lot_repository=ParkingLotRepository(connection),
        parking_space_repository=ParkingSpaceRepository(
            connection
        ),
        parking_ticket_repository=ParkingTicketRepository(
            connection
        ),
        allocation_policy=DefaultSpaceAllocationPolicy(),
        clock=SystemClock(),
    )

def get_exit_service(
    connection: Connection = Depends(get_connection),
) -> ExitService:
    return ExitService(
        connection=connection,
        parking_lot_repository=ParkingLotRepository(connection),
        parking_ticket_repository=ParkingTicketRepository(
            connection
        ),
        pricing_policy=FixedHourlyPricingPolicy(),
        clock=SystemClock(),
    )