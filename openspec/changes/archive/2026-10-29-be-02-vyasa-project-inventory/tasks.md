# Implementation Tasks: Vyasa project inventory

- **OpenSpec Change ID:** `be-02-vyasa-project-inventory`
- **Status:** In Progress (implementation complete; closeout pending)
- **Related artifacts:** `proposal.md`, `specs/`, `api-contract.md`, `design.md`, `adr.md`

## Planning rules applied here

Each slice is one observable behavior whose failing test is written first
(`knowledge/practices/vertical-slices.md`, `test-driven-development`). Automated tests
never start Vyasa: the application is tested through an inventory port double, and the
stdio adapter against a scripted local process. Structural document checks are
reported separately from executed tests.

## Prerequisites

Enabling work only, no user-observable behavior.

- [x] 1.1 Update the existing migration assertions from schema version 1 to 2
      (`tests/adapters/sqlite/test_migrations.py`, `tests/api/test_health.py`), confirm
      they fail, then add `002_project_inventory.sql` from `api-contract.md` §5.
      Red evidence: 3 failed (`schema_version == 2`, ledger `[1, 2]`, `Settings` has no
      `vyasa_mcp_command`). Green: `.venv/Scripts/python -m pytest -q` → 78 passed.
- [x] 1.2 Add the `SIDDHI_VYASA_MCP_COMMAND` setting with validation and a test; unset
      or blank means no source. A configured path is not required to exist at startup.
      Evidence: `test_vyasa_command_is_optional_and_blank_is_refused` (unset → `None`,
      set value kept verbatim, blank → `ConfigError` naming the setting).
- [x] 1.3 Add a test-double inventory port and a shared `TestClient` factory that
      accepts it (`tests/conftest.py`), without changing existing goal tests.
      Evidence: `tests/fakes.py` (`FakeSource`, `project()`, `inventory()`) and
      `tests/conftest.py::make_client`; the `client` fixture is unchanged.

## Slice 1: Explicit refresh publishes a project inventory

Covers: *Refresh Vyasa inventory explicitly*, *Preserve prior valid inventory when a
refresh fails*, *Local portfolio work survives Vyasa failure* (refresh half),
`api-contract.md` §3.1, §5.

- [x] 2.1 Failing contract tests for the refresh: completed refresh stores every
      project and reports counts; an identical repeat is all-unchanged and keeps
      `first_observed_at`; changed fields count as updated; a source failure returns
      `503 source_unavailable` with run and failure category while stored projects and
      goals stay unchanged; no configured source returns `503 source_not_configured`
      with no run row; a later failure publishes nothing new while the previous
      completed view stays served.
      Red evidence: `tests/api/test_refresh_inventory.py` failed collection with
      `ModuleNotFoundError: siddhi.domain.project`, then 4 of 7 failed with
      `database_unavailable` (run row inserted after the rows that reference it).
- [x] 2.2 Implement `domain/project.py`: observation vocabulary, required-field
      validation, allowed states, source failure category.
- [x] 2.3 Implement `application/inventory.py`: inventory and repository ports,
      `refresh_inventory`, failure-then-report behavior, run identifiers.
- [x] 2.4 Implement `adapters/sqlite/project_repository.py`: one transaction inserting
      the run and applying added/updated/removed/unchanged rows.
- [x] 2.5 Wire `POST /ingestion/vyasa/refresh` in `api/http.py` and inject the source in
      `bootstrap/app.py`; map `unavailable` errors without leaking source text.
- [x] 2.6 Tests pass at the contract layer; record the evidence.
      Evidence: `.venv/Scripts/python -m pytest -q` → 85 passed, 1 warning
      (Starlette `httpx` deprecation). `test_refresh_inventory.py` covers 7 cases
      including the duplicate-identifier rejection and a fake `SourceError` whose
      message contains a path (`"secret" not in failed.text`).

## Slice 2: List and retrieve the observed projects

Covers: *List and retrieve observed projects*, *Distinguish source state, freshness and
observation time*, *Remove only from a complete observation*, `api-contract.md` §3.2–3.3.

- [x] 3.1 Failing contract tests: list ordering and cursor page boundary; state filter;
      empty inventory is an empty list; unknown identifier is `404 project_not_found`;
      project payload carries state, identity status, providers, languages, first/last
      observation time and the observing run's freshness; `missing` is returned as a
      state without deletion; a project absent from a completed read disappears while a
      failed read removes nothing.
      Red evidence: `tests/api/test_list_projects.py` → 10 failed (all endpoints absent).
- [x] 3.2 Implement repository reads (keyset page, single project) and application
      listing/retrieval with cursor validation.
- [x] 3.3 Wire `GET /projects` and `GET /projects/{project_id}`.
- [x] 3.4 Tests pass; record the evidence.
      Evidence: `test_list_projects.py` → 10 passed; full suite → 95 passed, 1 warning.
      Rejected query values report `validation`/`invalid_field` with `state`, `cursor`
      and `limit`; the failed-read case is covered in `test_refresh_inventory.py`.

## Slice 3: Read-only Vyasa MCP adapter with explicit failures

Covers: *Read Vyasa only through the agreed read-only interface*, *Validate the source
contract and fail explicitly*, *Bound paging and reject a stalled cursor*,
`design.md` §4, §6.

- [x] 4.1 Failing adapter tests against a scripted local process: handshake and two
      pages produce one inventory; a tool result marked as an error becomes
      `tool_error`; a different `schema_version` becomes `unsupported_contract`; a
      repeated cursor becomes `protocol_error`; a silent process becomes `timeout`;
      the process is terminated on success and failure.
      Red evidence: `tests/adapters/vyasa` failed collection (`No module named
      siddhi.adapters.vyasa.mcp_source`).
- [x] 4.2 Implement `adapters/vyasa/mcp_source.py` with the stdlib stdio session,
      bounded paging, field validation and failure categories.
- [x] 4.3 Confirm no source message or executable path reaches a stored row, log line
      or response.
      Evidence: adapter surfaces only `SourceError.category`; `test_a_tool_error_stays_a
      _category_without_the_source_message` and the refresh contract test whose fake
      message contains `E:\secret\...` both pass. The adapter logs nothing.
- [x] 4.4 Tests pass; record the evidence.
      Evidence: `tests/adapters/vyasa` → 10 passed; full suite → 106 passed, 1 warning.
      Scenarios cover two pages, text-only answers, empty inventory, process close,
      tool error, unsupported version, missing field, repeated cursor, timeout and a
      missing executable.

## Slice 4: Health reports integration state truthfully

Covers: `api-contract.md` §3.4 and the failure half of *Local portfolio work survives
Vyasa failure*.

- [x] 5.1 Failing tests: not configured; configured with no run; last run completed;
      last run failed still reports service `ok`; no path or setting value in the
      payload.
      Red evidence: 4 of the 5 new health tests failed (integrations was the old
      `not_configured` constant).
- [x] 5.2 Implement the `integrations` block from the latest run and pass configuration
      state into health.
      Note: the last run is read by insertion order (`rowid`), because two refreshes in
      the same second share a `started_at`.
- [x] 5.3 Tests pass; record the evidence.
      Evidence: `tests/api/test_health.py` → 8 passed; full suite → 110 passed, 1 warning.

## Slice 5: Verification and closeout

- [x] 6.1 Run the full suite with `.venv/Scripts/python -m pytest -q`; record counts and
      warnings.
      Evidence: 111 passed, 1 warning (`StarletteDeprecationWarning`: `httpx` with
      `starlette.testclient` is deprecated in the installed environment).
- [x] 6.2 Run one manual smoke refresh against the real Vyasa MCP executable; record
      counts, freshness and a project read. Keep the path out of the repository.
      Evidence (2026-10-29, script outside the repository, temporary database):
      first refresh `completed`, 74 added, 0 updated/removed/unchanged, `freshness`
      `current`, `index_version` `"11"`; page of 3 returned `AgentNoir`, `Amsha`,
      `Bodha` with `has_more` true; one project read returned its native 32-hex id,
      `active`, `resolved`, `bitbucket`, `Python`; a second refresh was 74 unchanged.
      The smoke run found one real defect: Vyasa sends `index_version` as a number, so
      the adapter now keeps a numeric scalar as text (test added).
- [x] 6.3 Run `openspec validate be-02-vyasa-project-inventory` and the delta view.
      Evidence: `Change 'be-02-vyasa-project-inventory' is valid` (run twice, before and
      after the review round; no separate delta view was needed).
- [x] 6.4 Review against the contract with `code-reviewer`; security pass with
      `code-review-security` and `secrets-scan`; no dependency change, so no SCA run.
      Findings fixed: a failed handshake leaked the child process (now closed on any
      handshake failure, covered by a marker-file scenario); a page without `has_more`
      was treated as complete (now `unsupported_contract`); a tool-level `unavailable`
      was reported as `tool_error` (now `unavailable`); a `RecursionError` in the reader
      thread turned a fast failure into a timeout (now any unparseable line fails
      fast); unbounded `readline` (now capped at 1 MB); the refresh ignored an unknown
      body field (now `422`); `/health` omitted `last_run` in the non-configured and
      store-unavailable branches (now always present); a forged cursor with non-string
      values was coerced (now `422`); real-looking executable paths in `tests/bootstrap`
      replaced with `tmp_path` values; `*.db`/`*.bak`/`settings.json` ignored.
      Added: a cross-site `Origin` on a state-changing request is refused (`403
      cross_site_request`) before the source runs; an unexpected exception returns the
      `500 internal` envelope instead of a plaintext traceback.
      Accepted and recorded instead: per-message timeout is not a per-refresh deadline,
      concurrent refreshes are not serialised, the child inherits the environment, and
      loopback binding remains the only access control (no authentication).
      `secrets-scan`: no credentials; scanner not installed, so the result is
      pattern-based, not tool-certified.
- [x] 6.5 Report honest gaps: one deployment verified, no partial publication, run
      history unbounded, refresh synchronous.
      Gaps: only one Vyasa deployment was verified (v1 contract, `index_version` 11);
      the adapter returns only a complete inventory, so "failure after the first page
      publishes nothing" is enforced structurally rather than exercised end-to-end with
      a real second page; run history has no retention rule; a refresh is synchronous
      and neither the whole-refresh duration (100 pages x per-message timeout) nor
      concurrent refreshes are bounded; `MAX_PAGES`/`MAX_PROJECTS` bounds are not
      exercised by a test; `last_observed_at` is the run's `started_at`, and a project
      removed and later re-added gets a new `first_observed_at`. Source-supplied field
      lengths are bounded only by the 1 MB message cap.
- [x] 6.6 Merge `--no-ff` into `develop`, push, archive the change, and replace any
      placeholder `## Purpose` in the synced specs.
      Evidence: merged as `3cbf945`, pushed; archived as
      `2026-10-29-be-02-vyasa-project-inventory`; the `fun-02-project-inventory` and
      `tech-03-vyasa-mcp-adapter` purposes were written after archiving.
