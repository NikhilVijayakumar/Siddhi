# Change Proposal: Vyasa project inventory

## Why

Siddhi owns portfolio intent but has no inventory to attach it to. The requirement
baseline places source discovery and snapshot ingestion second in the delivery order,
and its only owner decision — which real Vyasa interface is supported first — was
closed by inspecting the local deployment read-only on 2026-10-29: a stdio MCP server
with read-only inventory tools (`docs/requirements/source-ingestion/requirement.md`).

Without this change, every later slice (goal-to-project relationships, evidence,
analysis) would invent a project identity or read Vyasa directly from unrelated code.
This change establishes the smallest observable inventory: an explicit refresh reads
the agreed Vyasa tools, stores what was observed with its source identifiers and
observation time, and serves it locally while keeping prior valid data when Vyasa is
unavailable. Requirement adoption here is a draft decision, not approval
(`docs/requirements/README.md`, `knowledge/practices/knowledge-and-delivery-separation.md`).

## What Changes

- **fun-02-project-inventory**: an explicit refresh of Vyasa inventory; a current
  project list and single-project read over HTTP; runs that record outcome, change
  counts, freshness and failure; prior valid inventory preserved on failure.
- **tech-03-vyasa-mcp-adapter**: a read-only Vyasa MCP adapter — one local stdio
  process per refresh, bounded paging, `schema_version` validation, and explicit
  failure categories — behind an application port that a test double can replace.

## Scope

In scope: project summaries (native identifier, display name, state, identity status,
providers, languages), ingestion run outcomes and counts, freshness context, current
project view, bounded listing and retrieval, health reporting of integration state.

Out of scope and deferred to later slices: checkout-level evidence (remotes, markers,
frameworks, per-checkout observation times), goal-to-project relationships, deleted
vs. moved project reconciliation, content-hash incremental processing (FR-013),
partial publication of a failed read, upstream rescan, authentication, and any
provider or synchronization automation.

## Affected interfaces and data

- HTTP: `POST /ingestion/vyasa/refresh`, `GET /projects`, `GET /projects/{id}`,
  and the `integrations` block of `/health`.
- Stored data: schema version 2 adds `ingestion_runs` and `projects`.
- Configuration: one machine-local executable setting for the Vyasa MCP server; the
  service still starts and serves goals when Vyasa is not configured or unreachable.
- Dependencies: none added. The adapter speaks the MCP stdio transport with the
  standard library (`knowledge/decisions/source-adapter-boundaries.md`).

## Compatibility and migration

Migration 002 is additive and forward-only; existing goals and revisions are
untouched. Databases at version 2 are refused by the current application if it
predates this change (existing fail-closed rule). No HTTP contract in use changes.

## Risks

- Vyasa's observed surface is one deployment and one index version. A schema,
  protocol or vocabulary change must fail the refresh explicitly rather than be
  coerced (`knowledge/technologies/vyasa-contract-direction.md`).
- A project that disappears from a completed read is removed from the current view;
  `missing` and `inaccessible` are source states, not deletions. The run ledger keeps
  the last observation time but not a full historical projection.
- A spawned process per refresh is the simplest correct transport; concurrency and
  process reuse can wait until refresh cost is measurable
  (`knowledge/decisions/proportionate-background-execution.md`).

## Roadmap phase

Delivery order step 2, "Verify the actual Vyasa contract and capture project
inventory" (`docs/requirements/README.md`).

## Knowledge References

- `knowledge/architecture/vyasa-integration.md` — inventory authority, observed MCP surface.
- `knowledge/technologies/vyasa-contract-direction.md` — verified fields and open guarantees.
- `knowledge/architecture/source-adapters.md` — adapter boundary and failure categories.
- `knowledge/architecture/ingestion-and-snapshots.md` — run, publication and last-known-good.
- `knowledge/architecture/data-ownership.md` — source facts versus Siddhi projections.
- `knowledge/concepts/evidence-semantics.md` — observation, absence and freshness.
- `knowledge/architecture/persistence.md` — versioned migrations.
- `knowledge/practices/vertical-slices.md` — slice boundaries.

## Open decisions

- Local authentication and origin policy (`docs/requirements/security/grill-log.md` Q5).
- Pre-1.0 compatibility policy (`docs/requirements/api-operations/grill-log.md` Q8).
- Reference workload and refresh cost targets (`docs/requirements/engineering-quality/grill-log.md` Q2).
- Source retention and recovery targets — not needed by this slice, but they govern
  how long run history is kept (`docs/requirements/persistence-recovery/grill-log.md` Q2, Q4).
