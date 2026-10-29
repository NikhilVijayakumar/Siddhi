# Implementation Tasks: Goal and local database baseline

- **OpenSpec Change ID:** `be-01-goal-and-persistence`
- **Status:** Not Started
- **Related artifacts:** `proposal.md`, `specs/`, `design.md`, `api-contract.md`, `adr.md`

## Planning rules applied here

Each slice is one observable behavior with its failing test written first
(`knowledge/practices/vertical-slices.md`, `test-driven-development`). No slice may
change behavior another slice already delivered without updating its test. Storage
refactors stay inside the slice that needs them. Structural document checks are
reported separately from executed tests.

## Prerequisite: dependencies and package layout

Enabling work only, no product behavior.

- [ ] 1.1 Add `fastapi`, `uvicorn`, `pydantic` to `[project].dependencies`; keep `pytest`
      in `dev`. Record the version constraints added.
- [ ] 1.2 Create the package layout from `design.md` §3: `api/`, `application/`,
      `domain/`, `adapters/sqlite/`, `adapters/sqlite/migrations/`, `bootstrap/`,
      `observability/`.
- [ ] 1.3 Add a test fixture that creates and removes a temporary SQLite file per test.
- [ ] 1.4 Confirm `python -m pytest` runs and reports zero tests without error.

Traceability: `design.md` §3; `proposal.md` constraints (NFR-033 controlled dependencies).

## Slice 1: schema version and controlled migration

Covers: *Report and evolve the database schema version*, *Fail closed when a migration fails*.

- [ ] 2.1 Failing tests: fresh database is created at version 1; a database recorded at
      a newer version is refused with both versions named; a migration that raises leaves
      the prior version and its rows readable.
- [ ] 2.2 Add migration `001_initial_schema.sql` matching `api-contract.md` §5 exactly.
- [ ] 2.3 Implement the migration runner: ordered files, one transaction each, recorded
      in `schema_version`, no down migrations.
- [ ] 2.4 Take a pre-migration copy of the database file before applying any migration;
      on failure keep the copy and report the reached version.
- [ ] 2.5 Tests pass, including the two failure scenarios.

Traceability: `fun-01`/`tech-02` specs; `api-contract.md` §6;
`knowledge/architecture/persistence.md`.

## Slice 2: create a goal

Covers: *Capture a goal before any project exists*, *Absent information stays explicitly
unknown*, and the create side of *Reject invalid changes atomically*.

- [ ] 3.1 Failing tests: minimal create returns `201` with `revision: 0` and every
      unrecorded field listed in `unknown_fields`; a publication-outcome goal requires no
      stage or time field; blank title and an unknown outcome type are rejected with no
      row created; an unknown request field is rejected.
- [ ] 3.2 Implement domain validation (title length after trim, outcome type set,
      priority set) and the goal entity.
- [ ] 3.3 Implement `POST /goals` with one transaction inserting the goal row and its
      initial revision (`changed_fields` = all supplied fields).
- [ ] 3.4 Tests pass.

Traceability: FR-001, FR-002, FR-005, FR-044; `data-model.md`, `portfolio-domain.md`.

## Slice 3: retrieve and list goals

Covers: *Retrieve and list goals*.

- [ ] 4.1 Failing tests: retrieval by id; unknown id is `404`; listing is bounded and
      active-only by default; following `next_cursor` yields the remaining goals with no
      duplicates or gaps; `status=archived` and `status=all` filter correctly; an
      invalid cursor is a validation error.
- [ ] 4.2 Implement keyset pagination on `(created_at DESC, id ASC)` and the opaque
      cursor codec.
- [ ] 4.3 Tests pass, including the page-boundary case.

Traceability: FR-043; `api-contract.md` §3.2–3.3.

## Slice 4: revise a goal with history

Covers: *Revise a goal and retain its history* and the update side of *Reject invalid
changes atomically*.

- [ ] 5.1 Failing tests: a PATCH stores the new value and appends a revision containing
      the prior value, changed field, time and reason; `revision` increments once;
      setting a field to `null` records a change back to unknown; a stale
      `expected_revision` returns `409` with the current revision and changes nothing;
      a server-owned field (`id`, `status`, `revision`, timestamps) is rejected; a
      rejected update creates no revision.
- [ ] 5.2 Implement `PATCH /goals/{goal_id}` with the revision insert inside the same
      transaction as the row update.
- [ ] 5.3 Implement `GET /goals/{goal_id}/revisions` with the same cursor mechanics.
- [ ] 5.4 Tests pass, including the conflict case.

Traceability: FR-006, NFR-007, NFR-014, NFR-016; `data-model.md`, `persistence.md`.

## Slice 5: archive without deleting

Covers: *Archive a goal without deleting it*.

- [ ] 6.1 Failing tests: archiving sets status and `archived_at`, appends one revision,
      and removes the goal from the default listing; the goal and its revisions remain
      retrievable; a second archive returns `200` and creates no revision; no row is
      deleted.
- [ ] 6.2 Implement `POST /goals/{goal_id}/archive` idempotently.
- [ ] 6.3 Tests pass.

Traceability: FR-001; `data-model.md`.

## Slice 6: local operation and diagnostics

Covers: *Serve only on the local interface with safe diagnostics*, *Configure local
operation without editing source*.

- [ ] 7.1 Failing tests: startup binds `127.0.0.1` only; a non-loopback value without an
      override fails before any socket opens; `/health` separates service, database and
      integrations; a database failure yields `503` with database `unavailable`; no error
      or health payload contains the database path or a credential-shaped value;
      configuration is read from environment and a machine-local file.
- [ ] 7.2 Implement configuration loading and validation with messages naming the
      setting only.
- [ ] 7.3 Implement `/health` composition and structured logging with correlation ids.
- [ ] 7.4 Tests pass.

Traceability: FR-046, FR-049, FR-050, NFR-022, NFR-026; `security-and-privacy.md`,
`configuration-and-secrets.md`, `observability.md`.

## Slice 7: end-to-end verification and reporting

- [ ] 8.1 End-to-end test over HTTP against a temporary database: create → retrieve →
      revise → list revisions → archive → confirm listing and history.
- [ ] 8.2 Failure-case sweep: invalid input, stale revision, unknown id, unavailable
      database, interrupted migration — each asserted to leave state unchanged or
      reported, not silently corrected.
- [ ] 8.3 Run `openspec validate be-01-goal-and-persistence` and
      `openspec show be-01-goal-and-persistence --json --deltas-only`.
- [ ] 8.4 Fill the verification record below with actual outcomes; report structural
      checks separately from executed tests, and leave unavailable checks marked as such.

Traceability: `knowledge/practices/testing-and-validation.md`;
`engineering-quality` grill Q1, Q3.

## Verification evidence

| Check | Command / artifact | Result | Notes |
|---|---|---|---|
| Goal specification scenarios | executed pytest suite | Not run | |
| Migration and rollback checks | executed pytest suite | Not run | |
| Loopback and diagnostics checks | executed pytest suite | Not run | |
| `openspec validate` | `openspec validate be-01-goal-and-persistence` | Not run | Structural |
| Deltas | `openspec show be-01-goal-and-persistence --json --deltas-only` | Not run | Structural |

## Out of scope (deliberately not started)

Source adapters, project association, analysis and findings, planning and reviews,
external analysis handoff, local authentication, remote binding, write-back to any
source, backups and retention policy. Each needs its own change and, for the last three,
an owner decision listed in `adr.md` §3.
