from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from fastapi.testclient import TestClient

from parking_lot.app import create_app
from parking_lot.database import initialise_database


class ParkingApiTest(TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        database_path = (
            Path(self.temporary_directory.name) / "test.db"
        )
        initialise_database(database_path)
        self.client = TestClient(create_app(database_path))

        response = self.client.post(
            "/parking-lots",
            json={
                "name": "Forum Parking",
                "small_space_count": 1,
                "medium_space_count": 1,
                "large_space_count": 1,
                "hourly_rate": 10,
            },
        )
        self.parking_lot_id = response.json()["id"]

    def tearDown(self) -> None:
        self.client.close()
        self.temporary_directory.cleanup()

    def test_park_vehicle_issues_ticket(self) -> None:
        response = self._park(" ka-01-ab-1234 ")

        self.assertEqual(201, response.status_code)

        ticket = response.json()
        self.assertEqual(
            "KA-01-AB-1234",
            ticket["registration_number"],
        )
        self.assertEqual(1, ticket["space_number"])
        self.assertEqual("SMALL", ticket["space_size"])
        self.assertEqual("PARKED", ticket["state"])
        self.assertIsNone(ticket["exited_at"])
        self.assertIsNone(ticket["billed_hours"])
        self.assertIsNone(ticket["total_cost"])
        self.assertEqual(10, ticket["hourly_rate"])

    def test_park_uses_next_compatible_space(self) -> None:
        self._park("KA-01-AB-0001")

        response = self._park("KA-01-AB-0002")

        self.assertEqual(201, response.status_code)
        self.assertEqual(2, response.json()["space_number"])
        self.assertEqual("MEDIUM", response.json()["space_size"])

    def test_park_rejects_duplicate_registration(self) -> None:
        self._park("KA-01-AB-1234")

        response = self._park("ka-01-ab-1234")

        self.assertEqual(409, response.status_code)
        self.assertEqual(
            "VEHICLE_ALREADY_PARKED",
            response.json()["error"]["code"],
        )

    def test_park_rejects_full_parking_lot(self) -> None:
        self._park("KA-01-AB-0001")
        self._park("KA-01-AB-0002")
        self._park("KA-01-AB-0003")

        response = self._park("KA-01-AB-0004")

        self.assertEqual(409, response.status_code)
        self.assertEqual(
            "PARKING_LOT_FULL",
            response.json()["error"]["code"],
        )

    def test_park_rejects_blank_registration(self) -> None:
        response = self._park(" ")

        self.assertEqual(422, response.status_code)
        self.assertEqual(
            "INVALID_REGISTRATION_NUMBER",
            response.json()["error"]["code"],
        )

    def test_park_rejects_unknown_parking_lot(self) -> None:
        response = self.client.post(
            "/parking-lots/999/tickets",
            json={"registration_number": "KA-01-AB-1234"},
        )

        self.assertEqual(404, response.status_code)
        self.assertEqual(
            "PARKING_LOT_NOT_FOUND",
            response.json()["error"]["code"],
        )

    def _park(self, registration_number: str):
        return self.client.post(
            f"/parking-lots/{self.parking_lot_id}/tickets",
            json={"registration_number": registration_number},
        )