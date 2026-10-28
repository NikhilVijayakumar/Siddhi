---
type: Practice
title: Layered testing and truthful validation
description: Unit, contract, integration, persistence, security, recovery, and workflow tests with explicit evidence limits.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Layered testing and truthful validation

Tests establish observed behavior under recorded conditions, not universal
correctness. This is a proposed practice, not evidence that a suite, pipeline,
HTTP schema, desktop automation, or release gate currently exists.

# Keep claims separate

Parsing establishes readability; schema validation establishes structural fit;
connection checks establish access under specific conditions. None proves source
truth, completeness, freshness, or successful implementation of a declared claim.
Deterministic analysis establishes application of a rule, not strategic correctness.
Model advice is neither verification nor approval.

Preserve failed, not evaluated, unknown, incomplete, stale, conflicting, inferred,
and unsupported states where meaningful. Missing evidence is not automatic pass
or fail. A narrowly passing check does not confirm an entire goal.

# Test layers

| Layer | Exercise | Avoid substituting |
|---|---|---|
| Unit | Domain invariants, transitions, transformations, typed errors, rules | Mock counts for meaningful results |
| Application | Authorized use cases with fake ports, duplicate/conflict handling | HTTP-only checks for core invariants |
| Contract | API shape/semantics and adapter capabilities | Schema validation alone for runtime behavior |
| Integration | Real repository, adapter, parser, credential boundaries | Fakes as evidence of actual dependencies |
| Persistence | Constraints, transactions, migrations, backup/restoration | Initialization as upgrade proof |
| Security | Allowed/denied access, hostile inputs, leakage, scope | Happy paths as authorization assurance |
| Recovery | Interruption, locks, disk/permission failure, restart | Restart alone as recovery proof |
| End-to-end | Few high-value capture-to-review/report workflows | UI automation for all lower-level coverage |

Use test-first Red–Green–Refactor where practical: demonstrate focused failure,
add the smallest coherent behavior, improve structure with checks still green.
Test observable effects/invariants rather than internal method layout.

# Fixtures and reproducibility

Use temporary databases, controlled local roots, fake credentials, and synthetic
metadata. Ordinary checks do not need production data, live keys, or modifications
to user settings. Label optional platform/live checks and report unavailability.

Cover complete, empty, partial, stale, duplicate, conflicting, unsupported-version,
malformed, missing-field, unknown-field, renamed/deleted, denied, oversized,
deeply nested, and hostile-instruction cases. Important fixtures explain format,
scenario, intentional scope, expected result, and assumptions. One fixture does
not establish support for all versions/workflow variants.

Use small golden datasets for normalization, evidence classes, findings, and
report summaries. Review differences before updating expectations. Compare
substantive deterministic results separately from variable execution timestamps.
Fix inputs, rule versions, and relevant settings.

# API, ports, and ownership

When transport exists, test valid/invalid bodies, methods, content types, IDs,
dates, enums, paging, limits, error codes, response models, authorization, and safe
serialization. Review schema and semantic compatibility. Client generation does
not prove server conformance.

Application tests show disabled sources stay untouched, transitions cannot bypass
approval, source-owned fields remain read-oriented, duplicate actions are controlled,
conflicting revisions are rejected, and outages do not erase history. Test the
invariant through multiple entry points where bypass is plausible.

Adapter contracts cover actual supported schemas, native identity, bounded scans,
completeness/freshness declarations, retries, partial failures, unknown metadata,
and read-only effects. Do not assume universal source conventions. Git observations
and declared task status do not automatically establish achieved outcomes.

# Persistence and recovery

Exercise fresh creation, per-connection foreign keys, uniqueness, stable IDs,
commit/rollback, revisions, atomic pointer updates, staging/publication isolation,
and checkpoints advancing only with committed data. Inject failures around
critical commits and publication boundaries.

Test supported prior schema paths with representative historical data, including
skipped releases where supported, interruption, ledger tampering, semantic
preservation, and newer unsupported stores. Migration success alone does not
prove preserved meaning.

Create consistent backups under supported journal/writer conditions, restore in
isolation, and validate schema, relationships, provenance, history, and application
behavior. Include corrupt/incompatible backups, disk-full, denied permissions,
contention, bounded retries, and interrupted jobs. Confirm failed refreshes retain
the usable view and retries do not duplicate records.

# Analysis and advisory outputs

Rules need positive, negative, boundary, missing, stale, conflicting, unsupported,
and not-evaluable cases. Goal mappings require explicit relations or explained
inference; keywords alone are not proof. Historical comparisons distinguish
changed evidence, portfolio revisions, rules, and assessments.

Provider tests verify minimal approved context, policy/model/template identity,
timeouts/retries, limits, response structure, unknown references, contradictions,
and unjustified certainty. Hostile content cannot authorize execution, disclosure,
approval, or policy updates. Provider failure leaves deterministic work usable.
Quality evaluations use explicit grounding, uncertainty, relevance, and policy
criteria, not claims of guaranteed behavior across models and provider updates.

# Security, diagnostics, and performance

Use synthetic secret markers to inspect responses, logs, exceptions, reports,
bundles, and provider payloads. Test backend authorization, loopback defaults,
narrow origins, traversal/symlink escape, read-only effects, network destination
boundaries, safe rendering, resource limits, and unauthorized setting updates.

Test health/readiness separation, optional degradation, stale check timestamps,
execution versus findings, concurrent correlation, logging failure, and absence
of false completion after persistence failure.

Performance evidence records dataset, workload, hardware/software, concurrency,
latency distribution, memory, growth, and recovery time. No numeric target is
assumed. Interactive impressions or one timing sample establish no guarantee.

# Workflow and release evidence

A high-value workflow configures a synthetic source, ingests, inspects coverage
and provenance, selects a goal, runs analysis, reviews findings, creates a report,
changes the source, refreshes, and compares history. Include stale/partial data.
Add client automation only when a client exists.

Run fast unit/contract checks frequently and required integration/security checks
at justified gates. Classify extended tests by cost without hiding missing coverage.
Do not rerun flaky checks until green; investigate, fix, or explicitly quarantine
without counting them as passing.

Record method, scope, environment, tool/rule version, time, result, and limitations.
Failed, skipped, unavailable, and unverified checks differ. Release evidence covers
supported upgrades, tested restore, reproducible analysis, security negatives,
contract/dependency review, and accepted risks. A checklist or readable scenario
is not an executable test by itself.

Related: [vertical slices](vertical-slices.md), [API boundary](../architecture/api-boundary.md),
[persistence](../architecture/persistence.md), [security](../architecture/security-and-privacy.md),
[observability](../architecture/observability.md).