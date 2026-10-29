# Design: Goal and local database baseline

## 1. Overview

### Purpose

Deliver the first observable product behavior — an owner can create, read, revise and
archive a goal that depends on no discovered project — on a database that knows its own
schema version and evolves only through controlled migrations.

### Scope

An HTTP service, one application service for goals, a SQLite repository, a migration
runner, startup configuration and health reporting. No source adapters, analysis,
planning, association or external analysis.

### Design principles

- One authority per fact: portfolio records belong to Siddhi, source facts to their
  source (`knowledge/architecture/data-ownership.md`).
- History is append-only; the current row is a projection of the latest revision.
- Absent data stays absent. No default dates, zero priorities or empty criteria.
- The HTTP boundary is the only client contract; no domain rule is duplicated in a
  client (`knowledge/decisions/ui-independent-http-boundary.md`).
- One transaction per write; a failed write leaves no trace.
- Fail closed on storage uncertainty rather than serving a guess.

## 2. Context and constraints

### Current state

`src/siddhi/__init__.py` is empty; `pyproject.toml` declares no runtime dependency and
already reserves package data paths `data/*.json` and
`adapters/sqlite/migrations/*.sql`, which this design uses. No application code, test
suite or database exists yet. Nothing here changes an existing behavior.

### Constraints

- Technical: Python 3.12, FastAPI + Pydantic (declared stack), stdlib `sqlite3`, pytest.
  Adding `fastapi`, `uvicorn` and `pydantic` to `[project].dependencies` is the only
  dependency change.
- Security and privacy: loopback binding only; no credentials; no request bodies in
  logs; errors name settings and allowed values, never submitted values.
- Performance and reliability: local single-user reads must not require a network
  round trip; writes are short single-statement-plus-revision transactions with a busy
  timeout. No numeric latency target is binding until the reference workload is agreed.
- Compatibility and migration: schema version 1 is a baseline with no prior data; no
  down migrations; forward-only, ordered, transactional.
- Operational: startup needs no manual step; an interrupted migration is reported and
  not silently retried.

### Existing decisions and conventions

`knowledge/decisions/local-first-sqlite.md`, `python-fastapi-backend.md`,
`modular-monolith.md`, `ui-independent-http-boundary.md`; architecture in
`knowledge/architecture/persistence.md`, `data-model.md`, `api-boundary.md`,
`configuration-and-secrets.md`, `security-and-privacy.md`.

## 3. Components

| Component | Responsibility | Depends on |
|---|---|---|
| `api/http` | Routing, request/response models, error mapping, correlation id | application |
| `application/goals` | Goal operations, validation of state transitions, revision creation | domain, repository port |
| `domain/goal` | Goal fields, outcome types, priority scale, status, revision rules | standard library |
| `adapters/sqlite` | Repository implementation, transactions, connection settings | stdlib `sqlite3` |
| `adapters/sqlite/migrations` | Ordered `NNN_*.sql` files | migration runner |
| `bootstrap` | Configuration loading/validation, migration run, app assembly | all of the above |
| `observability` | Structured logs, `/health` composition | bootstrap, repository |

Dependency direction is inward only: `api` → `application` → `domain`; adapters implement
ports declared by the application layer. The HTTP layer holds no SQL and the domain
holds no HTTP or SQLite types.

## 4. Data flow

### Write (`POST /goals`, `PATCH`, archive)

1. HTTP layer parses the body; unknown fields and server-owned fields are rejected.
2. Application layer validates the resulting goal state and computes the changed field
   set against the current revision.
3. One transaction: update the `goals` row and insert the `goal_revisions` row
   (`changed_fields`, `prior_state`, actor `owner`, optional reason).
4. Commit; map the stored row to the response goal, deriving `unknown_fields`.

A validation failure happens before the transaction opens. A conflict
(`expected_revision` mismatch) is detected inside the transaction by comparing the
current `revision`, and rolls back.

### Read (`GET /goals`, `GET /goals/{id}`, revisions)

Single read transaction per request; no writes, no source access. Listing uses keyset
pagination on `(created_at DESC, id ASC)`; the cursor encodes the last row's key, so
pages are stable under concurrent inserts.

### Startup

1. Load configuration from environment and a machine-local settings file; validate each
   value; fail with a message naming the setting.
2. Open the database, read `schema_version`, compare with the application's maximum.
3. If older, take a pre-migration copy of the file, apply pending migrations in order,
   each in its own transaction; on error, stop, keep the prior file usable, report.
4. If newer, fail closed.
5. Assemble the app and bind to the configured loopback address.

## 5. Key design choices

| Choice | Alternative rejected | Reason |
|---|---|---|
| Append-only revisions beside the current row | Mutable row with an audit log added later | History must exist from the first write; retrofitting it loses the first state |
| `null` + derived `unknown_fields` | Default values or a separate unknown boolean per field | One representation cannot disagree with itself |
| Keyset pagination with opaque cursors | Offset pagination | Offsets skip or repeat rows when new goals arrive |
| Optimistic concurrency via `expected_revision` | Last-write-wins | Two clients editing a goal must not silently discard a revision |
| Server-generated UUIDs | Client-chosen identifiers | Prevents collisions and client-owned identity |
| One transaction per write | Eventual consistency or a job queue | No cross-record work exists in this slice; a queue would be unearned |
| `schema_version` table + SQL files | ORM-managed schema | Auditable, ordered, testable upgrade path (`persistence.md`) |

## 6. Error handling

| Failure | Behavior |
|---|---|
| Invalid body | `422 validation`, field-level message, no state change |
| Unknown goal | `404 not_found` |
| Stale `expected_revision` | `409 conflict` with `current_revision`, no state change |
| Database locked beyond timeout | `503 unavailable`, correlation id, no partial write |
| Migration failure at startup | Process exits non-zero; prior schema and file intact |
| Unexpected exception | `500 internal`, correlation id only |

Correlation identifiers are generated per request, returned in the header and error
body, and written to structured logs alongside subsystem, outcome and duration only.

## 7. Security and privacy

- Bind `127.0.0.1` only; a non-loopback bind requires an explicit configuration override
  that this slice does not provide.
- No request body, goal content or file path is logged.
- The database path is configuration, never a response field.
- No credential storage, no source content, no outbound network call.
- Local client authentication remains an open owner decision; until it is made, this
  slice must not be exposed beyond loopback.

## 8. Testing and evidence

| Layer | Owns | Examples |
|---|---|---|
| Unit | Domain rules: field validation, status transitions, unknown derivation | Blank title, invalid outcome type, archive twice |
| Contract | Response shapes and error categories against `api-contract.md` | Goal payload fields, 409 body, cursor round-trip |
| Integration | HTTP + real temporary SQLite file | Create → revise → list → archive end to end |
| Persistence | Constraints, transaction rollback, migrations | Rejected write leaves no row; failed migration leaves v1 readable; newer-version refusal |
| Operational | Startup configuration and binding | Loopback only; invalid value fails before binding |

Failure cases each slice must exercise: invalid input, stale revision, unknown id,
database unavailable, interrupted migration. Tests run offline against a temporary
database; no network or external account is required. Document checks
(`scripts/verify_*.py`, `openspec validate`) are reported separately from executed test
results.

## 9. Risks

- SQLite write contention becomes real only when ingestion arrives; the first slice
  keeps transactions short and a busy timeout, and names the risk instead of building a
  queue now.
- Draft requirements could be read as approved behavior; every artifact keeps the draft
  label and the proposal states that adoption here is not approval.
- `unknown_fields` is derived per response; if a future field needs a tri-state
  (unknown / explicitly cleared / never offered), that requires a change, not a silent
  reinterpretation.

## 10. Knowledge References

- `knowledge/architecture/data-model.md`
- `knowledge/architecture/persistence.md`
- `knowledge/architecture/data-ownership.md`
- `knowledge/architecture/api-boundary.md`
- `knowledge/architecture/configuration-and-secrets.md`
- `knowledge/architecture/security-and-privacy.md`
- `knowledge/architecture/observability.md`
- `knowledge/practices/vertical-slices.md`
- `knowledge/practices/testing-and-validation.md`

## 11. Open decisions

These are owner decisions from the requirement grill, not gaps this design may fill:

- Local client authentication and origin policy (`docs/requirements/security/grill-log.md` Q5).
- Pre-1.0 compatibility policy and benchmark targets (`docs/requirements/api-operations/grill-log.md` Q8).
- Reference workstation and workload before any latency or capacity figure is binding
  (`docs/requirements/engineering-quality/grill-log.md` Q2).
- Recovery and retention targets — not required by this slice, but they govern the first
  backup schedule (`docs/requirements/persistence-recovery/grill-log.md` Q2, Q4).
