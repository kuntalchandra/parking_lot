import sqlite3
from unittest import TestCase

from parking_lot.database import (
    connect_database,
    initialise_schema,
)


class DatabaseTest(TestCase):
    def setUp(self) -> None:
        self.connection = connect_database(":memory:")
        initialise_schema(self.connection)

    def tearDown(self) -> None:
        self.connection.close()

    def test_initialise_schema_creates_expected_tables(self) -> None:
        rows = self.connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name IN (
                  'parking_lot',
                  'parking_space',
                  'parking_ticket'
              )
            ORDER BY name
            """
        ).fetchall()

        self.assertEqual(
            [
                "parking_lot",
                "parking_space",
                "parking_ticket",
            ],
            [row["name"] for row in rows],
        )

    def test_foreign_keys_are_enabled(self) -> None:
        enabled = self.connection.execute(
            "PRAGMA foreign_keys"
        ).fetchone()[0]

        self.assertEqual(1, enabled)

    def test_registration_can_have_only_one_parked_ticket(
        self,
    ) -> None:
        lot_id = self._insert_parking_lot()
        first_space_id = self._insert_parking_space(
            lot_id,
            1,
            "SMALL",
        )
        second_space_id = self._insert_parking_space(
            lot_id,
            2,
            "SMALL",
        )
        self._insert_parked_ticket(
            lot_id,
            first_space_id,
            "KA-01-AB-1234",
        )

        with self.assertRaises(sqlite3.IntegrityError):
            self._insert_parked_ticket(
                lot_id,
                second_space_id,
                "KA-01-AB-1234",
            )

    def test_space_can_have_only_one_parked_ticket(self) -> None:
        lot_id = self._insert_parking_lot()
        space_id = self._insert_parking_space(
            lot_id,
            1,
            "SMALL",
        )
        self._insert_parked_ticket(
            lot_id,
            space_id,
            "KA-01-AB-1234",
        )

        with self.assertRaises(sqlite3.IntegrityError):
            self._insert_parked_ticket(
                lot_id,
                space_id,
                "KA-02-CD-5678",
            )

    def test_exited_ticket_requires_exit_values(self) -> None:
        lot_id = self._insert_parking_lot()
        space_id = self._insert_parking_space(
            lot_id,
            1,
            "SMALL",
        )

        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                """
                INSERT INTO parking_ticket (
                    parking_lot_id,
                    parking_space_id,
                    registration_number,
                    parked_at,
                    hourly_rate,
                    state
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    lot_id,
                    space_id,
                    "KA-01-AB-1234",
                    "2026-09-21T10:30:00Z",
                    10,
                    "EXITED",
                ),
            )

    def _insert_parking_lot(self) -> int:
        cursor = self.connection.execute(
            """
            INSERT INTO parking_lot (name, hourly_rate)
            VALUES (?, ?)
            """,
            ("Forum Parking", 10),
        )
        return int(cursor.lastrowid)

    def _insert_parking_space(
        self,
        lot_id: int,
        space_number: int,
        size: str,
    ) -> int:
        cursor = self.connection.execute(
            """
            INSERT INTO parking_space (
                parking_lot_id,
                space_number,
                size
            ) VALUES (?, ?, ?)
            """,
            (lot_id, space_number, size),
        )
        return int(cursor.lastrowid)

    def _insert_parked_ticket(
        self,
        lot_id: int,
        space_id: int,
        registration_number: str,
    ) -> int:
        cursor = self.connection.execute(
            """
            INSERT INTO parking_ticket (
                parking_lot_id,
                parking_space_id,
                registration_number,
                parked_at,
                hourly_rate,
                state
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                lot_id,
                space_id,
                registration_number,
                "2026-09-21T10:30:00Z",
                10,
                "PARKED",
            ),
        )
        return int(cursor.lastrowid)