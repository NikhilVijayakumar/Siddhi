# Deterministic goal-to-evidence analysis

- **Status:** Draft; NOT approved for implementation.
- **Owns:** FR-026, FR-027, FR-028, FR-029, FR-030, NFR-017, NFR-018, NFR-020

## Scope and outcomes

| Baseline | Observable acceptance outcome |
|---|---|
| [FR-026](../functional-requirements.md#fr-026--compare-goals-with-existing-capabilities) | Compare declared outcomes and constraints with captured project, requirement, knowledge and other evidence using defined rules and recorded inputs. |
| [FR-027](../functional-requirements.md#fr-027--classify-findings) | Distinguish confirmed relationship, candidate match, identified gap, missing evidence, unresolved and stale/unavailable findings with explicit assessment basis. |
| [FR-028](../functional-requirements.md#fr-028--explain-analysis-results) | Each material finding exposes supporting sources/rules and assumptions or incomplete-data limitations. |
| [FR-029](../functional-requirements.md#fr-029--generate-reproducible-reports) | Generate reports with captured input versions, generation time and rule/report version; equivalent fixed inputs produce equivalent analytical findings. |
| [FR-030](../functional-requirements.md#fr-030--compare-historical-results) | Compare retained reports and distinguish changed evidence/portfolio inputs from changed rule interpretation. |

## Out of scope

Autonomous strategic approval, inferred absence from inaccessible sources, universal progress scores, hidden live-source refresh during analysis, AI as a routine dependency and final classification thresholds not yet agreed.

## Data and integration boundaries

Consume identified portfolio revisions and source snapshots rather than uncontrolled current repository contents. Findings retain rule/version, evidence references, limitations and processing context. Generation metadata may differ between runs without changing logical findings. Reports do not rewrite sources, historical reports or approved plans.

## NFR responsibilities

- [NFR-017](../non-functional-requirements.md#nfr-017--deterministic-processing): fixed normalized inputs, rule versions and configuration yield equivalent findings, independent of hidden ordering or wall-clock state.
- [NFR-018](../non-functional-requirements.md#nfr-018--analysis-provenance): preserve relevant source snapshots, portfolio state, rule/report versions and generation context.
- [NFR-020](../non-functional-requirements.md#nfr-020--historical-comparability): identify rule/schema changes and qualify comparisons rather than imply unqualified equivalence.

## Cross-package dependencies

- [portfolio](../portfolio/requirement.md) and [planning](../planning/requirement.md): owner outcomes, criteria and versioned context.
- [source-ingestion](../source-ingestion/requirement.md) and the evidence packages: captured inputs, freshness and native interpretation.
- [persistence-recovery](../persistence-recovery/requirement.md): retained report/input relationships.
- [external-analysis](../external-analysis/requirement.md): bounded advisory handoff, not deterministic finding authority.
- [api-operations](../api-operations/requirement.md): report access and operation outcomes.

## Unresolved questions

Initial rule library, confirmation sufficiency, conflict handling, final category vocabulary, reference-time policy, report format and retained reproduction inputs require decisions. Recommended first release: goal-to-evidence report, NOT an approved release choice. See [grill log](grill-log.md).

## Acceptance drafts

Features are non-executable acceptance drafts, with no runner or step definitions. Equivalent findings, not byte-identical run metadata, are the proposed determinism comparison.

## Knowledge References

- `knowledge/architecture/deterministic-analysis.md` — fixed inputs and versioned rules.
- `knowledge/concepts/evidence-semantics.md` — scoped gaps, unknowns and certainty.
- `knowledge/architecture/ingestion-and-snapshots.md` — available captured input history.
- `knowledge/architecture/data-model.md` — findings and report lineage.
- `knowledge/practices/testing-and-validation.md` — deterministic and failure fixtures.
- `knowledge/practices/knowledge-and-delivery-separation.md` — draft rules require review.