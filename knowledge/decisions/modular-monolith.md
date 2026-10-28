---
type: Decision
title: Modular monolith
description: Proposed single deployable application with explicit internal responsibility and dependency boundaries.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Context

Source integration, ingestion, portfolio modeling, analysis, reporting, and
external reasoning are distinct responsibilities. Distinct responsibilities
alone do not justify independently deployed services for a local owner.

# Decision

Proposed: implement one deployable application with explicit module boundaries.
Transport invokes application operations; core rules remain independent of
infrastructure details. Logical jobs or adapters need not be separate processes.
This draft records a proposal, not acceptance or an existing implementation.

# Alternatives considered

Microservices or multiple independently deployed services introduce network,
deployment, and cross-service consistency costs. An unstructured single module
avoids those operational costs but couples unrelated rules and impedes testing.

# Consequences

One deployment simplifies diagnosis and transactions while preserving testable
components. Boundaries still require active enforcement and clear rule ownership;
duplicating logic across application, domain, and analysis modules undermines
modularity. Shared store access needs coordination. Extract services only when
measured scale, deployment autonomy, or isolation needs justify the overhead.

Related: [system architecture](../architecture/system-architecture.md).