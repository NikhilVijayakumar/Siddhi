# Engineering quality and verifiable delivery

- **Status:** Draft; NOT approved for implementation.
- **Owns:** NFR-004, NFR-028, NFR-032, NFR-033, NFR-034, NFR-035, NFR-036, NFR-038

## Scope and outcomes

This NFR-only package owns the quality approach supporting product packages, not new functional capabilities. Acceptance distinguishes documented intent, structural checks and executed tests.

## Out of scope

Invented coverage percentages, unmeasured hard resource limits, mandatory distributed infrastructure, routine private-production dependencies, live AI prerequisites and claims that draft Gherkin is executable evidence.

## Data and integration boundaries

Use controlled source fixtures and replaceable external systems rather than private production repositories. Keep transport, application, domain, parsing, persistence, analysis, reporting and external reasoning responsibilities separate. Architectural rationale remains durable knowledge; package acceptance references it without copying delivery obligations into knowledge. No additional runtime architecture is selected here.

## NFR responsibilities and testable outcomes

| Owned baseline | Observable acceptance outcome |
|---|---|
| [NFR-004](../non-functional-requirements.md#nfr-004--resource-efficiency) | Measure representative workstation memory/storage and deterministic workloads without requiring dedicated servers, distributed databases, GPUs or AI; hard budgets await agreement. |
| [NFR-028](../non-functional-requirements.md#nfr-028--separation-of-concerns) | Test clear responsibility boundaries without making domain rules depend on source formats, HTTP or UI state. |
| [NFR-032](../non-functional-requirements.md#nfr-032--explicit-architectural-decisions) | Significant choices retain context, alternatives and consequences; ordinary changes explain when no new ADR is needed. |
| [NFR-033](../non-functional-requirements.md#nfr-033--controlled-dependencies) | Dependencies have purpose and appropriate constraints, with changes validated by tests rather than unnecessary frameworks. |
| [NFR-034](../non-functional-requirements.md#nfr-034--automated-test-coverage) | Automated tests cover critical domain/API/parser/persistence/migration/analysis/error behavior; percentages are not the sole quality measure. |
| [NFR-035](../non-functional-requirements.md#nfr-035--reproducible-test-fixtures) | Reproducible supported-version, malformed, missing-metadata, stale and conflicting fixtures work without private repositories or AI services. |
| [NFR-036](../non-functional-requirements.md#nfr-036--integration-isolation) | Test doubles isolate external systems and contract tests exercise documented integration interfaces. |
| [NFR-038](../non-functional-requirements.md#nfr-038--failure-path-testing) | Failure tests cover interruption, outage, invalid input, transaction failure, external timeout and retry behavior. |

## Cross-package dependencies

All product packages define observable behavior and supply risk-focused acceptance examples. [source-ingestion](../source-ingestion/requirement.md) supplies real supported-format contracts; [api-operations](../api-operations/requirement.md) supplies HTTP/operation contracts; [persistence-recovery](../persistence-recovery/requirement.md) owns migration validation NFR-037; [security](../security/requirement.md) owns security coverage NFR-039. This package coordinates quality without reallocating those specialized responsibilities.

## Unresolved questions

Deep review 2026-10-29 leaves one owner decision: the reference workstation and workload used for resource and latency measurements. The other seven questions carry recorded recommendations, including real versioned fixtures without private repositories, offline routine tests with separately invoked contract checks, critical-behavior coverage before any percentage, and a pinned Python 3.12/FastAPI/pytest stack with no Gherkin runner (see [grill log](grill-log.md)). A recorded recommendation is not an owner approval; the goal-to-evidence report remains a recommended first-release target, NOT an approved release choice.

## Acceptance drafts

The feature is a non-executable acceptance draft. No runner or step definitions are supplied. It describes future quality evidence, not tests already passed by the application.

## Knowledge References

- `knowledge/practices/testing-and-validation.md` — risk-focused layers and controlled fixtures.
- `knowledge/practices/vertical-slices.md` — reviewable behavior-oriented delivery.
- `knowledge/architecture/system-architecture.md` — responsibility boundaries.
- `knowledge/product/scope-and-roadmap.md` — proportionate initial scope.
- `knowledge/practices/knowledge-and-delivery-separation.md` — intent versus implementation evidence.