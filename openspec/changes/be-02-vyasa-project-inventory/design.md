# Design: Vyasa project inventory

## 1. Overview

### Purpose

Deliver the first source ingestion: one explicit refresh reads Vyasa project inventory
through the local MCP interface, stores a current project view with run context, and
serves it over HTTP. Failing to read Vyasa never hides local portfolio data.

### Scope

An application inventory service, a project repository, a read-only Vyasa MCP adapter,
one additive migration, one configuration setting, three HTTP operations, and an
extended health integration block. No checkout analysis, relationships or rescan.

### Design principles

- The source owns its facts; Siddhi owns the projection and the observation time
  (`knowledge/architecture/data-ownership.md`).
- A read is complete or it publishes nothing (`knowledge/architecture/ingestion-and-snapshots.md`).
- Source vocabulary is preserved, never translated into a Siddhi judgement.
- Failures are categories, not free text, and never leak paths or source messages.
- Reuse the existing HTTP envelope, cursor style, migration runner and repository shape.

## 2. Context and constraints

### Current state

`be-01-goal-and-persistence` implemented goals, revisions, the migration runner and the
HTTP surface. `create_app(db_path)` assembles goals only; `/health` reports
`integrations: not_configured`; schema version is 1. No adapter package exists.

### Constraints

- Python 3.12 standard library only for the new transport: `subprocess`, `json`,
  `queue`, `threading`. No new dependency, so no dependency audit is triggered.
- The Vyasa executable path is machine-local configuration; no path is stored,
  returned or logged.
- One refresh is synchronous in this slice; no background job or queue.
- Automated tests never start Vyasa; the port is replaced by a test double, and the
  stdio client is exercised against a scripted local process.

### Existing decisions and conventions

`knowledge/decisions/source-adapter-boundaries.md`,
`source-authority-and-read-only-ingestion.md`, `source-history-and-provenance.md`,
`versioned-history-and-migrations.md`, `local-first-sqlite.md`,
`proportionate-background-execution.md`; architecture in
`knowledge/architecture/source-adapters.md`, `ingestion-and-snapshots.md`,
`vyasa-integration.md`, `persistence.md`, `api-boundary.md`.

## 3. Components

| Component | Responsibility | Depends on |
|---|---|---|
| `domain/project` | Project observation vocabulary, inventory validation, source failure category | standard library |
| `application/inventory` | Inventory port, refresh/publication rules, listing, cursors, errors | domain, repository port |
| `adapters/sqlite/project_repository` | Projection upsert/removal, run rows, reads, diff counts | stdlib `sqlite3` |
| `adapters/vyasa/mcp_source` | Stdio MCP session, envelope validation, bounded paging, failure mapping | domain, standard library |
| `api/http` | Request/response models, routes, error mapping | application |
| `bootstrap` | Vyasa setting, adapter assembly | configuration, adapters |
| `observability/health` | Integration status from the latest run | repository |

Dependency direction stays inward: `api` → `application` → `domain`; adapters implement
ports declared by the application. `api` holds no SQL; the domain holds no transport.

## 4. Data flow

### Refresh (`POST /ingestion/vyasa/refresh`)

1. HTTP calls `refresh_inventory(repository, source)`; no body is accepted.
2. No source configured: raise `SourceNotConfigured` before opening a transaction.
3. Generate `run_id` and `started_at`; call `source.fetch_inventory()`.
4. The adapter starts one Vyasa process, handshakes, pages `search_projects` with
   `limit=100`, validates every answer, and returns an `Inventory` or raises
   `SourceError(category, message)`.
5. On `SourceError`: insert a failed run row (category only) in its own transaction,
   then raise `SourceUnavailable(category, run_id)`; HTTP maps to `503`.
6. On success: one transaction inserts the completed run row, compares the observed
   projects with the current view, upserts changed rows, deletes rows absent from the
   completed read, and writes the counts. Added/updated/removed/unchanged are computed
   against the pre-transaction rows, so a retry with identical input is all-unchanged.
7. Return the run report.

### Read (`GET /projects`, `GET /projects/{id}`)

One read transaction; no source access. Listing is keyset paginated on
`(display_name ASC, project_id ASC)`; the cursor carries the last row's key, so pages
are stable while a refresh inserts rows. `freshness` comes from the run that last
observed the row, so old data cannot borrow a newer run's freshness.

### Startup

Existing flow plus: read `SIDDHI_VYASA_MCP_COMMAND`; if unset the application has no
inventory source and still serves goals and stored projects. A configured path is not
checked at startup, because a broken Vyasa must not stop local work.

## 5. Key design choices

| Choice | Alternative rejected | Reason |
|---|---|---|
| Application port returning a validated `Inventory` | Letting the application parse MCP payloads | Keeps transport and vocabulary replaceable |
| Publish only a complete read | Publish per page | A partial page set is not a snapshot and would remove real projects |
| Diff inside the publish transaction | Read-then-write in the application | Keeps counts and rows consistent under concurrent refreshes |
| Run rows kept, project rows current-only | Full per-run project history now | Current view plus run ledger answers this slice; history is a later, larger slice |
| Minimal stdio JSON-RPC client | Add the `mcp` SDK dependency | The observed protocol is newline-delimited JSON; ~60 lines avoid a dependency and keep tests offline |
| One process per refresh | Long-lived MCP process | Refresh is explicit and rare; process reuse is unearned until cost is measured |
| Cursor carries `(name, id)` | Offset pagination | Stable pages while refreshes add and remove rows |
| Removal only on a completed read | Removing on failure or partial page | Absence in an incomplete read proves nothing |

## 6. Error handling

| Failure | Behavior |
|---|---|
| Vyasa not configured | `503 unavailable` / `source_not_configured`, no run row |
| Executable missing or process fails | failed run `connection_failed`, `503 source_unavailable` |
| Handshake or malformed JSON | failed run `protocol_error`, `503` |
| Read timeout | failed run `timeout`; process terminated, `503` |
| Tool result marked as an error | failed run `tool_error`, `503` |
| Unexpected `schema_version` or missing field | failed run `unsupported_contract`, `503` |
| Repeated or non-advancing cursor | failed run `protocol_error`, `503` |
| Invalid filter, limit or cursor | `422 validation`, no read |
| Unknown project | `404 not_found` / `project_not_found` |
| Database unavailable | existing `503 unavailable` / `database_unavailable` |
| Unexpected exception | `500 internal`, correlation id only |

The adapter never puts the source message or executable path into a stored row, a log
line or a response. Logs record the run id, outcome, category and duration only.

## 7. Security and privacy

- The executable is launched with an argument-free process; no shell is involved.
- The adapter's protocol client reads only newline-delimited JSON and ignores
  unsolicited messages; a bounded message size and timeout prevent a hung child.
- Source display names and language labels are stored and returned as data; they never
  reach logs or error text.
- No credentials exist in this slice; the local process inherits the environment, so
  no credential is passed explicitly.
- Loopback binding remains the only access control; local authentication stays an open
  owner decision.

## 8. Testing and evidence

| Layer | Owns | Examples |
|---|---|---|
| Unit | Inventory validation, diff counts, cursor encoding | Unknown state rejected; identical refresh is all-unchanged |
| Contract | Response shapes and error categories against `api-contract.md` | Refresh report; 503 details; project payload |
| Integration | Application + real SQLite file with a test double | Refresh, list, filter, page, retrieve |
| Persistence | Constraints, transaction rollback, removal rule | Failed refresh leaves rows; complete read removes absent row; version 2 migration |
| Adapter | Stdio client against a scripted process | Handshake, two pages, tool error, unsupported version, repeated cursor, timeout |
| Operational | Configuration and health | Unset setting; failed last run reported; no path in payload |

Tests run offline. One manual smoke refresh against the real Vyasa executable is
reported separately from the automated suite, together with its observed counts.

## 9. Risks

- The observed Vyasa contract is one deployment; any drift fails the refresh loudly. A
  future compatibility policy needs real fixtures from another deployment.
- Removal is based on a complete read, but Vyasa's `search_projects` filters default to
  no filter; a future filtered refresh must not reuse the removal path unchanged.
- Run history grows without a retention rule; acceptable for a local single-user store
  until retention is decided.
- A synchronous refresh blocks one HTTP request; bounded by page cap and timeout.

## 10. Knowledge References

- `knowledge/architecture/vyasa-integration.md`
- `knowledge/technologies/vyasa-contract-direction.md`
- `knowledge/architecture/source-adapters.md`
- `knowledge/architecture/ingestion-and-snapshots.md`
- `knowledge/architecture/data-ownership.md`
- `knowledge/concepts/evidence-semantics.md`
- `knowledge/architecture/persistence.md`
- `knowledge/architecture/api-boundary.md`
- `knowledge/architecture/configuration-and-secrets.md`
- `knowledge/architecture/security-and-privacy.md`
- `knowledge/architecture/observability.md`
- `knowledge/practices/vertical-slices.md`
- `knowledge/practices/testing-and-validation.md`

## 11. Open decisions

Unchanged owner decisions: local authentication and origin policy, pre-1.0
compatibility policy, reference workload, and recovery/retention targets. None blocks
this slice, and none is assumed here.
