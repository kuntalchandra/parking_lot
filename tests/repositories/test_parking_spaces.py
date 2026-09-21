from unittest import TestCase

from parking_lot.database import (
    connect_database,
    initialise_schema,
)
from parking_lot.domain.models import ParkingSpaceSize
from parking_lot.repositories.parking_lots import (
    ParkingLotRepository,
)
from parking_lot.repositories.parking_spaces import (
    ParkingSpaceRepository,
)


class ParkingSpaceRepositoryTest(TestCase):
    def setUp(self) -> None:
        self.connection = connect_database(":memory:")
        initialise_schema(self.connection)

        lot_repository = ParkingLotRepository(self.connection)
        self.parking_lot = lot_repository.create(
            name="Forum Parking",
            hourly_rate=10,
            space_sizes=[
                ParkingSpaceSize.SMALL,
                ParkingSpaceSize.SMALL,
                ParkingSpaceSize.MEDIUM,
                ParkingSpaceSize.LARGE,
            ],
        )

        self.repository = ParkingSpaceRepository(self.connection)

    def tearDown(self) -> None:
        self.connection.close()

    def test_finds_nearest_space_using_size_priority(self) -> None:
        space = self.repository.find_nearest_available(
            parking_lot_id=self.parking_lot.id,
            preferred_sizes=(
                ParkingSpaceSize.SMALL,
                ParkingSpaceSize.MEDIUM,
                ParkingSpaceSize.LARGE,
            ),
        )

        self.assertIsNotNone(space)
        self.assertEqual(1, space.space_number)
        self.assertEqual(ParkingSpaceSize.SMALL, space.size)

    def test_skips_occupied_space(self) -> None:
        self._occupy_space(
            space_number=1,
            registration_number="KA-01-AB-1234",
        )

        space = self.repository.find_nearest_available(
            parking_lot_id=self.parking_lot.id,
            preferred_sizes=(
                ParkingSpaceSize.SMALL,
                ParkingSpaceSize.MEDIUM,
                ParkingSpaceSize.LARGE,
            ),
        )

        self.assertIsNotNone(space)
        self.assertEqual(2, space.space_number)
        self.assertEqual(ParkingSpaceSize.SMALL, space.size)

    def test_falls_back_to_medium_then_large(self) -> None:
        self._occupy_space(1, "KA-01-AB-0001")
        self._occupy_space(2, "KA-01-AB-0002")

        space = self.repository.find_nearest_available(
            parking_lot_id=self.parking_lot.id,
            preferred_sizes=(
                ParkingSpaceSize.SMALL,
                ParkingSpaceSize.MEDIUM,
                ParkingSpaceSize.LARGE,
            ),
        )

        self.assertIsNotNone(space)
        self.assertEqual(3, space.space_number)
        self.assertEqual(ParkingSpaceSize.MEDIUM, space.size)

    def test_returns_none_when_no_compatible_space_exists(
        self,
    ) -> None:
        self._occupy_space(1, "KA-01-AB-0001")
        self._occupy_space(2, "KA-01-AB-0002")
        self._occupy_space(3, "KA-01-AB-0003")
        self._occupy_space(4, "KA-01-AB-0004")

        space = self.repository.find_nearest_available(
            parking_lot_id=self.parking_lot.id,
            preferred_sizes=(
                ParkingSpaceSize.SMALL,
                ParkingSpaceSize.MEDIUM,
                ParkingSpaceSize.LARGE,
            ),
        )

        self.assertIsNone(space)

    def _occupy_space(
        self,
        space_number: int,
        registration_number: str,
    ) -> None:
        space = self.connection.execute(
            """
            SELECT id
            FROM parking_space
            WHERE parking_lot_id = ?
              AND space_number = ?
            """,
            (self.parking_lot.id, space_number),
        ).fetchone()

        self.connection.execute(
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
                self.parking_lot.id,
                space["id"],
                registration_number,
                "2026-09-21T10:30:00Z",
                10,
            ),
        )
        self.connection.commit()