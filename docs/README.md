# Documentation map

Siddhi's documentation has two maintained tracks and one historical input area.
The application remains a skeleton; architecture and requirements are draft.

| Area | Authority | Start here |
|---|---|---|
| Reusable product and engineering knowledge | Independent OKF v0.2 concepts | [Knowledge index](../knowledge/index.md) |
| Behavioral intent and acceptance drafts | Requirement baselines and owned packages | [Requirements guide](requirements/README.md) |
| Agreed change behavior and implementation planning | Reviewed OpenSpec changes, later capability specs | [Workflow configuration](../openspec/config.yaml) |
| Migration history | Source mappings and retained unreconciled inputs, not maintained behavior | [Migration report](documentation-migration.md) |

## Dependency direction

Requirements reference knowledge. Later specifications retain requirement IDs
and cite knowledge. Implementation and tests follow specifications. Knowledge
never depends on requirements, specifications, changes, or code. Requirements
remain available after specification conversion; conversion is not deletion.

The former Product, Architecture, Integration, and API paths are redirects. Their
detailed mixed drafts are retained only as [historical inputs](requirements/_source/README.md),
so proposed fields, routes, workflows, and unanswered questions are not lost or
silently treated as approved contracts.

## Next delivery work

Choose a concrete useful release outcome, inspect the real upstream interfaces,
and review the relevant package's grill log one question at a time. Only after
decisions are resolved or explicitly accepted should a product change derive
specifications, contracts, design, tasks, implementation, and executed tests.