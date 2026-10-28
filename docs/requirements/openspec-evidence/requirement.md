# OpenSpec evidence

- **Status:** Draft; NOT approved for implementation.
- **Owns:** FR-014, FR-015, FR-016, FR-017

## Scope and outcomes

| Baseline | Observable acceptance outcome |
|---|---|
| [FR-014](../functional-requirements.md#fr-014--inventory-requirements-and-development-artifacts) | Expose requirements, scenarios, changes, tasks and declared statuses available under explicitly supported schemas. |
| [FR-015](../functional-requirements.md#fr-015--summarize-declared-development-progress) | Summarize declared progress with artifact references, separately from independent implementation or verification evidence. |
| [FR-016](../functional-requirements.md#fr-016--identify-missing-or-incomplete-requirement-evidence) | Report schema-supported missing references and incomplete workflows with an explicit basis and scoped applicability. |
| [FR-017](../functional-requirements.md#fr-017--preserve-source-authority) | Routine ingestion and analysis leave authoritative requirements, tasks, schemas and change artifacts unchanged. |

## Out of scope

Authoring or repairing OpenSpec, treating task completion as delivery proof, assuming every repository uses this repository's schema, and mandating every artifact in every project.

## Data and integration boundaries

Retain artifact identity, supported schema/version, declared status, source location and snapshot/revision when available. Inventory and interpretation consume source-ingestion outputs; evidence does not grant write authority or approve Siddhi requirements.

## NFR responsibilities

No NFR is owned here. Apply source-ingestion's schema/provenance/source-authority responsibilities, security's read-only boundaries and engineering-quality's controlled format fixtures.

## Cross-package dependencies

- [source-ingestion](../source-ingestion/requirement.md): supported format detection and qualified snapshot capture.
- [analysis](../analysis/requirement.md): assessed findings using declarations without inflating them to verification.
- [git-evidence](../git-evidence/requirement.md): separately attributed implementation and verification observations.
- [security](../security/requirement.md): non-mutating authorized reads.

## Unresolved questions

Deep review 2026-10-29 records a recommendation for all eight questions: initial support limited to this repository's `backend` schema, native identifiers as artifact identity, and completeness checks limited to what the schema declares (see [grill log](grill-log.md)). A recorded recommendation is not an owner approval; recommended first release: goal-to-evidence report, NOT an approved release choice.

## Acceptance drafts

Non-executable acceptance drafts only; no runner or step definitions. Structural scenario coverage neither approves behavior nor establishes a working OpenSpec adapter.

## Knowledge References

- `knowledge/architecture/openspec-integration.md` — schema-aware development declarations.
- `knowledge/architecture/source-adapters.md` — format/access boundaries.
- `knowledge/concepts/evidence-semantics.md` — declared versus verified status.
- `knowledge/practices/knowledge-and-delivery-separation.md` — delivery authority and drafts.