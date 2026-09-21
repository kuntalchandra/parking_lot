from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from fastapi.testclient import TestClient

from parking_lot.app import create_app
from parking_lot.database import initialise_database


class ParkingQueryApiTest(TestCase):
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
                "small_space_count": 2,
                "medium_space_count": 1,
                "large_space_count": 1,
                "hourly_rate": 10,
            },
        )
        self.parking_lot_id = lot_response.json()["id"]
        self.ticket = self._park("KA-01-AB-1234").json()

    def tearDown(self) -> None:
        self.client.close()
        self.temporary_directory.cleanup()

    def test_get_availability(self) -> None:
        response = self.client.get(
            f"/parking-lots/{self.parking_lot_id}"
            "/availability"
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                "parking_lot_id": self.parking_lot_id,
                "available": {
                    "small": 1,
                    "medium": 1,
                    "large": 1,
                },
                "total_available": 3,
            },
            response.json(),
        )

    def test_list_current_occupancy(self) -> None:
        response = self.client.get(
            f"/parking-lots/{self.parking_lot_id}"
            "/spaces?occupied=true"
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json()["spaces"]))

        occupied = response.json()["spaces"][0]
        self.assertEqual(1, occupied["space_number"])
        self.assertEqual("SMALL", occupied["space_size"])
        self.assertEqual(
            "KA-01-AB-1234",
            occupied["registration_number"],
        )
        self.assertEqual(
            self.ticket["id"],
            occupied["ticket_id"],
        )

    def test_get_ticket(self) -> None:
        response = self.client.get(
            f"/parking-lots/{self.parking_lot_id}"
            f"/tickets/{self.ticket['id']}"
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.ticket, response.json())

    def test_search_active_ticket_by_registration(self) -> None:
        response = self.client.get(
            f"/parking-lots/{self.parking_lot_id}/tickets",
            params={
                "registration_number": "ka-01-ab-1234",
                "state": "PARKED",
            },
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            [self.ticket],
            response.json()["tickets"],
        )

    def test_ticket_search_returns_empty_collection(self) -> None:
        response = self.client.get(
            f"/parking-lots/{self.parking_lot_id}/tickets",
            params={
                "registration_number": "KA-01-XX-9999",
                "state": "PARKED",
            },
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json()["tickets"])

    def test_ticket_history_includes_exited_ticket(self) -> None:
        self.client.post(
            f"/parking-lots/{self.parking_lot_id}"
            f"/tickets/{self.ticket['id']}/exit"
        )

        response = self.client.get(
            f"/parking-lots/{self.parking_lot_id}/tickets"
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json()["tickets"]))
        self.assertEqual(
            "EXITED",
            response.json()["tickets"][0]["state"],
        )

    def test_get_unknown_ticket_returns_not_found(self) -> None:
        response = self.client.get(
            f"/parking-lots/{self.parking_lot_id}"
            "/tickets/999"
        )

        self.assertEqual(404, response.status_code)
        self.assertEqual(
            "PARKING_TICKET_NOT_FOUND",
            response.json()["error"]["code"],
        )

    def test_occupied_false_is_rejected(self) -> None:
        response = self.client.get(
            f"/parking-lots/{self.parking_lot_id}"
            "/spaces?occupied=false"
        )

        self.assertEqual(422, response.status_code)

    def _park(self, registration_number: str):
        return self.client.post(
            f"/parking-lots/{self.parking_lot_id}/tickets",
            json={"registration_number": registration_number},
        )