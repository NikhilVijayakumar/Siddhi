# Independent OKF evidence

- **Status:** Draft; NOT approved for implementation.
- **Owns:** FR-018, FR-019, FR-020, FR-021

## Scope and outcomes

| Baseline | Observable acceptance outcome |
|---|---|
| [FR-018](../functional-requirements.md#fr-018--inventory-engineering-knowledge) | Expose supported knowledge packages, metadata, concepts, decisions, links, references and declared validation status where available. |
| [FR-019](../functional-requirements.md#fr-019--assess-knowledge-availability) | Summarize available and missing/inaccessible/unlinked/stale/unsupported knowledge without equating availability with correctness or applicability. |
| [FR-020](../functional-requirements.md#fr-020--keep-knowledge-independent-of-requirements) | Discover and use knowledge without requirements and retain requirements without matching knowledge; relationships are not mandatory one-to-one mappings. |
| [FR-021](../functional-requirements.md#fr-021--preserve-knowledge-authority) | Routine reads and analysis leave authoritative OKF artifacts untouched. |

## Out of scope

Knowledge authoring, source-profile repair, automatic validation claims, correctness certification and forced requirement-to-concept mapping. Future publishing needs its own authorization and specification.

## Data and integration boundaries

OKF is the knowledge authority. Siddhi retains attributable projections of supported profile metadata, relationships and validation declarations, qualified by snapshot/revision and actual availability. Parsing or successful validation does not establish practical engineering fitness.

## NFR responsibilities

No NFR is owned here. Apply source-ingestion's schema, provenance and explicit-state responsibilities, security's read-only/untrusted-input controls and engineering-quality's profile fixtures.

## Cross-package dependencies

- [source-ingestion](../source-ingestion/requirement.md): capture and profile/version detection.
- [analysis](../analysis/requirement.md): criterion-specific relevance and qualified findings.
- [openspec-evidence](../openspec-evidence/requirement.md): optional links only; neither inventory requires the other.
- [security](../security/requirement.md): authorized paths and non-execution.

## Unresolved questions

Supported OKF profiles and extensions, concept identity across moves, stale thresholds, meaningful link checks and validation evidence coverage remain open. Recommended first release: goal-to-evidence report, NOT an approved release choice. See [grill log](grill-log.md).

## Acceptance drafts

Features are non-executable acceptance drafts. No runner or step definitions exist for them; inventory completeness is not semantic approval.

## Knowledge References

- `knowledge/architecture/okf-integration.md` — profile-aware independent knowledge.
- `knowledge/concepts/evidence-semantics.md` — availability, certainty and validation limits.
- `knowledge/architecture/data-ownership.md` — knowledge source authority.
- `knowledge/practices/knowledge-and-delivery-separation.md` — one-way delivery dependencies.