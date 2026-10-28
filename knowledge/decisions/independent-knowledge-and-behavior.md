---
type: Decision
title: Independent knowledge and behavioral intent
description: Keep engineering knowledge and delivery intent independently useful with explicit optional traceability rather than lifecycle coupling.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Context

Reusable engineering knowledge can exist before a current delivery need, and a
desired behavior can be recorded before sufficient supporting knowledge exists.
The two have different purposes, ownership, and lifecycles.

# Decision

Established direction: preserve independent knowledge and behavioral-intent
domains. Either can be discovered, interpreted, and assessed without requiring
the other to exist. Delivery can reference knowledge; reusable knowledge stands
alone. This agent-authored draft does not fabricate a human acceptance event.

# Alternatives considered

Requiring every knowledge item to originate from active delivery excludes useful
research and prior understanding. Treating knowledge as attachments ties its
lifecycle to temporary work. Treating desired behavior as complete engineering
knowledge erases rationale and uncertainty.

# Consequences

Independent ingestion and missing-information assessment are needed. Optional
relationships are explicit or derived by documented rules, not assumed from
co-location. Missing cross-links do not invalidate either source. Traceability
does not transfer authority or make reusable concepts dependent on temporary
delivery artifacts.

Related: [knowledge and delivery separation](../practices/knowledge-and-delivery-separation.md),
[data ownership](../architecture/data-ownership.md).