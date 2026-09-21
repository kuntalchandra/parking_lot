from __future__ import annotations

import sqlite3

from parking_lot.database import transaction
from parking_lot.domain.allocation import SpaceAllocationPolicy
from parking_lot.domain.clock import Clock
from parking_lot.domain.exceptions import (
    InvalidRegistrationNumberError,
    ParkingLotFullError,
    ParkingLotNotFoundError,
    VehicleAlreadyParkedError,
)
from parking_lot.domain.models import (
    ParkingTicket,
    VehicleSize,
)
from parking_lot.repositories.parking_lots import (
    ParkingLotRepository,
)
from parking_lot.repositories.parking_spaces import (
    ParkingSpaceRepository,
)
from parking_lot.repositories.parking_tickets import (
    ParkingTicketRepository,
)


class ParkingService:
    def __init__(
        self,
        connection: sqlite3.Connection,
        parking_lot_repository: ParkingLotRepository,
        parking_space_repository: ParkingSpaceRepository,
        parking_ticket_repository: ParkingTicketRepository,
        allocation_policy: SpaceAllocationPolicy,
        clock: Clock,
    ) -> None:
        self.connection = connection
        self.parking_lot_repository = parking_lot_repository
        self.parking_space_repository = parking_space_repository
        self.parking_ticket_repository = parking_ticket_repository
        self.allocation_policy = allocation_policy
        self.clock = clock

    def park_vehicle(
        self,
        parking_lot_id: int,
        registration_number: str,
    ) -> ParkingTicket:
        normalised_registration = (
            registration_number.strip().upper()
        )

        if not normalised_registration:
            raise InvalidRegistrationNumberError(
                "Registration number cannot be blank"
            )

        try:
            with transaction(self.connection):
                parking_lot = self.parking_lot_repository.get(
                    parking_lot_id
                )

                if parking_lot is None:
                    raise ParkingLotNotFoundError(
                        f"Parking lot {parking_lot_id} does not exist"
                    )

                existing_ticket = (
                    self.parking_ticket_repository
                    .find_parked_by_registration(
                        normalised_registration
                    )
                )

                if existing_ticket is not None:
                    raise VehicleAlreadyParkedError(
                        f"Vehicle {normalised_registration} "
                        "is already parked"
                    )

                preferred_sizes = (
                    self.allocation_policy.preferred_space_sizes(
                        VehicleSize.SMALL
                    )
                )
                parking_space = (
                    self.parking_space_repository
                    .find_nearest_available(
                        parking_lot_id,
                        preferred_sizes,
                    )
                )

                if parking_space is None:
                    raise ParkingLotFullError(
                        "No compatible parking space is available"
                    )

                return (
                    self.parking_ticket_repository.create_parked(
                        parking_lot=parking_lot,
                        parking_space=parking_space,
                        registration_number=normalised_registration,
                        parked_at=self.clock.now(),
                    )
                )

        except sqlite3.IntegrityError as exception:
            message = str(exception)

            if "registration_number" in message:
                raise VehicleAlreadyParkedError(
                    f"Vehicle {normalised_registration} "
                    "is already parked"
                ) from exception

            raise ParkingLotFullError(
                "The selected parking space is no longer available"
            ) from exception