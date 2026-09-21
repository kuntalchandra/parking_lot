from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from fastapi.testclient import TestClient

from parking_lot.app import create_app
from parking_lot.database import initialise_database


class ExitApiTest(TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        database_path = (
            Path(self.temporary_directory.name) / "test.db"
        )
        initialise_database(database_path)
        self.client = TestClient(create_app(database_path))

        lot_response = self.client.post(
            "/parking-lots",
            json={
                "name": "Forum Parking",
                "small_space_count": 1,
                "medium_space_count": 0,
                "large_space_count": 0,
                "hourly_rate": 10,
            },
        )
        self.parking_lot_id = lot_response.json()["id"]

    def tearDown(self) -> None:
        self.client.close()
        self.temporary_directory.cleanup()

    def test_exit_returns_updated_ticket(self) -> None:
        parked_ticket = self._park("KA-01-AB-1234").json()

        response = self._exit(parked_ticket["id"])

        self.assertEqual(200, response.status_code)

        exited_ticket = response.json()
        self.assertEqual("EXITED", exited_ticket["state"])
        self.assertIsNotNone(exited_ticket["exited_at"])
        self.assertEqual(1, exited_ticket["billed_hours"])
        self.assertEqual(10, exited_ticket["total_cost"])

    def test_exit_rejects_already_exited_ticket(self) -> None:
        parked_ticket = self._park("KA-01-AB-1234").json()
        self._exit(parked_ticket["id"])

        response = self._exit(parked_ticket["id"])

        self.assertEqual(409, response.status_code)
        self.assertEqual(
            "PARKING_TICKET_ALREADY_EXITED",
            response.json()["error"]["code"],
        )

    def test_exit_rejects_unknown_ticket(self) -> None:
        response = self._exit(999)

        self.assertEqual(404, response.status_code)
        self.assertEqual(
            "PARKING_TICKET_NOT_FOUND",
            response.json()["error"]["code"],
        )

    def test_exit_releases_space(self) -> None:
        first_ticket = self._park("KA-01-AB-0001").json()
        self._exit(first_ticket["id"])

        second_response = self._park("KA-01-AB-0002")

        self.assertEqual(201, second_response.status_code)
        self.assertEqual(
            first_ticket["space_number"],
            second_response.json()["space_number"],
        )

    def _park(self, registration_number: str):
        return self.client.post(
            f"/parking-lots/{self.parking_lot_id}/tickets",
            json={"registration_number": registration_number},
        )

    def _exit(self, ticket_id: int):
        return self.client.post(
            f"/parking-lots/{self.parking_lot_id}"
            f"/tickets/{ticket_id}/exit"
        )