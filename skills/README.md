# Skill Catalog

Authoritative inventory of every skill in `skills/`, with its home category and
its role in the lifecycle.

- **Core** — required for the shared lifecycle; every change may rely on them.
- **Conditional** — required when a change has the relevant impact (testing,
  architecture, behavioral specification, review).
- **Optional** — adopt or invoke deliberately.

Use only skills present in this directory. A skill mentioned anywhere but absent
here does not exist in the repository.

## Layout

Every skill lives in exactly one category directory under `skills/`, and that
directory is the skill's home:

```
skills/
├── shared/      # lifecycle spine and cross-cutting quality
└── backend/     # boundary checklists: contracts, data ownership, SQLite, phase gates; conditional inherited Vyasa/MCP guidance
```

`openspec/config.yaml` may name only skills homed in `skills/shared/`. The
`backend` schema (`openspec/schemas/backend/`) may name shared skills and the
skills in `skills/backend/`.

Agent directories (`.opencode/skills/`, `.agents/skills/`, `.claude/skills/`,
`.github/skills/`, `.codex/skills/`) stay **flat**: one directory link per
skill name, whatever its home. `scripts/sync_skills.py` creates and verifies
those links.

## `skills/shared/`

### Core

| Skill | Responsibility |
|---|---|
| `openspec-propose` | Propose a new OpenSpec change with generated artifacts |
| `openspec-apply-change` | Implement tasks from an approved OpenSpec change |
| `openspec-update-change` | Revise an existing change's planning artifacts coherently |
| `openspec-sync-specs` | Sync delta specs from a change into main specs |
| `openspec-archive-change` | Archive a completed change |
| `openspec-git-discipline` | Branch naming, change-ID traceability, review/verification gates |
| `git-flow-branch-creator` | Create feature/fix branches per the branching model |
| `git-commit` | Conventional commit analysis, staging, and message generation |
| `git-guardrails-claude-code` | Hooks blocking dangerous git commands in Claude Code |
| `neat-freak` | Reconcile documentation and knowledge with what was implemented (closeout) |
| `knowledge-first` | Check `knowledge/` before any requirement or artifact; create missing OKF concepts first; reference them; capture lessons at closeout |

### Conditional

| Skill | Required when | Responsibility |
|---|---|---|
| `openspec-explore` | Thinking through an idea before/during a change | Socratic exploration and problem clarification |
| `grill-me` | Proposal or design needs assumptions challenged | Relentless interview to expose gaps and risks |
| `gherkin-authoring` | Writing or reviewing behavioral scenarios | Gherkin syntax and scenario best practice |
| `acceptance-test-authoring` | Specifications and tasks are approved | Turn scenarios into traceable acceptance checks |
| `spec-analysis` | Ingesting source documents for a change | Extract traceable requirements, conflicts, scope, gaps without inventing behaviour |
| `clarification-management` | Ambiguous or conflicting decisions surface | Maintain a prioritized clarification log |
| `test-driven-development` | Writing or changing production code | Red–Green–Refactor discipline |
| `test-strategy` | Planning verification; specs/tasks mention testing | Test layers and boundaries, coverage expectations, tooling decisions, requirement-ID traceability |
| `test-debugging` | Any automated check fails or flakes | Evidence-based diagnosis; product vs test vs environment vs flake |
| `pytest-skill` | Writing or changing pytest tests | Fixtures, parametrize, markers, mocking, conftest patterns |
| `code-reviewer` | Before considering a change complete | Correctness, regressions, security, scope, tests |
| `architecture-review` | Change affects architecture or interfaces | Component boundaries, data flow, quality attributes |
| `architectural-decision-records` | A durable architectural decision is (or isn't) introduced | Write/review ADRs; record explicitly when none is needed |
| `c4-diagrams` | Diagrams materially clarify boundaries or data flow | Produce C4 context/container/component diagrams |
| `code-review-security` | Reviewing any code change before merge | OWASP Top 10 / ASVS-mapped security review |
| `secrets-scan` | Before commit/merge; auditing for leaked credentials | Hardcoded keys, tokens, and secrets in code and config |
| `sca-audit` | Dependencies added, upgraded, or flagged | Known-CVE audit of dependency manifests and lockfiles |

### Optional

| Skill | Responsibility |
|---|---|
| `ponytail` | Minimal-solution discipline (YAGNI, ladder of simplicity) applied to code and design |
| `graphify` | Turn code, docs, papers or images into a knowledge graph (HTML, JSON, GRAPH_REPORT.md); query paths and concepts |

## `skills/backend/`

Named by the `backend` schema.

Siddhi's intended boundary is HTTP API, application operations, portfolio domain,
source adapters, ingestion, deterministic analysis, SQLite persistence, and an
optional manual external-analysis export/import handoff. The application remains
a skeleton; architecture and technology proposals are draft. These skills do not
approve product requirements, select providers, add dependencies, or imply that
Siddhi implements an MCP server, Google Sheets synchronization, or a
scanner/detector index architecture.

Inherited Vyasa/MCP checklists apply only to the boundary actually affected.
General contract/testing, ownership, and database checks remain relevant to
Siddhi; do not import another product's read-only-tool rules, field policies,
sync format, or architecture as Siddhi requirements. MCP-specific skills are
conditional only when an MCP interface is actually touched or selected as an
upstream source interface, not whenever local paths or credentials are involved.

| Skill | Required when | Responsibility |
|---|---|---|
| `api-contract-testing` | HTTP/application operations, source adapter calls, manual analysis export/import, or an affected CLI contract changes | Contract checks from approved contracts; flag gaps, invent nothing |
| `database-integration-testing` | SQLite schema, queries, transactions, or migrations change | Constraints, transactions, queries, migrations on a disposable database file |
| `mcp-server-review` | An MCP interface is actually touched or selected as an upstream source interface, with relevant transport/client or security impact | Conditional OWASP MCP security checklist; not a mandate for a Siddhi MCP server |
| `deterministic-scanner` | Source discovery/parsing or metadata resolution changes make its checks applicable | Conditional inherited checklist for bounded reads, evidence, and observation status; not a mandated scanner/detector architecture |
| `mcp-contract-review` | An MCP interface is actually touched or selected as an upstream source interface, with relevant tool/payload contract impact | Conditional inherited MCP checklist; reconcile read-only-tool and error rules with the approved upstream contract |
| `data-ownership-review` | Source or portfolio fields, projections, SQLite records, or import/export ownership changes | Apply ownership, precedence, machine-local isolation, and conflict checks against Siddhi's knowledge and approved behavior, not inherited Vyasa field policies |
| `phase-gate-verification` | Before declaring a roadmap phase complete | Acceptance matrix from executed checks, later-phase leak check, explicit unverified items |

## Rules for maintainers

- Vendored skills stay unmodified; each carries `UPSTREAM.md` (source,
  commit, license) and its upstream `LICENSE`. OWASP skills are CC-BY-4.0,
  which requires keeping the attribution.
- Vyasa-specific skills (`deterministic-scanner`, `mcp-contract-review`,
  `data-ownership-review`, `phase-gate-verification`) and MCP checklists are
  inherited guidance, not product scope. Legacy `docs/` pointers inside a
  checklist do not override Siddhi's ownership: `knowledge/` owns architecture
  and engineering knowledge; `docs/requirements/` owns observable behavioral
  intent; approved OpenSpec specifications refine agreed behavior. Use
  `knowledge/architecture/data-ownership.md` for Siddhi ownership context.
  Keep draft status and open decisions explicit; update authoritative project
  guidance rather than modifying skill content or vendored material.
- A skill has exactly one home. Two categories may not claim the same skill
  name — the flat agent directories could not link it. `sync_skills.py` fails
  on a duplicate name.
- Adding a skill requires a catalog entry here; then run
  `python3 scripts/sync_skills.py` to create or refresh agent references,
  `--verify` to check them, `--prune` to drop stale ones.
- Project-authored skills may declare `metadata.scope` (`shared` or
  `backend`); the sync script checks it against the skill home.
