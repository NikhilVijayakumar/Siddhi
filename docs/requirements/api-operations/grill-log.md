# API-operations desk review

Desk review only, no interview or user confirmation. Recommended first-release goal: goal-to-evidence report, NOT an approved release choice. No endpoint catalogue, numeric performance commitment or job framework is approved here.

Deep review 2026-10-29: every question now records the options considered, the trade-off, and a resolution. `Recommended` means a recommendation is on record and may be adopted by a draft specification; `Decision needed` means the answer needs owner input that the documents cannot supply.

## Intent

**Q1. Can an independent client consume implemented capabilities without copying domain rules?**
- **Options:** client embeds portfolio rules; server exposes documented HTTP contracts; both share a library.
- **Trade-off:** embedding rules duplicates and diverges them; a shared library couples the desktop client to backend internals; documented HTTP contracts keep one authority.
- **Recommendation:** Expose validated documented HTTP contracts while keeping portfolio rules in the backend.
- **Why:** Separate desktop development requires an authoritative shared boundary.
- **Resolution:** Every client-visible capability is an HTTP operation with a documented request/response schema generated from the implementation. The client holds presentation logic only.
- **Status:** Recommended
- **Feeds:** FR-043, NFR-030, NFR-040, NFR-048
- **Knowledge:** `knowledge/architecture/api-boundary.md`, `knowledge/decisions/ui-independent-http-boundary.md`

## Scope

**Q2. Which refreshes and analyses should run outside a held HTTP request?**
- **Options:** all operations synchronous; all operations background; synchronous reads and writes, tracked jobs for ingestion and analysis.
- **Trade-off:** all-synchronous holds connections during long work; all-async makes trivial reads needless work; the split is simple and proportionate.
- **Recommendation:** Measure representative workloads and select the simplest execution model that preserves responsiveness and observable outcomes.
- **Why:** Neither fully synchronous work nor a broker is justified by assumption.
- **Resolution:** Goal and read operations are synchronous. Ingestion and analysis run as tracked jobs with polling. No message broker or worker fleet in the first slice; measurement against the reference workload decides any later change.
- **Status:** Recommended
- **Feeds:** FR-045, NFR-001, NFR-002; execution model and benchmark environment
- **Knowledge:** `knowledge/architecture/workflow-coordination.md`, `knowledge/architecture/api-boundary.md`

## Behaviour

**Q3. What lifecycle and retry/cancellation semantics should clients observe?**
- **Options:** fire-and-forget; a full job state machine with resume; a small explicit state set with cancellation at safe points.
- **Trade-off:** fire-and-forget hides failure; a resume-capable machine is more than local workloads need; a small state set is observable and honest.
- **Recommendation:** Agree progress/final-state, failure and safe-retry meanings; allow cancellation only at integrity-safe boundaries.
- **Why:** A cancel acknowledgement cannot promise rollback of already committed work.
- **Resolution:** States: queued, running, succeeded, failed, cancelled. Cancellation takes effect before the next commit boundary; already committed work stays committed and the response says so. Retry is a new job with a new identifier.
- **Status:** Recommended
- **Feeds:** FR-045, NFR-044, NFR-051; operation lifecycle contract
- **Knowledge:** `knowledge/architecture/workflow-coordination.md`, `knowledge/architecture/persistence.md`

## Data

**Q4. Which error categories and collection bounds should the public contract standardize?**
- **Options:** free-text errors; provider-specific codes; a small stable category set with opaque cursors.
- **Trade-off:** free text cannot be handled by clients; provider codes leak internals; a small set keeps clients stable without fixing field names too early.
- **Recommendation:** Agree structured categories and bounded retrieval without assuming exact codes, field names or page sizes.
- **Why:** Clients need consistent meanings while actual schemas remain undecided.
- **Resolution:** Categories: validation, not_found, conflict, unsupported, unavailable, internal. Collections use opaque cursor pagination with a server-chosen bound. Exact payloads are fixed in the change's `api-contract.md`.
- **Status:** Recommended
- **Feeds:** FR-044, NFR-042, NFR-043; HTTP error and pagination contract
- **Knowledge:** `knowledge/architecture/api-boundary.md`, `knowledge/practices/testing-and-validation.md`

## Integration

**Q5. Should a remote source outage make local application health fail automatically?**
- **Options:** one overall health flag; health fails on any integration outage; separate local, database and integration readiness.
- **Trade-off:** one flag cannot explain an outage; failing on integration outage blocks unrelated work; separate readiness reports each truthfully.
- **Recommendation:** Distinguish local availability, database access and integration readiness with safe diagnostic details.
- **Why:** Unrelated local capabilities may remain fully usable.
- **Resolution:** Health reports three independent sections. Only local availability and database access determine whether the service is usable; integration readiness is reported separately with no secrets or repository content.
- **Status:** Recommended
- **Feeds:** FR-046, NFR-052
- **Knowledge:** `knowledge/architecture/observability.md`, `knowledge/architecture/api-boundary.md`

## Architecture

**Q6. Where should operation context be linked to diagnostic logs?**
- **Options:** log full requests; log operation ids with redacted fields; log nothing.
- **Trade-off:** full requests leak content; logging nothing defeats diagnosis; ids plus redacted subsystem fields support both.
- **Recommendation:** Use useful operation/correlation identifiers and redacted subsystem details, not copied request or repository payloads.
- **Why:** Debuggability does not require leaking private content.
- **Resolution:** Each operation gets a correlation identifier that appears in its responses and in structured logs. Log entries carry subsystem, outcome and duration; request bodies, paths and credentials are excluded.
- **Status:** Recommended
- **Feeds:** FR-046, NFR-050, NFR-053
- **Knowledge:** `knowledge/architecture/observability.md`, `knowledge/architecture/security-and-privacy.md`

## Acceptance

**Q7. What should happen when validation or transactional processing fails?**
- **Options:** best-effort partial write; roll back and report; leave partial state and mark it recoverable.
- **Trade-off:** best-effort corrupts; rollback with a structured error is the simplest correct behavior; recoverable partial state is only justified for multi-step jobs.
- **Recommendation:** Assert consistent safe errors and no unintended partial state changes, alongside generated contract checks.
- **Why:** Documentation-only validation cannot prove write atomicity.
- **Resolution:** A failed validation or transaction leaves no changed rows and returns a structured error with the correlation identifier. Tests assert both the response category and the unchanged state.
- **Status:** Recommended
- **Feeds:** FR-043, FR-044, NFR-040, NFR-042
- **Knowledge:** `knowledge/practices/testing-and-validation.md`, `knowledge/architecture/persistence.md`

## Ambiguity

**Q8. How much contract stability is required before desktop packaging?**
- **Options:** freeze contracts now; allow breaking changes freely during early development; an explicit pre-1.0 policy with change notes.
- **Trade-off:** freezing early blocks learning; free changes break the desktop client; a stated pre-1.0 policy sets expectations without pretending stability.
- **Recommendation:** Agree an early-development compatibility/versioning policy and benchmark targets with the consumer before treating proposals as commitments.
- **Why:** Silent breaking changes and unmeasured latency claims undermine independent integration.
- **Resolution:** Recommended default: pre-1.0, breaking changes allowed only with a recorded change note and client-visible version bump; benchmark environment and targets agreed before any NFR-001 figure is treated as binding. Owner and client-consumer agreement is the input that closes this.
- **Status:** Decision needed
- **Feeds:** NFR-001, NFR-041, NFR-048; compatibility and performance acceptance
- **Knowledge:** `knowledge/architecture/api-boundary.md`, `knowledge/practices/knowledge-and-delivery-separation.md`
