---
type: Decision
title: Versioned history and migrations
description: Proposed explicit evolution of stored schemas, source transformations, criteria, rules, and report structures.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Context

Persisted data and analysis outlive individual parser and rule versions. Storage
layout evolution differs from a changed criterion's business meaning; silently
reinterpreting old records prevents reliable historical explanation.

# Decision

Proposed: version relevant storage schemas, supported source formats,
transformations, analysis rules/configuration, criteria, and report structures.
Use explicit tested database migrations and retain meaningful plan/decision
history. Exact tools and compatibility policies remain open. No human acceptance
or safe-upgrade guarantee is asserted by this draft.

# Alternatives considered

Timeless reports and unversioned payloads hide meaning changes. Reprocessing all
history under the latest rules erases original context. Manual schema alteration,
database recreation, and untracked automatic mutation risk user data and make
upgrades difficult to reproduce.

# Consequences

History identifies versions and whether changed inputs, rules, or criteria explain
new findings. Parser changes can require deliberate reprocessing rather than
silent replacement. Upgrades need representative previous-store tests, backups,
failure/recovery behavior, and compatibility review. Migration machinery has
maintenance cost but avoids treating development convenience as safe production
evolution. Retention and privacy policies still limit what can be reconstructed.

Related: [logical data model](../architecture/data-model.md),
[source history and provenance](source-history-and-provenance.md).