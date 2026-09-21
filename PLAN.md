# Parking Lot LLD Revision Plan

## 1. Purpose

Revise the stale Parking Lot project to refresh low-level design (LLD) concepts through a practical, step-by-step implementation.

The work will focus on:

- clarifying functional requirements before designing;
- defining simple API and method contracts;
- identifying responsibilities and boundaries;
- applying relevant object-oriented design principles;
- isolating persistence and tests;
- discussing design choices, alternatives, and trade-offs;
- reviewing each small change before moving forward.

The goal is learning and context refresh—not building an over-engineered parking platform.

## 2. Scope

This revision covers points 0, 1, and 2 from the README's **Further, plan of actions**:

0. Clean up and refactor the design affected by the earlier database integration.
1. Isolate the test database with automatic setup and teardown.
2. Separate parking, exit, availability, and query responsibilities.

Point 3—supporting different vehicle types—is deferred to a later extension. The current design must nevertheless remain open to this extension in line with the Open/Closed Principle. We will create only the extension boundary justified now; we will not implement unused vehicle types or speculative abstractions.

Points 4–7 are outside the current scope, except that the confirmed fixed hourly pricing requirement should leave a clear path for a later pricing-policy extension.

## 3. Confirmed Functional Understanding

### 3.1 Parking lot and parking spaces

- A `ParkingLot` represents the complete parking facility.
- A parking lot contains multiple `ParkingSpace`s.
- Parking spaces have three sizes: `SMALL`, `MEDIUM`, and `LARGE`.
- The count of each parking-space size is configured when a parking lot is created; counts are not hard-coded.
- The initial version treats every vehicle as small.
- Allocation priority is:
  1. nearest available small space;
  2. nearest available medium space when no small space is available;
  3. nearest available large space when neither small nor medium space is available.
- Within an eligible size, the lowest space number represents the nearest available space.

### 3.2 Vehicle identification

- Registration number uniquely identifies a vehicle.
- Colour is deferred and removed from the current functional requirements, API contracts, queries, and tests.
- The same registration number cannot hold more than one active parking ticket.

### 3.3 Parking and ticketing

- A successful parking operation allocates a suitable parking space and issues a ticket.
- The ticket records at least:
  - a unique ticket identifier;
  - vehicle registration number;
  - allocated parking space;
  - parking start time;
  - exit time once the vehicle leaves;
  - calculated parking cost once the vehicle leaves.
- Issuing the ticket and occupying the parking space form one successful operation; partial state must not remain if either step fails.

### 3.4 Exit and pricing

- The ticket is used to process a vehicle's exit.
- A successful exit records the exit time and releases the parking space.
- Parking cost is fixed and hourly based in the initial version.
- The charging rule, including partial-hour rounding, will be confirmed before implementation.
- Fixed hourly pricing should be replaceable by a different pricing policy later without changing parking or exit orchestration.
- Updating the ticket and releasing the parking space form one successful operation.

### 3.5 Availability and search

- The system reports parking-space availability by size.
- The system reports current occupancy.
- The system finds the active parking details and allocated space using a registration number.
- The system finds a ticket using its ticket identifier.

### 3.6 Interface and persistence

- The stale CLI will be replaced by REST APIs.
- FastAPI will provide the HTTP layer and OpenAPI documentation.
- File-backed SQLite will store development data in GitHub Codespaces.
- A fresh in-memory SQLite database will isolate each test.
- Python's standard `sqlite3` module will be used initially; no ORM is required.
- Tests will primarily use `unittest.TestCase` style.

## 4. Design Principles

- Keep each phase as small as possible while still forming a coherent design step.
- Apply SRP through meaningful responsibility boundaries, not one class per method.
- Apply OCP only at known variation points: vehicle/space compatibility and pricing policy.
- Keep HTTP validation and response formatting outside business logic.
- Keep SQL and database connection handling outside business logic.
- Supply dependencies explicitly so tests can use an isolated database.
- Keep each business operation transactional where multiple state changes must remain consistent.
- Prefer standard terminology: parking lot, parking space, vehicle, ticket, pricing policy, repository, service, request, and response.
- Avoid duplicate models, wrappers, services, or documentation unless they provide a clear boundary.
- Do not introduce a design pattern unless the current requirement or confirmed extension point justifies it.
- Put the API contract directly above the corresponding method signature when implementation begins, so the public contract and code remain easy to review together.

## 5. Working Agreement

For each phase:

1. I will explain the requirement and relevant LLD concepts first.
2. I will propose the smallest design needed for that phase.
3. I will show API contracts, method signatures, and on-the-fly design artefacts needed for review.
4. You will review and confirm or request corrections.
5. Only after confirmation will I provide ready-to-copy commands or patches for GitHub Codespaces.
6. We will run focused tests and then the full test suite.
7. We will discuss responsibilities, correctness, failure cases, and extension points.
8. We will update the progress tracker and decision log.
9. We will not start the next phase without your confirmation.

Entities, class diagrams, method signatures, API request/response bodies, and implementation details will be produced during the relevant phase rather than predicted in this plan.

## 6. Phases

### Phase 1 — Requirements and API contracts

Purpose: translate the confirmed problem into precise, reviewable contracts before writing code.

Work:

- finalise the use cases and terminology;
- resolve the remaining questions in Section 7;
- define success and failure behaviour;
- define REST endpoints using standard HTTP semantics;
- place each API contract above its proposed handler/method signature;
- define only the request and response fields needed now;
- identify business invariants;
- walk through parking, exit, availability, occupancy, and lookup flows;
- identify the minimum responsibility boundaries required for Phase 2.

Discussion focus:

- requirement clarification;
- API versus method contracts;
- entities, value objects, services, and repositories at a conceptual level;
- invariants and state transitions;
- OCP extension points for vehicle types and pricing without implementing them;
- avoiding premature abstraction.

Deliverable: a reviewed Phase 1 design proposal. No implementation is committed until it is approved.

### Phase 2 — Project baseline and isolated SQLite foundation

Purpose: create a clean, testable foundation without implementing full parking behaviour.

Work:

- modernise the Python project and dependencies;
- establish the minimum package structure approved in Phase 1;
- replace MySQL setup with SQLite connection management;
- add version-controlled schema initialisation;
- configure a file-backed database for Codespaces;
- create a fresh in-memory database fixture for each test;
- remove the global database singleton from active code paths;
- add copy-paste setup, run, and test commands;
- establish a green test baseline.

Discussion focus:

- dependency injection;
- connection lifetime;
- repository boundaries;
- test isolation;
- schema constraints as a final correctness guard.

Deliverable: an isolated SQLite foundation with passing setup tests.

### Phase 3 — Parking-space configuration and allocation

Purpose: implement configurable parking spaces and the size-aware allocation rule.

Work:

- create a parking lot with configurable small, medium, and large space counts;
- keep parking-space numbering and proximity rules deterministic;
- model the current vehicle as small while preserving the approved compatibility extension point;
- implement small-to-medium-to-large allocation priority;
- reject parking when no compatible space is available;
- prevent duplicate active parking for a registration number;
- test configuration, allocation order, full-lot behaviour, and failure cases.

Discussion focus:

- ownership of allocation logic;
- SRP and cohesion;
- OCP without speculative subclasses;
- deterministic behaviour;
- correctness under competing requests at the level appropriate for SQLite.

Deliverable: reviewed parking-space configuration and allocation behaviour.

### Phase 4 — Ticket issuance and parking transaction

Purpose: issue a ticket as part of one consistent parking operation.

Work:

- issue a unique ticket after selecting a parking space;
- record registration number, allocated space, and start time;
- persist ticket creation and space occupancy atomically;
- return the ticket through the approved REST contract;
- test successful issuance, duplicate registration, full lot, and rollback behaviour.

Discussion focus:

- entity lifecycle and identity;
- transaction ownership;
- database constraints versus service validation;
- separating HTTP models from business and persistence concerns.

Deliverable: a tested park-and-issue-ticket flow.

### Phase 5 — Exit and fixed hourly pricing

Purpose: complete the parking lifecycle with ticket-based exit and cost calculation.

Work:

- retrieve the active ticket;
- calculate cost using the confirmed fixed hourly rule;
- record exit time and final cost;
- release the parking space in the same transaction;
- define repeated-exit and unknown-ticket behaviour;
- keep pricing behind the approved replaceable policy boundary;
- test duration boundaries, rounding, invalid tickets, repeated exit, rollback, and space reuse.

Discussion focus:

- state transitions;
- idempotency;
- time as an injected dependency for deterministic tests;
- Strategy as a justified pricing extension point;
- transaction consistency.

Deliverable: a tested ticket-exit-cost-space-reuse flow.

### Phase 6 — Availability, occupancy, and lookups

Purpose: add the required read operations without mixing them into parking and exit flows.

Work:

- report available parking-space counts by size;
- report current occupancy;
- find active parking details by registration number;
- find ticket details by ticket identifier;
- guarantee deterministic response ordering;
- add only indexes justified by these access patterns;
- test empty and populated results.

Discussion focus:

- command and query responsibilities;
- read-model shape;
- returning data instead of mutable internal objects;
- indexing from actual queries rather than assumption.

Deliverable: tested availability, occupancy, and lookup APIs.

### Phase 7 — Cleanup, documentation, and final design discussion

Purpose: remove stale paths and consolidate the learning from the completed design.

Work:

- remove superseded CLI, MySQL, singleton, cleanup scripts, and obsolete tests;
- update README context, setup, run, test, and API examples;
- document the final package structure and important decisions;
- run the complete workflow from a clean Codespace setup;
- review how vehicle types and dynamic pricing can be added later;
- conduct a final LLD discussion covering requirements, contracts, responsibilities, flows, errors, persistence, testing, and trade-offs.

Discussion focus:

- explaining why each boundary exists;
- identifying limitations honestly;
- distinguishing current requirements from future extensibility;
- evaluating whether each abstraction earned its place.

Deliverable: a clean, documented project and final design walkthrough.

## 7. Questions to Resolve in Phase 1

1. Is the fixed hourly rate configured per parking lot or globally?
2. How should partial hours be charged: rounded up, rounded down, or prorated?
3. Which currency should the API return?
4. Are parking-space numbers unique within one parking lot only? The recommended answer is yes.
5. Should one running application manage multiple parking lots? The requirements currently allow creating a parking lot with its own size configuration, so the recommended answer is yes.
6. Should parking-lot deletion and resizing be excluded from the first version? The recommended answer is yes.
7. Should an exit return the updated ticket as the receipt? The recommended answer is yes.
8. Should registration numbers be normalised for uniqueness and lookup, for example by trimming spaces and using uppercase? The recommended answer is yes.

## 8. Codespaces and SQLite Direction

The intended workflow remains:

- file-backed SQLite for normal application execution;
- one in-memory SQLite database connection per test;
- schema stored in source control;
- generated database files excluded from Git;
- no separately running database server;
- copy-paste commands supplied only when the relevant phase is approved.

One important constraint will be retained: an in-memory SQLite database belongs to its connection. Repositories participating in one test must therefore share the injected test connection.

## 9. Decision Log

| Decision | Status | Reason |
| --- | --- | --- |
| Cover README points 0–2 | Confirmed | Current revision scope |
| Defer vehicle types but keep an OCP extension boundary | Confirmed | Point 3 is planned later |
| Remove colour from current requirements | Confirmed | Registration number is the required vehicle identifier |
| Registration number is unique for active parking | Confirmed | Prevent duplicate simultaneous occupancy |
| Parking lot contains configurable parking spaces | Confirmed | Clarifies facility versus individual space |
| Support small, medium, and large parking spaces | Confirmed | Required capacity model |
| Treat current vehicles as small | Confirmed | Initial vehicle-size assumption |
| Allocate small, then medium, then large | Confirmed | Required allocation priority |
| Issue a ticket on successful parking | Confirmed | Required parking contract |
| Record start and exit times on the ticket | Confirmed | Required lifecycle and pricing inputs |
| Use fixed hourly pricing initially | Confirmed | Current pricing requirement |
| Keep pricing replaceable for later dynamic pricing | Confirmed | Known future variation point |
| Replace CLI with REST APIs | Confirmed | Selected external interface |
| Use FastAPI | Confirmed | Simple validation and OpenAPI support |
| Use file-backed SQLite at runtime | Confirmed | No database server required in Codespaces |
| Use in-memory SQLite per test | Confirmed | Isolated and disposable tests |
| Use `sqlite3` without an ORM initially | Confirmed | Keep persistence and transactions visible |
| Hourly rate, rounding, and currency | Pending | Resolve in Phase 1 |
| Multiple lots per running application | Pending | Confirm in Phase 1 |
| Registration-number normalisation | Pending | Confirm in Phase 1 |

## 10. Progress Tracker

| Phase | Status | Notes |
| --- | --- | --- |
| Plan revision | In review | Awaiting confirmation and commit |
| Phase 1 — Requirements and API contracts | Completed | Revised plan is committed |
| Phase 2 — Project baseline and isolated SQLite foundation | Completed | SQLite schema, connection management and isolated tests committed |
| Phase 3 — Parking-space configuration and allocation | Completed | Configurable spaces, allocation and parking-lot APIs completed |
| Phase 4 — Ticket issuance and parking transaction | Completed | Transactional parking and ticket issuance completed |
| Phase 5 — Exit and fixed hourly pricing | Completed | Ticket exit, hourly cost and space release completed |
| Phase 6 — Availability, occupancy, and lookups | Completed | Availability, occupancy and ticket queries completed |
| Phase 7 — Cleanup, documentation, and final design discussion | Not started |  |

## 11. Definition of Done

The current revision is complete when:

- confirmed use cases are available through reviewed REST APIs;
- parking-space counts are configurable by size;
- allocation follows small, then medium, then large priority;
- successful parking issues a ticket with a start time;
- exit records the exit time, calculates fixed hourly cost, and releases the space;
- registration-number, ticket, availability, and occupancy lookups work as agreed;
- parking and exit state changes are transactional;
- responsibilities are separated without unnecessary classes or patterns;
- the design remains open to vehicle-type and pricing-policy extensions;
- every test uses an isolated in-memory SQLite database;
- no MySQL server or local database installation is required;
- all tests pass from a clean Codespace setup;
- stale CLI and MySQL paths are removed;
- README and the final design discussion accurately describe the completed system.

