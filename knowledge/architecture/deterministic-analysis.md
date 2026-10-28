---
type: Architecture
title: Deterministic portfolio analysis
description: Frozen input resolution, explicit versioned rules, evidence sufficiency, finding reconciliation, and reproducible reports.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Deterministic portfolio analysis

Deterministic analysis evaluates portfolio records and captured evidence through
explicit rules. It is the baseline for routine comparisons, coverage checks,
freshness, dependency inspection, and reports. Equivalent normalized inputs,
rules, configuration, and reference time yield equivalent logical findings.
That property neither proves source truth nor establishes strategic judgment.

A finding is an observation or rule-derived conclusion. A recommendation proposes
an action; an approved decision records a choice. Analysis preserves these
boundaries and does not automatically change source records, plans, priorities,
acceptance criteria, or approvals. No LLM is needed for routine evaluation.

# Architecture and input resolution

The proposed module consumes portfolio revisions and normalized evidence through
an input resolver, applies focused rules, persists findings, and renders reports.
Ordinary functions and explicit configuration are preferable to an elaborate
general-purpose rule platform before the workload justifies one. A separate service
or distributed computation is not implied by the logical rule boundary.

The resolver freezes entity scope, source snapshots, plan/decision revisions,
rule set, configuration, reference date/time, and known limitations before execution.
Historical runs do not silently substitute newer sources. Rules consume declared
inputs rather than reading arbitrary files, accessing uncontrolled wall-clock time,
calling models, or depending on unstable iteration order.

A run logically identifies type, scope, start/end time, snapshot and portfolio
revision references, rule/engine versions, configuration revision, reference time,
execution outcome, findings, errors, and limitations. Execution time differs from
the period represented by the evidence. Generated run IDs and recording timestamps
can differ without changing logical result equivalence.

Succeeded, partial, failed, and cancelled describe execution, not portfolio health.
A successful run can find missing evidence. Missing prerequisites produce a
not-evaluable outcome, not a fabricated finding or a successful empty result.
Independent noncritical rules can fail without blocking unrelated rules.

# Rule families

| Family | Typical question | Necessary qualification |
|---|---|---|
| Portfolio integrity | Missing outcomes, unresolved mappings or entity references? | Some exploratory relationships are intentionally optional |
| Evidence coverage/quality | Are expected sources available and applicable? | Scope and association can be insufficient |
| Source freshness/operations | Old publication, failed refresh, interrupted capture? | Freshness is not truth |
| Plan/milestone consistency | Dates passed, criteria missing, plan revisions changed? | Recorded status is not verified outcome |
| Dependencies | Unresolved links, downstream impact, prohibited cycles? | Not every graph type forbids cycles |
| Cross-source consistency | Comparable claims disagree? | Check identity, revision, environment, period, and authority |
| Goal criteria | Explicit measurable conditions satisfied? | Judgment-intensive conditions remain unresolved |
| Historical comparison | Inputs, rules, plans, or findings changed? | Disappearing finding need not mean resolution |

Each rule identifies purpose, stable ID/version, applicable entities, required
fields/coverage, evaluation logic, output types, severity/classification, exclusions,
limitations, and validation examples. Thresholds and policy choices are explicit
versioned inputs, not invented defaults.

# Evidence state and quality

Expected evidence can be present, not found within a sufficiently inspected scope,
inaccessible, uncollected, partial, ambiguously associated, or not defined by the
assessment criteria. These are not one present/absent flag. No evidence found does
not establish implementation failure or global absence.

Claim-specific categories can include confirmed, candidate, missing, unknown, stale,
conflicting, and unverified. They do not replace source statuses, and the final
universal versus method-specific vocabulary remains open. Separate provenance,
identity, freshness, coverage, verification, consistency, and relevance dimensions
are more informative than an opaque confidence score. Numerical confidence needs
a justified calibrated method, not model wording or invented precision.

Source declarations, direct observations, deterministic derivations, independent
verification, and uncertainty remain distinct. A task marker is not a passing
test; a passing test applies to its revision/scope, not every linked business claim.
See [evidence semantics](../concepts/evidence-semantics.md).

# Freshness, plans, and dependencies

Freshness can use last ingestion/publication, source revision, trustworthy source
times, expiry/review dates, applicable verification age, and failed refreshes.
Thresholds differ by source and question. A failed scan retains prior history with
current-access qualifications; it is not proof of no records.

Milestone checks can identify elapsed due dates, changed dates, unresolved
dependencies, or missing completion evidence under defined criteria. Date rules
fix timezone, inclusivity, reference date, authoritative plan revision, and excluded
states such as cancelled work. An overdue date does not alone imply project failure.
Plan comparison preserves additions/removals, dependencies, statuses, criteria,
scope, and outcomes without assuming every revision is improvement or regression.

Dependency rules distinguish declared and inferred relationships. Cycle checks
apply only where a relationship policy prohibits cycles; knowledge references may
legitimately be cyclic. Recorded dependency information can target invalidation
and downstream review instead of rerunning every analysis on any source change.

# Authority-aware consistency and goal assessment

Compare only claims about the same entity, applicable revision, environment, and
period. Inventory reporting an artifact and an inaccessible artifact store are
different observations, not automatically a contradiction. A recent source is not
automatically more authoritative than an older one. Record conflict and its basis
without overwriting native declarations.

Goal-specific acceptance criteria govern sufficiency. A document plus review,
revision-specific tests, an approved milestone record, or an applicable verification
artifact can support different goal claims. Keep criterion outcomes passed, failed,
and not-evaluable distinguishable. Reuse value, creative quality, investment merit,
and context-sensitive architecture fitness may require human judgment; the engine
can assemble relevant evidence without pretending to decide them objectively.

No universal progress formula follows from commits, changed lines, document count,
task markers, milestones, or repository count. Descriptive activity measures need
their scope and cannot stand in for strategic value. Declared goal lifecycle,
evidence coverage, computed criterion results, and human-approved outcome decisions
are separate state dimensions.

# Findings and historical comparison

A finding logically records ID/reconciliation basis, rule/version, run, category,
affected entities, explanation, severity, classification, evidence/snapshots,
scope, first/last observation, limitations, and supersession/resolution context.
Severity derives from explicit policy, not simply record count. Findings do not
automatically become alerts; notification policy is a different concern.

Reruns distinguish new, persistent, changed, unsupported, not-reassessable, and
rule-changed findings. A missing finding can reflect changed coverage, scope,
prerequisites, or rule version, not resolution. Comparing new rules against old
fixed inputs separates changed interpretation from changed portfolio evidence.
Recorded dependency references can identify which assessments need review when
supporting inputs change.

Persisted reports identify run/scope, reference date, source snapshots, portfolio
and plan revisions, rule/configuration versions, grouped findings, evidence,
limitations, failed/skipped rules, and comparable historical differences. Rendering
an old report does not recompute it against today's sources. Pruned inputs require
an honest incomplete-reproduction statement rather than an allegedly exact reconstruction.

# External handoff, security, and performance

Selected findings and relevant evidence can inform a bounded strategic question,
with goals, constraints, assumptions, conflicts, and missing information explicitly
included. Imported recommendations retain request/context/model origin, uncertainty,
and review state separately from deterministic findings. See
[external analysis](external-analysis.md).

Analysis uses authorized snapshots and untrusted source data, not executable
evidence text. Reports avoid unnecessary sensitive payloads and preserve access
constraints. Transactional result persistence avoids half-visible historical runs.
Indexed queries, bounded scope, stable IDs/fingerprints, dependency-aware recomputation,
and pagination are proportionate local-first options; numerical performance targets
need representative measurement rather than an invented portfolio size.

# Validation strategy and open choices

Validation compares logical findings for fixed inputs/reference time; exercises
missing required/optional fields, unknown metadata, partial coverage, conflicts,
stale sources, failed capture, ambiguous mappings, plan revisions, applicable cycles,
criteria that cannot be computed, independent rule failures, source/rule upgrades,
finding reconciliation, and historical replay. It also checks separation from
external recommendations, source non-mutation, and bounded large-input behavior.

Still open: initial rule library and reference criteria, code/configuration split,
status vocabulary, per-goal versus reusable criterion templates, freshness and
sufficiency policies, any justified numerical measures, finding reconciliation,
retained analysis inputs, automatic/on-demand triggering, notification policy,
authorization, and measured performance budgets. This draft approves none of them.

Related: [ingestion and snapshots](ingestion-and-snapshots.md),
[deterministic routine processing](../decisions/deterministic-routine-processing.md).