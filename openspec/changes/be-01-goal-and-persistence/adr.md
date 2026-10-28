# Architecture Decision Record: Goal and local database baseline

## 1. Decision Status

- **Status:** Not Required
- **Date:** 2026-10-29
- **OpenSpec Change ID:** `be-01-goal-and-persistence`
- **Decision owners:** project owner (draft authors; no approval recorded)
- **Related artifacts:** `proposal.md`, `design.md`, `specs/`

## 2. Decision Checkpoint

- [ ] **New decision required:** This change introduces or alters a significant architectural decision.
- [x] **Existing decision applies:** An existing ADR governs this decision.
- [x] **No new ADR required:** The change does not introduce a significant architectural decision.

### Rationale

Both boxes are checked because the two questions are separate: every architectural
question this change actually touches is already decided, and nothing durable is left
open.

- Storage is local SQLite: `knowledge/decisions/local-first-sqlite.md`.
- The service is a Python/FastAPI modular monolith:
  `knowledge/decisions/python-fastapi-backend.md`,
  `knowledge/decisions/modular-monolith.md`.
- Clients consume HTTP only, with rules server-side:
  `knowledge/decisions/ui-independent-http-boundary.md`.
- Ownership of portfolio records versus source projections:
  `knowledge/architecture/data-ownership.md`.

The choices this change does make are applications of that established architecture,
not new architectural commitments:

- Append-only goal revisions with a current-state projection follow
  `knowledge/architecture/data-model.md` (stable identifiers, revision context) and
  `knowledge/architecture/persistence.md` (transaction and schema-evolution rules).
- Ordered SQL migrations with a recorded schema version are the mechanism those
  documents already prescribe; the alternative is an ORM-owned schema, which would add
  a dependency and hide the upgrade order.
- Optimistic concurrency with `expected_revision` and keyset pagination are local
  interface decisions with no cross-cutting consequence, recorded in `design.md` §5 and
  `api-contract.md`.

If a second entity adopts the same append-only revision pattern, that convention becomes
a general data-model rule and should be promoted to a `Decision` concept in
`knowledge/decisions/` rather than copied per change.

## 3. Deferred decisions

These are deliberately not decided here and are not implied by this change:

- Local authentication and origin policy (`security` grill Q5).
- Pre-1.0 API compatibility policy and binding performance targets
  (`api-operations` grill Q8, `engineering-quality` grill Q2).
- Backup frequency, recovery targets and retention (`persistence-recovery` grill Q2, Q4).

Each needs owner input; none blocks schema version 1 or the goal operations.
