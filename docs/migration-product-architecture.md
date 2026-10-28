# Product and architecture migration register

Date: 2026-10-28. Scope: two Product and six Architecture originals.
Authorization covers documentation separation, not approval of product proposals.
This register is a migration audit, not a product requirement package or a second
maintained architecture description.

# Destinations and preservation

All eight originals were read fully. Their original byte hashes were captured
before edits. Content-preserving editor patches moved each body to its archive;
all eight archive hashes were checked against the captured originals **before**
old-path redirects were created. No archive header was prepended. Source detail
including illustrative package layouts, field catalogues, workflows, numerical
identifiers, and unresolved questions remains in those unchanged historical bodies.

Archives are **historical, unreconciled, non-authoritative** inputs. Their old
relative links and future-tense claims are preserved as history, not repaired or
endorsed. Maintained knowledge is standalone; behavioral reconciliation belongs
in the [requirements guide](requirements/README.md) and the eventual packages.

Package names below are **candidate destinations**, not newly allocated ownership
or settled release scope. Their files and the requirements guide are owned by
the coordinating agent and may not exist until the combined migration completes.

| Original (now redirect) | Reusable knowledge | Candidate behavioral packages | Exact historical source |
|---|---|---|---|
| [docs/Product/vision.md](Product/vision.md) | [Vision](../knowledge/product/vision.md); [portfolio domain](../knowledge/concepts/portfolio-domain.md) | [portfolio](requirements/portfolio/) | [Product/vision.md](requirements/_source/Product/vision.md) |
| [docs/Product/scope-and-roadmap.md](Product/scope-and-roadmap.md) | [Scope/roadmap](../knowledge/product/scope-and-roadmap.md); [system architecture](../knowledge/architecture/system-architecture.md) | [portfolio](requirements/portfolio/), [analysis](requirements/analysis/), [planning](requirements/planning/) | [Product/scope-and-roadmap.md](requirements/_source/Product/scope-and-roadmap.md) |
| [docs/Architecture/system-architecture.md](Architecture/system-architecture.md) | [System architecture](../knowledge/architecture/system-architecture.md); [ownership](../knowledge/architecture/data-ownership.md); [decisions](../knowledge/decisions/index.md) | [portfolio](requirements/portfolio/), [analysis](requirements/analysis/), [planning](requirements/planning/) | [Architecture/system-architecture.md](requirements/_source/Architecture/system-architecture.md) |
| [docs/Architecture/data-model.md](Architecture/data-model.md) | [Logical model](../knowledge/architecture/data-model.md); [portfolio domain](../knowledge/concepts/portfolio-domain.md); [evidence](../knowledge/concepts/evidence-semantics.md) | [portfolio](requirements/portfolio/), [planning](requirements/planning/), [analysis](requirements/analysis/) | [Architecture/data-model.md](requirements/_source/Architecture/data-model.md) |
| [docs/Architecture/data-ownership.md](Architecture/data-ownership.md) | [Ownership](../knowledge/architecture/data-ownership.md); [evidence](../knowledge/concepts/evidence-semantics.md); [authority/read-only rationale](../knowledge/decisions/source-authority-and-read-only-ingestion.md) | [portfolio](requirements/portfolio/), [analysis](requirements/analysis/), [planning](requirements/planning/) | [Architecture/data-ownership.md](requirements/_source/Architecture/data-ownership.md) |
| [docs/Architecture/domain-model.md](Architecture/domain-model.md) | [Portfolio domain](../knowledge/concepts/portfolio-domain.md); [evidence](../knowledge/concepts/evidence-semantics.md); [glossary](../knowledge/concepts/glossary.md); [logical model](../knowledge/architecture/data-model.md) | [portfolio](requirements/portfolio/), [planning](requirements/planning/), [analysis](requirements/analysis/) | [Architecture/domain-model.md](requirements/_source/Architecture/domain-model.md) |
| [docs/Architecture/application-workflows.md](Architecture/application-workflows.md) | [Workflow coordination](../knowledge/architecture/workflow-coordination.md); [portfolio domain](../knowledge/concepts/portfolio-domain.md); [human control](../knowledge/decisions/human-controlled-decisions.md) | [portfolio](requirements/portfolio/), [analysis](requirements/analysis/), [planning](requirements/planning/) | [Architecture/application-workflows.md](requirements/_source/Architecture/application-workflows.md) |
| [docs/Architecture/architectural-decisions.md](Architecture/architectural-decisions.md) | [Semantic decisions](../knowledge/decisions/index.md); [system architecture](../knowledge/architecture/system-architecture.md) | [portfolio](requirements/portfolio/), [analysis](requirements/analysis/), [planning](requirements/planning/) | [Architecture/architectural-decisions.md](requirements/_source/Architecture/architectural-decisions.md) |

# Original byte checksums

SHA-256 applies to the complete original bytes, including final newlines and
trailing whitespace; each archived file has the same value. No newline
normalization discrepancy was observed.

| Original | Bytes | Original SHA-256 (= archived SHA-256) |
|---|---:|---|
| [Product/vision.md](requirements/_source/Product/vision.md) | 12270 | 28d4525cbbbcbd8e0b1a88b96f39eaa49b5cc27dc9bc58e943407b9525bcbcbd |
| [Product/scope-and-roadmap.md](requirements/_source/Product/scope-and-roadmap.md) | 21875 | 19da8923ef97c1e565e1bb38e2487a9042b4d18324372f5320f88bd0c4740f9c |
| [Architecture/application-workflows.md](requirements/_source/Architecture/application-workflows.md) | 34966 | 5387348c98291478f827592e7c5fcf36c6c2886e09fba1a70b01224a1112a708 |
| [Architecture/architectural-decisions.md](requirements/_source/Architecture/architectural-decisions.md) | 24948 | 52724b6bab0a1cb0f7776609602190a92998cd18c77824fc161958735a26217f |
| [Architecture/data-model.md](requirements/_source/Architecture/data-model.md) | 38778 | 48322d6ea7226f9ec698cf5c8df67e1cd1985bc8bd06702422e4035dbeee7f92 |
| [Architecture/data-ownership.md](requirements/_source/Architecture/data-ownership.md) | 27506 | 175071b8cf9bfc7aab3333853eb07f9ccc77d7f0c74a3750e46a599628ca8072 |
| [Architecture/domain-model.md](requirements/_source/Architecture/domain-model.md) | 23797 | df8d6fe4facd6caf026a090fb3c748b1a106265c153d6023ed834aad09dce812 |
| [Architecture/system-architecture.md](requirements/_source/Architecture/system-architecture.md) | 31086 | 00e840826cd706f7fe41a9ef26b6c4ebe15cdd5da3bb55efcde88123d9af2277 |

# Historical ADR identifier conflicts

The system architecture's ten-item summary and the consolidated twenty-item
decision register use the same ADR numbers for different subjects. For example,
ADR-002 means SQLite in the former and FastAPI in the latter. No historical ID is
adopted as an extracted concept's identity. The following subject mapping records
the relationship without renumbering history or implying acceptance.

| Subject | System architecture summary | Consolidated decision register | Draft semantic concept |
|---|---|---|---|
| Python / FastAPI | ADR-001 (combined) | ADR-001 / ADR-002 | [Python/FastAPI](../knowledge/decisions/python-fastapi-backend.md) |
| SQLite / local-first operation | ADR-002 / local operating model | ADR-003 / ADR-020 | [Local-first SQLite](../knowledge/decisions/local-first-sqlite.md) |
| Modular monolith | ADR-003 | ADR-004 | [Modular monolith](../knowledge/decisions/modular-monolith.md) |
| Separate frontend, independent rules, HTTP compatibility | ADR-004 / component boundaries | ADR-005 / ADR-006 / ADR-019 | [UI-independent boundary](../knowledge/decisions/ui-independent-http-boundary.md) |
| Source adapters | ADR-005 | ADR-007 | [Adapter boundaries](../knowledge/decisions/source-adapter-boundaries.md) |
| Snapshots and provenance | ADR-006 | ADR-008 | [History/provenance](../knowledge/decisions/source-history-and-provenance.md) |
| Source authority / routine read-only access | Ownership table / ADR-010 | ADR-009 / ADR-014 | [Authority/read-only](../knowledge/decisions/source-authority-and-read-only-ingestion.md) |
| Independent knowledge and behavioral intent | Independent-source explanation | ADR-010 | [Independent domains](../knowledge/decisions/independent-knowledge-and-behavior.md) |
| Deterministic routines | ADR-007 | ADR-011 | [Deterministic processing](../knowledge/decisions/deterministic-routine-processing.md) |
| Recommendation versus approval | ADR-008 | ADR-012 | [Human-controlled decisions](../knowledge/decisions/human-controlled-decisions.md) |
| Structured external handoff | ADR-009 | ADR-013 | [Structured handoffs](../knowledge/decisions/structured-external-analysis-handoffs.md) |
| Versioning and migrations | Persistence / reproducibility explanations | ADR-015 / ADR-017 | [Versioned history/migrations](../knowledge/decisions/versioned-history-and-migrations.md) |
| Workload-driven background jobs | Long-operation explanation | ADR-016 | [Proportionate execution](../knowledge/decisions/proportionate-background-execution.md) |
| No mandatory time logging | Product planning direction | ADR-018 | [Outcomes without time logging](../knowledge/decisions/outcomes-without-time-logging.md) |

The consolidated register labels independence, determinism, human control,
read-only processing, and no mandatory time logging “Accepted design principle.”
Extraction describes these as **established direction**, not independently
verified human approvals. Other implementation-specific choices remain **proposed**.
All 23 extracted concepts have draft metadata and no invented verification actor.
Explicit alternatives combine the original rationale with analytical comparison;
they do not claim a historical owner interview occurred.

# Unresolved semantic and design issues

1. **Goal versus intention/outcome:** the domain text calls a goal a desired
   result, while the logical model also treats it as strategic intention with
   separate outcomes. Vision and planning examples sometimes speak as though
   success criteria already exist. Whether creation needs outcomes, whether they
   may be added later, and whether a goal can remain outcome-free are unresolved.
   Knowledge explains intention, observed result, and assessment separately rather
   than silently making one draft authoritative.
2. **Direct project-to-goal links:** the logical model and workflow describe a
   lightweight direct link, while the domain model leaves its availability open.
   Preserve it as a proposal, not a reconciled cardinality rule.
3. **Plan versus revision/milestone membership:** the domain text describes plans
   as versioned arrangements with milestones, while the logical model associates
   milestones to a plan identity and separately stores revisions. Mutable milestone
   dates/status can rewrite what an earlier approved revision appeared to promise.
   Revision-owned membership, versioned milestone values, and current/approved
   revision pointers require explicit design. No finalized table mapping is inferred.
4. **Source refresh publication:** “preserve completed stages” and “do not replace
   the last valid snapshot on failure” need a defined per-source, per-project, or
   whole-refresh publication boundary. Retaining captured observations and
   promoting a new current usable state are not the same operation.
5. **Status and evidence vocabulary:** certainty, sufficiency, freshness,
   verification, processing outcome, approval, and execution are distinct. Proposed
   enum lists overlap and are not agreed transitions. Missing evidence is not an
   established gap; declared completion is not observed successful execution.
6. **External analysis automation:** architecture and scope favour initial
   export/import, whereas one workflow invokes an external service. Direct provider
   automation, scheduling, and disclosure consent remain unresolved rather than
   automatically included in the first release.
7. **Initial usable release:** deterministic discovery-to-report is proposed;
   whether plan creation/review must be included remains open. Roadmap phases and
   workflow priorities are not approved release boundaries.
8. **Operational policies:** confirm actual Vyasa contract, supported formats,
   local versus remote-only coverage, access/approval identity, correction and
   retention rules, sensitive payload deletion, history/reproducibility budgets,
   export/restore, concurrency, and persistent-job recovery. Extraction approves
   none of these implementation choices.

# Ownership handoff and checks

Created: 23 concepts (2 Product, 4 Architecture, 3 Concept, 14 Decision), plus
product/concepts/decisions section indexes, 8 exact archives, 8 redirects, and this
register. The coordinating agent owns the combined architecture index and root
knowledge navigation/log. No shared architecture index was written here.

Read-only checks confirmed all eight archived SHA-256 values before redirects.
Final concept/profile/link and combined-bundle check outcomes are recorded below
after validation. Baseline requirements, package allocation, scripts, workflow,
application behavior, and Git staging are outside this migration slice.