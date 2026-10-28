# Historical documentation proposal

This is retained planning context, not the current workflow or an approved
document inventory. Start with the [documentation map](README.md) and
[requirements guide](requirements/README.md). The current sequence is independent
knowledge → reviewed requirement package → OpenSpec specifications/contracts →
implementation and verification. Requirement sources remain after conversion;
knowledge never depends on delivery artifacts. The original proposal follows.

---

Yes. I think that is a better approach for Siddhi. We should first create a complete documentation baseline for the backend, review and refine it, and only then separate the content into OpenSpec requirements and OKF knowledge.

The important distinction is that we are not writing every possible document in final form immediately. We are building a coherent body of engineering documentation, resolving architectural questions, and then classifying each piece according to its purpose.

## Proposed workflow

Phase 1 — Complete documentation baseline

Start here

Define Siddhi API's scope, architecture, domain model, data ownership, integration contracts, workflows, security, testing, and operations.

Phase 2 — Review and grill

Challenge assumptions, identify missing scenarios, resolve conflicting decisions, and record unresolved questions. Avoid silently turning assumptions into facts.

Phase 3 — Classify into OpenSpec and OKF

Extract behavioral requirements into OpenSpec and reusable engineering knowledge into OKF. Cross-reference related items without making knowledge dependent on requirements.

Phase 4 — Validate completeness

Verify traceability, consistency, coverage, acceptance criteria, and readiness for implementation.

## Phase 1: Proposed document inventory

I suggest the following initial set for `siddhi-api`. These are conceptual documents; we should consolidate overlapping topics where appropriate.

### 1. Product and scope

| Document                        | Purpose                                           |
| ------------------------------- | ------------------------------------------------- |
| `vision.md`                     | Why Siddhi exists and the problem it solves       |
| `scope-and-roadmap.md`          | Backend scope, exclusions, phases, and boundaries |
| `functional-overview.md`        | End-to-end capabilities and user workflows        |
| `stakeholders-and-use-cases.md` | Users, actors, use cases, and expected outcomes   |
| `glossary.md`                   | Consistent terminology across the project         |

### 2. Architecture and domain

| Document                     | Purpose                                                          |
| ---------------------------- | ---------------------------------------------------------------- |
| `system-architecture.md`     | Components, responsibilities, and interactions                   |
| `architectural-decisions.md` | Decisions, rationale, alternatives, and consequences             |
| `domain-model.md`            | Portfolio, goal, initiative, plan, review, and decision concepts |
| `data-ownership.md`          | Authority of Siddhi, Vyasa, OpenSpec, OKF, and Git               |
| `data-model.md`              | Entities, relationships, identifiers, constraints, and history   |
| `application-workflows.md`   | Refresh, analysis, planning, approval, and review flows          |

### 3. Integration and processing

| Document                     | Purpose                                                       |
| ---------------------------- | ------------------------------------------------------------- |
| `source-integration.md`      | Integration boundaries and adapter responsibilities           |
| `vyasa-integration.md`       | Project discovery and repository identity mapping             |
| `openspec-integration.md`    | Requirement and development-artifact ingestion                |
| `okf-integration.md`         | Knowledge discovery and ingestion                             |
| `git-evidence.md`            | Revision, commit, branch, and release evidence                |
| `ingestion-and-snapshots.md` | Parsing, normalization, change detection, and history         |
| `deterministic-analysis.md`  | Matching, gap detection, evidence classification, and reports |
| `external-analysis.md`       | AI briefs, structured results, provenance, and approval       |

### 4. API, persistence, and operations

| Document                           | Purpose                                                            |
| ---------------------------------- | ------------------------------------------------------------------ |
| `api-design.md`                    | Endpoint conventions, request/response models, and error semantics |
| `persistence-and-migrations.md`    | SQLite storage, transactions, schema evolution, and recovery       |
| `configuration-and-secrets.md`     | Environment configuration and credential handling                  |
| `security-and-privacy.md`          | Access boundaries, private repositories, and data sharing          |
| `testing-and-validation.md`        | Testing layers, fixtures, contract tests, and reproducibility      |
| `observability-and-diagnostics.md` | Logs, health checks, error reporting, and troubleshooting          |
| `deployment-and-packaging.md`      | Local service lifecycle and future Electron integration            |
| `non-functional-requirements.md`   | Performance, reliability, maintainability, and portability         |

### 5. Delivery and governance

| Document                    | Purpose                                                       |
| --------------------------- | ------------------------------------------------------------- |
| `implementation-roadmap.md` | Implementation order and dependencies                         |
| `risk-register.md`          | Technical risks, uncertainty, and mitigation                  |
| `open-questions.md`         | Unresolved decisions requiring owner input                    |
| `documentation-map.md`      | Document relationships and eventual OpenSpec/OKF destinations |

This inventory should be reviewed before we write the documents. Some may be combined, and we may discover additional topics during requirements grilling.

## One important rule for this process

Each document should distinguish three kinds of statements:

- Confirmed decision: explicitly agreed and ready to guide design.
- Proposal: recommended approach awaiting review.
- Open question: an unresolved issue that must not be treated as settled.

For example, Python + FastAPI and SQLite are our current proposed backend stack. The precise integration contracts, database schema, and API endpoints still need to be worked out.

We should also inspect your actual OpenSpec and OKF conventions before the final conversion, so we do not create a parallel documentation system that conflicts with either one.

My recommendation: first approve the document inventory, then author the baseline in dependency order—starting with vision, scope, functional overview, data ownership, and system architecture. Once the complete baseline has been reviewed, we can derive OpenSpec requirements and OKF knowledge from it without losing context or duplicating content unnecessarily.