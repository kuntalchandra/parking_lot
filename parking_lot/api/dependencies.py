from collections.abc import Iterator
from sqlite3 import Connection

from fastapi import Depends, Request

from parking_lot.database import connect_database
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