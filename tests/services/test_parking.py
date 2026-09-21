from datetime import datetime, timezone
from unittest import TestCase

from parking_lot.database import (
    connect_database,
    initialise_schema,
)
from parking_lot.domain.allocation import (
    DefaultSpaceAllocationPolicy,
)
from parking_lot.domain.exceptions import (
    InvalidRegistrationNumberError,
    ParkingLotFullError,
    ParkingLotNotFoundError,
    VehicleAlreadyParkedError,
)
from parking_lot.domain.models import (
    ParkingSpaceSize,
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
from parking_lot.services.parking import ParkingService


class FixedClock:
    def __init__(self, current_time: datetime) -> None:
        self.current_time = current_time

    def now(self) -> datetime:
        return self.current_time


class ParkingServiceTest(TestCase):
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
            space_sizes=[
                ParkingSpaceSize.SMALL,
                ParkingSpaceSize.MEDIUM,
                ParkingSpaceSize.LARGE,
            ],
        )

        self.parked_at = datetime(
            2026,
            9,
            21,
            10,
            30,
            tzinfo=timezone.utc,
        )
        self.service = ParkingService(
            connection=self.connection,
            parking_lot_repository=self.lot_repository,
            parking_space_repository=self.space_repository,
            parking_ticket_repository=self.ticket_repository,
            allocation_policy=DefaultSpaceAllocationPolicy(),
            clock=FixedClock(self.parked_at),
        )

    def tearDown(self) -> None:
        self.connection.close()

    def test_park_issues_ticket_for_nearest_space(self) -> None:
        ticket = self.service.park_vehicle(
            self.parking_lot.id,
            " ka-01-ab-1234 ",
        )

        self.assertEqual("KA-01-AB-1234", ticket.registration_number)
        self.assertEqual(1, ticket.space_number)
        self.assertEqual(ParkingSpaceSize.SMALL, ticket.space_size)
        self.assertEqual(self.parked_at, ticket.parked_at)
        self.assertEqual(TicketState.PARKED, ticket.state)
        self.assertIsNone(ticket.exited_at)
        self.assertIsNone(ticket.total_cost)

    def test_park_uses_next_compatible_space(self) -> None:
        self.service.park_vehicle(
            self.parking_lot.id,
            "KA-01-AB-0001",
        )

        ticket = self.service.park_vehicle(
            self.parking_lot.id,
            "KA-01-AB-0002",
        )

        self.assertEqual(2, ticket.space_number)
        self.assertEqual(ParkingSpaceSize.MEDIUM, ticket.space_size)

    def test_park_rejects_duplicate_registration(self) -> None:
        self.service.park_vehicle(
            self.parking_lot.id,
            "KA-01-AB-1234",
        )

        with self.assertRaises(VehicleAlreadyParkedError):
            self.service.park_vehicle(
                self.parking_lot.id,
                "ka-01-ab-1234",
            )

    def test_park_rejects_blank_registration(self) -> None:
        with self.assertRaises(InvalidRegistrationNumberError):
            self.service.park_vehicle(
                self.parking_lot.id,
                " ",
            )

    def test_park_rejects_unknown_parking_lot(self) -> None:
        with self.assertRaises(ParkingLotNotFoundError):
            self.service.park_vehicle(
                999,
                "KA-01-AB-1234",
            )

    def test_park_rejects_full_parking_lot(self) -> None:
        for index in range(3):
            self.service.park_vehicle(
                self.parking_lot.id,
                f"KA-01-AB-{index:04d}",
            )

        with self.assertRaises(ParkingLotFullError):
            self.service.park_vehicle(
                self.parking_lot.id,
                "KA-01-AB-9999",
            )