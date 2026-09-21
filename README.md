# Parking Lot

A REST-based parking lot service designed as a focused low-level design exercise.

The service manages one configurable parking lot, allocates the nearest compatible parking space, issues tickets, calculates fixed hourly parking costs, processes exits, and provides availability and occupancy queries.

## Functional Scope

- Create one parking lot with configurable numbers of:
  - small spaces;
  - medium spaces;
  - large spaces.
- Treat the currently supported vehicle as small.
- Allocate spaces using this priority:
  1. nearest available small space;
  2. nearest available medium space;
  3. nearest available large space.
- Issue a ticket when a vehicle parks.
- Prevent the same registration number from parking twice simultaneously.
- Record parking and exit times.
- Charge a fixed hourly rate using integer rupee values.
- Round every started hour upwards, with a minimum charge of one hour.
- Release the parking space when the ticket exits.
- Query:
  - availability by space size;
  - current occupancy;
  - a ticket by ID;
  - tickets by registration number and state;
  - complete ticket history.

Colour-based searches and multiple vehicle types are deferred.

## Design

```text
HTTP request
    → FastAPI router
    → Application service
    → Repository
    → SQLite
```

### Responsibilities

- **API layer**: HTTP validation, response models and error mapping.
- **Application services**: parking, exit, configuration and query use cases.
- **Domain layer**: models, allocation policy, pricing policy and expected errors.
- **Repositories**: SQL execution and database-row mapping.
- **SQLite schema**: relational constraints and final consistency protection.

Dependencies are supplied explicitly. Repositories do not obtain a global database connection.

Each API request owns one SQLite connection. Repositories participating in the request share that connection, allowing parking and exit operations to use one transaction.

## Important Design Decisions

### Availability is derived

A parking space does not store an independent `available` flag.

A space is occupied when it has a ticket in the `PARKED` state. Changing the ticket to `EXITED` makes the space available again. This avoids contradictory occupancy and availability state.

### Allocation policy

Vehicle-to-space compatibility is represented through `SpaceAllocationPolicy`.

The current implementation supports small vehicles and returns this priority:

```text
SMALL → MEDIUM → LARGE
```

The parking service depends on the policy contract rather than hard-coding compatibility rules.

### Pricing policy

Parking cost is represented through `PricingPolicy`.

The current `FixedHourlyPricingPolicy` calculates:

```text
billable_hours = max(1, ceil(duration_seconds / 3600))
total_cost = billable_hours × hourly_rate
```

A different pricing policy can be supplied without changing exit orchestration.

### Ticket lifecycle

A ticket has two states:

```text
PARKED → EXITED
```

Parking and ticket creation form one transaction. Exit, cost calculation and ticket closure form another transaction.

The ticket snapshots the hourly rate at parking time so an existing session is not affected by later configuration changes.

### Database connection lifecycle

The application uses request-scoped SQLite connections rather than a singleton connection.

Tests use isolated in-memory databases or temporary file-backed databases.

## Requirements

- Python 3.11 or newer
- No separately running database server

SQLite support is provided by Python's standard library.

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Initialise the development database:

```bash
python -m parking_lot.database initialise
```

This creates:

```text
data/parking_lot.db
```

Generated database files are excluded from Git.

## Run

```bash
uvicorn parking_lot.app:app --reload
```

Open the generated API documentation:

```text
http://127.0.0.1:8000/docs
```

The root path intentionally has no endpoint.

## API Summary

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/parking-lots` | Create the parking lot and its spaces |
| `GET` | `/parking-lots` | List parking lots |
| `GET` | `/parking-lots/{lot_id}` | Retrieve the parking lot |
| `POST` | `/parking-lots/{lot_id}/tickets` | Park a vehicle and issue a ticket |
| `POST` | `/parking-lots/{lot_id}/tickets/{ticket_id}/exit` | Exit and calculate cost |
| `GET` | `/parking-lots/{lot_id}/tickets/{ticket_id}` | Retrieve a ticket |
| `GET` | `/parking-lots/{lot_id}/tickets` | Search ticket history |
| `GET` | `/parking-lots/{lot_id}/availability` | Get availability by size |
| `GET` | `/parking-lots/{lot_id}/spaces?occupied=true` | Get current occupancy |

## Example Flow

### Create the parking lot

```bash
curl -X POST http://127.0.0.1:8000/parking-lots \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Forum Parking",
    "small_space_count": 2,
    "medium_space_count": 1,
    "large_space_count": 1,
    "hourly_rate": 10
  }'
```

### Park a vehicle

```bash
curl -X POST http://127.0.0.1:8000/parking-lots/1/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "registration_number": "KA-01-AB-1234"
  }'
```

A successful response contains a `PARKED` ticket and the allocated space.

### Check availability

```bash
curl http://127.0.0.1:8000/parking-lots/1/availability
```

### Check occupancy

```bash
curl "http://127.0.0.1:8000/parking-lots/1/spaces?occupied=true"
```

### Find active parking by registration number

```bash
curl \
  "http://127.0.0.1:8000/parking-lots/1/tickets?registration_number=KA-01-AB-1234&state=PARKED"
```

### Exit

Replace `1` at the end with the issued ticket ID:

```bash
curl -X POST \
  http://127.0.0.1:8000/parking-lots/1/tickets/1/exit
```

The response contains the updated `EXITED` ticket, billed hours and total cost.

## Tests

Run the complete revised test suite:

```bash
python -m unittest discover \
  -s tests \
  -p "test_*.py" \
  -v
```

Tests cover:

- schema constraints and foreign-key enforcement;
- allocation priority;
- fixed-hour pricing boundaries;
- repository mapping;
- service validation and transactions;
- parking, exit and space reuse;
- REST contracts and error responses;
- availability, occupancy and ticket queries.

## Entities and Schemas

### Domain entities

#### ParkingLot

Represents the complete parking facility.

| Field | Type | Description |
| --- | --- | --- |
| `id` | `int` | Parking-lot identifier |
| `name` | `str` | Parking-lot name |
| `hourly_rate` | `int` | Fixed hourly rate in rupees |
| `small_space_count` | `int` | Number of small spaces |
| `medium_space_count` | `int` | Number of medium spaces |
| `large_space_count` | `int` | Number of large spaces |

#### ParkingSpace

Represents one physical parking space within a parking lot.

| Field | Type | Description |
| --- | --- | --- |
| `id` | `int` | Internal space identifier |
| `parking_lot_id` | `int` | Owning parking lot |
| `space_number` | `int` | Number representing proximity to the entrance |
| `size` | `ParkingSpaceSize` | `SMALL`, `MEDIUM`, or `LARGE` |

The business reference for a space is:

```text
parking_lot_id + space_number

#### ParkingTicket

Represents one vehicle-parking session and its lifecycle.

| Field | Type | Description |
| --- | --- | --- |
| `id` | `int` | Ticket identifier |
| `parking_lot_id` | `int` | Parking lot used |
| `parking_space_id` | `int` | Internal allocated-space identifier |
| `space_number` | `int` | Allocated space number |
| `space_size` | `ParkingSpaceSize` | Allocated space size |
| `registration_number` | `str` | Normalised vehicle registration number |
| `parked_at` | `datetime` | Parking start time |
| `exited_at` | `datetime \| None` | Exit time |
| `billed_hours` | `int \| None` | Final billed duration |
| `hourly_rate` | `int` | Rate captured when parking started |
| `total_cost` | `int \| None` | Final cost in rupees |
| `state` | `TicketState` | `PARKED` or `EXITED` |

#### Vehicle

Represents a uniquely registered vehicle.

| Field | Type | Description |
| --- | --- | --- |
| `id` | `int` | Internal vehicle identifier |
| `registration_number` | `str` | Unique normalised registration number |
| `size` | `VehicleSize` | Current value is `SMALL` |

## Relationship
ParkingLot
    └── ParkingSpace

Vehicle
    └── ParkingTicket
            ├── ParkingLot
            └── ParkingSpace

## Project Structure

```text
parking_lot/
├── api/
│   ├── dependencies.py
│   ├── errors.py
│   ├── parking_lots.py
│   ├── parking_spaces.py
│   ├── schemas.py
│   └── tickets.py
├── domain/
│   ├── allocation.py
│   ├── clock.py
│   ├── exceptions.py
│   ├── models.py
│   └── pricing.py
├── repositories/
│   ├── parking_lots.py
│   ├── parking_spaces.py
│   └── parking_tickets.py
├── services/
│   ├── exit.py
│   ├── parking.py
│   ├── parking_lots.py
│   └── queries.py
├── app.py
├── database.py
└── schema.sql
```

## Deferred Extensions

### Multiple vehicle types

The current API treats every vehicle as small. A later extension can add vehicle size/type to the parking request and supply the corresponding allocation policy.

### Multiple parking lots

The first version permits one parking lot. Data, repository queries and API paths already use `parking_lot_id`, keeping lot state isolated when support for additional lots is enabled.

### Dynamic pricing

A later pricing policy can consider space size, duration, time of day, occupancy or location without changing the ticket-exit workflow.
