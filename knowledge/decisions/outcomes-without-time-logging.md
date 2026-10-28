---
type: Decision
title: Outcomes without mandatory time logging
description: Evaluate portfolio intent with milestones and evidence rather than compulsory timesheets or invented work-hour estimates.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Context

Siddhi aims to improve investment and outcome decisions with less administrative
overhead. Recorded activity and hours are not reliable substitutes for delivered
value, and repository history does not reveal exact working time.

# Decision

Established direction: do not require hours-per-task or hours-per-project logging.
Use goals, criteria, milestones, source observations, and explicit assessments
for planning and review. This draft captures direction without asserting a new
human approval or ruling out all voluntarily supplied effort information.

# Alternatives considered

Mandatory timesheets add entry burden and can encourage activity-based judgment.
Commit counts are easy to compute but do not measure contribution or effort.
Inferring precise working hours from commit timestamps invents unsupported facts.

# Consequences

Actual effort can remain unknown. Constraints and capacity assumptions should be
explicitly supplied and qualified rather than reverse-engineered from activity.
Review can use dates, evidence, and milestone changes without employee monitoring.
Outcome assessment still needs goal-specific criteria, not one universal maturity
or productivity score.

Related: [vision](../product/vision.md),
[portfolio domain](../concepts/portfolio-domain.md).