from __future__ import annotations

import sqlite3
from datetime import datetime

from parking_lot.domain.models import (
    ParkingLot,
    ParkingSpace,
    ParkingSpaceSize,
    ParkingTicket,
    TicketState,
)


class ParkingTicketRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def find_parked_by_registration(
        self,
        registration_number: str,
    ) -> ParkingTicket | None:
        row = self.connection.execute(
            """
            SELECT
                ticket.id,
                ticket.parking_lot_id,
                ticket.parking_space_id,
                space.space_number,
                space.size AS space_size,
                ticket.registration_number,
                ticket.parked_at,
                ticket.exited_at,
                ticket.billed_hours,
                ticket.hourly_rate,
                ticket.total_cost,
                ticket.state
            FROM parking_ticket AS ticket
            JOIN parking_space AS space
                ON space.id = ticket.parking_space_id
               AND space.parking_lot_id = ticket.parking_lot_id
            WHERE ticket.registration_number = ?
              AND ticket.state = 'PARKED'
            """,
            (registration_number,),
        ).fetchone()

        return self._to_ticket(row) if row is not None else None

    def create_parked(
        self,
        parking_lot: ParkingLot,
        parking_space: ParkingSpace,
        registration_number: str,
        parked_at: datetime,
    ) -> ParkingTicket:
        cursor = self.connection.execute(
            """
            INSERT INTO parking_ticket (
                parking_lot_id,
                parking_space_id,
                registration_number,
                parked_at,
                hourly_rate,
                state
            ) VALUES (?, ?, ?, ?, ?, 'PARKED')
            """,
            (
                parking_lot.id,
                parking_space.id,
                registration_number,
                parked_at.isoformat(),
                parking_lot.hourly_rate,
            ),
        )

        ticket = self.get(int(cursor.lastrowid))

        if ticket is None:
            raise RuntimeError(
                "Created parking ticket could not be retrieved"
            )

        return ticket

    def get(self, ticket_id: int) -> ParkingTicket | None:
        row = self.connection.execute(
            """
            SELECT
                ticket.id,
                ticket.parking_lot_id,
                ticket.parking_space_id,
                space.space_number,
                space.size AS space_size,
                ticket.registration_number,
                ticket.parked_at,
                ticket.exited_at,
                ticket.billed_hours,
                ticket.hourly_rate,
                ticket.total_cost,
                ticket.state
            FROM parking_ticket AS ticket
            JOIN parking_space AS space
                ON space.id = ticket.parking_space_id
               AND space.parking_lot_id = ticket.parking_lot_id
            WHERE ticket.id = ?
            """,
            (ticket_id,),
        ).fetchone()

        return self._to_ticket(row) if row is not None else None

    def mark_exited(
        self,
        ticket_id: int,
        exited_at: datetime,
        billed_hours: int,
        total_cost: int,
    ) -> ParkingTicket | None:
        cursor = self.connection.execute(
            """
            UPDATE parking_ticket
            SET exited_at = ?,
                billed_hours = ?,
                total_cost = ?,
                state = 'EXITED'
            WHERE id = ?
              AND state = 'PARKED'
            """,
            (
                exited_at.isoformat(),
                billed_hours,
                total_cost,
                ticket_id,
            ),
        )

        if cursor.rowcount == 0:
            return None

        return self.get(ticket_id)

    @staticmethod
    def _to_ticket(row: sqlite3.Row) -> ParkingTicket:
        return ParkingTicket(
            id=row["id"],
            parking_lot_id=row["parking_lot_id"],
            parking_space_id=row["parking_space_id"],
            space_number=row["space_number"],
            space_size=ParkingSpaceSize(row["space_size"]),
            registration_number=row["registration_number"],
            parked_at=datetime.fromisoformat(row["parked_at"]),
            exited_at=(
                datetime.fromisoformat(row["exited_at"])
                if row["exited_at"] is not None
                else None
            ),
            billed_hours=row["billed_hours"],
            hourly_rate=row["hourly_rate"],
            total_cost=row["total_cost"],
            state=TicketState(row["state"]),
        )

    def get_for_parking_lot(
        self,
        parking_lot_id: int,
        ticket_id: int,
    ) -> ParkingTicket | None:
        row = self.connection.execute(
            """
            SELECT
                ticket.id,
                ticket.parking_lot_id,
                ticket.parking_space_id,
                space.space_number,
                space.size AS space_size,
                ticket.registration_number,
                ticket.parked_at,
                ticket.exited_at,
                ticket.billed_hours,
                ticket.hourly_rate,
                ticket.total_cost,
                ticket.state
            FROM parking_ticket AS ticket
            JOIN parking_space AS space
                ON space.id = ticket.parking_space_id
               AND space.parking_lot_id =
                   ticket.parking_lot_id
            WHERE ticket.parking_lot_id = ?
              AND ticket.id = ?
            """,
            (parking_lot_id, ticket_id),
        ).fetchone()

        return self._to_ticket(row) if row is not None else None

    def list_for_parking_lot(
        self,
        parking_lot_id: int,
        registration_number: str | None = None,
        state: TicketState | None = None,
    ) -> list[ParkingTicket]:
        conditions = ["ticket.parking_lot_id = ?"]
        parameters: list[object] = [parking_lot_id]

        if registration_number is not None:
            conditions.append(
                "ticket.registration_number = ?"
            )
            parameters.append(registration_number)

        if state is not None:
            conditions.append("ticket.state = ?")
            parameters.append(state.value)

        where_clause = " AND ".join(conditions)

        rows = self.connection.execute(
            f"""
            SELECT
                ticket.id,
                ticket.parking_lot_id,
                ticket.parking_space_id,
                space.space_number,
                space.size AS space_size,
                ticket.registration_number,
                ticket.parked_at,
                ticket.exited_at,
                ticket.billed_hours,
                ticket.hourly_rate,
                ticket.total_cost,
                ticket.state
            FROM parking_ticket AS ticket
            JOIN parking_space AS space
                ON space.id = ticket.parking_space_id
               AND space.parking_lot_id =
                   ticket.parking_lot_id
            WHERE {where_clause}
            ORDER BY ticket.parked_at DESC, ticket.id DESC
            """,
            parameters,
        ).fetchall()

        return [self._to_ticket(row) for row in rows]