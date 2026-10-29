# Interface and data contract: Vyasa project evidence

- **OpenSpec Change ID:** `be-03-vyasa-project-evidence`
- **Proposing team:** be (backend team)
- **Related proposal:** `proposal.md`
- **Related specifications:** `specs/fun-03-project-evidence/spec.md`, `specs/tech-03-vyasa-mcp-adapter/spec.md`
- **Related design:** `design.md`
- **Related ADR:** `adr.md`

## 1. Purpose and scope

Adds the targeted evidence read on top of the inventory change: one stored project, one
source retrieval, checkout-level evidence back to the caller. Checkout evidence is served
for this change; storing it per project is deferred.

## 2. Conventions

- Transport: HTTP/1.1 over the loopback interface only; JSON bodies, UTF-8.
- Timestamps: ISO-8601 UTC with an explicit `Z` suffix. Source timestamps are kept in the
  form the source supplies them and are never relabelled as Siddhi times.
- Identifiers: `project_id` is the source's opaque identifier, stored verbatim;
  `run_id` is a server-generated UUIDv4. Clients never choose either.
- Media type: `application/json`. Every response carries `X-Correlation-Id`.
- Unknown request fields are rejected as validation errors, not ignored.

## 3. Interface surface

### 3.1 `GET /projects/{project_id}/evidence` — retrieve project evidence

Reads the stored project first (unknown identifier → `404 not_found` / `project_not_found`),
then asks the configured source for that project's checkout-level evidence.

Response `200`:

```json
{
  "project_id": "e620f8eda2274e9397a3f7430f22c012",
  "freshness": "current",
  "checkouts": [
    {
      "remote": "https://github.com/owner/repo",
      "status": "clean",
      "observed_at": "2026-10-29T12:00:00Z"
    }
  ],
  "languages": ["Python"],
  "markers": ["implementation:complete"],
  "frameworks": ["fastapi"]
}
```

- `checkouts` is the source's list of checkout observations; each entry carries what the
  source supplied (for example `remote`, `status`, `observed_at`). An absent optional field
  is absent, not zero and not an error; the caller distinguishes an empty list from a missing
  optional group only through the presence of the key.
- Optional groups absent from the source stay absent from the response rather than becoming
  empty defaults. Missing required identity fields are a source failure.

Errors: `503 unavailable` with code `source_unavailable` when the source fails or cannot
retrieve the project; the source's failure category is carried in `details` as
`[{"run_id": null, "failure": "<category>"}]`. No run row is written for a targeted read.

### 3.2 Errors (unchanged plus this read)

The error model and categories are those of the inventory change; this read adds no new
category and uses the `unavailable` / `not_found` codes already fixed there.

## 4. Error model

Unchanged from the inventory contract; a targeted evidence read reuses `source_unavailable`
with a null run id and never exposes a source message.

## 5. Data model

No new tables. Targeted evidence reads are served without publishing; the published
inventory from the inventory change remains the stored current view.

## 6. Migration and compatibility

No migration. No change to existing operations, storage, or response payloads.

## 7. Trust and disclosure boundary

- The source answer is untrusted; the adapter validates the schema version and the project
  identity before returning evidence.
- Only the configured executable path is machine-local configuration and never surfaces in
  responses, logs, or run rows.
- Source messages never reach responses or logs; only a failure category is recorded.
- Loopback binding plus the cross-site guard of the inventory change cover the new read.

## 8. Traceability

| Requirement | Operation | Contract section | Scenario |
|---|---|---|---|
| Retrieve checkout-level evidence | `GET /projects/{id}/evidence` | 3.1 | Stored project; source failure; unsupported capability |

## 9. Open contract questions

- Whether the source's per-checkout `status`/`observed_at` mean the same thing during partial
  reads is still open from the inventory change; this contract does not reinterpret it.
- Storage of checkout evidence as a separate observation remains a later change.
