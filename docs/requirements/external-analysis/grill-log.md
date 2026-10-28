# External-analysis desk review

Desk review, no interview or user confirmation. Recommended first-release goal: goal-to-evidence report, NOT an approved release choice. Manual handoff and any provider integration remain recommendations or open decisions.

## Intent

**Q1. Which work should remain possible when external analysis is unavailable?**
- **Recommendation:** Keep routine parsing and defined-rule reporting independent of external analysis and investigation.
- **Why:** Strategic judgment assistance is optional, not a local-operation dependency.
- **Status:** Recommended
- **Feeds:** FR-042, NFR-019

## Scope

**Q2. Is a manual structured handoff sufficient before integrating provider APIs?**
- **Recommendation:** Evaluate manual brief export and result import first; require a separate decision for automation.
- **Why:** A useful advisory workflow does not imply provider orchestration is needed.
- **Status:** Decision needed
- **Feeds:** FR-038, FR-039; transfer mode and release scope

## Behaviour

**Q3. Can a structurally valid recommendation change approved priorities?**
- **Recommendation:** Keep imports advisory and require explicit owner review and consequential operations.
- **Why:** Validation does not establish truth or strategic authority.
- **Status:** Recommended
- **Feeds:** FR-040, FR-041, NFR-019

## Data

**Q4. Which result fields and reference failures should reject or qualify an import?**
- **Recommendation:** Agree a versioned structure and invalid/incomplete/unsupported-reference treatment, preserving unknown origin metadata rather than guessing it.
- **Why:** Valid syntax and valid evidence support are distinct checks.
- **Status:** Decision needed
- **Feeds:** FR-039, FR-040; external result contract

## Integration

**Q5. What can leave the local portfolio in a brief?**
- **Recommendation:** Confirm recipient and authorized minimum context with explicit disclosure review before export or transmission.
- **Why:** Accessible private data is not automatically shareable.
- **Status:** Decision needed
- **Feeds:** FR-038, NFR-024; disclosure policy

## Architecture

**Q6. Does importing an agent investigation authorize executing its suggested commands?**
- **Recommendation:** Validate the structured return as untrusted data and keep action authorization separate.
- **Why:** External content cannot enlarge filesystem or operational permissions.
- **Status:** Recommended
- **Feeds:** FR-040, FR-042; security dependency

## Acceptance

**Q7. How do we demonstrate advisory separation after a successful import?**
- **Recommendation:** Import a valid recommendation and verify it remains distinguishable from deterministic findings and leaves approved state unchanged.
- **Why:** Success-path imports are where authority can be accidentally promoted.
- **Status:** Recommended
- **Feeds:** FR-040, FR-041, NFR-019

## Ambiguity

**Q8. Does acceptance mean approval to investigate, revise a plan or publish a change?**
- **Recommendation:** Agree explicit acceptance effects; preserve rejection, deferral and investigation outcomes without implicit publication.
- **Why:** Review vocabulary otherwise conceals materially different permissions.
- **Status:** Decision needed
- **Feeds:** FR-041, FR-042; recommendation review contract