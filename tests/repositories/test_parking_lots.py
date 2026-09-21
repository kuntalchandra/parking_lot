from unittest import TestCase

from parking_lot.database import (
    connect_database,
    initialise_schema,
)
from parking_lot.domain.exceptions import (
    ParkingLotAlreadyExistsError,
)
from parking_lot.domain.models import ParkingSpaceSize
from parking_lot.repositories.parking_lots import (
    ParkingLotRepository,
)


class ParkingLotRepositoryTest(TestCase):
    def setUp(self) -> None:
        self.connection = connect_database(":memory:")
        initialise_schema(self.connection)
        self.repository = ParkingLotRepository(self.connection)

    def tearDown(self) -> None:
        self.connection.close()

    def test_create_generates_sequential_spaces_by_size(self) -> None:
        parking_lot = self.repository.create(
            name="Forum Parking",
            hourly_rate=10,
            space_sizes=[
                ParkingSpaceSize.SMALL,
                ParkingSpaceSize.SMALL,
                ParkingSpaceSize.MEDIUM,
                ParkingSpaceSize.LARGE,
            ],
        )

        rows = self.connection.execute(
            """
            SELECT space_number, size
            FROM parking_space
            WHERE parking_lot_id = ?
            ORDER BY space_number
            """,
            (parking_lot.id,),
        ).fetchall()

        self.assertEqual(
            [
                (1, "SMALL"),
                (2, "SMALL"),
                (3, "MEDIUM"),
                (4, "LARGE"),
            ],
            [(row["space_number"], row["size"]) for row in rows],
        )

        self.assertEqual(2, parking_lot.small_space_count)
        self.assertEqual(1, parking_lot.medium_space_count)
        self.assertEqual(1, parking_lot.large_space_count)

    def test_create_rejects_a_second_parking_lot(self) -> None:
        self.repository.create(
            name="First Parking",
            hourly_rate=10,
            space_sizes=[ParkingSpaceSize.SMALL],
        )

        with self.assertRaises(ParkingLotAlreadyExistsError):
            self.repository.create(
                name="Second Parking",
                hourly_rate=20,
                space_sizes=[ParkingSpaceSize.SMALL],
            )

    def test_get_returns_none_for_unknown_parking_lot(self) -> None:
        self.assertIsNone(self.repository.get(999))

    def test_list_all_returns_created_parking_lot(self) -> None:
        created = self.repository.create(
            name="Forum Parking",
            hourly_rate=10,
            space_sizes=[
                ParkingSpaceSize.SMALL,
                ParkingSpaceSize.MEDIUM,
            ],
        )

        self.assertEqual([created], self.repository.list_all())