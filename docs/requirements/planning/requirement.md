# Planning and reviews

- **Status:** Draft; NOT approved for implementation.
- **Owns:** FR-003, FR-031, FR-032, FR-033, FR-034, FR-035, FR-036

## Scope and outcomes

| Baseline | Observable acceptance outcome |
|---|---|
| [FR-003](../functional-requirements.md#fr-003--manage-initiatives) | Coordinate multiple goals and projects in an initiative that can precede a repository and retain disposition decisions. |
| [FR-031](../functional-requirements.md#fr-031--create-and-revise-plans) | Create and revise outcome-oriented plans with relevant activities, milestones, dependencies, dates, assumptions and risks without universal stages. |
| [FR-032](../functional-requirements.md#fr-032--preserve-plan-versions) | Retrieve prior plan versions and revision rationale where supplied; advice does not overwrite an approved plan. |
| [FR-033](../functional-requirements.md#fr-033--track-milestones-and-dependencies) | Inspect milestone dates, status and links with incomplete or inconsistent dependencies explicitly uncertain. |
| [FR-034](../functional-requirements.md#fr-034--support-execution-reviews) | Compare execution against the plan, new evidence, milestones, blockers, risks and the prior review, retaining proposed actions and decisions. |
| [FR-035](../functional-requirements.md#fr-035--support-strategic-reviews) | Review outcomes, available commercial results, internal investments, neglected goals and trade-offs without automatic commercial or internal-work preference. |
| [FR-036](../functional-requirements.md#fr-036--preserve-review-and-decision-history) | Retrieve reviews, proposed actions, decisions and rationale with recommendation, pending, approved and evidenced implementation states distinguished. |

## Out of scope

Automatic priority changes, mandatory time accounting, invented commercial metrics, fixed workflow stages and repository publication. Initial weekly execution and monthly strategic cadences are baseline starting points, not inflexible scheduling rules.

## Data and integration boundaries

Siddhi owns initiatives, plan versions, reviews and decision records. Reviews reference captured source evidence rather than rewriting it. Approval does not establish execution. Review scheduling, lifecycle fields and decision transitions require later contracts.

## NFR responsibilities

No NFR is owned here. Consume persistence-recovery's historical and referential integrity controls and analysis's qualified report comparisons; engineering-quality owns test strategy.

## Cross-package dependencies

- [portfolio](../portfolio/requirement.md): goal identity, constraints and FR-006 cross-entity history.
- [analysis](../analysis/requirement.md): attributed findings and historical differences.
- [external-analysis](../external-analysis/requirement.md): reviewed advice, not automatic plan revisions.
- [persistence-recovery](../persistence-recovery/requirement.md): durable plan and review versions.

## Unresolved questions

Minimum plan shape, milestone dependency rules, approval authority, review triggering and representation of commercial results remain open. The recommended first release is a goal-to-evidence report, NOT an approved release choice; planning breadth must be confirmed. See [grill log](grill-log.md).

## Acceptance drafts

Features are non-executable acceptance drafts, with no runner or step definitions. They do not prove application behavior or owner agreement.

## Knowledge References

- `knowledge/concepts/portfolio-domain.md` — initiatives and outcome relationships.
- `knowledge/architecture/workflow-coordination.md` — reviews and explicit decisions.
- `knowledge/architecture/data-model.md` — versioned planning records.
- `knowledge/concepts/evidence-semantics.md` — approval versus execution.
- `knowledge/product/scope-and-roadmap.md` — proposed delivery sequencing.
- `knowledge/practices/knowledge-and-delivery-separation.md` — recommendation status.