from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from fastapi.testclient import TestClient

from parking_lot.app import create_app
from parking_lot.database import initialise_database


class ParkingLotApiTest(TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.database_path = (
            Path(self.temporary_directory.name) / "test.db"
        )
        initialise_database(self.database_path)

        self.client = TestClient(
            create_app(self.database_path)
        )

    def tearDown(self) -> None:
        self.client.close()
        self.temporary_directory.cleanup()

    def test_create_parking_lot(self) -> None:
        response = self._create_parking_lot()

        self.assertEqual(201, response.status_code)
        self.assertEqual(
            {
                "id": 1,
                "name": "Forum Parking",
                "hourly_rate": 10,
                "small_space_count": 2,
                "medium_space_count": 1,
                "large_space_count": 1,
            },
            response.json(),
        )

    def test_create_rejects_second_parking_lot(self) -> None:
        self._create_parking_lot()

        response = self._create_parking_lot()

        self.assertEqual(409, response.status_code)
        self.assertEqual(
            "PARKING_LOT_ALREADY_EXISTS",
            response.json()["error"]["code"],
        )

    def test_create_requires_at_least_one_space(self) -> None:
        response = self.client.post(
            "/parking-lots",
            json={
                "name": "Forum Parking",
                "small_space_count": 0,
                "medium_space_count": 0,
                "large_space_count": 0,
                "hourly_rate": 10,
            },
        )

        self.assertEqual(422, response.status_code)
        self.assertEqual(
            "INVALID_PARKING_LOT_CONFIGURATION",
            response.json()["error"]["code"],
        )

    def test_get_parking_lot(self) -> None:
        created = self._create_parking_lot().json()

        response = self.client.get(
            f"/parking-lots/{created['id']}"
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(created, response.json())

    def test_get_unknown_parking_lot_returns_not_found(
        self,
    ) -> None:
        response = self.client.get("/parking-lots/999")

        self.assertEqual(404, response.status_code)
        self.assertEqual(
            "PARKING_LOT_NOT_FOUND",
            response.json()["error"]["code"],
        )

    def test_list_parking_lots(self) -> None:
        created = self._create_parking_lot().json()

        response = self.client.get("/parking-lots")

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {"parking_lots": [created]},
            response.json(),
        )

    def _create_parking_lot(self):
        return self.client.post(
            "/parking-lots",
            json={
                "name": "Forum Parking",
                "small_space_count": 2,
                "medium_space_count": 1,
                "large_space_count": 1,
                "hourly_rate": 10,
            },
        )