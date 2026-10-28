# Portfolio intent

- **Status:** Draft; NOT approved for implementation.
- **Owns:** FR-001, FR-002, FR-004, FR-005, FR-006, FR-037

## Scope and outcomes

Maintain owner-defined outcomes independently of source inventory. These are concise refinements of the draft baseline, not a replacement or approval of it.

| Baseline | Observable acceptance outcome |
|---|---|
| [FR-001](../functional-requirements.md#fr-001--define-goals) | Create, retrieve, revise and archive a goal with stable identity before associating any repository. |
| [FR-002](../functional-requirements.md#fr-002--represent-different-types-of-outcomes) | Record software, creative, research and internal-investment outcomes without imposing identical lifecycle or maturity criteria. |
| [FR-004](../functional-requirements.md#fr-004--link-projects-to-portfolio-goals) | Associate goals or initiatives with discovered projects while retaining association basis and approval state; inferred candidates remain unconfirmed. |
| [FR-005](../functional-requirements.md#fr-005--record-priorities-and-constraints) | Retrieve entered priorities, dates, constraints and assumptions with missing values still identifiable as unknown. |
| [FR-006](../functional-requirements.md#fr-006--preserve-portfolio-history) | Explain meaningful portfolio changes through prior state, change time and rationale when supplied. |
| [FR-037](../functional-requirements.md#fr-037--avoid-mandatory-time-logging) | Use portfolio workflows without manual hours; absent execution evidence remains visible. |

## Out of scope

Competing project inventory, automatic strategic approval, mandatory time tracking and universal progress scores. Initiative and plan behavior belongs to planning.

## Data and integration boundaries

Siddhi owns goal revisions, constraints and relationship approval, not Vyasa project identities. Source references arrive through source-ingestion; analysis proposes relationships without approving them. Historical goal references must remain explainable after archival.

## NFR responsibilities

No NFR is owned here. Apply persistence-recovery's integrity/history controls, security's access controls and engineering-quality's domain tests without reallocating their ownership.

## Cross-package dependencies

- [source-ingestion](../source-ingestion/requirement.md): discovered project references.
- [planning](../planning/requirement.md): initiatives, plan and review revisions; portfolio owns FR-006's cross-entity traceability obligation.
- [analysis](../analysis/requirement.md): candidate basis and limitations, never implicit approval.
- [persistence-recovery](../persistence-recovery/requirement.md): durable revision relationships.

## Unresolved questions

Deep review 2026-10-29 records a recommendation for all eight questions, including the minimum creation field set, priority representation, association approval and achievement confirmation (see the [desk-review questions](grill-log.md)). A recorded recommendation is not an owner approval, and the goal-to-evidence report remains a recommended first-release target, NOT an approved release choice.

## Acceptance drafts

The feature documents are non-executable acceptance drafts. No runner or step definitions are supplied, and structural validation is not evidence of implemented behavior.

## Knowledge References

- `knowledge/product/vision.md` — outcomes rather than activity accounting.
- `knowledge/concepts/portfolio-domain.md` — goals, initiatives and relationships.
- `knowledge/architecture/data-ownership.md` — owner records versus source projections.
- `knowledge/architecture/data-model.md` — stable references and revision context.
- `knowledge/practices/knowledge-and-delivery-separation.md` — draft intent is not approval.