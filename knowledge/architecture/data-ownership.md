---
type: Architecture
title: Data ownership and authority
description: Field-specific source authority, local projections, permissions, conflict handling, provenance, and historical data boundaries.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Data ownership and authority

Authority follows a category of information or claim, not every attribute of an
entity. Inventory may declare a repository location while repository-local
configuration supplies different origin evidence. Retain the discrepancy rather
than treating one source as universally authoritative or the latest read as truth.

Source independence, read-oriented routine processing, explicit provenance,
and human-controlled portfolio decisions are established direction. Detailed
field policies, retention, access roles, and correction mechanics remain proposed.
This concept is an unverified draft, not a human approval record.

# Authority matrix

| Information | Authority | Siddhi's role |
|---|---|---|
| Project/repository inventory and declared metadata | Vyasa within its actual contract | Discover, reference, normalize, compare, and retain observations |
| Development intent and change-management artifacts | OpenSpec | Index and analyze attributable declarations, not rewrite them |
| Engineering knowledge, relationships, and declared review metadata | OKF | Index and relate independent knowledge without changing its semantics |
| Revision history and repository-local configuration | Git/VCS | Observe history and discrepancies, not infer completion from activity |
| Test, build, and release observations | Producing verification system or artifact | Retain scope, revision, result, time, and limitations |
| Goals, outcomes, contributions, priorities, and constraints | Siddhi | Maintain owner-directed portfolio context and revisions |
| Plans, milestones, reviews, and decisions | Siddhi | Preserve versions, authority, rationale, and explicit approval |
| Normalized projections, snapshots, assessments, and reports | Siddhi's local records | Preserve input ownership and processing provenance |
| External recommendations | Attributed external producer; Siddhi maintains the received record | Store context and review state, not recast output as verified fact |

A local projection does not become an independently editable authority over its
source. A mapping between knowledge and a portfolio goal belongs to Siddhi unless
the source itself authored it. Knowledge and development artifacts remain
independently discoverable and usable; missing cross-links invalidate neither.

# Data categories and permissions

**Source references** retain source identity and locators, allowing relocation
without recreating records. They do not grant permission to modify a source.

**Snapshots** capture observed scope and time. Their substantive history is
preserved under explicit correction and retention policies; retaining one does
not make it current. Payload minimization can coexist with durable metadata.

**Normalized records** are derived, versioned representations that may be
regenerated. Preserve source, snapshot, transformation version, and limitations.

**Evidence** records relevant observations. **Assessments** interpret observations
against criteria. Revising an interpretation does not rewrite the observation.
Material findings preserve evidence, method, criterion, time, and uncertainty.

**Recommendations** propose actions. **Decisions** record explicit choices by
an authorized person, with time, rationale, approval state, and context.
Rejection, reversal, and supersession preserve earlier reasoning. A model does
not become a portfolio decision-maker by returning a structured result.

# Reading and writing

Normal discovery, ingestion, and analysis are read-oriented. They do not commit,
merge, checkout, reset, alter source status, publish reports, or modify knowledge.
Repository content does not authorize actions or supply executable instructions.

A future write capability needs a separately defined source, record scope,
permitted operations, acting identity, authorization/confirmation policy, audit,
failure handling, and reversal approach. Read permission, approval of a plan,
or write access to another source does not imply this capability.

# Source-specific interpretation traps

- An inventory entry does not prove active maintenance or complete scanning.
- A documentation directory does not prove accurate or sufficient content.
- A declared task completion does not prove successful implementation.
- A knowledge document's existence or declared validation metadata is not
  independently performed technical verification by Siddhi.
- A recent commit is activity, not useful outcome progress; an old commit does
  not prove abandonment. A tag is not necessarily a production release.
- A passing test is an observation at a revision and scope, not automatic
  satisfaction of a strategic criterion.

# Refresh, absence, and conflict

An ingestion attempt records source, scope, start/completion time, relevant
revision, adapter/parser version, discovered/processed/skipped/rejected counts,
and limitations where available. Parsing success does not establish accuracy,
currency, completeness, or technical correctness.

Stable external identities support repeated capture without duplicate logical
records. A documented composite strategy may be needed when sources lack IDs;
name similarity alone does not justify merging ambiguous records.

Disappearance from a successful complete scope differs from access failure,
filtering, movement, rename, unsupported format, or parse failure. Preserve
linked goals and history rather than cascading disappearance into deletion.
Apply field-specific authority rules to conflicting observations when defined;
otherwise retain the conflict and allow an authorized resolution with rationale.

# Provenance, privacy, and retention

Trace material findings through artifact identity, revision or fingerprint,
snapshot, observation time, transformation, criterion, analysis version, and
relevant owner changes. Missing retained inputs limit reproducibility claims.
Freshness, certainty, sufficiency, verification, and execution are distinct;
see [evidence semantics](../concepts/evidence-semantics.md).

Collect only needed information. Credentials remain separate from ordinary source
metadata, snapshots, prompts, reports, and diagnostics. External analysis includes
only authorized selected information and records its scope without unnecessarily
duplicating sensitive content. Local-first operation does not remove access,
backup, filesystem, or disclosure risks.

Retention distinguishes current projections, historical snapshots, evidence,
assessments, decisions, operational logs, temporary data, and credentials.
Corrections to source facts belong in the source; local corrections to derived
interpretations need visible history. Removing a local reference does not delete
the source; removing a source does not automatically erase historical decisions.
Privacy/security deletion obligations may require payload removal with deliberate
handling of dependent history rather than a blanket “retain forever” rule.

# Enforcement and open policy

Enforce ownership through narrow adapter capabilities, separate write paths,
immutable or versioned observation history, explicit approval operations, conflict
visibility, idempotent identity resolution, and secret-safe diagnostics. Exercise
partial scans, permission failure, renames, parser upgrades, corrections,
rejected recommendations, and source disappearance in tests.

Open policies include field-level Vyasa authority, retention duration and storage
strategy, correction rules, approver identity, disclosure/redaction consent,
deletion obligations, export coverage, local access security, and external-result
retention. Conservative direction is no silent conflict resolution, source writes,
approval, or deletion of dependent portfolio history.

Related: [logical data model](data-model.md),
[source authority and read-only ingestion](../decisions/source-authority-and-read-only-ingestion.md).