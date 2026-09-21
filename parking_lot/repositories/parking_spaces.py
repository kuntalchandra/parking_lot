from __future__ import annotations

import sqlite3
from collections.abc import Sequence
from datetime import datetime

from parking_lot.domain.models import (
    OccupiedSpace,
    ParkingAvailability,
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

    def get_availability(
        self,
        parking_lot_id: int,
    ) -> ParkingAvailability:
        row = self.connection.execute(
            """
            SELECT
                COALESCE(
                    SUM(
                        CASE
                            WHEN space.size = 'SMALL' THEN 1
                            ELSE 0
                        END
                    ),
                    0
                ) AS small,
                COALESCE(
                    SUM(
                        CASE
                            WHEN space.size = 'MEDIUM' THEN 1
                            ELSE 0
                        END
                    ),
                    0
                ) AS medium,
                COALESCE(
                    SUM(
                        CASE
                            WHEN space.size = 'LARGE' THEN 1
                            ELSE 0
                        END
                    ),
                    0
                ) AS large
            FROM parking_space AS space
            WHERE space.parking_lot_id = ?
              AND NOT EXISTS (
                  SELECT 1
                  FROM parking_ticket AS ticket
                  WHERE ticket.parking_lot_id =
                        space.parking_lot_id
                    AND ticket.parking_space_id = space.id
                    AND ticket.state = 'PARKED'
              )
            """,
            (parking_lot_id,),
        ).fetchone()

        return ParkingAvailability(
            parking_lot_id=parking_lot_id,
            small=row["small"],
            medium=row["medium"],
            large=row["large"],
        )

    def list_occupied(
        self,
        parking_lot_id: int,
    ) -> list[OccupiedSpace]:
        rows = self.connection.execute(
            """
            SELECT
                space.space_number,
                space.size AS space_size,
                ticket.registration_number,
                ticket.id AS ticket_id,
                ticket.parked_at
            FROM parking_space AS space
            JOIN parking_ticket AS ticket
                ON ticket.parking_lot_id =
                   space.parking_lot_id
               AND ticket.parking_space_id = space.id
               AND ticket.state = 'PARKED'
            WHERE space.parking_lot_id = ?
            ORDER BY space.space_number
            """,
            (parking_lot_id,),
        ).fetchall()

        return [
            OccupiedSpace(
                space_number=row["space_number"],
                space_size=ParkingSpaceSize(
                    row["space_size"]
                ),
                registration_number=row[
                    "registration_number"
                ],
                ticket_id=row["ticket_id"],
                parked_at=datetime.fromisoformat(
                    row["parked_at"]
                ),
            )
            for row in rows
        ]