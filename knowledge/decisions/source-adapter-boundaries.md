---
type: Decision
title: Source adapter boundaries
description: Proposed isolation of source access, formats, supported versions, normalization, and failure semantics.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Context

Inventory, engineering knowledge, development artifacts, revision history, and
verification records use different access methods and evolving formats.
Treating them as one homogeneous schema loses limitations and couples core logic
to external details.

# Decision

Proposed: use explicit source adapters with declared capabilities, supported
formats/versions, identity strategy, provenance, and failure reporting. Preserve
source-specific metadata while exposing consistent normalized observations.
Actual source contracts remain to be confirmed; no approval is asserted here.

# Alternatives considered

Embedding parser logic throughout the application spreads coupling. Assuming
identical repository layouts misinterprets unsupported input. Delegating all
interpretation to an AI agent makes ordinary refresh less repeatable and harder
to audit. One universal parser can obscure source-specific semantics.

# Consequences

Adapters can be tested independently with representative supported, unsupported,
malformed, and inaccessible fixtures. Explicit contracts and fixture maintenance
have cost. Unsupported input stays visible rather than silently guessed.
An adapter reports observations, not portfolio priorities or implementation
completion. Provider changes can be contained without erasing provenance.

Related: [system architecture](../architecture/system-architecture.md),
[data ownership](../architecture/data-ownership.md).