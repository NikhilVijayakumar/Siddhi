# Architecture Decision Record: Vyasa project evidence

- **Status:** Proposed (recorded in the change; durable decision recorded under review)
- **Context:** The Vyasa adapter (`be-02-vyasa-project-inventory`) reads inventory pages but
  not per-project evidence; goal-to-project relationships and goal-to-evidence comparisons need
  checkout-level observations that later slices would otherwise invent.

## Decision

The targeted project evidence read (`get_project`) is served by the source adapter through a
bounded stdio session and exposed read-only over `GET /projects/{project_id}/evidence`;
checkout evidence is not stored in this change.

## Consequences

- Evidence reads are fresh source reads with the source's freshness context; no stale cache.
- The adapter must handle the unsupported capability case without conflating it with success.
- A later change owns storage of checkout evidence and goal-to-project mappings.

## Options considered

1. Fetch details during refresh — rejected for cost and failure-shape reasons.
2. Serve on demand from the source — chosen here; storage deferred.

## Decision outcome

Accepted for this change; the storage and relationship options remain open for later changes.

## No new ADR needed

None required beyond this change-level decision record: the storage split is a deferred scope
decision rather than a long-lived architectural commitment.
