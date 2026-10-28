---
type: Decision
title: Source history and provenance
description: Proposed identifiable observations and transformation history for explainable portfolio comparisons without indiscriminate source copying.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Context

Sources change or become inaccessible, and analysis rules evolve. A report that
retains only its conclusion cannot explain what was known at decision time or
whether later differences came from changed evidence or changed rules.

# Decision

Proposed: preserve normalized source observations, identifiable snapshots, and
traceable identity, revision, time, and transformation context sufficient for
the intended historical explanation. Separate observations from assessments.
Payload depth, retention, and snapshot publication unit remain unresolved;
this draft does not approve a storage schema or claim complete reproducibility.

# Alternatives considered

Latest-state-only storage loses history. URLs alone depend on continued source
availability. Summaries alone lose evidence context. Copying all repositories
maximizes storage and disclosure without necessarily providing useful provenance.
Hashes/references, selected normalized fields, full payloads, and hybrid/delta
storage have different reconstruction and privacy trade-offs.

# Consequences

Historical comparisons become explainable when required inputs and versions are
retained. Stable source identity, correction rules, retention budgets, and privacy
deletion policies are necessary. Historical observations remain historical, not
implicitly current. A failed refresh preserves last-known usable data with
qualification. Reproducibility claims are limited when input payloads or rule
versions cannot be recovered.

Related: [logical data model](../architecture/data-model.md),
[evidence semantics](../concepts/evidence-semantics.md).