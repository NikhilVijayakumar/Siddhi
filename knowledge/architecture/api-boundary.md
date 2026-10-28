---
type: Architecture
title: Application API boundary
description: Domain ports, proposed transport contracts, validation, errors, concurrency, and long-running operations.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Application API boundary

Clients access persistent portfolio operations through the backend, not SQLite
or raw source adapters. This draft describes architectural intent, not running
behavior. HTTP routes, payload schemas, OpenAPI publication, authentication,
background execution, and generated clients are proposed, not implemented here.

# Responsibilities and ports

| Boundary | Owns | Excludes |
|---|---|---|
| Transport | Routing, parsing, access checks, serialization, correlation | Portfolio rules, SQL, arbitrary source operations |
| Application | Authorized use cases, transaction scope, operation lifecycle | HTTP objects and provider-specific payloads |
| Domain | Meaning, invariants, approval and revision transitions | Framework exceptions, database sessions, filesystem discovery |
| Repository port | Domain-oriented persistence contracts | Public transport models and cross-domain orchestration |
| Source port | Declared read capabilities, scope, provenance, completeness | Arbitrary execution and authority over portfolio decisions |
| Credential port | Scoped resolution for an authorized integration | Global delivery of all credentials |

Infrastructure implements application/domain ports. Typed application errors
cross the boundary; only transport maps them to HTTP. Domain rules remain valid
for every authorized caller. Request, response, domain, and storage models can
evolve separately without leaking implementation details into the public contract.

# Resources and explicit actions

Portfolio resources include goals, initiatives, plans and revisions, milestones,
dependencies, reviews, and decisions. Source resources include connection
metadata, ingestion attempts, snapshots, evidence, and provenance. Analysis
resources include runs, findings, reports, and advisory recommendations.

Source-owned metadata is read-oriented; owned mappings and assessments are
separate records. Evidence is not generically editable source truth. Reviewing a
recommendation is not automatically approving a decision. Lifecycle transitions
are explicit actions, not read side effects or unrestricted status patches.
Revisions preserve the context of earlier reviews.

# Proposed HTTP conventions

A versioned namespace such as `/api/v1` is a candidate, not an installed API.
Use explicit bounded JSON models, stable opaque application identifiers, separate
source-native identities, timezone-aware timestamps, and date-only planning values
where time-of-day has no meaning. Field naming remains to be selected.

Collections need meaningful allowlisted filters, deterministic sorting, bounded
page sizes, and documented pagination consistency. Offset versus cursor paging
remains open. Responses expose safe lifecycle, revision, timestamps, and related
resource references without leaking repository or database internals.

Publish one backend-owned machine-readable contract when transport exists.
Generated client types consume it rather than becoming an independently edited
authority. Review additive, semantic, breaking, and deprecated changes separately;
a schema-compatible update can still break behavior. Define compatibility and
removal windows before clients rely on stability.

# Validation and safe errors

Validate syntax, types, lengths, identifiers, enums, dates, pagination, scope,
references, authorization, disclosure, and resource limits. Domain validation
checks current state and invariants; database constraints complement it.
Response allowlists prevent accidental exposure of internal or secret fields.

A proposed error representation has a stable code, safe summary, optional field
details, correlation identifier, and corrective action. Do not echo credentials,
private payloads, SQL parameters, stack traces, or sensitive paths.

| HTTP category | Proposed meaning |
|---|---|
| 200 / 201 / 204 | Completed operation / created resource / no body |
| 202 | Durably accepted unfinished work, not completed success |
| 400 / 422 | Malformed representation / semantic validation, consistently mapped |
| 401 / 403 / 404 | Authentication / authorization / absent or non-visible resource |
| 409 / 412 | State conflict / failed revision precondition |
| 413 / 429 | Size / usage limit exceeded |
| 500 / 503 | Unexpected failure / unavailable required capability |

These are design categories, not current response contracts. Partial outcomes
belong in explicit results rather than generic success that hides loss.

# Long-running operations and concurrency

Accepted operations need stable identity, type, scope, status, timestamps, result
reference, safe error, and measurable stages/counts where available. Unknown total
work does not justify invented progress. Request and operation IDs differ.

Keep slow source/provider work outside write transactions. Publish coherent
results atomically and preserve the last usable state on failure. Cancellation
is a request, not proof work stopped; expose the final observed outcome.
After restart, reconcile nonterminal runs rather than leaving them running forever.
Resume, retry, or interruption classification depends on persisted stages and
side-effect safety; no automatic recovery guarantee is implied.

Duplicate expensive actions may need idempotency keys with defined caller/action
scope, payload equivalence, expiration, and atomic result association. Reusing a
key with a different payload is not a harmless retry. Concurrent edits need
revision checks or ETags rather than silent protected-history overwrites.

# Deployment and unresolved choices

Loopback binding reduces exposure but authenticates no caller. Authorization is
backend-enforced, CORS is origin policy only, and remote exposure needs a separate
security model. Optional provider failure should not disable local work.

Resolve exact routes, health namespace, resource versus generic operation status,
authentication/session lifecycle, field naming, paging, deletion policy, revision
mechanism, idempotency retention, limits, and restart semantics before stabilizing
a client contract. A candidate endpoint catalogue is not evidence routes exist.

Related: [persistence](persistence.md), [security](security-and-privacy.md),
[configuration](configuration-and-secrets.md), [observability](observability.md),
[testing](../practices/testing-and-validation.md).