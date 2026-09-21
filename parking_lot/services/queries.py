from parking_lot.domain.exceptions import (
    InvalidRegistrationNumberError,
    ParkingLotNotFoundError,
    ParkingTicketNotFoundError,
)
from parking_lot.domain.models import (
    OccupiedSpace,
    ParkingAvailability,
    ParkingTicket,
    TicketState,
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


class ParkingQueryService:
    def __init__(
        self,
        parking_lot_repository: ParkingLotRepository,
        parking_space_repository: ParkingSpaceRepository,
        parking_ticket_repository: ParkingTicketRepository,
    ) -> None:
        self.parking_lot_repository = parking_lot_repository
        self.parking_space_repository = parking_space_repository
        self.parking_ticket_repository = (
            parking_ticket_repository
        )

    def get_availability(
        self,
        parking_lot_id: int,
    ) -> ParkingAvailability:
        self._require_parking_lot(parking_lot_id)

        return self.parking_space_repository.get_availability(
            parking_lot_id
        )

    def list_occupied_spaces(
        self,
        parking_lot_id: int,
    ) -> list[OccupiedSpace]:
        self._require_parking_lot(parking_lot_id)

        return self.parking_space_repository.list_occupied(
            parking_lot_id
        )

    def get_ticket(
        self,
        parking_lot_id: int,
        ticket_id: int,
    ) -> ParkingTicket:
        self._require_parking_lot(parking_lot_id)

        ticket = (
            self.parking_ticket_repository
            .get_for_parking_lot(
                parking_lot_id=parking_lot_id,
                ticket_id=ticket_id,
            )
        )

        if ticket is None:
            raise ParkingTicketNotFoundError(
                f"Parking ticket {ticket_id} does not exist"
            )

        return ticket

    def list_tickets(
        self,
        parking_lot_id: int,
        registration_number: str | None = None,
        state: TicketState | None = None,
    ) -> list[ParkingTicket]:
        self._require_parking_lot(parking_lot_id)

        normalised_registration = None

        if registration_number is not None:
            normalised_registration = (
                registration_number.strip().upper()
            )

            if not normalised_registration:
                raise InvalidRegistrationNumberError(
                    "Registration number cannot be blank"
                )

        return (
            self.parking_ticket_repository
            .list_for_parking_lot(
                parking_lot_id=parking_lot_id,
                registration_number=normalised_registration,
                state=state,
            )
        )

    def _require_parking_lot(
        self,
        parking_lot_id: int,
    ) -> None:
        if self.parking_lot_repository.get(
            parking_lot_id
        ) is None:
            raise ParkingLotNotFoundError(
                f"Parking lot {parking_lot_id} does not exist"
            )