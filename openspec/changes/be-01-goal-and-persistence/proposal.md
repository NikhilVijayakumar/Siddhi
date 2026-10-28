# Change Proposal: Independent goals on a versioned local database

## Why

Siddhi's requirement baseline is draft and no product capability is implemented. The
recommended first slice is "establish safe local persistence/access and create an
independent goal" (`docs/requirements/README.md`). Choosing a later slice first would
force goal, revision and source records into an unversioned database and make every
later change a migration of undecided data. This change establishes the smallest
observable product behavior — an owner can create, read, revise and archive a goal that
owes nothing to a discovered project — on a database that identifies its own schema
version.

## What Changes

- **fun-01-portfolio-goals**: goal creation without a project, retrieval and bounded
  listing, revision history, archival without deletion, explicit unknown values, and
  validated atomic writes.
- **tech-02-local-database-baseline**: schema version reporting, controlled forward
  migrations that fail closed, loopback-only startup with safe diagnostics, and
  machine-local configuration.

## Scope and constraints

In scope: FR-001, FR-002, FR-005, FR-043, FR-044, FR-046, FR-047, FR-048, FR-049,
FR-050 and the quality constraints NFR-001, NFR-007, NFR-013, NFR-014, NFR-015,
NFR-016, NFR-021, NFR-022, NFR-026, NFR-033, NFR-037, NFR-040, NFR-042, NFR-043.

Out of scope: any source adapter (Vyasa, OpenSpec, OKF, Git), analysis and findings,
planning and reviews, external analysis handoff, project association, authentication
beyond local binding, and provider automation. Goal-to-project association is
deliberately deferred to the change that delivers source ingestion.

Constraints: the served behavior is HTTP only; portfolio rules stay server-side
(`knowledge/decisions/ui-independent-http-boundary.md`); storage is local SQLite
(`knowledge/decisions/local-first-sqlite.md`); no new architectural decision is
introduced (see `adr.md`).

## Requirement source

`docs/requirements/portfolio/requirement.md` (FR-001, FR-002, FR-005, FR-006),
`docs/requirements/api-operations/requirement.md` (FR-043, FR-044, FR-046),
`docs/requirements/persistence-recovery/requirement.md` (FR-047, FR-048, FR-050),
`docs/requirements/security/requirement.md` (FR-049).

The requirement packages remain draft. FR-006 history and the portfolio package's deep
review carry recorded recommendations, not owner approval. This change adopts those
recommendations for a draft specification and records its own open questions; merging
it does not approve the baseline or the release scope.

## Knowledge References

- `knowledge/architecture/data-model.md` — stable identifiers, revision context, and relationship invariants.
- `knowledge/architecture/persistence.md` — transactions, schema evolution, and backups.
- `knowledge/architecture/data-ownership.md` — portfolio-owned records versus source projections.
- `knowledge/architecture/api-boundary.md` — the HTTP boundary independent clients build against.
- `knowledge/architecture/configuration-and-secrets.md` — machine-local settings separated from portable data.
- `knowledge/architecture/security-and-privacy.md` — local binding, least privilege, safe diagnostics.
- `knowledge/decisions/local-first-sqlite.md`, `knowledge/decisions/python-fastapi-backend.md`,
  `knowledge/decisions/modular-monolith.md`, `knowledge/decisions/ui-independent-http-boundary.md`.
- `knowledge/practices/vertical-slices.md` — one observable behavior per implementation slice.
- `knowledge/practices/testing-and-validation.md` — executed evidence versus documented intent.

## Traceability

- Change ID: `be-01-goal-and-persistence`
- Branch: `feature/be-01-goal-and-persistence`
- Capability specifications: `specs/fun-01-portfolio-goals/spec.md`, `specs/tech-02-local-database-baseline/spec.md`
- Roadmap: delivery step 1 of `docs/requirements/README.md`; not an approved release scope.
- Risks: SQLite write contention under future ingestion load; premature API stability
  expectations; draft requirements treated as approved. Mitigations: single-writer
  transactions with a busy timeout, an explicit pre-1.0 compatibility statement, and
  draft labels retained on every requirement reference.
- Acceptance: every in-scope requirement traced to a scenario and an executed check;
  structural document checks reported separately from executed test results.
