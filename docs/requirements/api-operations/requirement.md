# API contracts and operational visibility

- **Status:** Draft; NOT approved for implementation.
- **Owns:** FR-043, FR-044, FR-045, FR-046, NFR-001, NFR-002, NFR-030, NFR-040, NFR-041, NFR-042, NFR-043, NFR-044, NFR-048, NFR-050, NFR-051, NFR-052, NFR-053

## Scope and outcomes

| Baseline | Observable acceptance outcome |
|---|---|
| [FR-043](../functional-requirements.md#fr-043--expose-documented-api-operations) | Implemented capabilities have documented HTTP operations with validated request/response schemas usable by an independent frontend and contract tests. |
| [FR-044](../functional-requirements.md#fr-044--validate-requests) | Invalid requests produce consistent validation errors; validation or transactional failure does not leave unintended partial changes. |
| [FR-045](../functional-requirements.md#fr-045--expose-operation-status) | Long refresh/analysis operations expose progress or final status through an agreed mechanism chosen for measured workload and failures. |
| [FR-046](../functional-requirements.md#fr-046--provide-diagnostics) | Availability, database and integration diagnostics identify operational problems without exposing secrets or sensitive source content. |

## Out of scope

Invented endpoint paths/status codes, fixed transport error schema, predetermined queue/broker, unconditional cancellation guarantees, desktop packaging and frontend business-rule duplication.

## Data and integration boundaries

HTTP validates and serializes application operations; portfolio rules remain UI-independent. Operational identifiers connect diagnostics to runs without copying private payloads. Application availability, database accessibility and remote integration readiness are distinguishable observations. Persistence-recovery owns underlying transaction and service lifecycle safety; this package owns their observable API contract and reporting.

## NFR responsibilities

| Owned baseline | Responsibility |
|---|---|
| [NFR-001](../non-functional-requirements.md#nfr-001--api-responsiveness) | Measure representative local response latency; P95 reads 500 ms, writes 1 s and usual health 200 ms remain proposed, not approved commitments. |
| [NFR-002](../non-functional-requirements.md#nfr-002--long-running-operations) | Keep routine API access responsive during expensive operations. |
| [NFR-030](../non-functional-requirements.md#nfr-030--ui-independence) | Domain and analysis do not depend on React, Electron or presentation state. |
| [NFR-040](../non-functional-requirements.md#nfr-040--api-documentation) | Public schemas, validation and errors are documented; generate OpenAPI from actual implementation. |
| [NFR-041](../non-functional-requirements.md#nfr-041--contract-stability) | Manage breaking changes with an explicit compatibility/versioning policy. |
| [NFR-042](../non-functional-requirements.md#nfr-042--consistent-errors) | Distinguish validation, missing resource, conflict, unavailable integration and internal failures without secret leakage. |
| [NFR-043](../non-functional-requirements.md#nfr-043--pagination-and-bounded-responses) | Bound growing collections and return appropriate summaries/references instead of indiscriminate large payloads. |
| [NFR-044](../non-functional-requirements.md#nfr-044--operation-lifecycle) | Define status, completion, failure and safe retry; cancellation only where integrity can be maintained. |
| [NFR-048](../non-functional-requirements.md#nfr-048--frontend-integration-readiness) | Support the separate desktop client through a stable interface without duplicating portfolio rules. |
| [NFR-050](../non-functional-requirements.md#nfr-050--structured-operational-logging) | Provide structured operation/correlation context without unnecessary sensitive content. |
| [NFR-051](../non-functional-requirements.md#nfr-051--refresh-and-job-reporting) | Report refresh/analysis outcomes, warnings, unsupported sources and partial failures. |
| [NFR-052](../non-functional-requirements.md#nfr-052--health-checks) | Separate basic local availability from database and integration diagnostics where appropriate. |
| [NFR-053](../non-functional-requirements.md#nfr-053--actionable-error-reporting) | Identify the failed operation with safe actionable context; never execute diagnostic input. |

## Cross-package dependencies

- [portfolio](../portfolio/requirement.md), [planning](../planning/requirement.md), [analysis](../analysis/requirement.md): application capabilities exposed, not reimplemented in transport.
- [source-ingestion](../source-ingestion/requirement.md): qualified refresh outcomes.
- [persistence-recovery](../persistence-recovery/requirement.md): transactions, startup/shutdown and interrupted work.
- [security](../security/requirement.md): local exposure policy, client access and redaction.
- [engineering-quality](../engineering-quality/requirement.md): contract and failure-path tests.

## Unresolved questions

Synchronous/background split, execution model, lifecycle/cancellation/retry contract, errors, pagination and compatibility strategy, client access and benchmark environment remain open. Recommended first release: goal-to-evidence report, NOT an approved release choice. See [grill log](grill-log.md).

## Acceptance drafts

Features are non-executable acceptance drafts, with no runner or step definitions. Numerical targets are baseline proposals requiring representative measurements and review.

## Knowledge References

- `knowledge/architecture/api-boundary.md` — independent HTTP/application boundary.
- `knowledge/architecture/observability.md` — safe actionable diagnostic context.
- `knowledge/architecture/workflow-coordination.md` — operation tracking and proportionate execution.
- `knowledge/architecture/system-architecture.md` — UI-independent responsibilities.
- `knowledge/practices/testing-and-validation.md` — contract and workload checks.
- `knowledge/practices/knowledge-and-delivery-separation.md` — unresolved quantitative targets.