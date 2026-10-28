# API-operations desk review

Desk review only, no interview or user confirmation. Recommended first-release goal: goal-to-evidence report, NOT an approved release choice. No endpoint catalogue, numeric performance commitment or job framework is approved here.

## Intent

**Q1. Can an independent client consume implemented capabilities without copying domain rules?**
- **Recommendation:** Expose validated documented HTTP contracts while keeping portfolio rules in the backend.
- **Why:** Separate desktop development requires an authoritative shared boundary.
- **Status:** Recommended
- **Feeds:** FR-043, NFR-030, NFR-040, NFR-048

## Scope

**Q2. Which refreshes and analyses should run outside a held HTTP request?**
- **Recommendation:** Measure representative workloads and select the simplest execution model that preserves responsiveness and observable outcomes.
- **Why:** Neither fully synchronous work nor a broker is justified by assumption.
- **Status:** Decision needed
- **Feeds:** FR-045, NFR-001, NFR-002; execution model and benchmark environment

## Behaviour

**Q3. What lifecycle and retry/cancellation semantics should clients observe?**
- **Recommendation:** Agree progress/final-state, failure and safe-retry meanings; allow cancellation only at integrity-safe boundaries.
- **Why:** A cancel acknowledgement cannot promise rollback of already committed work.
- **Status:** Decision needed
- **Feeds:** FR-045, NFR-044, NFR-051; operation lifecycle contract

## Data

**Q4. Which error categories and collection bounds should the public contract standardize?**
- **Recommendation:** Agree structured categories and bounded retrieval without assuming exact codes, field names or page sizes.
- **Why:** Clients need consistent meanings while actual schemas remain undecided.
- **Status:** Decision needed
- **Feeds:** FR-044, NFR-042, NFR-043; HTTP error and pagination contract

## Integration

**Q5. Should a remote source outage make local application health fail automatically?**
- **Recommendation:** Distinguish local availability, database access and integration readiness with safe diagnostic details.
- **Why:** Unrelated local capabilities may remain fully usable.
- **Status:** Recommended
- **Feeds:** FR-046, NFR-052

## Architecture

**Q6. Where should operation context be linked to diagnostic logs?**
- **Recommendation:** Use useful operation/correlation identifiers and redacted subsystem details, not copied request or repository payloads.
- **Why:** Debuggability does not require leaking private content.
- **Status:** Recommended
- **Feeds:** FR-046, NFR-050, NFR-053

## Acceptance

**Q7. What should happen when validation or transactional processing fails?**
- **Recommendation:** Assert consistent safe errors and no unintended partial state changes, alongside generated contract checks.
- **Why:** Documentation-only validation cannot prove write atomicity.
- **Status:** Recommended
- **Feeds:** FR-043, FR-044, NFR-040, NFR-042

## Ambiguity

**Q8. How much contract stability is required before desktop packaging?**
- **Recommendation:** Agree an early-development compatibility/versioning policy and benchmark targets with the consumer before treating proposals as commitments.
- **Why:** Silent breaking changes and unmeasured latency claims undermine independent integration.
- **Status:** Decision needed
- **Feeds:** NFR-001, NFR-041, NFR-048; compatibility and performance acceptance