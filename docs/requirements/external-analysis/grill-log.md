# External-analysis desk review

Desk review, no interview or user confirmation. Recommended first-release goal: goal-to-evidence report, NOT an approved release choice. Manual handoff and any provider integration remain recommendations or open decisions.

Deep review 2026-10-29: every question now records the options considered, the trade-off, and a resolution. `Recommended` means a recommendation is on record and may be adopted by a draft specification; `Decision needed` means the answer needs an owner policy that the documents cannot supply.

## Intent

**Q1. Which work should remain possible when external analysis is unavailable?**
- **Options:** block analysis until a service is reachable; degrade to deterministic only; cache the last external result.
- **Trade-off:** blocking makes an optional service a dependency; deterministic degradation preserves the core product; caching an old recommendation misrepresents its freshness.
- **Recommendation:** Keep routine parsing and defined-rule reporting independent of external analysis and investigation.
- **Why:** Strategic judgment assistance is optional, not a local-operation dependency.
- **Resolution:** Ingestion, goal management and deterministic reports never call an external service. Every external feature is reachable only through the explicit handoff workflow.
- **Status:** Recommended
- **Feeds:** FR-042, NFR-019
- **Knowledge:** `knowledge/architecture/external-analysis.md`, `knowledge/concepts/evidence-semantics.md`

## Scope

**Q2. Is a manual structured handoff sufficient before integrating provider APIs?**
- **Options:** integrate a provider API first; manual export/import first; no external analysis at all.
- **Trade-off:** an API adds credentials, cost and disclosure surface before the workflow is proven; manual handoff proves the contract cheaply; dropping it removes the capability.
- **Recommendation:** Evaluate manual brief export and result import first; require a separate decision for automation.
- **Why:** A useful advisory workflow does not imply provider orchestration is needed.
- **Resolution:** First slice supports a manual brief file out and a structured result file in. Any provider API automation requires its own change with its own disclosure and credential decisions.
- **Status:** Recommended
- **Feeds:** FR-038, FR-039; transfer mode and release scope
- **Knowledge:** `knowledge/architecture/external-analysis.md`, `knowledge/architecture/security-and-privacy.md`

## Behaviour

**Q3. Can a structurally valid recommendation change approved state?**
- **Options:** import applies the recommendation; import records it for review; import rejects anything not matching current state.
- **Trade-off:** applying on import transfers authority to an external system; rejecting loses advice; recording keeps it advisory.
- **Recommendation:** Keep imports advisory and require explicit owner review and consequential operations.
- **Why:** Validation does not establish truth or strategic authority.
- **Resolution:** An import creates an advisory record only. Plan revision, association approval and publication remain separate owner operations that cite the advisory record if used.
- **Status:** Recommended
- **Feeds:** FR-040, FR-041, NFR-019
- **Knowledge:** `knowledge/concepts/evidence-semantics.md`, `knowledge/architecture/external-analysis.md`

## Data

**Q4. Which result fields and reference failures should reject or qualify an import?**
- **Options:** accept any parseable JSON; require a fixed schema and reject unknown versions; accept with warnings.
- **Trade-off:** permissive import admits fabricated references; strict rejection loses partly useful advice; a versioned envelope with warnings is both safe and usable.
- **Recommendation:** Agree a versioned structure and invalid/incomplete/unsupported-reference treatment, preserving unknown origin metadata rather than guessing it.
- **Why:** Valid syntax and valid evidence support are distinct checks.
- **Resolution:** Envelope carries schema version, source/model identity (or explicit unknown), generation time and references to known goal, finding or snapshot identifiers. Unknown schema version or unknown identifier rejects the item; absent origin is stored as unknown; other defects are warnings retained with the record.
- **Status:** Recommended
- **Feeds:** FR-039, FR-040; external result contract
- **Knowledge:** `knowledge/architecture/external-analysis.md`, `knowledge/architecture/data-model.md`

## Integration

**Q5. What can leave the local portfolio in a brief?**
- **Options:** everything the app can read; only explicitly selected items; a fixed minimum set chosen by the developer.
- **Trade-off:** broad export leaks strategy and unpublished work; a developer-chosen set may omit context the analysis needs; owner selection plus a preview is deliberate.
- **Recommendation:** Confirm recipient and authorized minimum context with explicit disclosure review before export or transmission.
- **Why:** Accessible private data is not automatically shareable.
- **Resolution:** Recommended default: the brief contains the goal statement, success criteria, and finding identifiers with categories only; no repository content, file paths, credentials or unpublished text. The owner previews the exact payload before it leaves the machine. The recipient and any wider content need an explicit owner decision.
- **Status:** Decision needed
- **Feeds:** FR-038, NFR-024; disclosure policy
- **Knowledge:** `knowledge/architecture/security-and-privacy.md`, `knowledge/architecture/external-analysis.md`

## Architecture

**Q6. Does importing an agent investigation authorize executing its suggested commands?**
- **Options:** trusted instructions; data only; data with a manual approval gate per command.
- **Trade-off:** trust turns advice into remote control; a per-command gate is safer but invites automation of execution; data-only keeps the boundary absolute.
- **Recommendation:** Validate the structured return as untrusted data and keep action authorization separate.
- **Why:** External content cannot enlarge filesystem or operational permissions.
- **Resolution:** Imported content is stored as data, never executed and never parsed as a path, command or configuration. Siddhi has no operation that runs an imported command.
- **Status:** Recommended
- **Feeds:** FR-040, FR-042; security dependency
- **Knowledge:** `knowledge/architecture/security-and-privacy.md`, `knowledge/concepts/evidence-semantics.md`

## Acceptance

**Q7. How do we demonstrate advisory separation after a successful import?**
- **Options:** a rejected import only; a successful import observed to change nothing; a manual review checklist.
- **Trade-off:** rejection tests the error path only; observing an unchanged approved state after success is the case where authority leaks.
- **Recommendation:** Import a valid recommendation and verify it remains distinguishable from deterministic findings and leaves approved state unchanged.
- **Why:** Success-path imports are where authority can be accidentally promoted.
- **Resolution:** Fixture: approved plan revision, one valid imported recommendation referencing a real finding. Expected: advisory record created with provenance, finding list unchanged, plan revision unchanged, no publication.
- **Status:** Recommended
- **Feeds:** FR-040, FR-041, NFR-019
- **Knowledge:** `knowledge/practices/testing-and-validation.md`, `knowledge/architecture/external-analysis.md`

## Ambiguity

**Q8. Does acceptance mean approval to investigate, revise a plan or publish a change?**
- **Options:** one "accepted" state with broad meaning; distinct review outcomes; acceptance applies the recommendation.
- **Trade-off:** one word hiding three permissions is dangerous; distinct outcomes cost a small vocabulary.
- **Recommendation:** Agree explicit acceptance effects; preserve rejection, deferral and investigation outcomes without implicit publication.
- **Why:** Review vocabulary otherwise conceals materially different permissions.
- **Resolution:** Review outcomes are recorded, deferred, rejected and investigated. Recorded means "available to planning"; investigated means an owner chose to look further. None of them revises a plan, approves an association or publishes anything.
- **Status:** Recommended
- **Feeds:** FR-041, FR-042; recommendation review contract
- **Knowledge:** `knowledge/concepts/evidence-semantics.md`, `knowledge/architecture/workflow-coordination.md`
