---
type: Decision
title: Human-controlled decisions
description: Separate recommendations, proposed choices, approvals, and observed execution to preserve portfolio authority and rationale.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Context

Strategic analysis can suggest consequential changes to investment, priorities,
and plans. Useful advice is not automatically authoritative, and its arrival
does not mean an owner agreed or the proposed action occurred.

# Decision

Established direction: maintain recommendations, proposed decisions, explicit
approved choices, and known execution outcomes separately. Consequential portfolio
changes remain under human control. Exact roles and proportionate confirmation
policies remain open; this draft is not itself a human approval record.

# Alternatives considered

Automatically applying model recommendations removes owner control. Treating
imported reports as approved plans confuses provenance with authority. Overwriting
a plan on every new recommendation destroys earlier reasoning. Requiring formal
approval for every minor finding can add unnecessary governance overhead.

# Consequences

Record decision authority, time, rationale, supporting context, and supersession.
New plan drafts do not replace approved revisions implicitly. Viewing a suggestion
does not approve it, acceptance is linked explicitly, and approval does not prove
execution. Repository publication requires separate authorization. Reviews can
defer a choice pending more evidence; uncertainty need not be forced into approval.

Related: [portfolio domain](../concepts/portfolio-domain.md),
[workflow coordination](../architecture/workflow-coordination.md).