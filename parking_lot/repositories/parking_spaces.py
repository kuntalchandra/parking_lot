from __future__ import annotations

import sqlite3
from collections.abc import Sequence

from parking_lot.domain.models import (
    ParkingSpace,
    ParkingSpaceSize,
)


class ParkingSpaceRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def find_nearest_available(
        self,
        parking_lot_id: int,
        preferred_sizes: Sequence[ParkingSpaceSize],
    ) -> ParkingSpace | None:
        for space_size in preferred_sizes:
            row = self.connection.execute(
                """
                SELECT
                    space.id,
                    space.parking_lot_id,
                    space.space_number,
                    space.size
                FROM parking_space AS space
                WHERE space.parking_lot_id = ?
                  AND space.size = ?
                  AND NOT EXISTS (
                      SELECT 1
                      FROM parking_ticket AS ticket
                      WHERE ticket.parking_lot_id =
                            space.parking_lot_id
                        AND ticket.parking_space_id = space.id
                        AND ticket.state = 'PARKED'
                  )
                ORDER BY space.space_number
                LIMIT 1
                """,
                (parking_lot_id, space_size.value),
            ).fetchone()

            if row is not None:
                return ParkingSpace(
                    id=row["id"],
                    parking_lot_id=row["parking_lot_id"],
                    space_number=row["space_number"],
                    size=ParkingSpaceSize(row["size"]),
                )

        return None