# Source discovery and snapshot ingestion

- **Status:** Draft; NOT approved for implementation.
- **Owns:** FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, NFR-003, NFR-005, NFR-006, NFR-008, NFR-009, NFR-011, NFR-012, NFR-013, NFR-016, NFR-029, NFR-031

## Scope and outcomes

| Baseline | Observable acceptance outcome |
|---|---|
| [FR-007](../functional-requirements.md#fr-007--discover-projects) | Retrieve Vyasa inventory through an agreed interface and retain source identifiers without competing project identities. |
| [FR-008](../functional-requirements.md#fr-008--identify-supported-source-artifacts) | Identify supported artifacts with absence distinguished from inability to inspect. |
| [FR-009](../functional-requirements.md#fr-009--parse-supported-formats) | Parse verified supported layouts and formats; explicitly report malformed input and unsupported versions. |
| [FR-010](../functional-requirements.md#fr-010--normalize-source-information) | Query normalized records with original source/revision references and unchanged source meaning and authority. |
| [FR-011](../functional-requirements.md#fr-011--refresh-source-data) | Explicitly refresh selected sources, compare snapshots, retain additions/modifications/removals/unchanged records and record time, outcome and partial failures. |
| [FR-012](../functional-requirements.md#fr-012--track-source-freshness-and-failures) | Expose freshness and failure states without replacing valid prior data with incomplete results. |
| [FR-013](../functional-requirements.md#fr-013--support-incremental-processing) | Reuse unchanged content when reliable revision/hash evidence permits, while remaining correct with unreliable metadata. |

## Out of scope

Invented Vyasa endpoints, arbitrary repository execution, automatic source repair, mandatory remote cloning, and settled partial-publication or retention policy. Source-specific interpretation belongs to the evidence packages.

## Data and integration boundaries

Adapters preserve native identity, supported schema/version, observed revision, source timestamps where available, ingestion time and access limitations. Siddhi owns normalized projections, snapshots and run outcomes, not authoritative source records. Inaccessible scope cannot establish removal. A retained partial observation is not automatically a new complete current view.

## NFR responsibilities

| Owned baseline | Responsibility |
|---|---|
| [NFR-003](../non-functional-requirements.md#nfr-003--incremental-processing) | Avoid unnecessary reparsing only when identity/revision evidence is reliable. |
| [NFR-005](../non-functional-requirements.md#nfr-005--failure-isolation) | Isolate source failures and qualify partial outcomes. |
| [NFR-006](../non-functional-requirements.md#nfr-006--preservation-of-valid-data) | Preserve last-known valid snapshots on incomplete refresh. |
| [NFR-008](../non-functional-requirements.md#nfr-008--idempotent-operations) | Unchanged retries do not duplicate logical source or portfolio records. |
| [NFR-009](../non-functional-requirements.md#nfr-009--graceful-degradation) | Keep locally satisfiable operations usable during source or optional AI outages. |
| [NFR-011](../non-functional-requirements.md#nfr-011--source-provenance) | Retain available origin, revision/snapshot and ingestion context. |
| [NFR-012](../non-functional-requirements.md#nfr-012--source-authority) | No silent mutation of authoritative source data. |
| [NFR-013](../non-functional-requirements.md#nfr-013--explicit-data-states) | Distinguish current, stale, unavailable, never retrieved, unsupported, invalid/partial and unresolved states as applicable. |
| [NFR-016](../non-functional-requirements.md#nfr-016--time-and-revision-semantics) | Separate source event/modification, ingestion and analysis times; never fabricate unavailable times. |
| [NFR-029](../non-functional-requirements.md#nfr-029--replaceable-adapters) | Replace an integration behind its contract without rewriting portfolio rules. |
| [NFR-031](../non-functional-requirements.md#nfr-031--schema-aware-parsing) | Explicit format/version detection prevents fallback to incompatible assumptions. |

## Cross-package dependencies

- [openspec-evidence](../openspec-evidence/requirement.md), [okf-evidence](../okf-evidence/requirement.md), [git-evidence](../git-evidence/requirement.md): native evidence interpretation.
- [persistence-recovery](../persistence-recovery/requirement.md): transactional publication and retained history.
- [api-operations](../api-operations/requirement.md): refresh status, bounded results and diagnostics.
- [security](../security/requirement.md): authorized roots, credentials and read-only access.
- [analysis](../analysis/requirement.md): frozen input snapshots and explicit uncertainty.

## Unresolved questions

Real Vyasa contract, supported OpenSpec/OKF versions and layouts, access methods, identity after moves, freshness thresholds, publication unit and interrupted-refresh retry/resume remain open. Recommended first release: goal-to-evidence report; NOT an approved release choice. See [grill log](grill-log.md).

## Acceptance drafts

Features are non-executable acceptance drafts, with no runner or step definitions. Their source and failure fixtures must be agreed before executable verification.

## Knowledge References

- `knowledge/architecture/source-adapters.md` — replaceable native adapters.
- `knowledge/architecture/vyasa-integration.md` — inventory authority and unknown contract.
- `knowledge/architecture/ingestion-and-snapshots.md` — attempts, publication and last-known-good state.
- `knowledge/architecture/data-ownership.md` — source versus projection ownership.
- `knowledge/concepts/evidence-semantics.md` — absence and freshness distinctions.
- `knowledge/practices/knowledge-and-delivery-separation.md` — unapproved interface choices.