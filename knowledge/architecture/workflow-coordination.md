---
type: Architecture
title: Workflow coordination
description: Proposed orchestration of source capture, assessment, planning, review, and recovery with explicit stage and approval boundaries.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Workflow coordination

A workflow composes bounded operations without turning their results into one
opaque success flag. Capture, normalization, evidence extraction, assessment,
reporting, approval, and execution have different meanings. Keeping those stages
visible supports partial recovery and protects historical context.

The flows here are proposed coordination patterns, not approved interfaces or
implemented automation. Deterministic routine processing, independent sources,
read-oriented access, and explicit material decisions are established direction.

# Setup and source configuration

Initialization checks configuration and storage, initializes the adapter registry,
and applies explicit migrations when needed. Existing user data is not overwritten
as a convenience; repeated setup should not duplicate default identities. Missing
optional sources need not disable unrelated local planning operations.

Source configuration records only needed access information. Credentials use a
separate mechanism. A read-oriented connection test can establish known or
explicitly unverified access, capabilities, and limitations; it does not prove
complete source coverage. Invalid configuration, authentication failure, and
unavailability are different outcomes. Disabling a source preserves history.

# Discovery, capture, and comparison

1. Establish requested source scope and record an ingestion attempt.
2. Read inventory, validate response shape and coverage, and resolve stable IDs.
3. Retain new observations, identity ambiguity, and changes in locators or names.
4. Select authorized engineering adapters and detect supported input formats.
5. Capture and normalize each source independently with revision/time context.
6. Compare against the applicable earlier successful observation.
7. Publish usable results according to a defined consistency boundary; report
   partial coverage, failed stages, warnings, and skipped sources separately.

OpenSpec and OKF capture do not require one another to exist. An adapter failure
must not erase independently successful observations. Missing artifacts in an
incomplete scan are not deletion evidence. Discovery itself does not imply a
checkout; repository retrieval depends on the actual access adapter.

The distinction between retaining a completed observation and making an entire
refresh current matters. Per-source, per-project, and whole-refresh publication
have different consistency properties; the initial unit remains unresolved.

# Goal refinement and relationship building

A user can record a goal before criteria or repositories exist, then add outcomes,
constraints, priorities, assumptions, and evidence expectations. Underdefinition
means clarification is needed, not automatic failure. Editing the current goal
does not reinterpret historical reports without a new assessment.

Contribution links carry rationale and provenance. Direct project-to-goal links
are proposed to avoid mandatory initiative wrappers. One project can support
multiple goals; linking expresses relevance, not achievement. Suggested matches
remain candidates where confirmation is needed. Removing a link does not delete
the underlying independent project, knowledge, or evidence.

# Assessment and report generation

Select the goal revision, applicable outcomes/criteria, and bounded evidence set.
Inspect provenance, freshness, coverage, and limitations before applying explicit
rules. Persist the run, findings, and criterion-level assessments with input and
rule versions. Compare later results without rewriting earlier decisions' basis.

A report combines declared status, observed evidence, derived findings, gaps,
dependencies, uncertainty, and approved choices while keeping their categories
distinct. A successful process can produce unresolved results. Insufficient
evidence is not failed outcome; a passing build is not sufficient for every goal.
Goal-achievement confirmation remains a separate policy.

Reusing prior analysis for identical inputs/rules can avoid redundant work.
An intentional new run can still create useful processing history without
duplicating the underlying logical observations. Dependency-aware reanalysis
can be narrow only when affected inputs are known reliably.

# Plans, reviews, and explicit choices

A plan revision records intended approach, milestones, target dates, assumptions,
and dependencies. Validate relationships before storage; approval is a separate
authorized action with rationale. A new draft does not advance the approved
revision or silently rewrite earlier targets.

Execution reviews focus on near-term progress and blockers; strategic reviews
focus on outcomes, investment balance, and opportunities. A review retains the
reports and plan revisions considered. It can produce proposed changes, explicit
decisions, or a request for more evidence. Not every finding needs a formal
decision; governance should remain proportionate.

For a recommendation, show origin, evidence, rationale, assumptions, uncertainty,
and alternatives. Record acceptance, rejection, deferral, or investigation as an
explicit choice with authority and time. Link any resulting plan revision.
Viewing output is not approval; approval is not execution or repository publication.

# Optional external analysis

External strategic reasoning starts with a defined question and selected evidence.
Apply disclosure policy, redaction, and consent before sharing. Preserve request
context and result provenance; validate returned structure and references without
claiming factual verification. Unsupported model claims remain visible.

Structured export/import is the initial proposal. Direct provider invocation
and scheduled analysis are alternative future capabilities, not assumed initial
automation. Provider failure leaves local portfolio records and prior results
usable. Recommendations cannot bypass approval.

# Failure, retries, and concurrency

Record failed stage, source/scope, time, safe diagnostic category, recoverability,
and retained successful work. Distinguish partial completion, failure, cancellation,
and successful completion. A failed analysis is not the next valid report.

Retry behavior uses stable identities and explicit idempotency semantics. Repeated
unchanged input does not create duplicate artifacts, evidence, goals, or decisions.
Retrying failed stages is different from generating a deliberate new run record.

Concurrent refreshes must not overwrite newer owner edits; concurrent plan or
decision edits need conflict detection. Locking, optimistic version checks, and
job persistence are implementation choices still requiring design. Short work can
remain synchronous; measured latency or recovery needs may justify background jobs.

# Archival, export, and observability

Archival identifies active dependencies and records consequences before removing
a record from active views. It does not imply failure, source deletion, automatic
archival of related entities, or erasure of decision history.

Export selects scope, applies sensitive-data exclusions, includes stable IDs and
relationships, and records format/version and limitations in a manifest. Exporting
Siddhi records does not back up every external source. Restore needs validation
and an explicit collision policy rather than silently overwriting current data.
Formats, restore behavior, and backup strategy remain open.

Workflow summaries expose requested scope, timing, stage outcomes, accessed/skipped
sources, counts, quality warnings, generated records, and safe recovery guidance.
Operational logs serve diagnosis; user summaries explain actionable outcomes.
Neither should disclose credentials or unnecessary sensitive payloads.

# Proposed sequencing and open choices

Prioritize discovery → independent goal → source capture → deterministic report →
historical comparison. Planning/governance, external strategic analysis, and
operational expansion can follow when justified; these are not fixed releases.
Open choices include confirmation boundaries, scheduling, automatic reanalysis,
achievement policy, review needs, publication/recovery unit, export formats,
concurrency protection, and status vocabulary.

Related: [system architecture](system-architecture.md),
[logical data model](data-model.md),
[proportionate background execution](../decisions/proportionate-background-execution.md).