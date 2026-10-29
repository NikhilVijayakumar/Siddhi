# Change Proposal: Vyasa project evidence

## Why

Siddhi stores a Vyasa project inventory, but it cannot yet retrieve the checkout-level
evidence that a stored project already observed (remote, languages, markers, frameworks,
per-checkout status and observation time). Goal-to-project relationships and later
goal-to-evidence comparisons need that evidence, and without it they would either invent
project identities or read the source outside the agreed adapter boundary.

## What Changes

- **fun-03-project-evidence**: a targeted read returns one known project's checkout-level
  evidence through the source port; the read fails explicitly when the source cannot supply
  it.
- **tech-03-vyasa-mcp-adapter**: the read-only adapter adds a `get_project` tool call to the
  existing bounded stdio session, with the same schema-version validation and failure
  categories as the inventory read.

## Scope

In scope: targeted retrieval of one project by its source identifier, evidence shape
validation, failure categories, the per-project evidence HTTP read, and the adapter/test
contract.

Out of scope and deferred: storing checkout evidence in SQLite, goal-to-project
relationship storage and links, deleted-versus-moved reconciliation, content-hash
incremental processing, upstream rescans, authentication, and provider automation.

## Affected interfaces and data

- HTTP: `GET /projects/{project_id}/evidence`.
- Source adapter: `tools/call` with `name: get_project`.
- Stored data: no migration; the published inventory from this change is unchanged, and the
  targeted read is served without publishing.

## Compatibility and migration

No database migration and no change to existing operations. Existing inventory reads keep
their contract.

## Risks

- The `get_project` answer may be partial; field-level availability must stay explicit rather
  than flattened into a full checkout list.
- The source may not expose targeted retrieval; the capability check must keep the
  unsupported case distinct from an empty success.

## Roadmap phase

Delivery order step 2 continuation of source ingestion (verify the actual Vyasa contract and
capture project inventory), before portfolio relationships and deterministic comparison.

## Knowledge References

- `knowledge/architecture/vyasa-integration.md` — inventory authority, observed MCP surface,
  logical information groups.
- `knowledge/architecture/source-adapters.md` — retrieval capability and read-only trust
  boundary.
- `knowledge/technologies/vyasa-contract-direction.md` — observed field shapes and open
  guarantees.
- `knowledge/architecture/ingestion-and-snapshots.md` — run, freshness and last-known-good.
- `knowledge/concepts/evidence-semantics.md` — observation dimensions and absence handling.

## Open decisions

- Whether checkout evidence is stored per project or served from the source on demand. The
  proposal keeps this slice read-side and records the storage decision for a later change.
- Owner approval status: the requirement packages remain drafts; this change records the draft
  decision, not an approval (`docs/requirements/README.md`).
