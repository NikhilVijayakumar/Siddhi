---
type: Decision
title: Local-first SQLite deployment
description: Proposed single-owner local service and transactional store without mandatory hosted infrastructure.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Context

The initial audience is one portfolio owner working with local engineering
sources. Durable goals, plans, snapshots, reports, and decisions are needed,
but a separate database server would add operational overhead.

# Decision

Proposed, pending review: start with a local Python service and SQLite database,
using explicitly configured source access and a dedicated persistence boundary.
Neither local deployment nor SQLite selection is presented as human-approved
by this draft.

# Alternatives considered

PostgreSQL offers server-oriented concurrency with additional operation.
MongoDB changes the modeling trade-offs without removing history needs.
Cloud databases and mandatory multi-tenant hosting add dependencies and exposure.
Files-only persistence is simple to inspect but complicates coordinated relational
updates and queries. Distributed services are not justified by initial scope.

# Consequences

Deployment is simpler and portfolio data stays locally controlled, but write
concurrency, transaction duration, history growth, file permissions, migrations,
backups, and recovery still need design. Remote integrations can require network
access. Local HTTP access still needs protection. A later server database or
multi-user deployment requires deliberate migration and review, not a promise
of effortless substitution.

Related: [logical data model](../architecture/data-model.md),
[versioned history and migrations](versioned-history-and-migrations.md).