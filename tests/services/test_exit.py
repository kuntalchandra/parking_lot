from datetime import datetime, timedelta, timezone
from unittest import TestCase

from parking_lot.database import (
    connect_database,
    initialise_schema,
)
from parking_lot.domain.allocation import (
    DefaultSpaceAllocationPolicy,
)
from parking_lot.domain.exceptions import (
    InvalidParkingDurationError,
    ParkingLotNotFoundError,
    ParkingTicketAlreadyExitedError,
    ParkingTicketNotFoundError,
)
from parking_lot.domain.models import (
    ParkingSpaceSize,
    TicketState,
)
from parking_lot.domain.pricing import (
    FixedHourlyPricingPolicy,
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
from parking_lot.services.exit import ExitService
from parking_lot.services.parking import ParkingService


class FixedClock:
    def __init__(self, current_time: datetime) -> None:
        self.current_time = current_time

    def now(self) -> datetime:
        return self.current_time


class ExitServiceTest(TestCase):
    def setUp(self) -> None:
        self.connection = connect_database(":memory:")
        initialise_schema(self.connection)

        self.lot_repository = ParkingLotRepository(
            self.connection
        )
        self.space_repository = ParkingSpaceRepository(
            self.connection
        )
        self.ticket_repository = ParkingTicketRepository(
            self.connection
        )

        self.parking_lot = self.lot_repository.create(
            name="Forum Parking",
            hourly_rate=10,
            space_sizes=[ParkingSpaceSize.SMALL],
        )

        self.parked_at = datetime(
            2026,
            9,
            21,
            10,
            0,
            tzinfo=timezone.utc,
        )
        self.exited_at = self.parked_at + timedelta(
            hours=1,
            minutes=1,
        )

        self.parking_service = ParkingService(
            connection=self.connection,
            parking_lot_repository=self.lot_repository,
            parking_space_repository=self.space_repository,
            parking_ticket_repository=self.ticket_repository,
            allocation_policy=DefaultSpaceAllocationPolicy(),
            clock=FixedClock(self.parked_at),
        )
        self.exit_service = self._create_exit_service(
            self.exited_at
        )

    def tearDown(self) -> None:
        self.connection.close()

    def test_exit_updates_ticket_and_calculates_cost(self) -> None:
        parked_ticket = self._park()

        exited_ticket = self.exit_service.exit_vehicle(
            parking_lot_id=self.parking_lot.id,
            ticket_id=parked_ticket.id,
        )

        self.assertEqual(TicketState.EXITED, exited_ticket.state)
        self.assertEqual(self.exited_at, exited_ticket.exited_at)
        self.assertEqual(2, exited_ticket.billed_hours)
        self.assertEqual(20, exited_ticket.total_cost)

    def test_exit_rejects_already_exited_ticket(self) -> None:
        parked_ticket = self._park()
        self.exit_service.exit_vehicle(
            self.parking_lot.id,
            parked_ticket.id,
        )

        with self.assertRaises(
            ParkingTicketAlreadyExitedError
        ):
            self.exit_service.exit_vehicle(
                self.parking_lot.id,
                parked_ticket.id,
            )

    def test_exit_rejects_unknown_ticket(self) -> None:
        with self.assertRaises(ParkingTicketNotFoundError):
            self.exit_service.exit_vehicle(
                self.parking_lot.id,
                999,
            )

    def test_exit_rejects_unknown_parking_lot(self) -> None:
        parked_ticket = self._park()

        with self.assertRaises(ParkingLotNotFoundError):
            self.exit_service.exit_vehicle(
                999,
                parked_ticket.id,
            )

    def test_exit_rejects_time_before_parking(self) -> None:
        parked_ticket = self._park()
        invalid_exit_service = self._create_exit_service(
            self.parked_at - timedelta(seconds=1)
        )

        with self.assertRaises(InvalidParkingDurationError):
            invalid_exit_service.exit_vehicle(
                self.parking_lot.id,
                parked_ticket.id,
            )

        stored_ticket = self.ticket_repository.get(
            parked_ticket.id
        )
        self.assertEqual(TicketState.PARKED, stored_ticket.state)

    def test_exit_releases_space_for_next_vehicle(self) -> None:
        first_ticket = self._park()
        self.exit_service.exit_vehicle(
            self.parking_lot.id,
            first_ticket.id,
        )

        second_ticket = self.parking_service.park_vehicle(
            self.parking_lot.id,
            "KA-01-AB-9999",
        )

        self.assertEqual(
            first_ticket.space_number,
            second_ticket.space_number,
        )

    def _park(self):
        return self.parking_service.park_vehicle(
            self.parking_lot.id,
            "KA-01-AB-1234",
        )

    def _create_exit_service(
        self,
        exited_at: datetime,
    ) -> ExitService:
        return ExitService(
            connection=self.connection,
            parking_lot_repository=self.lot_repository,
            parking_ticket_repository=self.ticket_repository,
            pricing_policy=FixedHourlyPricingPolicy(),
            clock=FixedClock(exited_at),
        )