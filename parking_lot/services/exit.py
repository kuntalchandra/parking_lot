from __future__ import annotations

import sqlite3

from parking_lot.database import transaction
from parking_lot.domain.clock import Clock
from parking_lot.domain.exceptions import (
    ParkingLotNotFoundError,
    ParkingTicketAlreadyExitedError,
    ParkingTicketNotFoundError,
)
from parking_lot.domain.models import (
    ParkingTicket,
    TicketState,
)
from parking_lot.domain.pricing import PricingPolicy
from parking_lot.repositories.parking_lots import (
    ParkingLotRepository,
)
from parking_lot.repositories.parking_tickets import (
    ParkingTicketRepository,
)


class ExitService:
    def __init__(
        self,
        connection: sqlite3.Connection,
        parking_lot_repository: ParkingLotRepository,
        parking_ticket_repository: ParkingTicketRepository,
        pricing_policy: PricingPolicy,
        clock: Clock,
    ) -> None:
        self.connection = connection
        self.parking_lot_repository = parking_lot_repository
        self.parking_ticket_repository = (
            parking_ticket_repository
        )
        self.pricing_policy = pricing_policy
        self.clock = clock

    def exit_vehicle(
        self,
        parking_lot_id: int,
        ticket_id: int,
    ) -> ParkingTicket:
        with transaction(self.connection):
            parking_lot = self.parking_lot_repository.get(
                parking_lot_id
            )

            if parking_lot is None:
                raise ParkingLotNotFoundError(
                    f"Parking lot {parking_lot_id} does not exist"
                )

            ticket = self.parking_ticket_repository.get(ticket_id)

            if (
                ticket is None
                or ticket.parking_lot_id != parking_lot_id
            ):
                raise ParkingTicketNotFoundError(
                    f"Parking ticket {ticket_id} does not exist"
                )

            if ticket.state is TicketState.EXITED:
                raise ParkingTicketAlreadyExitedError(
                    f"Parking ticket {ticket_id} has already exited"
                )

            exited_at = self.clock.now()
            charge = self.pricing_policy.calculate(
                parked_at=ticket.parked_at,
                exited_at=exited_at,
                hourly_rate=ticket.hourly_rate,
            )

            exited_ticket = (
                self.parking_ticket_repository.mark_exited(
                    ticket_id=ticket.id,
                    exited_at=exited_at,
                    billed_hours=charge.billed_hours,
                    total_cost=charge.total_cost,
                )
            )

            if exited_ticket is None:
                raise ParkingTicketAlreadyExitedError(
                    f"Parking ticket {ticket_id} has already exited"
                )

            return exited_ticket