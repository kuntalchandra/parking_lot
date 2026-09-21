from unittest import TestCase
from unittest.mock import create_autospec

from parking_lot.domain.exceptions import (
    InvalidParkingLotConfigurationError,
    ParkingLotNotFoundError,
)
from parking_lot.domain.models import (
    ParkingLot,
    ParkingSpaceSize,
)
from parking_lot.repositories.parking_lots import (
    ParkingLotRepository,
)
from parking_lot.services.parking_lots import (
    ParkingLotService,
)


class ParkingLotServiceTest(TestCase):
    def setUp(self) -> None:
        self.repository = create_autospec(
            ParkingLotRepository,
            instance=True,
        )
        self.service = ParkingLotService(self.repository)

    def test_create_builds_spaces_in_size_priority_order(
        self,
    ) -> None:
        expected = ParkingLot(
            id=1,
            name="Forum Parking",
            hourly_rate=10,
            small_space_count=2,
            medium_space_count=1,
            large_space_count=1,
        )
        self.repository.create.return_value = expected

        result = self.service.create_parking_lot(
            name="  Forum Parking  ",
            small_space_count=2,
            medium_space_count=1,
            large_space_count=1,
            hourly_rate=10,
        )

        self.assertEqual(expected, result)
        self.repository.create.assert_called_once_with(
            name="Forum Parking",
            hourly_rate=10,
            space_sizes=[
                ParkingSpaceSize.SMALL,
                ParkingSpaceSize.SMALL,
                ParkingSpaceSize.MEDIUM,
                ParkingSpaceSize.LARGE,
            ],
        )

    def test_create_rejects_blank_name(self) -> None:
        with self.assertRaises(
            InvalidParkingLotConfigurationError
        ):
            self.service.create_parking_lot(
                name=" ",
                small_space_count=1,
                medium_space_count=0,
                large_space_count=0,
                hourly_rate=10,
            )

        self.repository.create.assert_not_called()

    def test_create_rejects_negative_space_count(self) -> None:
        with self.assertRaises(
            InvalidParkingLotConfigurationError
        ):
            self.service.create_parking_lot(
                name="Forum Parking",
                small_space_count=-1,
                medium_space_count=1,
                large_space_count=1,
                hourly_rate=10,
            )

    def test_create_requires_at_least_one_space(self) -> None:
        with self.assertRaises(
            InvalidParkingLotConfigurationError
        ):
            self.service.create_parking_lot(
                name="Forum Parking",
                small_space_count=0,
                medium_space_count=0,
                large_space_count=0,
                hourly_rate=10,
            )

    def test_create_rejects_non_positive_hourly_rate(self) -> None:
        with self.assertRaises(
            InvalidParkingLotConfigurationError
        ):
            self.service.create_parking_lot(
                name="Forum Parking",
                small_space_count=1,
                medium_space_count=0,
                large_space_count=0,
                hourly_rate=0,
            )

    def test_get_raises_when_parking_lot_is_unknown(self) -> None:
        self.repository.get.return_value = None

        with self.assertRaises(ParkingLotNotFoundError):
            self.service.get_parking_lot(999)

    def test_list_returns_repository_results(self) -> None:
        parking_lot = ParkingLot(
            id=1,
            name="Forum Parking",
            hourly_rate=10,
            small_space_count=1,
            medium_space_count=0,
            large_space_count=0,
        )
        self.repository.list_all.return_value = [parking_lot]

        self.assertEqual(
            [parking_lot],
            self.service.list_parking_lots(),
        )