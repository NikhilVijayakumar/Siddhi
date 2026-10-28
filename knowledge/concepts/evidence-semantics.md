---
type: Concept
title: Evidence semantics
description: Separate attributable observations from assessments and keep certainty, sufficiency, freshness, and execution state independent.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Evidence semantics

Evidence is an attributable observation relevant to a question. An assessment
interprets evidence against a criterion. A finding records an analytical
conclusion; a recommendation suggests an action; an approved decision records a
choice. None is automatically interchangeable with another.

An observation can be source-declared, directly observed in history, imported
from a verification artifact, supplied by the owner, or derived by an explicit
rule. External model output remains an attributed claim or interpretation,
not verified source fact because it parses successfully or sounds confident.

# Independent dimensions

| Dimension | Question answered | What it does not establish |
|---|---|---|
| Certainty | How strongly is this particular interpretation supported, and what ambiguity remains? | Whether every criterion or relevant source is covered |
| Sufficiency | Is there enough applicable evidence to assess this criterion within the stated scope? | That the supported result is positive, current, or executed |
| Freshness | When was the source successfully observed, and is it usable for this time-sensitive question? | Truth, completeness, or verification |
| Execution state | Did an operation or intended action actually run, finish, fail, or remain unexecuted? | Goal achievement or decision approval |

**Certainty** is claim-specific confidence, not necessarily a numeric probability.
A textual match may suggest relevance without establishing it. Conflicting
observations and identity ambiguity lower certainty even if every source was read.
Any numerical thresholds need a justified method; none is settled here.

**Sufficiency** depends on criteria and coverage. A complete test record can
still be insufficient for a publication or commercial outcome. Evidence can be
sufficient to establish a negative result, or insufficient to decide either way.
Completeness describes the scope obtained; sufficiency asks whether that scope
and kind of information can answer the question.

**Freshness** includes observation time, revision applicability, last successful
refresh, and failed or skipped refresh context. An old test result can be a
reliable historical fact yet stale for the current revision. A recently parsed
document can be wrong or incomplete. Availability, format support, and validity
are related operational dimensions, not synonyms for age.

**Execution state** applies both to processing attempts and to actions chosen by
the owner. A successful analysis run can yield an unresolved finding; an approved
plan may have no execution evidence. A task marked complete is a declaration,
not observed successful execution. Keep approval, execution, and outcome assessment
separate even when one interface presents all three.

Verification is another independent property: a recorded process checked a
particular scope and revision. Parsing success proves interpretability under a
parser, not technical correctness. A successful test demonstrates only what that
test covers, not every linked strategic result.

# Finding vocabulary

Useful analytical categories include:

- **Confirmed relationship:** explicit evidence or an applicable confirmation
  rule establishes a relationship. It does not establish outcome satisfaction.
- **Candidate match:** potentially relevant, but not established.
- **Identified gap:** an applicable criterion is demonstrably unmet.
- **Missing evidence:** needed information was not available within the searched
  scope; no global claim of nonexistence follows.
- **Unresolved:** ambiguity, conflict, or inadequate support prevents a conclusion.
- **Stale or unavailable input:** the relevant source cannot be treated as current
  or accessed as requested; preserve last-known observations with qualification.

These are not a single exclusive status set: a candidate may also use stale
information and insufficient coverage. More precise methods can classify support,
partial support, contradiction, conflicting evidence, or not-assessed results.
The final universal versus method-specific vocabulary remains open.

# Absence, conflict, and identity

A complete, successful observation of a defined source scope can support an
artifact-removal finding. Inaccessibility, partial enumeration, filtering,
renaming, unsupported format, and parse failure cannot establish deletion.
“Not found in these locations” is narrower than “does not exist.”

Preserve conflicting values with their field-level sources, revisions, and
observation times. Authority is claim-specific, not “latest source wins.” Names,
paths, and keywords alone do not safely merge identities. Preserve unresolved
matching when stable identifiers are unavailable.

# Provenance and reproducibility

A useful chain connects source identity and artifact to snapshot, normalization
version, evidence, criterion, analysis rule/configuration version, finding, and
report. Retain search scope, limitations, and the relevant portfolio revision.
Observation, recording, processing, effective, and decision times mean different
things and should not be substituted for one another.

Assessments can change when criteria, rules, or inputs change without altering
the original observation. A correction can point to an earlier observation while
preserving why the former assessment existed. Historical reports describe their
captured context; a new report does not silently rewrite an old decision's basis.

Determinism means equivalent findings from equivalent recorded inputs and rules,
not proof that source claims are true. A reproducibility claim is qualified when
payloads, revisions, transformations, or rule versions were not retained.

# Worked distinctions

- A fresh inventory entry establishes discovery, not maintenance or release readiness.
- A passing test at revision A is an observed execution result; it may be stale
  at revision B and insufficient for the goal's business outcome.
- No result in a partial scan means missing evidence, not failed implementation.
- An accepted recommendation establishes a decision only through explicit
  approval; neither the recommendation nor approval establishes execution.
- An overdue milestone compares a date against a plan; it is not proof of failure.

These distinctions are established direction. Exact thresholds, achievement
confirmation policies, permitted statuses, and correction/retention mechanics
remain proposed. No human approval is asserted by this draft.

Related: [portfolio domain](portfolio-domain.md),
[data ownership](../architecture/data-ownership.md),
[deterministic routine processing](../decisions/deterministic-routine-processing.md).