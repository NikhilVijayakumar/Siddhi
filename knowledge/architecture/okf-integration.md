---
type: Architecture
title: OKF knowledge integration
description: Independent knowledge ingestion, source-native metadata and relationships, layered validation, mapping, and freshness.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# OKF knowledge integration

OKF supplies engineering context: architectural rationale, constraints, decisions,
capabilities, dependencies, and reuse opportunities. The source owns its content,
metadata, relationships, and recorded trust signals. Siddhi owns relevance and gap
assessments and portfolio mappings; cached normalized records do not become source
authority. Knowledge presence, source-declared review, and independently verified
implementation are distinct claims.

Knowledge remains useful without portfolio interpretation, and local planning
does not depend on OKF availability. No associated OpenSpec declaration is needed
for a knowledge item to be meaningful. Different bundles can have different
taxonomies and stricter profiles; an unfamiliar type can remain a generic knowledge
item rather than be discarded or forced into Siddhi's preferred categories.

# Pipeline and access boundary

Configured source → access/discovery → format/profile detection → reader/parser →
normalized concepts and relationships → snapshot/provenance → comparison/freshness →
portfolio interpretation. Logical stages can coexist in one application. Keeping
them separate limits the effect of format evolution on domain semantics.

Possible access methods include an approved filesystem root, an existing repository,
a supplied immutable repository snapshot, a supported read-only CLI, or an export.
No universal CLI/API contract is assumed. The simplest reliable method is preferred,
but direct parsing cannot silently bypass important source validation semantics,
and a CLI is not a mandatory dependency merely because one exists.

Source configuration logically records source ID/name, optional project/repository
reference, approved location, detected format/version/profile, access method,
enabled state, configuration revision, latest attempt/success, and outcome. Missing
sources are not silently replaced by another nearby bundle. Conflicting format or
profile signals need explicit resolution rather than an arbitrary selection.

# Normalized knowledge and identity

A logical concept observation can contain source ID, native concept identity,
path/URI, original type, title/description, source metadata, content/snapshot
reference, relationships, provenance, source lifecycle/review declarations,
fingerprint/revision, first/last observation, last observed content change, and
parse outcome. These are desired optional fields, not promises about every source.

Retain unknown metadata where safe and feasible. Keep source fields separate from
Siddhi-derived assessments so the latter cannot overwrite a native status. A
documented title fallback is not a stable identity guarantee. Use path-derived
identity only when that is the source convention; use path-independent IDs when
the actual format guarantees them. A rename is confirmed only with sufficient
evidence; otherwise retain reidentification ambiguity.

Fingerprint relevant content and metadata deterministically. Exclude collection
time and irrelevant serialization differences; document what is canonicalized.
Distinguish source change, parser reinterpretation, unreadable content, excluded
items, uncertain moves, additions, and adequately established removals. A failed
scan is not a mass deletion event.

# Relationships and portfolio mapping

Source-defined edges retain source/target identities, kind if declared, originating
concept, resolution state, and observation snapshot. Unresolved references can
remain useful diagnostics. Cycles in knowledge links are not inherently invalid;
graph policy depends on the relationship type.

Portfolio associations can arise from explicit stable references, configured rules,
reliable deterministic matches, analytical candidates, or human confirmation.
Retain the method and uncertainty. Similar titles, keywords, or directory proximity
can suggest candidates but cannot prove project membership or goal satisfaction.

Cross-source correlation preserves separate authorities: a concept can describe
a capability, a project declaration can propose its extension, Git can record
changes, and tests can observe behavior. Their combination does not erase the
scope of each claim or automatically establish a completed capability.

# Validation layers and trust

| Layer | What it establishes | What it does not establish |
|---|---|---|
| Access | A configured source was reachable | Full coverage |
| Parsing | The parser interpreted a document | Profile conformance or truth |
| Format/profile validation | A validator checked a particular revision and scope | Current or implemented design |
| Recorded review/verification | The source records an actor/event and claim | Independent certification |
| Portfolio assessment | Relevance or sufficiency under defined criteria | Source-authored fact |
| Implementation verification | Separate execution evidence for a revision | All strategic outcomes |

A validation observation identifies validator/version, applicable format/profile,
time, scope, source revision/snapshot, result, diagnostics, and detailed report
reference if retained. Not performed and unavailable are not successful validation.
A later source edit can make a previous validation inapplicable to current content.
Generated or verified metadata remains a source declaration with its actual scope.

Freshness can use observation times, source revision, trustworthy modification
signals, review/expiry declarations, lifecycle status, and applicable validation
age. Old does not imply false; recent does not imply correct. Thresholds require
explicit policy. Last-known snapshots and unknown current source state remain distinct.

# Capture, history, and analysis

Capture records source/configuration, run scope, discovered/parsed/accepted/rejected
counts, revisions, changes, validation, warnings, and outcome. The exact publication
and content-pruning policy is separate from collecting successful individual
observations; see [ingestion and snapshots](ingestion-and-snapshots.md).

Deterministic processing can list concepts, inspect metadata and unresolved links,
compare snapshots, identify declared stale/deprecated items, and report mapping
and evidence gaps. It does not need an LLM. Strategic reuse or investment questions
can consume selected knowledge through [external analysis](external-analysis.md),
with recommendations still attributed and advisory.

Claim-specific classifications can include confirmed, candidate, missing, unknown,
stale, conflicting, and unverified. These are analytical dimensions, not replacement
source lifecycle values or a settled universal enumeration. A scoped search finding
is not a global absence claim. See [evidence semantics](../concepts/evidence-semantics.md).

# Failure and security model

Handle failures at the smallest safe scope: unavailable source retains history;
unsupported profile produces diagnostics; one malformed concept need not discard
all others; validation failure does not authorize source repair; unresolved links
remain explicit; persistence failure prevents a success claim. Source mutation
during a read qualifies consistency. Interrupted work needs a reconciled retry.
Unchanged reprocessing does not create duplicate concepts or artificial changes.

Approved roots and path containment limit access. Documents, metadata, and embedded
prompt-like text are untrusted data. Routine reads do not execute scripts, repair
metadata, author concepts, or reorganize the source. Controlled CLI invocation uses
approved non-mutating operations and arguments, not shell interpolation. No complete
knowledge collection is shared externally by default; disclosure is explicitly scoped.

# Validation strategy and open choices

Fixtures include multiple types/profiles, extra and missing metadata, malformed
documents, unresolved/cyclic links, moves, partial access, retries, changing source,
unavailable validators, review declarations, prompt-like content, standalone
knowledge, and sparse documentation despite implementation evidence. They expose
false trust, accidental source overwrite, and false absence risks.

The locally inspected bundle establishes an OKF v0.2-oriented Markdown/profile
direction, not universal upstream implementation compatibility; see
[OKF format direction](../technologies/okf-format-direction.md). Still open: real
target versions/extensions, source locations and access methods, identity on moves,
supported metadata/edge types, validator guarantees, project association, mapping
confirmation, retention/pruning, and permitted external context size.

Related: [source adapters](source-adapters.md), [OpenSpec](openspec-integration.md),
[deterministic analysis](deterministic-analysis.md).