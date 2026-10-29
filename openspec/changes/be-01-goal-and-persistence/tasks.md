# Implementation Tasks: Goal and local database baseline

- **OpenSpec Change ID:** `be-01-goal-and-persistence`
- **Status:** In Progress (prerequisite complete)
- **Related artifacts:** `proposal.md`, `specs/`, `design.md`, `api-contract.md`, `adr.md`

## Planning rules applied here

Each slice is one observable behavior with its failing test written first
(`knowledge/practices/vertical-slices.md`, `test-driven-development`). No slice may
change behavior another slice already delivered without updating its test. Storage
refactors stay inside the slice that needs them. Structural document checks are
reported separately from executed tests.

## Prerequisite: dependencies and package layout

Enabling work only, no product behavior.

- [x] 1.1 Add `fastapi`, `uvicorn`, `pydantic` to `[project].dependencies`; keep `pytest`
      in `dev`. Record the version constraints added.
      Constraints: `fastapi>=0.121,<1`, `pydantic>=2.13,<3`, `uvicorn>=0.52,<1`.
- [x] 1.2 Create the package layout from `design.md` §3: `api/`, `application/`,
      `domain/`, `adapters/sqlite/`, `adapters/sqlite/migrations/`, `bootstrap/`,
      `observability/`.
- [x] 1.3 Add a test fixture that creates and removes a temporary SQLite file per test.
      `tests/conftest.py::db_path` returns a path under `tmp_path`; the file is not
      created, so the fresh-database migration case can start from nothing.
- [x] 1.4 Confirm `python -m pytest` runs and reports zero tests without error.
      Collected 0 items, no collection errors; exit code 5 is pytest's "no tests ran".

Traceability: `design.md` §3; `proposal.md` constraints (NFR-033 controlled dependencies).

## Slice 1: schema version and controlled migration

Covers: *Report and evolve the database schema version*, *Fail closed when a migration fails*.

- [x] 2.1 Failing tests: fresh database is created at version 1; a database recorded at
      a newer version is refused with both versions named; a migration that raises leaves
      the prior version and its rows readable.
      `tests/adapters/sqlite/test_migrations.py` (7 tests: baseline, no backup on
      creation, newer-version refusal, failed migration, duplicate versions, backup on
      upgrade, connection pragmas). Written and confirmed failing first (ImportError).
- [x] 2.2 Add migration `001_initial_schema.sql` matching `api-contract.md` §5.
      Contract amended first: `schema_version.version` is now `INTEGER PRIMARY KEY`
      (grill decision) so a double-applied migration fails instead of hiding. The
      runner writes the ledger row; the SQL file is pure DDL.
- [x] 2.3 Implement the migration runner: ordered files, one transaction each, recorded
      in `schema_version`, no down migrations.
      `src/siddhi/adapters/sqlite/runner.py`. Named `runner.py` because a
      `migrations.py` module would be shadowed by the `migrations/` SQL directory.
      Each script is split with `sqlite3.complete_statement`, applied under
      `BEGIN IMMEDIATE`, and committed with its ledger row.
- [x] 2.4 Take a pre-migration copy of the database file before applying any migration;
      on failure keep the copy and report the reached version.
      `<db>.v<version>.<UTC stamp>.bak`, skipped when there is nothing to lose
      (version 0). The copy is never restored automatically; the migration's own
      rollback leaves the prior version readable. A WAL store is refused rather than
      copied unsafely.
- [x] 2.5 Tests pass, including the two failure scenarios.
      `python -m pytest` → 7 passed. Non-zero process exit was not observable at this
      point: no process entrypoint existed until slice 6, which is where the typed errors
      map to exit status (closed in 7.4: `python -m siddhi` exits `1` on
      `ConfigError`/`MigrationFailed`/`SchemaTooNew`).

Traceability: `fun-01`/`tech-02` specs; `api-contract.md` §6;
`knowledge/architecture/persistence.md`.

## Slice 2: create a goal

Covers: *Capture a goal before any project exists*, *Absent information stays explicitly
unknown*, and the create side of *Reject invalid changes atomically*.

- [x] 3.1 Failing tests: minimal create returns `201` with `revision: 0` and every
      unrecorded field listed in `unknown_fields`; a publication-outcome goal requires no
      stage or time field; blank title and an unknown outcome type are rejected with no
      row created; an unknown request field is rejected.
      `tests/api/test_create_goal.py` (9 tests, confirmed failing first). Covers the
      reported-null fields, both non-software outcomes, validation with no row written,
      unknown/priority/extra-field rejection, the initial revision, and the correlation id.
- [x] 3.2 Implement domain validation (title length after trim, outcome type set,
      priority set) and the goal entity.
      `domain/goal.py`: value sets, `Goal` with derived `unknown_fields`, `InvalidGoal`
      naming the field, `validate_new_goal`.
- [x] 3.3 Implement `POST /goals` with one transaction inserting the goal row and its
      initial revision (`changed_fields` = all supplied fields).
      `application/goals.py` (port + `create_goal`), `adapters/sqlite/goal_repository.py`
      (`BEGIN IMMEDIATE`, goal row + revision row), `api/http.py` (models, route,
      correlation id, contract-shaped 422), `bootstrap/app.py` (`create_app`).
      Decisions: the creation revision is `revision_number 0` with `prior_state {}` so
      `goals.revision` still equals the highest revision number (contract §5 invariant);
      "supplied fields" means the fields carrying a non-null value. A title is stored as
      submitted (only blank-checked after trimming) because the spec asks for a goal
      "retrievable exactly as created". OpenAPI/docs routes are off: the contract is the
      only surface.
- [x] 3.4 Tests pass.
      `.venv/Scripts/python -m pytest` → 16 passed. Not the system interpreter: the
      global environment has `starlette 1.6.0` against `fastapi 0.121.3`, which requires
      `starlette<0.51`, so `FastAPI()` raises before routing. Project venv created
      (gitignored); `httpx` added to the `dev` extra because `TestClient` needs it.

Traceability: FR-001, FR-002, FR-005, FR-044; `data-model.md`, `portfolio-domain.md`.

## Slice 3: retrieve and list goals

Covers: *Retrieve and list goals*.

- [x] 4.1 Failing tests: retrieval by id; unknown id is `404`; listing is bounded and
      active-only by default; following `next_cursor` yields the remaining goals with no
      duplicates or gaps; `status=archived` and `status=all` filter correctly; an
      invalid cursor is a validation error.
      `tests/api/test_list_goals.py` (12 tests, confirmed failing first: new routes
      returned `405`/`{"detail": …}` before they existed). Adds round-trip retrieval,
      archived-goal retrieval, the three-status filter, an identical-`created_at`
      ordering case, invalid cursors and out-of-range `limit`/`status`.
- [x] 4.2 Implement keyset pagination on `(created_at DESC, id ASC)` and the opaque
      cursor codec.
      `list_page` in `adapters/sqlite/goal_repository.py` selects `limit + 1` rows and
      filters on `created_at < ? OR (created_at = ? AND id > ?)`; `application/goals.py`
      encodes `{"created_at","id"}` as unpadded urlsafe base64 and rejects a cursor that
      does not decode with `InvalidGoal("cursor", …)`. The shared `client` fixture moved
      to `tests/conftest.py`.
- [x] 4.3 Tests pass, including the page-boundary case.
      `.venv/Scripts/python -m pytest` → 28 passed. Known gap: an unknown *path* (not an
      unknown goal) still returns FastAPI's default `{"detail": …}` body, because only
      `404` for a missing goal is mapped into the contract envelope.

Traceability: FR-043; `api-contract.md` §3.2–3.3.

## Slice 4: revise a goal with history

Covers: *Revise a goal and retain its history* and the update side of *Reject invalid
changes atomically*.

- [x] 5.1 Failing tests: a PATCH stores the new value and appends a revision containing
      the prior value, changed field, time and reason; `revision` increments once;
      setting a field to `null` records a change back to unknown; a stale
      `expected_revision` returns `409` with the current revision and changes nothing;
      a server-owned field (`id`, `status`, `revision`, timestamps) is rejected; a
      rejected update creates no revision.
      `tests/api/test_revise_goal.py` (18 tests, confirmed failing first with `405`) plus
      `tests/adapters/sqlite/test_goal_repository.py` for the lost-update guard. Also
      covers: absent fields untouched, a matching `expected_revision`, a no-op update
      creating no revision, and an over-long `revision_reason`.
- [x] 5.2 Implement `PATCH /goals/{goal_id}` with the revision insert inside the same
      transaction as the row update.
      `revise_goal` compares the proposed values with the current row, so only fields
      that actually change are recorded; `repository.revise` updates `WHERE id = ? AND
      revision = ?` and rolls back when the row moved on, and the application re-reads
      the current revision for the `409`.
- [x] 5.3 Implement `GET /goals/{goal_id}/revisions` with the same cursor mechanics.
      Keyset on `revision_number DESC` through a second cursor codec; an unknown goal is
      `404` before any page is read.
- [x] 5.4 Tests pass, including the conflict case.
      `.venv/Scripts/python -m pytest` → 48 passed. The `409` body carries
      `details: [{"current_revision": n}]`, a shape `api-contract.md` §4 did not name;
      recorded there and in the verification notes rather than invented silently.

Traceability: FR-006, NFR-007, NFR-014, NFR-016; `data-model.md`, `persistence.md`.

## Slice 5: archive without deleting

Covers: *Archive a goal without deleting it*.

- [x] 6.1 Failing tests: archiving sets status and `archived_at`, appends one revision,
      and removes the goal from the default listing; the goal and its revisions remain
      retrievable; a second archive returns `200` and creates no revision; no row is
      deleted.
      `tests/api/test_archive_goal.py` (5 tests, confirmed failing first with `405`).
- [x] 6.2 Implement `POST /goals/{goal_id}/archive` idempotently.
      `archive_goal` returns an already-archived goal untouched and otherwise reuses the
      same guarded `repository.revise`, so archival inherits the lost-update check and
      the `changed_fields: ["status"]` revision.
- [x] 6.3 Tests pass.
      `.venv/Scripts/python -m pytest` → 53 passed.

Traceability: FR-001; `data-model.md`.

## Slice 6: local operation and diagnostics

Covers: *Serve only on the local interface with safe diagnostics*, *Configure local
operation without editing source*.

- [x] 7.1 Failing tests: startup binds `127.0.0.1` only; a non-loopback value without an
      override fails before any socket opens; `/health` separates service, database and
      integrations; a database failure yields `503` with database `unavailable`; no error
      or health payload contains the database path or a credential-shaped value;
      configuration is read from environment and a machine-local file.
      `tests/bootstrap/test_config.py` (11 tests), `tests/api/test_health.py` (4) and
      `tests/bootstrap/test_serve.py` (4), confirmed failing first (`ModuleNotFoundError`
      for `siddhi.bootstrap.config`, then `404` for `/health`).
- [x] 7.2 Implement configuration loading and validation with messages naming the
      setting only.
      `bootstrap/config.py`: built-in defaults → `~/.siddhi/settings.json` → `SIDDHI_*`
      environment → explicit argument. `ConfigError` carries the setting name and a
      message that states the allowed values but never echoes the submitted one; a
      non-loopback `bind_host` is refused during `load_settings`, before any socket.
- [x] 7.3 Implement `/health` composition and structured logging with correlation ids.
      `observability/health.py` reads only reachability and the schema version, returning
      `503`/`unavailable` without a traceback. `observability/logging.py` writes one JSON
      line per event; the correlation middleware emits `http.request` with method, path,
      status and duration, never a body. `serve()` in `bootstrap/app.py` and
      `src/siddhi/__main__.py` give the process its entrypoint: failures to load
      configuration or migrate exit `1` with the reason on stderr.
- [x] 7.4 Tests pass.
      `.venv/Scripts/python -m pytest` → 74 passed. Verified against a real process as
      well: `python -m siddhi` with `SIDDHI_BIND_HOST=0.0.0.0` prints
      `siddhi: SIDDHI_BIND_HOST: must be a loopback address (127.0.0.1 or localhost)` and
      exits `1`; started normally on `127.0.0.1:8177` it answered `GET /health` with `200`
      and the contract payload, and logged
      `{"event":"http.request","correlation_id":…,"path":"/health","status":200,…}`
      to stdout. This closes slice 1's unverified non-zero exit.

Traceability: FR-046, FR-049, FR-050, NFR-022, NFR-026; `security-and-privacy.md`,
`configuration-and-secrets.md`, `observability.md`.

## Slice 7: end-to-end verification and reporting

- [x] 8.1 End-to-end test over HTTP against a temporary database: create → retrieve →
      revise → list revisions → archive → confirm listing and history.
      `tests/test_end_to_end.py::test_a_goal_runs_its_whole_lifecycle_on_one_database`
      drives all five routes through one `TestClient` on a temporary database file,
      including `GET /health` at the end.
- [x] 8.2 Failure-case sweep: invalid input, stale revision, unknown id, unavailable
      database, interrupted migration — each asserted to leave state unchanged or
      reported, not silently corrected.
      `test_rejected_requests_change_nothing` runs eight rejected requests (missing title,
      blank title, bad priority, stale revision, three unknown-identifier cases, unknown
      route) and compares full `goals` and `goal_revisions` dumps before and after.
      `test_an_unusable_database_is_reported_and_not_repaired` replaces the database file
      with a directory: reads, writes and `/health` all answer `503 unavailable` with no
      path in the body, and the path is not recreated. The interrupted-migration case is
      `test_migrations.py::test_failed_migration_leaves_prior_version_and_rows_readable`.
      Closing a contract gap found here: `sqlite3.Error` now maps to
      `503 unavailable/database_unavailable` (contract §4 already listed the category;
      nothing else was invented) and only the exception type is logged, because SQLite
      messages embed the database path.
- [x] 8.3 Run `openspec validate be-01-goal-and-persistence` and
      `openspec show be-01-goal-and-persistence --json --deltas-only`.
      `Change 'be-01-goal-and-persistence' is valid`; the delta view parses and reports
      `deltaCount: 10` (6 `fun-01-portfolio-goals`, 4 `tech-02-local-database-baseline`).
- [x] 8.4 Fill the verification record below with actual outcomes; report structural
      checks separately from executed tests, and leave unavailable checks marked as such.
      Filled below; known gaps are listed rather than smoothed over.

Traceability: `knowledge/practices/testing-and-validation.md`;
`engineering-quality` grill Q1, Q3.

## Verification evidence

Executed suite: `.venv/Scripts/python -m pytest -q` → **77 passed, 1 warning** (the warning
is Starlette's `httpx` deprecation notice, unrelated to Siddhi code).

### Executed checks, by requirement

| Requirement (delta) | Evidence | Result |
|---|---|---|
| Capture a goal before any project exists | `tests/api/test_create_goal.py` (9), lifecycle test | pass |
| Retrieve and list goals | `tests/api/test_list_goals.py` (12): bounded page, cursor walk, status filters, tie-break, invalid cursor | pass |
| Revise a goal and retain its history | `tests/api/test_revise_goal.py` (18) + `tests/adapters/sqlite/test_goal_repository.py` (1, lost-update guard) | pass |
| Archive a goal without deleting it | `tests/api/test_archive_goal.py` (5) | pass |
| Absent information stays explicitly unknown | `unknown_fields` asserted on create and after an explicit `null`; `prior_state` rows read back from SQLite | pass |
| Reject invalid changes atomically | `tests/test_end_to_end.py::test_rejected_requests_change_nothing` (8 cases, state compared before/after) | pass |
| Report and evolve the database schema version | `tests/adapters/sqlite/test_migrations.py` (6) | pass |
| Fail closed when a migration fails | `test_failed_migration_leaves_prior_version_and_rows_readable`; `tests/bootstrap/test_serve.py::test_main_reports_a_failed_migration` (exit `1`) | pass |
| Serve only on the local interface with safe diagnostics | `tests/bootstrap/test_config.py` (11), `tests/api/test_health.py` (4), `tests/bootstrap/test_serve.py` (4); manual process smoke test | pass |
| Configure local operation without editing source | `tests/bootstrap/test_config.py`: defaults, file, environment precedence, refusals | pass |

Suite sizes: `tests/adapters/sqlite` 8, `tests/api` 49, `tests/bootstrap` 17,
`tests/test_end_to_end.py` 3.

Manual process check (not part of the suite): `python -m siddhi` with
`SIDDHI_BIND_HOST=0.0.0.0` printed
`siddhi: SIDDHI_BIND_HOST: must be a loopback address (127.0.0.1 or localhost)` and exited
`1`; with a loopback host on port 8177 it served `GET /health` → `200` with the contract
payload and wrote one JSON request line to stdout.

### Structural checks

| Check | Command | Result |
|---|---|---|
| Change validity | `openspec validate be-01-goal-and-persistence` | `Change 'be-01-goal-and-persistence' is valid` |
| Delta parse and count | `openspec show be-01-goal-and-persistence --json --deltas-only` | 10 deltas: 6 `fun-01-portfolio-goals`, 4 `tech-02-local-database-baseline` |

### Not verified, or verified only in part

- **Gherkin scenarios are documentation, not executable.** No Gherkin runner or step
  definitions exist, so each scenario is represented by a pytest assertion rather than
  executed as Gherkin.
- **Unknown-path 404 shape.** `GET /agenda` returns `404` with FastAPI's default
  `{"detail": …}` body; only an unknown *goal* identifier is mapped into the contract
  envelope. Deferred rather than silently claimed as conformant.
- **Coverage is not measured.** No coverage tool or threshold is configured, so no
  percentage is reported.
- **Concurrency** is verified only through the repository's guarded update, not with
  parallel processes or a second connection racing a write.
- **Performance and load** are unmeasured; this is a single-user local store.
- **Backups** are copied before a migration but never pruned, and there is no index for
  the `(created_at DESC, id ASC)` listing.

## Out of scope (deliberately not started)

Source adapters, project association, analysis and findings, planning and reviews,
external analysis handoff, local authentication, remote binding, write-back to any
source, backups and retention policy. Each needs its own change and, for the last three,
an owner decision listed in `adr.md` §3.
