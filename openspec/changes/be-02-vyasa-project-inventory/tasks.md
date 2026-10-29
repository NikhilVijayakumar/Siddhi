# Implementation Tasks: Vyasa project inventory

- **OpenSpec Change ID:** `be-02-vyasa-project-inventory`
- **Status:** Artifacts complete; implementation not started
- **Related artifacts:** `proposal.md`, `specs/`, `api-contract.md`, `design.md`, `adr.md`

## Planning rules applied here

Each slice is one observable behavior whose failing test is written first
(`knowledge/practices/vertical-slices.md`, `test-driven-development`). Automated tests
never start Vyasa: the application is tested through an inventory port double, and the
stdio adapter against a scripted local process. Structural document checks are
reported separately from executed tests.

## Prerequisites

Enabling work only, no user-observable behavior.

- [ ] 1.1 Update the existing migration assertions from schema version 1 to 2
      (`tests/adapters/sqlite/test_migrations.py`, `tests/api/test_health.py`), confirm
      they fail, then add `002_project_inventory.sql` from `api-contract.md` §5.
      Red evidence, then green evidence, recorded in this file.
- [ ] 1.2 Add the `SIDDHI_VYASA_MCP_COMMAND` setting with validation and a test; unset
      or blank means no source. A configured path is not required to exist at startup.
- [ ] 1.3 Add a test-double inventory port and a shared `TestClient` factory that
      accepts it (`tests/conftest.py`), without changing existing goal tests.

## Slice 1: Explicit refresh publishes a project inventory

Covers: *Refresh Vyasa inventory explicitly*, *Preserve prior valid inventory when a
refresh fails*, *Local portfolio work survives Vyasa failure* (refresh half),
`api-contract.md` §3.1, §5.

- [ ] 2.1 Failing contract tests for the refresh: completed refresh stores every
      project and reports counts; an identical repeat is all-unchanged and keeps
      `first_observed_at`; changed fields count as updated; a source failure returns
      `503 source_unavailable` with run and failure category while stored projects and
      goals stay unchanged; no configured source returns `503 source_not_configured`
      with no run row; a failure after the first page publishes nothing.
- [ ] 2.2 Implement `domain/project.py`: observation vocabulary, required-field
      validation, allowed states, source failure category.
- [ ] 2.3 Implement `application/inventory.py`: inventory and repository ports,
      `refresh_inventory`, failure-then-report behavior, run identifiers.
- [ ] 2.4 Implement `adapters/sqlite/project_repository.py`: one transaction inserting
      the run and applying added/updated/removed/unchanged rows.
- [ ] 2.5 Wire `POST /ingestion/vyasa/refresh` in `api/http.py` and inject the source in
      `bootstrap/app.py`; map `unavailable` errors without leaking source text.
- [ ] 2.6 Tests pass at the contract layer; record the evidence.

## Slice 2: List and retrieve the observed projects

Covers: *List and retrieve observed projects*, *Distinguish source state, freshness and
observation time*, *Remove only from a complete observation*, `api-contract.md` §3.2–3.3.

- [ ] 3.1 Failing contract tests: list ordering and cursor page boundary; state filter;
      empty inventory is an empty list; unknown identifier is `404 project_not_found`;
      project payload carries state, identity status, providers, languages, first/last
      observation time and the observing run's freshness; `missing` is returned as a
      state without deletion; a project absent from a completed read disappears while a
      failed read removes nothing.
- [ ] 3.2 Implement repository reads (keyset page, single project) and application
      listing/retrieval with cursor validation.
- [ ] 3.3 Wire `GET /projects` and `GET /projects/{project_id}`.
- [ ] 3.4 Tests pass; record the evidence.

## Slice 3: Read-only Vyasa MCP adapter with explicit failures

Covers: *Read Vyasa only through the agreed read-only interface*, *Validate the source
contract and fail explicitly*, *Bound paging and reject a stalled cursor*,
`design.md` §4, §6.

- [ ] 4.1 Failing adapter tests against a scripted local process: handshake and two
      pages produce one inventory; a tool result marked as an error becomes
      `tool_error`; a different `schema_version` becomes `unsupported_contract`; a
      repeated cursor becomes `protocol_error`; a silent process becomes `timeout`;
      the process is terminated on success and failure.
- [ ] 4.2 Implement `adapters/vyasa/mcp_source.py` with the stdlib stdio session,
      bounded paging, field validation and failure categories.
- [ ] 4.3 Confirm no source message or executable path reaches a stored row, log line
      or response.
- [ ] 4.4 Tests pass; record the evidence.

## Slice 4: Health reports integration state truthfully

Covers: `api-contract.md` §3.4 and the failure half of *Local portfolio work survives
Vyasa failure*.

- [ ] 5.1 Failing tests: not configured; configured with no run; last run completed;
      last run failed still reports service `ok`; no path or setting value in the
      payload.
- [ ] 5.2 Implement the `integrations` block from the latest run and pass configuration
      state into health.
- [ ] 5.3 Tests pass; record the evidence.

## Slice 5: Verification and closeout

- [ ] 6.1 Run the full suite with `.venv/Scripts/python -m pytest -q`; record counts and
      warnings.
- [ ] 6.2 Run one manual smoke refresh against the real Vyasa MCP executable; record
      counts, freshness and a project read. Keep the path out of the repository.
- [ ] 6.3 Run `openspec validate be-02-vyasa-project-inventory` and the delta view.
- [ ] 6.4 Review against the contract with `code-reviewer`; security pass with
      `code-review-security` and `secrets-scan`; no dependency change, so no SCA run.
- [ ] 6.5 Report honest gaps: one deployment verified, no partial publication, run
      history unbounded, refresh synchronous.
- [ ] 6.6 Merge `--no-ff` into `develop`, push, archive the change, and replace any
      placeholder `## Purpose` in the synced specs.
