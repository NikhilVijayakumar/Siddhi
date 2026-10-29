# Design: Vyasa project evidence

## Context

The Vyasa inventory change (`be-02-vyasa-project-inventory`) delivered an explicit refresh
that reads the source to completion, publishes project summaries, and serves them. Its
deferred scope named checkout-level evidence (remotes, markers, frameworks, per-checkout
status and observation time).

The observed source surface already includes `get_project` as a read-only tool that returns
one project's identity, aliases, checkouts with remote status, languages, markers and
frameworks, with per-group `status` and `observed_at`.

## Decision

This change adds targeted retrieval (`get_project`) on top of the existing stdio adapter
session and exposes it through `GET /projects/{project_id}/evidence`.

- The source port gains `get_project(project_id) -> dict`; the adapter keeps one process per
  retrieval and reuses the bounded session, handshake, message cap and timeout.
- The adapter validates the answer: `schema_version` must be `"1"`, the returned
  `project_id` must equal the requested identifier, required identity fields must be usable.
- The application shapes the evidence response from the validated answer and maps failures to
  the existing source error vocabulary; targeted reads do not write run rows.
- Storage of checkout evidence is deliberately deferred; the published inventory stays the
  stored current view.

## Consequences

- Reads of evidence are source-backed and freshness-labelled, not cached in this change.
- Unsupported capabilities fail loudly rather than behaving like an empty success.
- Failure semantics match the inventory change, so a failed evidence read reuses the
  `unavailable` / source category mapping without inventing categories.

## Alternatives considered

- Fetch details during refresh: rejected, because refresh is a bounded complete read and
  per-project detail fan-out changes its cost and failure shape.
- Store evidence during refresh: deferred to a later change, kept out of this vertical slice.

## Risks

- Partial source answers: optional fields may be absent; the response keeps their absence
  explicit. Exact semantics of `status`/`observed_at` during partial reads remain open.
