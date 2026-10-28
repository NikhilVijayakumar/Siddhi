---
type: Decision
title: Python and FastAPI backend
description: Proposed data-oriented backend stack with validated HTTP contracts and framework-independent core rules.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Context

Siddhi combines diverse artifact parsing, normalization, deterministic analysis,
reports, persistence, and optional external reasoning. An independent client
needs a documented interface without a heavyweight web-platform dependency.

# Decision

Proposed, not confirmed: use Python for backend processing and FastAPI with
Pydantic for HTTP validation and interface documentation. Keep portfolio rules
outside route handlers and test them without a running HTTP service.
This draft does not attest human approval or implementation.

# Alternatives considered

Kotlin/Spring offers strong type safety and mature service architecture.
TypeScript/Node can align client and server language but does not inherently
simplify data/AI workloads. Flask and Django are viable Python frameworks with
different conventions and platform scope. A command-line-only interface would
not serve the intended independent client; direct database access bypasses the
application boundary.

# Consequences

Python fits parsing and automation ecosystems but needs deliberate typing,
validation, dependency management, linting, and tests. FastAPI reduces interface
boilerplate but does not maintain compatibility automatically. Request/response
schemas need independent review; domain meaning is not defined by generated
documentation. The client can still use TypeScript.

Related: [system architecture](../architecture/system-architecture.md),
[UI-independent HTTP boundary](ui-independent-http-boundary.md).