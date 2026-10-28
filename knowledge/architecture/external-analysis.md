---
type: Architecture
title: External analysis handoff and advisory boundary
description: Bounded manual evidence export and result import, claim validation, disclosure, review, and conditional provider automation.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# External analysis handoff and advisory boundary

External analysis can synthesize trade-offs and options when explicit deterministic
rules cannot answer a strategic question. It remains optional and advisory. Local
evidence, routine findings, planning, and previous decisions remain usable without
a provider. A recommendation is neither a source fact nor an approved action.

The proposed initial direction is **manual structured evidence-brief export and
structured result import**. Direct provider APIs, automated scheduling, and
multi-provider orchestration are possible extensions, not assumed initial runtime
capabilities. Describing provider failure semantics does not approve provider
automation. See [structured handoffs](../decisions/structured-external-analysis-handoffs.md).

# Purpose and balanced context

Useful questions include prioritization, opportunities, internal investment, reuse,
scope reduction, risks/dependencies, evidence gaps, plan review, and review
preparation. Templates specialize objective and expected output without becoming
separate AI subsystems. Select only templates that support a real decision.

Context should not automatically privilege commercial products or internal tools.
Direct outcomes, enabling capabilities, cross-project reuse, dependencies, costs,
opportunity costs, and constraints all matter. Insufficient information, conditional
advice, unresolved assumptions, multiple options, and requests for clarification
are valid results, not provider failures to be hidden.

# Logical components and stages

Objective/scope → selected deterministic findings/evidence → context manifest →
disclosure review/redaction → export/manual transfer → structured import →
structural and claim-reference validation → advisory records → human review →
separately authorized portfolio operation.

Request creation, context selection, disclosure evaluation, validation, recommendation
processing, and review are distinct responsibilities. A future provider adapter
can replace manual transfer while keeping the portfolio domain independent of
vendor authentication and payload formats. Neither mode grants an external process
direct database/filesystem access or permission to operate on source systems.

# Request and context records

A logical request records stable identity, analysis type, objective/question,
requester/origin, scope, selected entity/plan revisions, snapshot IDs, deterministic
run IDs, context version/fingerprint, disclosure decision, template/output-contract
versions, creation/completion times, transfer/execution outcome, imported response,
errors, and limitations. Provider/model identity is captured when actually known;
manual transfer does not justify inventing missing origin metadata.

The context can include goal outcomes, initiative relationships, approved constraints,
plan revisions, findings, evidence/provenance, selected engineering knowledge,
declared work status, Git summaries, execution results, prior decisions, assumptions,
and unresolved questions. Accessibility is not permission to include everything.

A context manifest identifies request/package, included entities/snapshots/findings,
excluded categories, selection rules, redactions/transformations, creation time,
version, and fingerprint. Retain exact content only where policy permits; otherwise
retain the permitted representation and acknowledge weaker reproducibility.
Historical questions use historical context, not silently substituted current state.

Request preparation, transfer/execution, response validation, review, and closure
can have separate status dimensions. A structurally usable import does not mean
its conclusions are approved. Repeated analyses get distinct execution/response
records rather than overwriting old advice; reused contexts remain identifiable.

# Structured result and claim checking

| Record | Useful content |
|---|---|
| Recommendation | Identity, summary, option/action, intended outcome, rationale, evidence, assumptions, risks, dependencies, uncertainty, validation steps, alternatives, affected entities, request, review state |
| Claim | Claim text/type, references, direct/inferential/absent support, contradictions, further evidence needed |
| Review | Reviewer/time, accepted/rejected/deferred interpretation, rationale, requested clarification, supersession |
| Decision linkage | Separately approved choice, alternatives, authority/time, accepted risks, follow-up, evidence and request references |

Versioned result structures can validate required fields/types, classifications,
and identifier syntax. Missing values are not guessed to manufacture a valid
recommendation. Bounded correction or explicit rejection is safer. Partial output
can be retained as incomplete rather than represented as a full recommendation set.

Resolve references against the supplied context and its snapshot versions. Existing
source IDs alone do not prove that a source supports a generated claim. Check
applicable quotations, explicit fields, valid entity references, constraints, and
requested alternatives where feasible. Fabricated or unresolved citations remain
unsupported. Structural conformance and deterministic checks cannot certify every
strategic interpretation.

Self-reported model confidence is not a calibrated probability. Prefer stated
conditions, uncertainty, evidence gaps, and alternatives. Relevant options can
include build/extend, reuse, adopt externally, reduce scope, defer, or gather
evidence; not every question needs every option.

# Review versus decision

Proposed, awaiting review, accepted for investigation/planning, rejected, deferred,
superseded, and withdrawn are useful recommendation lifecycle concepts. Acceptance
for planning is not itself approval of a priority, investment, deadline, or plan.
The consequential domain operation remains explicit and authorized.

An approved decision records the original question, analysis and alternatives,
supporting snapshots/findings, decision-maker and time, rationale, accepted
assumptions/risks, and review/follow-up conditions. Later advice does not silently
replace it. Source conflicts cannot be resolved merely because a model picked a side.

# Disclosure and untrusted content

Minimum necessary disclosure applies before both manual export and automated calls.
Consider source confidentiality, private repository content, personal data, commercial
plans, proprietary designs, credentials, contractual restrictions, and recipient
retention/training terms. Unknown permission calls for policy-directed blocking
or an explicit authorized decision, not automatic sharing.

Redact secrets, irrelevant personal identifiers, sensitive URLs/paths, and unnecessary
implementation detail where appropriate. Record material redaction and resulting
analysis limitations; removing essential evidence cannot silently preserve a claim
of complete context. Local retention and later export follow the same privacy rules.

Separate operational instructions, the owner's question, and quoted source data.
Imported documents, commit text, and provider responses remain untrusted. Do not
execute generated commands or allow embedded instructions to change objective,
permissions, or disclosure policy.

# Conditional provider extension

If automated providers are introduced, an adapter can validate configuration,
submit/retrieve structured requests, record execution metadata, and declare
cancellation and structured-output capabilities. Configuration logically contains
provider/endpoint/model, secret reference, timeout, size/usage limits, permitted
analysis types, retention policy, retries, and configuration revision.

Selection considers disclosure suitability, capabilities, context size, latency,
cost, availability, and organizational restrictions. A primary failure is not
permission to route sensitive context to another provider. Fallback requires the
same policy and any necessary explicit authorization.

Bound execution duration, input/output size, cost where measurable, retries, and
correction requests. Distinguish invalid requests, policy rejection, authentication,
rate limits, timeout, service failure, oversized context, malformed/unsupported
output, reference failures, and review rejection. Temporary errors can be retried;
invalid credentials and policy denials need intervention. A timed-out request with
unknown external completion is not safely resubmitted without reconciliation;
provider idempotency is useful only where its actual contract supports it.

Disabling a provider does not corrupt retained responses or decisions. Offline
fixtures or a mock provider can exercise the logical boundary without network calls.

# Traceability, evaluation, and limits

Retain request/context references, selected source and portfolio revisions,
deterministic runs, actual origin/model metadata, template/output versions,
response and validation, review events, decision links, and follow-up. If policy
prevents full retention, record that limitation. A template/model change can alter
advice without any portfolio change; do not mislabel it as changed source evidence.

Usefulness signals can include unsupported-reference rate, structural failures,
reviewer usefulness, substantial corrections, omitted alternatives, cost/latency,
and accepted/rejected/deferred recommendations. Acceptance rate is not correctness.
Reuse deterministic findings and bounded context rather than automatically paying
for strategic analysis after every refresh. Scheduling needs an explicit benefit
and disclosure/cost policy.

# Validation strategy and unresolved choices

Fixtures cover context selection, historical snapshots, disclosure/redaction,
malformed/partial imports, missing fields, fabricated references, conflicting
claims, prompt-like content, oversized payloads, review transitions, explicit
approval, template changes, retention, and independence from provider outages.
Conditional API tests additionally cover authentication, rate limits, uncertain
timeouts, retry/idempotency, fallback restrictions, and cost limits.

Still open: first useful question/templates, exact export/import serialization and
output structures, permitted data/recipients, full-context retention, review impact
policy, usefulness criteria, budgets, and whether/when to add automated providers.
Provider choice, comparison, synchronous/background execution, and automatic
selection remain conditional decisions, not commitments made by this draft.

Related: [deterministic analysis](deterministic-analysis.md),
[ingestion and snapshots](ingestion-and-snapshots.md),
[human-controlled decisions](../decisions/human-controlled-decisions.md).