from __future__ import annotations

import sqlite3
from collections.abc import Sequence

from parking_lot.domain.exceptions import (
    ParkingLotAlreadyExistsError,
)
from parking_lot.domain.models import (
    ParkingLot,
    ParkingSpaceSize,
)


class ParkingLotRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def create(
        self,
        name: str,
        hourly_rate: int,
        space_sizes: Sequence[ParkingSpaceSize],
    ) -> ParkingLot:
        """Create the initial parking lot and all its spaces atomically."""

        with self.connection:
            existing_count = self.connection.execute(
                "SELECT COUNT(*) FROM parking_lot"
            ).fetchone()[0]

            if existing_count > 0:
                raise ParkingLotAlreadyExistsError(
                    "A parking lot already exists"
                )

            cursor = self.connection.execute(
                """
                INSERT INTO parking_lot (name, hourly_rate)
                VALUES (?, ?)
                """,
                (name, hourly_rate),
            )
            parking_lot_id = int(cursor.lastrowid)

            self.connection.executemany(
                """
                INSERT INTO parking_space (
                    parking_lot_id,
                    space_number,
                    size
                ) VALUES (?, ?, ?)
                """,
                [
                    (
                        parking_lot_id,
                        space_number,
                        space_size.value,
                    )
                    for space_number, space_size in enumerate(
                        space_sizes,
                        start=1,
                    )
                ],
            )

        parking_lot = self.get(parking_lot_id)

        if parking_lot is None:
            raise RuntimeError(
                "Created parking lot could not be retrieved"
            )

        return parking_lot

    def get(self, parking_lot_id: int) -> ParkingLot | None:
        row = self.connection.execute(
            """
            SELECT
                lot.id,
                lot.name,
                lot.hourly_rate,
                SUM(
                    CASE WHEN space.size = 'SMALL' THEN 1 ELSE 0 END
                ) AS small_space_count,
                SUM(
                    CASE WHEN space.size = 'MEDIUM' THEN 1 ELSE 0 END
                ) AS medium_space_count,
                SUM(
                    CASE WHEN space.size = 'LARGE' THEN 1 ELSE 0 END
                ) AS large_space_count
            FROM parking_lot AS lot
            LEFT JOIN parking_space AS space
                ON space.parking_lot_id = lot.id
            WHERE lot.id = ?
            GROUP BY lot.id, lot.name, lot.hourly_rate
            """,
            (parking_lot_id,),
        ).fetchone()

        if row is None:
            return None

        return self._to_parking_lot(row)

    def list_all(self) -> list[ParkingLot]:
        rows = self.connection.execute(
            """
            SELECT
                lot.id,
                lot.name,
                lot.hourly_rate,
                SUM(
                    CASE WHEN space.size = 'SMALL' THEN 1 ELSE 0 END
                ) AS small_space_count,
                SUM(
                    CASE WHEN space.size = 'MEDIUM' THEN 1 ELSE 0 END
                ) AS medium_space_count,
                SUM(
                    CASE WHEN space.size = 'LARGE' THEN 1 ELSE 0 END
                ) AS large_space_count
            FROM parking_lot AS lot
            LEFT JOIN parking_space AS space
                ON space.parking_lot_id = lot.id
            GROUP BY lot.id, lot.name, lot.hourly_rate
            ORDER BY lot.id
            """
        ).fetchall()

        return [self._to_parking_lot(row) for row in rows]

    @staticmethod
    def _to_parking_lot(row: sqlite3.Row) -> ParkingLot:
        return ParkingLot(
            id=row["id"],
            name=row["name"],
            hourly_rate=row["hourly_rate"],
            small_space_count=row["small_space_count"],
            medium_space_count=row["medium_space_count"],
            large_space_count=row["large_space_count"],
        )