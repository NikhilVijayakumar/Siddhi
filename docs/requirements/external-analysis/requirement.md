# Optional external analysis and investigation

- **Status:** Draft; NOT approved for implementation.
- **Owns:** FR-038, FR-039, FR-040, FR-041, FR-042, NFR-019, NFR-024

## Scope and outcomes

| Baseline | Observable acceptance outcome |
|---|---|
| [FR-038](../functional-requirements.md#fr-038--prepare-analysis-briefs) | Assemble a purpose-specific brief with goals, context, selected evidence, constraints, gaps, assumptions and judgment questions, excluding unnecessary private content. |
| [FR-039](../functional-requirements.md#fr-039--import-external-analysis) | Import structured external results with origin and available model/tool, time, input references, assumptions, recommendations and uncertainty. |
| [FR-040](../functional-requirements.md#fr-040--validate-external-results) | Identify invalid/incomplete structures and unsupported references while keeping even valid imports advisory. |
| [FR-041](../functional-requirements.md#fr-041--approve-recommendations-explicitly) | Record owner acceptance, rejection, deferral or further-investigation decisions without automatic priority changes or repository publication. |
| [FR-042](../functional-requirements.md#fr-042--support-deeper-repository-investigation) | Request an authorized, question-focused coding-agent investigation and validate its structured return without making routine processing depend on it. |

## Out of scope

Default provider automation, model selection, secret-sharing, autonomous plan approval, executing imported commands and granting unrestricted repository access. Manual structured handoff is a recommendation, not an approved transport choice.

## Data and integration boundaries

Export only the authorized minimal context. Preserve selected portfolio/snapshot versions, purpose and disclosure scope. Imported outputs are untrusted advisory records, not normalized source facts. Unavailable origin metadata remains unavailable. Investigation return passes validation before becoming usable evidence; receiving it does not authorize actions.

## NFR responsibilities

- [NFR-019](../non-functional-requirements.md#nfr-019--separation-of-deterministic-and-ai-generated-results): keep model-generated recommendations distinguishable from deterministic findings, even after valid import.
- [NFR-024](../non-functional-requirements.md#nfr-024--external-data-sharing): require an explicitly authorized disclosure workflow and minimize sensitive repository, creative and strategic content.

## Cross-package dependencies

- [analysis](../analysis/requirement.md): deterministic findings and input references.
- [portfolio](../portfolio/requirement.md) and [planning](../planning/requirement.md): separately controlled consequential revisions.
- [security](../security/requirement.md): disclosure, credentials and untrusted-content controls.
- [api-operations](../api-operations/requirement.md): import validation errors and conditional operation tracking.
- [persistence-recovery](../persistence-recovery/requirement.md): advisory and decision history.

## Unresolved questions

Deep review 2026-10-29 leaves one owner decision: what may leave the local machine in a brief, and to whom. A minimal default payload and a preview step are recommended, but disclosure needs explicit authorization. The other seven questions carry recorded recommendations, including manual handoff before any provider automation and a versioned result envelope (see [grill log](grill-log.md)). A recorded recommendation is not an owner approval; the goal-to-evidence report remains a recommended first-release target, NOT an approved release choice.

## Acceptance drafts

Features are non-executable acceptance drafts, with no runner or step definitions. No provider or coding-agent integration is claimed available.

## Knowledge References

- `knowledge/architecture/external-analysis.md` — bounded advisory handoff.
- `knowledge/concepts/evidence-semantics.md` — recommendation versus fact and decision.
- `knowledge/architecture/security-and-privacy.md` — explicit disclosure authorization.
- `knowledge/architecture/workflow-coordination.md` — review and authorized consequential operations.
- `knowledge/practices/knowledge-and-delivery-separation.md` — unapproved alternatives stay visible.