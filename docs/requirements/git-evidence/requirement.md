# Git and verification evidence

- **Status:** Draft; NOT approved for implementation.
- **Owns:** FR-022, FR-023, FR-024, FR-025

## Scope and outcomes

| Baseline | Observable acceptance outcome |
|---|---|
| [FR-022](../functional-requirements.md#fr-022--collect-available-revision-evidence) | Retrieve supported commit, branch, tag, timestamp and changed-path observations within the access mechanism's actual capabilities. |
| [FR-023](../functional-requirements.md#fr-023--distinguish-activity-from-achievement) | Report activity as supporting evidence without presenting counts, recent commits or branch existence as successful delivery. |
| [FR-024](../functional-requirements.md#fr-024--represent-verification-evidence) | Retain supported test/build/release artifacts with available source, revision and time; missing data remains unknown/unavailable. |
| [FR-025](../functional-requirements.md#fr-025--read-without-modifying-repositories) | Routine refresh and analysis leave contents, checked-out branch, commits and published plans unchanged. |

## Out of scope

Running repository tests as part of ingestion, source mutation, automatic checkout/commit/publication, universal productivity scores, assumed provider support and interpreting a tag as proof of deployment.

## Data and integration boundaries

Keep exact observed revision and source/access scope where available. Local/shallow history is not automatically complete remote history. Verification artifact outcomes retain their own revision applicability and provenance. Git observations do not own portfolio achievement or approvals.

## NFR responsibilities

No NFR is owned here. Apply source-ingestion's provenance and source-state rules, security's controlled read-only access and engineering-quality's bounded Git/verification fixtures.

## Cross-package dependencies

- [source-ingestion](../source-ingestion/requirement.md): repository references, snapshot capture and coverage.
- [openspec-evidence](../openspec-evidence/requirement.md): independently attributed development declarations.
- [analysis](../analysis/requirement.md): criterion-specific interpretation, never activity-only proof.
- [security](../security/requirement.md): no execution of repository-defined commands or hooks.

## Unresolved questions

Deep review 2026-10-29 leaves one owner decision: which verification artifact formats are accepted first, closed by one real test or CI result sample; no format is accepted initially. The other seven questions carry recorded recommendations, including local-only read-only collection, exact revisions with a coverage flag, and separately attributed verification evidence (see [grill log](grill-log.md)). A recorded recommendation is not an owner approval; the goal-to-evidence report remains a recommended first-release target, NOT an approved release choice.

## Acceptance drafts

Features are non-executable acceptance drafts, with no runner or step definitions. No repository integration is claimed verified by their presence.

## Knowledge References

- `knowledge/architecture/git-evidence.md` — bounded non-mutating revision observation.
- `knowledge/concepts/evidence-semantics.md` — activity versus achievement and verification.
- `knowledge/architecture/source-adapters.md` — access capability declarations.
- `knowledge/practices/knowledge-and-delivery-separation.md` — draft evidence policy.