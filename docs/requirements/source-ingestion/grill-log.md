# Source-ingestion desk review

Desk review, not an interview; no user confirmation occurred. The recommended first-release goal is a goal-to-evidence report, NOT an approved release choice. Native contracts below remain unconfirmed.

## Intent

**Q1. Does inventory ingestion create a second authoritative project registry?**
- **Recommendation:** Retain Vyasa source identifiers and map them to internal references without competing identities.
- **Why:** Discovery and portfolio ownership have different authorities.
- **Status:** Recommended
- **Feeds:** FR-007, FR-010, NFR-011, NFR-012

## Scope

**Q2. Which real Vyasa interface and artifact versions are supported first?**
- **Recommendation:** Inspect the real contract and representative repositories before naming versions, paths or access methods.
- **Why:** An assumed layout or API cannot establish compatibility.
- **Status:** Decision needed
- **Feeds:** FR-007, FR-008, FR-009, NFR-029, NFR-031; adapter support matrix

## Behaviour

**Q3. Can an inaccessible source be treated as having removed all prior artifacts?**
- **Recommendation:** Retain prior data with unavailable/stale qualifications; establish removal only within sufficiently observed scope.
- **Why:** Access failure is not deletion evidence.
- **Status:** Recommended
- **Feeds:** FR-011, FR-012, NFR-005, NFR-006, NFR-009, NFR-013

## Data

**Q4. Which timestamps and revision signals establish unchanged content?**
- **Recommendation:** Prefer reliable revisions or content hashes and distinguish source times from ingestion time; re-evaluate safely when signals are unreliable.
- **Why:** Equal timestamps do not prove equal content.
- **Status:** Recommended
- **Feeds:** FR-013, NFR-003, NFR-016

## Integration

**Q5. How should a retry of the same captured revision affect logical records?**
- **Recommendation:** Preserve attempt outcomes without duplicate logical source records or artificial changes.
- **Why:** Retrying an observation must not inflate inventory or progress.
- **Status:** Recommended
- **Feeds:** FR-011, FR-013, NFR-008

## Architecture

**Q6. Is partial publication atomic per source, project or portfolio?**
- **Recommendation:** Agree a publication unit and independently report capture coverage before allowing partial results to replace usable views.
- **Why:** A transaction cannot manufacture cross-source atomic observations.
- **Status:** Decision needed
- **Feeds:** FR-011, FR-012, NFR-006; persistence-recovery publication contract

## Acceptance

**Q7. What demonstrates schema-aware failure isolation?**
- **Recommendation:** Refresh one supported source alongside malformed and unsupported sources while proving existing portfolio reads remain usable.
- **Why:** A successful happy-path parser does not demonstrate safe degradation.
- **Status:** Recommended
- **Feeds:** FR-009, FR-012, NFR-005, NFR-009, NFR-031

## Ambiguity

**Q8. Should interrupted refreshes resume or restart, and when is data stale?**
- **Recommendation:** Agree source-specific checkpoint/retry and freshness policies from actual capabilities; never advance uncommitted progress.
- **Why:** Universal cursor and age assumptions risk skipped records and misleading currency.
- **Status:** Decision needed
- **Feeds:** FR-011, FR-012, FR-013; refresh recovery and freshness policy