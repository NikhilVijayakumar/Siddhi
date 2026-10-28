---
type: Architecture
title: Git evidence collection and interpretation
description: Bounded non-mutating history observation, exact revision comparisons, reachability changes, and limits of source-control evidence.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Git evidence collection and interpretation

Git supplies recorded objects, references, and relationships between revisions.
Siddhi can use them to explain repository evolution and identify evidence needing
review. Git activity does not by itself establish correctness, deployed behavior,
business value, working time, or goal completion. This draft describes a proposed
collection and interpretation boundary, not a verified runtime integration.

The inspected repository is authoritative only for its observed history. A local
copy can be shallow, stale, filtered, or missing remote references. Vyasa supplies
inventory context where available; source-control observations, behavioral
declarations, knowledge, execution results, deployment state, and portfolio
assessments retain their separate authorities.

# Access and non-mutation

Resolve an existing repository through inventory or explicit configuration. Native
repository IDs are preferable where reliable. A directory name, display name,
local path, or default branch does not safely identify a repository across moves,
transfers, mirrors, and clones. Retain origin and environment context without
silently merging apparently similar repositories.

Access can use an existing local repository, a supported remote provider API, or
an approved export. Their capabilities differ and are recorded separately. Local
inspection is a reasonable proposed starting point when repositories already
exist; remote providers and authentication scope remain open choices.

Ordinary collection does not clone, check out, commit, amend, reset, merge, rebase,
push, pull, repair, change remotes/configuration, or create/delete references.
Even fetch changes local remote-tracking metadata and is not an implicit read.
Remote freshness can come from an approved API or separately authorized operation.
Unavailable access is a limitation, not permission to change the source.

Optional working-tree observations are separate from committed history. A clean
or dirty indication cannot stand in for the contents of a commit; uncommitted
content can change independently and may be especially sensitive. Its collection
is not assumed to be part of the initial scope.

# Logical evidence records

| Record | Useful fields | Important distinction |
|---|---|---|
| Repository observation | Source ID/origin, access method, observed revision/refs, time, coverage, outcome | Local state is not current remote state |
| Commit observation | Full object ID, parents, message, author/committer metadata and times, paths, optional signature result | Recorded names are not verified human identity |
| Changed path | Commit/comparison, status, old/new path, statistics, patch availability, omissions | Missing patch does not imply no change |
| Reference observation | Name, type, target object, local/remote-tracking/provider basis, time | Branch names do not establish lifecycle state |
| Tag observation | Target, annotated/lightweight kind if exposed, tagger/message, optional signature context | Tag is not a hosted release or deployment |
| Comparison | Exact base/target objects, method, commits/paths, time, coverage | Mutable branch names alone do not reproduce a comparison |

Logical entities connect to shared snapshots and evidence rather than becoming an
independent portfolio model. First/last observation times describe collection, not
commit creation. Author and committer fields have different meanings. Signature
verification, if collected, needs its own declared method and trust semantics.

# Bounded and incremental collection

A run fixes source, access method, query scope, observation context, and limits;
collects history and selected references/paths; normalizes and compares with a
previous applicable snapshot; persists provenance; and records coverage/freshness.
Collection policies can include bounded initial history, a date window, reference
tips, exact revision ranges, or targeted path history. Scanning every commit on
every refresh is neither necessary nor assumed affordable.

Incremental continuation depends on reachability and source semantics. A missing
prior revision, shallow history, expired API cursor, or rewrite can invalidate it.
Record the limitation and use a controlled reconciliation/rescan policy rather
than invent a complete continuation. Pagination, API limits, diff limits, binary
content, generated files, and execution duration qualify what was actually observed.

# Changes across observations

Distinguish new commit objects from existing commits newly reachable from a
reference. A reference can advance, retarget, remain unchanged, disappear from
scope, or be renamed. Tags can also be added, removed, or retargeted. A disappearing
reference does not prove that its former objects were deleted. A changed scope
can explain an apparent disappearance without any source change.

Record exact base and target objects for history comparisons. Preserve old
reference observations after rewrites; current history need not contain every
previously observed object. A partial/failed scan cannot mark all previous commits
or references removed. Reprocessing an unchanged range is idempotent and produces
no artificial progress events.

# Association and sufficiency

Repository-to-project links, explicit source IDs in messages, known path mappings,
revision references in reviews, configured rules, and user-confirmed relationships
can support evidence associations. Record basis and confirmation state. Branch
names, keywords, or model suggestions can identify candidates, not achieved outcomes.

Correlating a checked source task with matching commits supports a claim of declared
and recorded work. It still needs appropriate execution evidence to support a
claim of working behavior. A documentation outcome, production reliability goal,
and reusable capability need different evidence. No universal commit-count or
lines-changed formula measures their progress.

Commit counts, path counts, reachability differences, latest observed activity,
reference age, and directory changes can be useful descriptive metrics. Their
reports identify repository, interval/range, method, exact revision context,
observation time, collected and omitted evidence, and limitations. Raw counts are
not comparable measures of productivity, effort, quality, or strategic value.

# Failure and operational safeguards

Unavailable paths/providers preserve prior evidence and failed-refresh context.
Invalid repositories are not repaired automatically. Authentication failure,
command failure, oversized history, missing prior revisions, partial references,
unsupported metadata, interruption, source mutation during collection, and
persistence failure remain distinct diagnostics. Retry is bounded and reconciles
what was committed; authentication failures do not cause endless attempts.

Use approved roots, controlled command arguments, and read-only access scopes.
Do not execute hooks, repository-defined scripts, arbitrary diff helpers, or
commands drawn from repository text. Sensitive URLs and credentials are not log
content. Commit messages, paths, and diffs are untrusted data; prompt-like text
does not become operational instructions. Full patches are not automatically
retained or sent to external analysis.

# History policy and validation

Snapshots retain repository identity, exact revisions/references, collection
scope, timestamps, method, and limits. Retaining full diffs has different storage
and confidentiality costs from compact commit metadata. Historical traceability
does not imply unlimited copies or indefinite reproducibility; retention remains
an explicit policy in [ingestion and snapshots](ingestion-and-snapshots.md).

Fixtures cover linear/merge histories, annotated/lightweight tags, path additions,
deletions and renames, shallow history, uncommitted work, reference retargeting,
rewrites, missing prior revisions, API pagination, private access, retries, unchanged
ranges, binary/large diffs, and misleading or prompt-like messages. A project can
have Git evidence without OpenSpec, or completion declarations without execution
evidence. Source non-mutation and fixed-input reproducibility need direct checks.

Still open: local/remote/export support, provider choice, inventory identity,
history window, working-tree scope, patch retention, reference categories,
rewrite representation, association identifiers, signature verification, limits,
and criteria sufficient for particular goal claims. See
[Git technology direction](../technologies/git-observation-direction.md).

Related: [source adapters](source-adapters.md),
[deterministic analysis](deterministic-analysis.md),
[evidence semantics](../concepts/evidence-semantics.md).