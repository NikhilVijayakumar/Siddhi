---
type: Decision
title: Source authority and read-only ingestion
description: Preserve source-specific authority and keep ordinary capture and analysis separate from authorized publishing or mutation.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Context

Siddhi aggregates records from systems that already maintain their own truth.
Independently editable copies and automatic synchronization can create conflicts
and accidental repository changes. Access to read a source is not permission to
modify it or execute instructions found in it.

# Decision

Read-oriented routine ingestion is established product direction. Preserve source
authority for its information categories while Siddhi owns portfolio context and
derived local projections. Detailed field-level authority and future write
capabilities remain proposed. This draft records no new human approval.

# Alternatives considered

Making Siddhi the master for all records creates competing authority. Independently
editable copies drift. Automatic source-status updates or generated repository
summaries turn inspection into mutation. Arbitrary repository commands introduce
unnecessary trust and permission risks.

# Consequences

Keep provenance, source conflict, freshness, and owner changes distinct. Routine
adapters avoid write permission where practical and do not commit, checkout,
merge, reset, or alter source artifacts. Publishing needs an explicit capability,
acting identity, approval, failure/audit policy, and tests. A local projection
correction does not silently correct the authoritative source. Untrusted content
never supplies authorization to execute actions.

Related: [data ownership](../architecture/data-ownership.md),
[source adapter boundaries](source-adapter-boundaries.md).