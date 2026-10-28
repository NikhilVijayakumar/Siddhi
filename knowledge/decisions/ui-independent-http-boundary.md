---
type: Decision
title: UI-independent HTTP boundary
description: Proposed separation of desktop presentation, application rules, and persistence through an explicit compatible HTTP interface.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Context

The backend should be useful and testable before a desktop UI exists. A future
React/TypeScript/MUI/Electron client and possible other clients should not
duplicate portfolio rules or inherit internal database structure as public meaning.

# Decision

Proposed: keep desktop and backend in separate projects, communicate through
documented HTTP schemas, and keep domain and application logic independent of
React, Electron, HTTP request objects, and database access details. Manage
compatibility deliberately. This is not a recorded human approval.

# Alternatives considered

A coupled desktop/backend project can simplify early packaging at the expense
of independent delivery. Frontend business rules or direct SQLite access bypass
backend control. Shared internal models or endpoints designed only for immediate
UI screens can accidentally expose persistence details and unstable contracts.

# Consequences

Domain tests need not launch a server; backend and client can evolve independently
within an explicit compatibility policy. Validation and interface tests become
important. Startup, shutdown, packaging, origin/access controls, and compatible
release versions need coordination. Generated interface documentation helps but
does not substitute for compatibility review or a secure local service boundary.

Related: [system architecture](../architecture/system-architecture.md),
[Python and FastAPI backend](python-fastapi-backend.md).