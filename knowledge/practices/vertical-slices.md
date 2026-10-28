---
type: Practice
title: Delivering coherent vertical slices
description: Observable capabilities spanning boundary, application, domain, persistence, diagnostics, and failure verification.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Delivering coherent vertical slices

A vertical slice delivers one useful observable capability across only the layers
it needs. It is not a phase that creates every route, table, or adapter before any
outcome works. This draft practice claims no implemented example capability or
HTTP contract.

# Select a narrow outcome

Describe an actor, authorized action, input, visible result, retained state, and
failure boundary. Prefer creating/retrieving one owned goal to scaffolding the
entire resource catalogue. One supported synthetic source with truthful publication
can provide value before many adapters exist.

Keep ownership, approval, provenance, and uncertainty explicit. An early slice
must not introduce a shortcut that treats partial data as complete or model
advice as approved decisions. Safety belongs in the outcome, not solely in a
later generic hardening phase.

# Trace the complete path

| Concern | Slice question |
|---|---|
| Boundary | What bounded input and safe output does the actor observe? |
| Authorization | Who may perform or inspect the operation? |
| Application | Which use case coordinates action and errors? |
| Domain | Which invariant or transition gives the action meaning? |
| Ports | Which small repository/source/credential capabilities are needed? |
| Persistence | What commits together, and what history remains? |
| Operations | Synchronous completion or durable acceptance/status? |
| Diagnostics | How are failure and retained usable data explained safely? |
| Verification | Which success, denial, conflict, and interruption cases matter? |

Not every slice needs new infrastructure. Reuse suitable ports; add the smallest
meaningful abstraction when a real boundary appears. Avoid a generic platform
justified only by hypothetical future resources.

# Test-first execution

1. Define observable examples and the key invariant, including a negative case.
2. Add a focused failing test at the lowest meaningful layer.
3. Implement minimal domain/application behavior behind narrow ports.
4. Integrate real persistence or adapters where the outcome needs them.
5. Add transport validation, serialization, errors, and access checks.
6. Exercise the complete path with isolated data and critical failure injection.
7. Refactor with passing checks and state remaining limitations honestly.

Schema-only or fake-only checks cannot complete a persistence-dependent outcome.
Expensive end-to-end checks should not replace focused invariant tests. Use the
[layered testing practice](testing-and-validation.md).

# Coherent increments

- **Owned record:** validate a goal, enforce invariants, commit, retrieve after
  restart, reject a conflicting update, and report persistence failure safely.
- **Publication:** read one bounded format without source modification, normalize
  identity/provenance, stage and atomically publish, then show that failed/partial
  retries preserve the previous usable view.
- **Analysis:** capture one input set and rule version, generate explained findings,
  retain a report, distinguish missing evidence from execution failure.
- **Recovery:** back up consistently, restore separately, validate history and
  constraints, and promote only after verification. File creation is insufficient.

These are capability shapes, not a fixed release sequence or endpoint inventory.
Optional external analysis should not become a prerequisite for local slices.

# Scope and completion

Split work that adds unrelated outcomes, independent policy choices, or a broad
technology platform. Unknown source contracts warrant bounded investigation and
an honest unverified-support statement rather than invented integration behavior.

Completion evidence shows authorized access, invariants, durable effects where
needed, consistent errors, safe diagnostics, cleanup, and consequential failure
handling. Report failed/unavailable checks and unsupported environments. Capture
reusable lessons independently of delivery history so the practice remains useful
after individual work is finished.

Related: [API boundary](../architecture/api-boundary.md),
[persistence](../architecture/persistence.md),
[knowledge and delivery separation](knowledge-and-delivery-separation.md).