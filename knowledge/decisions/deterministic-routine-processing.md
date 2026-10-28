---
type: Decision
title: Deterministic routine processing
description: Use explicit rules for ordinary capture and analysis while reserving external reasoning for attributed judgment.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Context

Routine source extraction, normalization, comparison, and reporting recur often.
Repeated free-form model interpretation makes costs, variation, and errors harder
to diagnose even when the underlying evidence is unchanged.

# Decision

Established direction: use explicit deterministic transformations and rules for
ordinary processing. Equivalent recorded inputs and rule versions produce
equivalent substantive findings. Use external reasoning for synthesis and judgment
where valuable, with attribution. This draft asserts no new human approval.

# Alternatives considered

An AI agent for every refresh creates an unnecessary provider dependency.
Free-form generation for every report weakens reproducibility. Mixing calculations
and undocumented model judgments hides which method supports a conclusion.
Avoiding external reasoning entirely would forgo useful strategic synthesis.

# Consequences

Inputs, portfolio context, criteria, and rule versions need explicit identity.
Rules and classifications can be independently tested. Reports distinguish
candidates from confirmed relationships and source changes from rule changes.
Determinism does not establish source truth or outcome achievement. External
claims remain separate, and routine local functionality remains useful without
provider access. Generation timestamps can differ without changing substantive
deterministic findings.

Related: [evidence semantics](../concepts/evidence-semantics.md),
[structured external analysis handoffs](structured-external-analysis-handoffs.md).