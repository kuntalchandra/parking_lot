PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS parking_lot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    hourly_rate INTEGER NOT NULL CHECK (hourly_rate > 0)
);

CREATE TABLE IF NOT EXISTS parking_space (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parking_lot_id INTEGER NOT NULL,
    space_number INTEGER NOT NULL CHECK (space_number > 0),
    size TEXT NOT NULL CHECK (
        size IN ('SMALL', 'MEDIUM', 'LARGE')
    ),
    FOREIGN KEY (parking_lot_id) REFERENCES parking_lot(id),
    UNIQUE (parking_lot_id, space_number),
    UNIQUE (parking_lot_id, id)
);

CREATE TABLE IF NOT EXISTS parking_ticket (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parking_lot_id INTEGER NOT NULL,
    parking_space_id INTEGER NOT NULL,
    registration_number TEXT NOT NULL
        CHECK (length(trim(registration_number)) > 0),
    parked_at TEXT NOT NULL,
    exited_at TEXT,
    billed_hours INTEGER CHECK (billed_hours > 0),
    hourly_rate INTEGER NOT NULL CHECK (hourly_rate > 0),
    total_cost INTEGER CHECK (total_cost >= 0),
    state TEXT NOT NULL CHECK (
        state IN ('PARKED', 'EXITED')
    ),
    FOREIGN KEY (parking_lot_id, parking_space_id)
        REFERENCES parking_space(parking_lot_id, id),
    CHECK (
        (
            state = 'PARKED'
            AND exited_at IS NULL
            AND billed_hours IS NULL
            AND total_cost IS NULL
        )
        OR
        (
            state = 'EXITED'
            AND exited_at IS NOT NULL
            AND billed_hours IS NOT NULL
            AND total_cost IS NOT NULL
        )
    )
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_parked_registration
    ON parking_ticket(registration_number)
    WHERE state = 'PARKED';

CREATE UNIQUE INDEX IF NOT EXISTS uq_occupied_space
    ON parking_ticket(parking_lot_id, parking_space_id)
    WHERE state = 'PARKED';

CREATE INDEX IF NOT EXISTS ix_ticket_lot_state
    ON parking_ticket(parking_lot_id, state);