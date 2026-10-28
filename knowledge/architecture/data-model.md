---
type: Architecture
title: Logical data model
description: Proposed portfolio, source, evidence, analysis, and governance records with explicit identity, time, revision, and provenance semantics.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Logical data model

This is a proposed logical organization, not a finalized relational schema,
serialization contract, or declaration of implemented tables. It preserves
source authority, observations, assessments, recommendations, decisions, and
historical context as distinguishable information. The corresponding meanings
are explained in [portfolio domain](../concepts/portfolio-domain.md).

# Record groups

| Group | Logical records | Key information |
|---|---|---|
| Portfolio | Goal, intended outcome, initiative, project reference, priority, constraint, assumption | Stable identity, purpose, declared state, criteria, scope, rationale, authorship, effective dates |
| Planning and governance | Plan, revision, milestone, dependency, review, decision/history | Scope, predecessor, approval, targets, selected context, responsible authority |
| Source integration | Source system, artifact reference, ingestion run, snapshot, normalized record | Source-scoped identity, locators, captured revision, coverage, processing/transform versions |
| Evidence and assessment | Evidence record, criterion, assessment, evidence-to-scope association | Observation, provenance, applicability, method, support/uncertainty, assessed context |
| Analysis and reporting | Analysis run, finding, report | Input set, rule/configuration version, outcome, explanations, limitations, generated artifact |
| External reasoning | Request/brief, returned result, recommendation | Authorized scope, provider/model when known, template version, parsing/review state, rationale |
| Operations | Refresh job, processing error, quality observation | Requested scope, child runs, stage outcomes, safe diagnostics, recovery and resolution state |

These groups need not correspond one-to-one with tables, packages, or services.
Use the simplest physical structure that preserves the necessary distinctions.

# Portfolio associations

Goals may have several outcomes with qualitative or quantitative criteria.
Measurement definitions can carry baseline, target, unit, and target date; material
changes need version context. A declared goal state is not evidence of achievement.

Many-to-many associations connect goals to initiatives and initiatives to project
references. Direct project-to-goal associations are also proposed so a lightweight
path need not introduce an initiative. Associations can carry rationale, provenance,
state, and effective dates. Initiative completion does not automatically determine
goal achievement.

Priorities can be ordered ranks or richer owner-controlled assessments rather
than one universal scoring formula. Constraints and assumptions retain scope,
origin, validity, and review state; an assumption can be validated or invalidated
without silently becoming a source fact.

# Source identity and observations

A source system identifies adapter type/version and configuration references,
not embedded secrets. A source artifact retains source-system context, stable
external identity when available, artifact type, locators, first/last observation,
and availability. A local project reference points to that identity and its
applicable metadata observation.

Names and paths are mutable attributes. A content hash can detect byte changes
but is neither permanent source identity nor proof of semantic equivalence.
When stable external IDs are absent, record a documented composite strategy and
unresolved matches instead of merging lookalike names automatically.

An ingestion run is a bounded attempt with scope, times, adapter version, counts,
and outcome. A snapshot identifies source artifact or defined source scope,
ingestion context, observation time, revision/hash when known, capture outcome,
format version, and payload or payload reference. A valid empty scope differs
from an unavailable or partial observation.

Normalized records identify input snapshot and transformation version. Variable
source payloads can use structured storage while identities, provenance, and
lifecycle remain queryable. Payload storage can be separated from snapshot
metadata without changing snapshot identity.

# Evidence and assessment

Evidence retains claim/observation, type, observed and recorded times, source and
snapshot references, derivation method/version, and limitations. Derived evidence
can have several input observations. Substantive corrections need a replacement
or correction relationship rather than unexplained historical mutation; exact
immutability and erasure policy remains open.

A criterion defines applicable scope, evaluation method, rule version, needed
inputs, and applicability conditions. An assessment identifies its scope,
criterion version, analysis context, time, result, rationale, and predecessor
where relevant. Evidence-to-scope relationships allow reuse without asserting
that the same observation is sufficient for every linked outcome.

Supported, partially supported, contradicted, insufficient, not assessed,
conflicting, and stale are useful method-specific results, not universal lifecycle
states. Keep certainty, sufficiency, freshness, and execution independent as
explained in [evidence semantics](../concepts/evidence-semantics.md).

# Analysis and external reasoning

An analysis run records scope, selected source snapshots and portfolio context,
rule/configuration versions, processing times, outcome, warnings, and errors.
Findings retain classification, explanation, relevant criterion/evidence,
limitations, and search coverage for missing-information claims. Reports retain
run identity, generation/version context, content reference, and freshness summary.

An external request or exported brief records purpose, selected inputs, authorized
disclosure scope, template version, provider/model metadata when available, and
request state. The received result preserves origin, structure, parsing version,
limitations, and review state. Full sensitive prompts/responses need not be kept
when non-sensitive provenance is sufficient and policy forbids unnecessary copying.

A recommendation identifies its origin, affected scope, rationale, supporting
evidence, uncertainty, time, and review state. Acceptance links to an explicit
decision; a changed plan is not evidence that acceptance occurred.

# Plans, revisions, and decisions

A plan has stable identity and scope. A revision records predecessor, content,
revision identifier, creator, time, change summary, and rationale. Proposed,
approved, and active revisions are not interchangeable. Creating a draft does
not advance the approved pointer.

Milestones have criteria, target dates, dependencies, status declarations, and
evidence relationships. The historical attachment of milestones is unresolved:
linking only to a mutable plan cannot by itself reconstruct what an earlier
approved revision promised. Options include revision-owned milestones or stable
milestone identities with revision-specific values and membership.

A review identifies the exact report, evidence, and plan revision examined.
Decisions record issue, choice, authority, approval state, time, rationale, and
superseding context. Whether history uses immutable decision events or explicit
revision records is a physical design choice; silent loss of prior reasoning is not.

# Integrity, temporal meaning, and lifecycle

- Validate typed references and permitted relationship targets. Avoid unconstrained
  polymorphic links when explicit associations can enforce stronger integrity.
- Reject self-dependencies and detect cycles where a dependency type requires a DAG.
- Distinguish observed time, recorded time, processing time, effective time, and
  decision time, using consistent timezone-aware representations.
- Preserve source context and transformation versions through provenance links,
  not only embedded prose. Shared observations can support multiple findings.
- Separate current editable records, meaningful revisions, captured observations,
  append-only processing history, and superseded reports.
- Archival changes active visibility, not referential validity. Deleting a draft
  or link does not automatically delete independent evidence or external sources.
- A failed stage does not erase independently completed observations. Which staged
  captures become current depends on the explicit publication boundary.
- A schema migration changes storage; a new criterion or rule may change meaning.
  Preserve that distinction and version compatibility metadata.

Relational records are proposed for core identities and associations, with
structured payloads for source-specific shapes and a data-access boundary around
SQLite. The frontend does not directly access the store. Exact identifiers, ORM,
indexes, payload representation, history depth, and transaction mapping remain open.

# Unresolved modeling choices

Clarify goal-versus-intention semantics and mandatory outcomes, direct association
policy, milestone revision membership, observation correction/immutability,
which entities need full history, snapshot payload strategy, universal versus
method-specific result vocabularies, source identity fallback, approval roles,
custom states, privacy erasure, and minimum retained input for reproducibility.
Historical direction does not settle these into approved schemas.

Related: [data ownership](data-ownership.md),
[source history and provenance](../decisions/source-history-and-provenance.md),
[versioned history and migrations](../decisions/versioned-history-and-migrations.md).