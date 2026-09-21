from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


DEFAULT_DATABASE_PATH = Path("data/parking_lot.db")
SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def connect_database(database_path: str | Path) -> sqlite3.Connection:
    """Open a configured SQLite connection.

    The caller owns the connection and must close it. Passing ``:memory:``
    creates an isolated database suitable for one test.
    """
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialise_schema(connection: sqlite3.Connection) -> None:
    """Create the current schema on the supplied connection."""
    connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def initialise_database(
    database_path: Path = DEFAULT_DATABASE_PATH,
) -> None:
    """Create a file-backed development database and apply the schema."""
    database_path.parent.mkdir(parents=True, exist_ok=True)

    with connect_database(database_path) as connection:
        initialise_schema(connection)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parking lot database tools"
    )
    parser.add_argument("command", choices=["initialise"])
    parser.add_argument(
        "--database",
        type=Path,
        default=DEFAULT_DATABASE_PATH,
        help="SQLite database path",
    )
    args = parser.parse_args()

    if args.command == "initialise":
        initialise_database(args.database)
        print(f"Initialised SQLite database at {args.database}")


if __name__ == "__main__":
    main()