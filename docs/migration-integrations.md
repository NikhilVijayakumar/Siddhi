# Integration documentation migration

**Date:** 2026-10-28  
**Status:** Documentation migration; all extracted knowledge remains draft. No
product interface, behavior, provider integration, or source compatibility is approved.

## Ownership and preservation

The eight former integration documents mixed architecture, behavioral obligations,
logical schemas, checklists, implementation phases, and open questions. Their exact
original bytes are retained under the historical source paths below. These sources
are **historical, unreconciled, and non-authoritative**, not parallel maintained
behavioral packages or approved contracts. Embedded paths, cross-references, external
citations, rendering markup, proposed package trees, and contradictions are preserved
as historical text rather than silently repaired.

Original SHA-256 values were computed before archiving. File moves using the edit
interface preserved the full bodies. All eight archive checksums were compared with
those recorded originals and passed **before** redirect files were created at the
old paths. No terminal command wrote archive or redirect content.

Standalone knowledge extracts architecture, interface meaning, rationale, trust
boundaries, failure models, and unsettled choices rather than copying acceptance
checklists wholesale. Draft behavioral packages are owned separately; see the
[requirements guide](requirements/README.md). Original detailed bodies remain
available even where a focused concept deliberately omits delivery sequencing or
an illustrative physical schema. Preservation is lossless, not a claim that every
historical proposal has been reconciled or accepted.

## Source-to-destination mappings

| Original path / redirect | Exact historical source | Primary standalone draft knowledge | Draft behavioral package |
|---|---|---|---|
| [docs/Integration/source-integration.md](Integration/source-integration.md) | [source-integration.md](requirements/_source/Integration/source-integration.md) | [source adapters](../knowledge/architecture/source-adapters.md) | [source-ingestion](requirements/source-ingestion/requirement.md) |
| [docs/Integration/vyasa-integration.md](Integration/vyasa-integration.md) | [vyasa-integration.md](requirements/_source/Integration/vyasa-integration.md) | [Vyasa inventory integration](../knowledge/architecture/vyasa-integration.md) | [source-ingestion](requirements/source-ingestion/requirement.md) |
| [docs/Integration/openspec-integration.md](Integration/openspec-integration.md) | [openspec-integration.md](requirements/_source/Integration/openspec-integration.md) | [OpenSpec evidence integration](../knowledge/architecture/openspec-integration.md) | [openspec-evidence](requirements/openspec-evidence/requirement.md) |
| [docs/Integration/okf-integration.md](Integration/okf-integration.md) | [okf-integration.md](requirements/_source/Integration/okf-integration.md) | [OKF knowledge integration](../knowledge/architecture/okf-integration.md) | [okf-evidence](requirements/okf-evidence/requirement.md) |
| [docs/Integration/git-evidence.md](Integration/git-evidence.md) | [git-evidence.md](requirements/_source/Integration/git-evidence.md) | [Git evidence](../knowledge/architecture/git-evidence.md) | [git-evidence](requirements/git-evidence/requirement.md) |
| [docs/Integration/ingestion-and-snapshots.md](Integration/ingestion-and-snapshots.md) | [ingestion-and-snapshots.md](requirements/_source/Integration/ingestion-and-snapshots.md) | [ingestion, snapshots, and publication](../knowledge/architecture/ingestion-and-snapshots.md) | [source-ingestion](requirements/source-ingestion/requirement.md) |
| [docs/Integration/deterministic-analysis.md](Integration/deterministic-analysis.md) | [deterministic-analysis.md](requirements/_source/Integration/deterministic-analysis.md) | [deterministic analysis](../knowledge/architecture/deterministic-analysis.md) | [analysis](requirements/analysis/requirement.md) |
| [docs/Integration/external-analysis.md](Integration/external-analysis.md) | [external-analysis.md](requirements/_source/Integration/external-analysis.md) | [external analysis handoff](../knowledge/architecture/external-analysis.md) | [external-analysis](requirements/external-analysis/requirement.md) |

Package links are coordination targets maintained by the package-owning agent.
They do not turn historical bodies into approved requirements. The requirements
guide and architecture section index are outside this migration slice's ownership.

## Original checksums and verified archive equality

All digests are SHA-256 of raw bytes, not normalized Markdown. The archive has the
same digest as the corresponding original listed here.

| Original filename | Bytes | Original lines | Original SHA-256 | Archive equality |
|---|---:|---:|---|---|
| [source-integration.md](requirements/_source/Integration/source-integration.md) | 33065 | 773 | 7b547cffc5c38b228727380a0f3f0e05b45141675dfcc3096af2bc9e0428bb2e | Verified before redirect |
| [vyasa-integration.md](requirements/_source/Integration/vyasa-integration.md) | 28602 | 626 | 6adeb42ccc29b6fb1a3321ccaf8358eb2a7723c8e9ef930cd663de810487ee67 | Verified before redirect |
| [openspec-integration.md](requirements/_source/Integration/openspec-integration.md) | 32353 | 787 | 9ed3064ebbab948889698cdac18dae79c0245afda18890fbc56e5cf2bb7e1d5b | Verified before redirect |
| [okf-integration.md](requirements/_source/Integration/okf-integration.md) | 33697 | 704 | 08c3e0b72eb4919784f30dd956300feb5adf5e87471e6bf4446c4f3a69ec1843 | Verified before redirect |
| [git-evidence.md](requirements/_source/Integration/git-evidence.md) | 32585 | 739 | 4c53930559c4f9e49f3545edb05a38fa76c2ea12a841cf67d1470b0eefafcaea | Verified before redirect |
| [ingestion-and-snapshots.md](requirements/_source/Integration/ingestion-and-snapshots.md) | 39874 | 982 | f3cc8b55f6cbd3c547a7230c23ad2354ee96cbbfb3dc965ac33a779396dccdd9 | Verified before redirect |
| [deterministic-analysis.md](requirements/_source/Integration/deterministic-analysis.md) | 36261 | 944 | 212b3d0f9f3e2b61f269bde4e5e883d49e2acf2aefcb6df62f25a1f65ca6864e | Verified before redirect |
| [external-analysis.md](requirements/_source/Integration/external-analysis.md) | 36698 | 945 | f5ebbea757a5cafab795ac0ab09a7b6b842975b07e58fe16964a7ded1eaeb6cf | Verified before redirect |

**Preserved total:** 8 bodies, 273135 bytes, 6500 lines. The exact drafts include all
logical field catalogues, detailed workflows, acceptance checklists, examples,
implementation phases, open-question identifiers, and reference material.

## Extraction coverage and intentional classification

| Topic | Substantial knowledge retained in focused form | Detailed historical material retained without approval |
|---|---|---|
| Shared adapters | Capability/result envelope, authority, identity, normalization, provenance, read-oriented trust, retry/partial model, execution and validation rationale | Proposed source configuration fields, module tree, implementation ordering, full operation/checklist catalogues |
| Vyasa | Inventory versus portfolio responsibility, logical optional information groups, independent statuses, identity ambiguity, stale scans, refresh and failure interpretation | Proposed field contracts, four detailed workflows, readiness checklist, ten unresolved source-contract questions |
| OpenSpec | Ingested-project ownership, schema resolution, logical relationships, task/declaration/archive limits, CLI/file consistency, parser and provenance failure models | Full suggested attributes, discovery/configuration catalogues, detailed change/delta handling and compatibility tests |
| OKF | Independent taxonomy/knowledge, metadata and relationship preservation, mapping provenance, layered validation/review, freshness, scoped absence, security | Complete logical fields and validation observations, classified evidence examples, test matrix, phase deliverables, external references |
| Git | No implicit fetch/checkout, objects versus refs, exact revision comparisons, reachability/rewrite semantics, bounded observation, activity versus sufficiency | Full record fields, collection/report catalogues, working-tree/signature options, all edge-case fixtures and open policies |
| Ingestion | Capture/publication split, manifests, last-known-good state, checkpoint commit boundary, source-aware removals, failure recovery, retention constraints | Full lifecycle/capability/status catalogues, acceptance and test lists, phase sequencing, background-reference links |
| Deterministic analysis | Frozen inputs/time, explicit versioned rules, quality dimensions, authority comparisons, criterion sufficiency, finding reconciliation and reports | All example rule families, proposed model fields, date/plan details, reports/checklists, initial-rule and scheduling questions |
| External analysis | Manual structured handoff, bounded context, disclosure, claim/reference validation, advisory/review/decision split, conditional provider failure model | Provider-first historical phases, full request/provider/output catalogues, detailed review and evaluation examples, provider automation questions |

Concepts are not asserted to be lossless copies of the mixed drafts. Losslessness
is supplied by the checksum-verified archives; knowledge is a deliberate standalone
extraction. No obligation, proposed schema, or draft detail has been destroyed.

## Technology notes: observation versus assumption

The [technology index](../knowledge/technologies/index.md) links:

- [OKF format direction](../knowledge/technologies/okf-format-direction.md): locally
  observed v0.2-oriented Markdown/frontmatter and a stricter local profile; not a
  universal external bundle schema, validator contract, or trust certification.
- [OpenSpec format direction](../knowledge/technologies/openspec-format-direction.md):
  locally observed YAML configuration, named schema, version declaration, artifact
  IDs/generated locations/templates/dependencies. A schema version is not a CLI
  software version, nor evidence of support for every target project convention.
- [Vyasa contract direction](../knowledge/technologies/vyasa-contract-direction.md):
  intended inventory boundary only. No actual upstream Vyasa interface, response,
  repository, runtime, or contract test was inspected.
- [Git observation direction](../knowledge/technologies/git-observation-direction.md):
  read-oriented object/reference design, with actual tooling/provider/version and
  access compatibility explicitly unverified.

Technology notes and architecture concepts use the requested draft metadata and
generation actor/time. Their links remain inside the knowledge bundle and do not
depend on this register, the original inputs, code, or delivery artifacts.

## Outstanding decisions and tensions surfaced

1. **Real Vyasa contract.** Inspect the actual supported transport, authentication,
   native project/repository IDs, field optionality, inference/provenance, pagination,
   visibility restrictions, scan completeness, targeted read/refresh, history and
   incremental guarantees. Logical consumer fields are not evidence of real APIs.
2. **Supported schemas and formats.** Select actual OpenSpec versions/schema
   revisions/custom artifacts and actual OKF versions/profiles/validators. Confirm
   effective schema resolution, non-mutating commands, task grammar, unknown-artifact
   treatment, missing native IDs, and revision alignment for hybrid access.
3. **No evidence does not mean absence.** Absence/removal needs sufficiently observed
   scope and source semantics. Unsupported, inaccessible, unexecuted, filtered,
   malformed, moved, partial, and uncollected are not interchangeable. The exact
   assessment vocabulary and claim-specific confirmation rules remain open.
4. **Partial observation versus publication.** Preserve useful records/diagnostic
   snapshots without implying current-view replacement. Decide publication unit,
   per-source completeness gates, independently publishable subscopes, and partial
   presentation. A local transaction cannot make unrelated external reads atomic.
5. **Retained history policy.** Decide budgets for raw content, normalized versions,
   manifests, diffs, run diagnostics, and referenced reports/decisions. Address
   pruning, lineage, privacy, licensing/access constraints, and explicit loss of
   reproducibility. Fingerprints alone cannot reconstruct discarded content.
6. **Manual external handoff versus provider automation.** The historical external
   draft proposes provider APIs early; current proposed initial direction is manual
   structured brief export and result import. Preserve both the historical proposal
   and this unresolved scope distinction. Confirm serialization, disclosure approval,
   result validation and review first; provider choice, credentials, cost limits,
   scheduling, fallback and background automation are not approved by migration.
7. **Git collection policy.** Decide local/remote/export access, providers, history
   window/reference categories, working-tree scope, signatures, diff retention,
   rewrite representation, safe command policy, and association identifiers.
8. **Analysis policy.** Select initial rules, explicit reference-time semantics,
   goal-specific criteria, freshness/sufficiency thresholds, reconciliation of
   changed rules, notifications, access policy, retained inputs, and any justified
   numerical measures. Counts and declarations are not strategic outcomes.
9. **Operations and trust.** Decide refresh triggers, actual source limits and
   numerical budgets, source-local consistency, checkpoint scope/upgrade handling,
   cancellation/resumption, credential storage, privacy/export restrictions, and
   the first concrete verification source. None is settled by preserving a draft.

Historical question IDs and phased readiness statements remain exactly in their
archives. No fabricated interview answer, human verification, acceptance, or
runtime compatibility claim has been introduced.

## Scope and coordination handoff

Outputs owned by this slice: 8 exact archives, 8 old-path redirects, 8 architecture
concepts, 4 technology notes plus their index, and this migration register: **30
paths total**. No architecture section index, root knowledge index/log, requirement
package, baseline, workflow, script, application code, or product specification is
created or changed by this slice. No staging, commit, reset, or repository mutation
operation is performed.

The main agent owns architecture-index/root navigation integration and package/guide
creation. Archive contents are not independently validated as current link targets:
their legacy links and markup are intentionally untouched. The migration's active
knowledge and redirects are the maintained navigation surfaces.