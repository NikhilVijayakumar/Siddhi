---
type: Decision
title: Proportionate background execution
description: Proposed measured introduction of job tracking and recovery without premature distributed orchestration.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Context

Local edits can be quick, while source scans and broad analyses can exceed a
reasonable interactive request. Responsiveness, cancellation, and interruption
recovery are separate concerns from whether work runs in another thread or process.

# Decision

Proposed: keep short operations synchronous where appropriate and introduce
background execution with observable state only where runtime and recovery needs
justify it. Persistence of job state is a deliberate choice, not implied by the
word “background.” No initial queue technology or human approval is claimed.

# Alternatives considered

All-synchronous processing can block clients during large scans. A distributed
queue from the outset adds operational dependencies. Making every operation
asynchronous creates unnecessary lifecycle overhead. In-memory background work
alone cannot guarantee recovery after process interruption.

# Consequences

Define stage scope, status, retry safety, cancellation, partial completion,
publication boundaries, and concurrency conflicts. Stable identities support
idempotent retries without duplicate logical evidence or decisions. A failed
stage does not erase independently completed work. Persistent jobs may be needed
for recovery, but a message broker is not automatically required. Choose based
on measured workload and the selected failure model.

Related: [workflow coordination](../architecture/workflow-coordination.md),
[modular monolith](modular-monolith.md).