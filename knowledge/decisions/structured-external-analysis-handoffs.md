---
type: Decision
title: Structured external analysis handoffs
description: Proposed initial export/import workflow for bounded evidence briefs and attributed strategic recommendations.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Context

Strategic synthesis can help compare opportunities and trade-offs, but routine
portfolio work should not depend on one model vendor or automated provider calls.
Disclosure of source content needs deliberate scope and permission.

# Decision

Proposed: begin with structured evidence-brief export and structured result import.
Record question, selected inputs, constraints, limitations, origin, assumptions,
uncertainty, and recommendations. Add direct provider adapters when justified.
No provider automation or human approval is implied by this draft.

# Alternatives considered

Immediate multi-provider integration adds credentials, failure modes, and upkeep.
A proprietary single-provider workflow risks lock-in. An agent for every operation
undermines the deterministic foundation. No external analysis at all loses useful
judgment beyond explicit rules. Direct invocation remains a possible later path.

# Consequences

Input/output structures and reference validation are needed. Manual transfer may
be part of the initial experience. Valid structure does not verify claims; results
retain provenance and review status. Authorized disclosure and redaction precede
sharing, and provider terms affect retained content. Recommendations remain
separate from approved decisions. Provider failure does not invalidate local
evidence or previous reports.

Related: [workflow coordination](../architecture/workflow-coordination.md),
[human-controlled decisions](human-controlled-decisions.md).