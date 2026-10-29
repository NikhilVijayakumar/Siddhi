---
type: Technology
title: Vyasa contract direction and uncertainty
description: Intended inventory role, the partially verified local MCP surface, and the guarantees that remain open.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Vyasa contract direction and uncertainty

The local integration direction names Vyasa as the project and repository inventory
source. That remains an authority boundary rather than a promise that every Vyasa
deployment exposes the same interface.

**Partially verified on 2026-10-29.** One local Vyasa deployment was read only: an
MCP server over stdio with read-only tools answering from a local index. Its
inventory tools, response envelope, identifier shape, state vocabulary, and
freshness values were observed and are recorded in
[Vyasa inventory integration](../architecture/vyasa-integration.md). One deployment
and one index version are not evidence of general compatibility, and nothing was
executed against Vyasa beyond read-only tool calls.

# Desired consumer information, not upstream field claims

The consumer would benefit from stable project/repository identities, repository
origins and permitted locations, technology classifications, engineering-artifact
indicators, source scan times, coverage, errors, pagination, and provenance.

The observed summary answer supplies stable-looking project identifiers, display
names, project state, identity status, providers, languages, and page cursors.
Repository origins, checkout locations, marker and framework detail, per-group
observation times, and completeness status appear only in the single-project
answer; scan coverage and history remain outside the inventory read.

Source scan time differs from the time inventory is retrieved. Read-only retrieval
is confirmed; requesting a targeted refresh or initiating workspace discovery is
not, and none is assumed.

# Contract inspection questions

| Area | Verified on 2026-10-29 | Still open |
|---|---|---|
| Access | Local stdio MCP process; read-only tools | Authentication, permissions, and non-local deployment |
| Identity | 32-hex `project_id`, `identity_status` of resolved/provisional/ambiguous | Scope, stability, and rename/transfer/clone behavior |
| Shape | `schema_version` `"1"` envelope, summary and detail fields, JSON error object | Versioning policy and unknown-field behavior |
| Inventory scope | Filters, `limit`/`next_cursor`/`has_more`, states active/missing/inaccessible | Cursor stability guarantees and visibility restrictions |
| Discovery quality | `meta.freshness` current/stale/partial/unknown, latest run with counts | Per-field basis and completeness of a partial scan |
| Refresh | None; tools never rescan | Selected-project reads, targeted rescan, scan lifecycle |
| Incremental/history | Opaque cursors only | Deletion semantics, historical observations |
| Failure | `isError` with `unavailable` and `internal_error` codes | Rate limits, retries, timeouts, partial records |

The adapter exposes a stable logical result while preserving those differences.
Unsupported and unavailable stay explicit; an empty record list alone cannot prove
there are no projects. There is no basis to choose direct database coupling,
promise fields, or implement a second scanner to hide missing capabilities.

Related: [Vyasa architecture](../architecture/vyasa-integration.md),
[source adapters](../architecture/source-adapters.md), [technology index](index.md).
