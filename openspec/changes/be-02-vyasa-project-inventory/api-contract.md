# Interface and data contract: Vyasa project inventory

- **OpenSpec Change ID:** `be-02-vyasa-project-inventory`
- **Proposing team:** be (backend team)
- **Related proposal:** `proposal.md`
- **Related specifications:** `specs/fun-02-project-inventory/spec.md`, `specs/tech-03-vyasa-mcp-adapter/spec.md`
- **Related design:** `design.md`

## 1. Purpose and scope

Fixes the second HTTP surface and the first source ingestion: an explicit refresh that
reads Vyasa project inventory, a stored current project view with run context, and
read operations over that view. Checkout-level evidence, project relationships,
analysis, and upstream rescan are excluded and have no placeholder fields here.

## 2. Conventions

- Transport: HTTP/1.1 over the loopback interface only; JSON bodies, UTF-8.
- Timestamps: ISO-8601 UTC with an explicit `Z` suffix. Source timestamps are kept in
  the form the source supplies them and are never relabelled as Siddhi times.
- Identifiers: `project_id` is the source's opaque identifier, stored verbatim;
  `run_id` is a server-generated UUIDv4. Clients never choose either.
- Media type: `application/json`. Every response carries `X-Correlation-Id`.
- Unknown request fields are rejected as validation errors, not ignored.
- Cursors are opaque unpadded base64; clients must not construct or interpret them.

## 3. Interface surface

### 3.1 `POST /ingestion/vyasa/refresh` — refresh project inventory

No request body. Reads the configured Vyasa inventory to completion, then publishes it.

Response `200`:

```json
{
  "run_id": "3f0c1f8e-6b0a-4b5e-9c4a-1f0d2e3c4b5a",
  "source": "vyasa",
  "started_at": "2026-10-29T12:00:00Z",
  "finished_at": "2026-10-29T12:00:02Z",
  "outcome": "completed",
  "index_version": "11",
  "freshness": "current",
  "projects_total": 74,
  "counts": { "added": 74, "updated": 0, "removed": 0, "unchanged": 0 }
}
```

`counts.added` + `updated` + `removed` + `unchanged` describe the transition from the
previous current view to this one. `projects_total` is the number of projects in the
completed read and equals added + updated + unchanged. `index_version` and `freshness`
are the source's values, `null` when the source did not supply them; `index_version`
is normalized to text (the source may send a number).

Errors: `503 unavailable` with code `source_unavailable` when the source fails
(`details` carries `[{"run_id": ..., "failure": "<category>"}]`), or code
`source_not_configured` when no Vyasa executable is configured (`run_id: null`).
A failed refresh writes one failed run row and changes no project row.

### 3.2 `GET /projects` — list observed projects

Query parameters: `state` (`active` | `missing` | `inaccessible` | `all`, default
`all`), `limit` (1–100, default 25), `cursor` (opaque, from a previous response).

Response `200`:

```json
{
  "items": [
    {
      "project_id": "e620f8eda2274e9397a3f7430f22c012",
      "display_name": "Siddhi",
      "state": "active",
      "identity_status": "resolved",
      "providers": ["github"],
      "languages": ["Python"],
      "first_observed_at": "2026-10-29T12:00:00Z",
      "last_observed_at": "2026-10-29T12:00:00Z",
      "freshness": "current"
    }
  ],
  "next_cursor": null,
  "has_more": false
}
```

Ordering is `display_name` ascending, then `project_id` ascending as a stable
tie-break. An empty list means the current view is empty, not that Vyasa was read:
freshness and observation time on every item carry that context.

### 3.3 `GET /projects/{project_id}` — retrieve one observed project

Response `200` with the project object. Unknown identifier → `404 not_found` with code
`project_not_found`. The query reads the local store only; it never contacts Vyasa.

### 3.4 `GET /health` — diagnostics (changed)

The `integrations` check is replaced:

```json
"integrations": {
  "status": "configured",
  "source": "vyasa",
  "last_run": {
    "run_id": "3f0c1f8e-6b0a-4b5e-9c4a-1f0d2e3c4b5a",
    "outcome": "completed",
    "finished_at": "2026-10-29T12:00:02Z",
    "freshness": "current"
  }
}
```

`status` is `configured` when an executable is configured, `not_configured`
otherwise; `last_run` is `null` until one refresh exists. A failed last run is
reported here as `outcome: "failed"`. When the store itself cannot be read, this check
reports `status: "unavailable"` instead. Integration state never decides service
usability and no setting value, path, or source message appears in this payload.

## 4. Error model

The envelope and categories stay as fixed by `be-01-goal-and-persistence`:

```json
{
  "error": {
    "category": "unavailable",
    "code": "source_unavailable",
    "message": "the Vyasa source is unavailable",
    "field": null,
    "correlation_id": "8a2f...",
    "details": [{ "run_id": "3f0c...", "failure": "connection_failed" }]
  }
}
```

| Category | HTTP | Codes added here | Meaning |
|---|---|---|---|
| `validation` | 422 | `invalid_field` | Rejected query or cursor before any read |
| `not_found` | 404 | `project_not_found` | No stored project uses that identifier |
| `unavailable` | 503 | `source_unavailable`, `source_not_configured` | Vyasa could not supply inventory; local data unchanged |
| `internal` | 500 | `internal_error` | Unexpected failure; correlation id only |

Failure categories reported in `details[].failure` are `unavailable` (the source has
no usable index), `tool_error`, `unsupported_contract`, `protocol_error`, `timeout`,
`connection_failed`, and `not_configured`. Categories are additive; clients branch on
the error `category` and `code`, never on a source message.

## 5. Data model (schema version 2)

```sql
CREATE TABLE ingestion_runs (
    id            TEXT    PRIMARY KEY,
    source        TEXT    NOT NULL CHECK (source = 'vyasa'),
    started_at    TEXT    NOT NULL,
    finished_at   TEXT    NOT NULL,
    outcome       TEXT    NOT NULL CHECK (outcome IN ('completed', 'failed')),
    failure       TEXT,
    index_version TEXT,
    freshness     TEXT,
    projects_total INTEGER NOT NULL DEFAULT 0 CHECK (projects_total >= 0),
    added         INTEGER NOT NULL DEFAULT 0 CHECK (added >= 0),
    updated       INTEGER NOT NULL DEFAULT 0 CHECK (updated >= 0),
    removed       INTEGER NOT NULL DEFAULT 0 CHECK (removed >= 0),
    unchanged     INTEGER NOT NULL DEFAULT 0 CHECK (unchanged >= 0),
    CHECK ((outcome = 'completed' AND failure IS NULL)
        OR (outcome = 'failed' AND failure IS NOT NULL))
);

CREATE TABLE projects (
    project_id        TEXT PRIMARY KEY,
    display_name      TEXT NOT NULL,
    state             TEXT NOT NULL CHECK (state IN ('active', 'missing', 'inaccessible')),
    identity_status   TEXT NOT NULL,
    providers         TEXT NOT NULL,
    languages         TEXT NOT NULL,
    first_observed_at TEXT NOT NULL,
    last_observed_at  TEXT NOT NULL,
    last_run_id       TEXT NOT NULL REFERENCES ingestion_runs(id)
);

CREATE INDEX projects_by_name ON projects (display_name, project_id);
```

`providers` and `languages` are JSON arrays of strings. `identity_status` is stored as
the source's value without a CHECK: it is source vocabulary, not a Siddhi decision.

Invariants enforced in the write transaction, not by triggers:

- A completed refresh inserts its run row and its project changes in one transaction.
- A failed refresh inserts one run row with zero counts and does not touch `projects`.
- `projects` holds at most one row per `project_id`; an observed project updates
  in place, keeps `first_observed_at`, and takes the run's start time as
  `last_observed_at`.
- A project is removed only by a completed refresh whose read did not include it.
- `freshness` is the source's value copied unchanged; absent stays `null`.

## 6. Migration and compatibility

- Version 2 is additive: two new tables and one index. Goals, revisions and the
  schema ledger are untouched. A version-1 database gets a pre-migration copy in the
  existing way (`.bak` beside the store).
- A database at version 2 is refused by an application that only supports version 1;
  the existing fail-closed rule already covers this.
- The `/health` `integrations` block changes shape. No consumer exists in the
  repository; the change is additive for every other field.
- No down migration. Rollback means restoring the pre-migration copy.

## 7. Trust and disclosure boundary

- Vyasa answers are untrusted data. The adapter parses only named fields, rejects an
  unexpected contract version or missing required field, and never executes anything
  the source supplies.
- Only the configured executable path is machine-local configuration; it is never
  returned by an API, logged, or stored in a run row.
- Source messages and internal exception text are not stored or served; only a
  failure category is recorded.
- Project text (display names, providers, languages) is stored verbatim and returned
  as data. It is not interpreted as instructions and does not reach logs.
- Inventory reads are read-only; the adapter never triggers a Vyasa scan and never
  writes to Vyasa.
- Loopback binding remains the only access control in this slice.

## 8. Traceability

| Requirement | Operation | Contract section | Scenario |
|---|---|---|---|
| Refresh inventory explicitly | `POST /ingestion/vyasa/refresh` | 3.1 | Record a completed refresh; repeat unchanged |
| Preserve prior valid inventory | `POST /ingestion/vyasa/refresh`, `GET /projects` | 3.1, 3.2, 4 | Source unavailable; failure during paging |
| List and retrieve projects | `GET /projects`, `GET /projects/{id}` | 3.2, 3.3 | Page boundary; state filter; unknown identifier |
| Distinguish state, freshness, observation time | `GET /projects*` | 3.2, 3.3, 5 | Missing project; stale inventory |
| Remove only from a complete read | refresh | 3.1, 5 | Project absent from a complete read |
| Survive Vyasa failure | all project operations, `/health` | 3.1, 3.4, 4 | Not configured; unreachable source |
| Read-only interface and contract validation | adapter | 7, 4 | Unsupported version; tool error; repeated cursor |
| Replaceable adapter boundary | application port | 3.1, 5 | Test double supplies the observation |

## 9. Open contract questions

- Vyasa cursor stability across scans is not guaranteed; the adapter treats any
  repeated or non-advancing cursor as a failure rather than a loop.
- A future Vyasa state or `schema_version` fails the refresh until this contract is
  extended; it is never coerced into an existing state.
- Freshness policy (what makes inventory stale) belongs to Vyasa; Siddhi copies the
  reported value and does not compute its own threshold.
- Run-history retention has no limit in this slice.
