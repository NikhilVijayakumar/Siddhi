# Engineering-quality desk review

Desk review only, no interview or user confirmation. A goal-to-evidence report is the recommended first-release goal, NOT an approved release choice. These quality drafts do not claim passing application tests.

## Intent

**Q1. What distinguishes structural acceptance documents from verified application behavior?**
- **Recommendation:** Report document checks separately from executed automated tests and their actual results.
- **Why:** Tagged Gherkin without a runner or step definitions is not passing evidence.
- **Status:** Recommended
- **Feeds:** NFR-034; verification reporting

## Scope

**Q2. Which workstation and repository sizes should resource measurements represent?**
- **Recommendation:** Agree reference hardware and typical/largest portfolio fixtures before setting hard memory, storage or latency budgets.
- **Why:** Unmeasured enterprise-scale infrastructure would violate proportionate local operation.
- **Status:** Decision needed
- **Feeds:** NFR-004; reference workload

## Behaviour

**Q3. Which failures must be exercised before a vertical slice is considered verified?**
- **Recommendation:** Select relevant interruption, outage, invalid-data, failed-transaction, timeout and retry cases for each slice.
- **Why:** Successful execution alone cannot demonstrate recoverable failure behavior.
- **Status:** Recommended
- **Feeds:** NFR-034, NFR-038

## Data

**Q4. Which supported versions and malformed-source fixtures are required first?**
- **Recommendation:** Agree real versioned fixtures with missing metadata, staleness and conflict, all reproducible without private repositories.
- **Why:** Synthetic happy-path-only samples cannot establish source compatibility.
- **Status:** Decision needed
- **Feeds:** NFR-035; initial fixture catalogue

## Integration

**Q5. Should routine test runs require live Vyasa or an external AI account?**
- **Recommendation:** Isolate external systems with controlled doubles and use separate documented contract compatibility checks.
- **Why:** Network and account state must not determine routine test reproducibility.
- **Status:** Recommended
- **Feeds:** NFR-035, NFR-036

## Architecture

**Q6. How should significant design and dependency choices be justified?**
- **Recommendation:** Retain architectural alternatives/consequences and dependency purpose with appropriate version constraints and testable updates.
- **Why:** Unexplained frameworks and blurred module boundaries increase maintenance cost.
- **Status:** Recommended
- **Feeds:** NFR-028, NFR-032, NFR-033

## Acceptance

**Q7. What coverage criteria should supersede a bare percentage target?**
- **Recommendation:** Identify critical behaviors and failure risks across all layers before agreeing any numeric coverage threshold.
- **Why:** A high percentage can still omit the integrity and trust boundaries that matter.
- **Status:** Decision needed
- **Feeds:** NFR-034, NFR-038; critical-coverage policy

## Ambiguity

**Q8. Which runtime/dependency versions and acceptance execution tooling are actually supported?**
- **Recommendation:** Confirm support versions and whether a Gherkin runner adds value; do not imply tooling exists merely because scenarios are written.
- **Why:** Proposed stack direction and executable compatibility require different evidence.
- **Status:** Decision needed
- **Feeds:** NFR-033, NFR-034, NFR-036; support and acceptance tooling policy