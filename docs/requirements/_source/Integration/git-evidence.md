# Git Evidence

**Document:** `git-evidence.md`  
**System:** Siddhi — Portfolio Intelligence & Strategic Planning System  
**Status:** Draft for review  
**Scope:** Read-only collection and assessment of Git version-control evidence

**Related documents:** `source-integration.md`, `vyasa-integration.md`, `openspec-integration.md`, `okf-integration.md`, `data-ownership.md`, `data-model.md`, `application-workflows.md`

---

## 1. Purpose

This document defines how Siddhi collects, stores, compares, and interprets Git evidence to understand the evolution of engineering work across the portfolio.

Git provides evidence about recorded source-control activity, including commits, branches, tags, changed files, and relationships between revisions. Siddhi uses that evidence to support portfolio questions such as:

- Has a repository changed since the previous review?
- Which engineering areas have recorded changes during a period?
- What work was recorded against a particular initiative or milestone?
- Which branches or revisions contain changes that have not been integrated into a designated reference branch?
- What changed between two recorded versions?
- Is there recent source-control activity relevant to a goal?
- Which portfolio assessments need refreshing because the underlying repository changed?
- Is there enough implementation evidence to justify a stronger conclusion, or is additional verification required?

Git evidence is one input to portfolio assessment. It does not independently establish whether work is correct, complete, deployed, useful, or aligned with a business outcome.

## 2. Design principles

### 2.1 Git is authoritative for its recorded history

Git is the authority for the version-control objects and relationships observable in the repository being inspected.

Siddhi must distinguish between the history actually observed and any broader claims about the project's state. A local repository may not contain every remote branch or the latest remote changes.

### 2.2 Read-only by default

Siddhi must not modify source repositories as part of routine evidence collection.

The integration must not:

- Commit or amend changes.
- Create, delete, or rename branches or tags.
- Merge or rebase branches.
- Check out a different branch.
- Reset the working tree.
- Push or pull changes as an implicit side effect of analysis.
- Automatically resolve merge conflicts.
- Change Git configuration or repository remotes.

The integration should inspect existing local repositories or use an approved remote repository API. If the configured source is unavailable, it must report the limitation rather than silently changing the repository.

### 2.3 Evidence is not completion

The following distinctions are mandatory:

- A commit proves that a commit object exists in the observed history; it does not prove that the code passes tests.
- A changed source file proves that a recorded change touched that path; it does not prove the feature is complete.
- A commit message mentioning a goal does not prove that the goal was achieved.
- A branch being merged does not prove that the resulting functionality works.
- A tag or release reference does not prove that the software was deployed.
- Recent activity does not necessarily indicate progress; inactive work is not necessarily blocked or abandoned.

Stronger conclusions require additional evidence and explicit assessment rules.

### 2.4 Deterministic collection and analysis

Routine Git collection, normalization, fingerprinting, comparison, and reporting must be deterministic.

External AI may help interpret a selected set of changes in relation to a portfolio goal. Such interpretation is an assessment, not a substitute for recorded Git facts or verification results.

### 2.5 Preserve provenance and uncertainty

Every Git-derived record must retain sufficient provenance to identify the repository, revision, observation time, and collection method.

Siddhi must distinguish:

- Directly observed facts.
- Source-declared information.
- Derived deterministic metrics.
- Candidate associations.
- AI-generated interpretations.
- Missing or unavailable evidence.

## 3. Scope

### 3.1 Included

The integration covers:

1. Identifying repositories through Vyasa or explicit source configuration.
2. Reading accessible Git metadata and history.
3. Collecting commit, reference, tag, and changed-path evidence.
4. Comparing repository observations across snapshots.
5. Detecting changes to branch and tag references.
6. Supporting bounded history queries.
7. Linking evidence to projects, goals, initiatives, and other evidence sources.
8. Reporting repository access, scan coverage, and freshness.
9. Preserving historical observations for portfolio reviews.
10. Supporting deterministic reports and optional AI-assisted interpretation.

### 3.2 Excluded

The initial integration does not:

- Clone every repository automatically.
- Check out repositories to collect evidence.
- Modify repositories or their configuration.
- Infer feature completion from commit volume.
- Treat commit authorship as a verified person's identity.
- Treat commit timestamps as proof of working time.
- Treat branch names or commit messages as authoritative goal mappings.
- Replace OpenSpec's requirements and change status.
- Replace OKF's engineering knowledge.
- Replace CI/CD, test, security scanning, or deployment evidence.
- Require a particular Git hosting provider.
- Require all repositories to use the same branch naming convention.
- Require mandatory time tracking.

## 4. Source ownership and relationships

| Information | Authority |
|---|---|
| Repository identity and inventory | Vyasa, with the repository as source of its own Git metadata |
| Local repository location | Local environment/Vyasa where recorded |
| Git commit graph and commit objects | Git repository |
| Branch and tag references observed | Git repository or explicitly queried remote provider |
| Requirements and scenarios | OpenSpec |
| Engineering knowledge and design rationale | OKF |
| Test/build/release results | Their originating verification systems |
| Deployment state | Deployment or runtime source |
| Portfolio goals and priorities | Siddhi |
| Evidence-to-goal associations | Siddhi |
| Goal progress assessment | Siddhi |
| Recommendations and approved portfolio decisions | Siddhi |

Git-derived observations may be joined with Vyasa, OpenSpec, and OKF records, but each source's authority must remain distinct.

## 5. Integration architecture

The Git evidence integration uses the common source-adapter architecture defined in `source-integration.md`.

```text
Vyasa Project Inventory / Explicit Configuration
                    |
                    v
           Repository Resolver
                    |
                    v
          Read-only Git Adapter
                    |
                    v
      Commits, Refs, Tags, Changed Paths
                    |
                    v
          Normalization and Provenance
                    |
                    v
         Snapshot and Change Detection
                    |
                    v
          Portfolio Evidence Records
                    |
          +---------+----------+
          |                    |
          v                    v
    Deterministic         Optional External
      Analysis             AI Assessment
          |                    |
          +---------+----------+
                    |
                    v
             Siddhi Reports
```

### 5.1 Adapter responsibilities

The adapter must:

- Resolve the configured repository identity.
- Confirm that the source is a valid, accessible repository or supported remote source.
- Collect supported Git metadata without changing the source.
- Apply bounded query parameters and resource limits.
- Normalize observations into Siddhi's internal evidence model.
- Preserve the revision and observation context for each collection.
- Report partial coverage and errors.
- Expose its capabilities and limitations to the ingestion service.

The adapter must not assign strategic priority, decide that a goal is achieved, or modify portfolio decisions.

## 6. Repository discovery and access

### 6.1 Repository identity

Vyasa should be the preferred source for discovering portfolio repositories and their known locations.

Siddhi should use a stable repository identifier from Vyasa when available. If the source does not provide one, Siddhi may maintain its own configured source identifier while retaining the repository's observed origin and location.

Repository identity should not depend solely on:

- Directory name.
- Project display name.
- Current local path.
- Default branch name.

Repositories can be renamed, relocated, transferred, or mirrored. Siddhi should retain enough metadata to reconcile those changes without accidentally combining unrelated repositories.

### 6.2 Access methods

The implementation may support the following methods.

**Local read-only repository inspection**

Read an already available repository using controlled Git commands or a suitable library. This is the preferred initial method where the repository is already present.

**Remote provider API**

Use a supported API to collect accessible commit, branch, tag, and comparison metadata without requiring a local clone. Capabilities vary by provider and authentication scope.

**Existing exported evidence**

Read an approved, machine-readable repository snapshot or evidence export if available.

These methods are not equivalent. Each source configuration must state which method is being used and which evidence types it can provide.

### 6.3 No implicit checkout or fetch

The initial integration must not run checkout operations.

It should also avoid implicit fetches because fetching updates local remote-tracking references and therefore changes the local repository's metadata. If remote freshness is required, use a remote API or a separately authorized operation with an explicit policy.

The source configuration must distinguish between:

- Evidence from the currently available local repository state.
- Evidence from remote references queried directly.
- Evidence from a previous snapshot.
- Evidence that could not be refreshed.

### 6.4 Working-tree state

When Siddhi can inspect a local working tree, it may optionally record whether the tree appears clean or contains uncommitted changes.

This observation must be kept separate from committed history. Uncommitted content may not be represented in commit objects and can change independently of the recorded commit graph.

The initial release may defer working-tree inspection if it adds complexity without materially improving portfolio decisions.

## 7. Evidence types

The adapter should support the following logical evidence categories where the selected access method permits them.

### 7.1 Repository observation

Records the repository identity and observation context.

Possible fields include:

- Repository source ID.
- Repository origin as observed.
- Local location, if applicable and permitted.
- Access method.
- Observation timestamp.
- Current checked-out revision, if available.
- Observed reference state.
- Working-tree state, if collected.
- Collection status and limitations.

### 7.2 Commit evidence

A commit observation may include:

- Full commit object ID.
- Parent commit IDs.
- Author metadata recorded in the commit.
- Committer metadata recorded in the commit.
- Author timestamp.
- Committer timestamp.
- Commit message.
- Relevant changed paths.
- Change statistics where available.
- Signature-verification metadata where supported.
- Source repository and observation snapshot.

The integration must preserve the difference between author and committer metadata. Names and email addresses recorded in Git are declarations in the commit object and are not automatically verified identities.

### 7.3 Changed-path evidence

Where collected, changed-path records should capture:

- Commit ID or comparison identifier.
- Path.
- Change status, such as added, modified, deleted, or renamed.
- Previous path when available.
- Change statistics when available.
- Whether a patch or detailed diff was collected.
- Collection limits or omissions.

Binary files, large diffs, generated files, and provider API limits may prevent full patch collection. A missing patch must not be interpreted as an absence of change.

### 7.4 Branch and reference evidence

A reference observation may include:

- Reference name.
- Reference type.
- Target object ID.
- Observation time.
- Source of the observation.
- Whether the reference was local, remote-tracking, or queried from a provider.

Branch names must not be assumed to follow a fixed policy such as `main`, `develop`, `feature/*`, or `fix/*`.

A branch's existence does not establish whether it is active, approved, complete, or safe to merge.

### 7.5 Tag and release-reference evidence

A tag observation may include:

- Tag name.
- Target object ID.
- Tag object metadata, if applicable.
- Tag message and tagger metadata, if available.
- Whether the tag is annotated or lightweight, where the access method exposes this distinction.
- Signature-verification information, if collected.
- Observation time.

A Git tag is a version-control reference. It is not equivalent to a hosted release record, a deployment event, or confirmation that a release is available to users.

### 7.6 Comparison evidence

Siddhi may compare two observed revisions or reference tips to determine:

- Commits present in one revision range but not another.
- Changed paths between revisions.
- Added, removed, and modified paths.
- Change statistics.
- Differences between snapshots.
- Whether a reference advanced, remained unchanged, or moved to another target.

The comparison must record the exact base and target revisions. Branch names alone are insufficient because branch tips change over time.

Git history and comparison operations provide deterministic evidence when the selected revisions and collection rules are fixed. See the [Git log documentation](https://git-scm.com/docs/git-log) and [Git show documentation](https://github.com/git/git/blob/master/Documentation/git-show.adoc).

## 8. Normalized data model

The Git adapter must map collected data into Siddhi's internal evidence model. The following entities are logical concepts, not a commitment to a specific database schema.

### 8.1 Git Repository Observation

Represents a repository as observed at a point in time.

Suggested fields:

- Observation ID.
- Siddhi repository source ID.
- Vyasa project reference, if known.
- Origin or remote identity, if available.
- Access method.
- Observation timestamp.
- Current revision, if available.
- Coverage summary.
- Collection outcome.
- Error and warning references.

### 8.2 Git Commit Observation

Represents a commit collected from a repository.

Suggested fields:

- Observation ID.
- Repository source ID.
- Commit object ID.
- Parent object IDs.
- Commit message.
- Recorded author and committer metadata.
- Recorded timestamps.
- Changed-path summary.
- Signature-verification result, if collected.
- First-observed and last-observed timestamps.
- Snapshot reference.

### 8.3 Git Reference Observation

Represents an observed branch or tag reference.

Suggested fields:

- Observation ID.
- Repository source ID.
- Reference name and type.
- Target object ID.
- Reference source.
- Observation timestamp.
- Snapshot reference.

### 8.4 Git Change Observation

Represents a detected change between revisions or snapshots.

Suggested fields:

- Change observation ID.
- Repository source ID.
- Base revision.
- Target revision.
- Change category.
- Related commit IDs, if collected.
- Changed-path summary.
- Detection timestamp.
- Comparison method.
- Coverage and limitations.

### 8.5 Evidence and provenance

Git observations must integrate with Siddhi's shared evidence model rather than create a disconnected portfolio data model.

Every evidence record should be traceable to:

- The source repository.
- The relevant commit or reference.
- The collection snapshot.
- The time of observation.
- The query or comparison scope.
- Any access, parsing, or collection limitations.

## 9. Ingestion workflow

A typical Git ingestion run should:

1. Resolve the repository using Vyasa or explicit configuration.
2. Confirm that the selected access method is available.
3. Record the source identity and observation context.
4. Collect the configured commit-history window.
5. Collect relevant branches, tags, or other references.
6. Collect changed paths or comparison details within configured limits.
7. Normalize commit, reference, and change observations.
8. Compare the results with the last successful snapshot.
9. Record additions, changes, deletions, and reference movements.
10. Persist the observations and provenance.
11. Update freshness and scan status.
12. Make the evidence available to portfolio analysis.

### 9.1 Bounded collection

The integration must not assume that scanning an entire repository's history on every run is necessary or affordable.

The source configuration should support an explicit collection policy, such as:

- Initial bounded history scan.
- Incremental collection from a known revision.
- Reference-tip snapshot.
- Date-bounded commit scan.
- Comparison between named or recorded revisions.
- Targeted path history for a specific analysis.

The exact policy must be recorded with the observation so that reports can explain what was inspected.

An incremental scan must handle cases where the prior revision is no longer reachable from the current observed references or the repository history has been rewritten. If safe incremental continuation is not possible, the adapter must report the limitation and use a controlled rescan policy.

### 9.2 Change detection

Siddhi should distinguish:

- New commits observed.
- Existing commits newly reachable from a reference.
- Reference tips that advanced.
- References that disappeared from the observed scope.
- Tags added, removed, or retargeted.
- Changed paths between revisions.
- Unavailable or incomplete history.
- Changes in collection coverage.

A reference disappearing from a scan does not necessarily mean the underlying commits were deleted. The reference may have been renamed, removed, or excluded by a different query scope.

A failed or partial scan must not mark all previously observed commits or references as deleted.

## 10. Linking Git evidence to portfolio goals

Siddhi may associate Git evidence with portfolio entities through explicit identifiers, configured mappings, deterministic rules, or user-confirmed relationships.

### 10.1 Association methods

Possible association signals include:

1. Explicit repository-to-project links from Vyasa.
2. Explicit change or requirement identifiers in commit messages.
3. Known source paths associated with an initiative.
4. Explicit revision references in review records.
5. User-confirmed mappings between a repository and a goal.
6. A candidate association proposed by a deterministic rule or AI analysis.

Each association should record its basis and status.

Commit-message keywords and branch-name patterns may help identify candidates, but they must not automatically establish that a goal has been satisfied.

### 10.2 Cross-system evidence

Git evidence becomes more useful when correlated with other authoritative sources:

- **Vyasa:** identifies the repository and its portfolio project.
- **OpenSpec:** identifies the intended requirement or change and its declared task status.
- **OKF:** provides engineering knowledge, architectural context, and documented capabilities.
- **Verification systems:** provide build, test, quality, and release results.
- **Deployment systems:** provide deployment or runtime evidence.

For example, an OpenSpec change may be marked complete and Git may show commits affecting the relevant paths. Together, these support a stronger statement that the work was recorded and declared complete. They still do not independently prove that the resulting behavior meets acceptance criteria unless appropriate verification evidence exists.

### 10.3 Evidence sufficiency

Siddhi must evaluate evidence against the goal's actual acceptance criteria.

A documentation-only goal may be supported by relevant document changes and review evidence. A production reliability goal may require tests, operational metrics, or deployment evidence. A reusable engineering capability may require implementation, integration, and consumer evidence.

The integration must not impose a single universal formula such as commit count or changed lines to measure progress across all goal types.

## 11. Deterministic metrics and reports

Siddhi may derive deterministic metrics from Git observations, provided each metric defines its inputs, scope, and limitations.

Examples include:

- Number of commits observed in a specified interval.
- Number of changed paths.
- Number of observed branches or tags.
- Commits reachable from one observed reference but not another.
- Age of the latest observed commit.
- Time since a reference last changed.
- Number of source-control changes associated with a mapped initiative.
- Changes to specified directories or file categories.
- Differences between two repository snapshots.

These metrics are descriptive signals, not universal measures of productivity, quality, or goal completion.

### 11.1 Reporting requirements

A Git evidence report should identify:

- The repository or repositories covered.
- The time window or revision range.
- The collection method.
- The reference or revision context.
- The observation timestamp.
- The evidence collected.
- The evidence not collected.
- Any errors or limitations.
- The distinction between observed facts and derived interpretations.

Reports must not compare raw commit counts across projects as if they were directly comparable measures of value or effort.

## 12. Freshness and historical records

Git observations represent repository state at a particular time.

Siddhi should record:

- Last successful observation.
- Last attempted observation.
- Latest observed revision.
- Latest observed reference state.
- History coverage.
- Collection method.
- Source availability.
- Whether the repository may have changed since the last observation.

A historical snapshot must remain identifiable after a newer snapshot is collected.

If a branch advances or a tag is retargeted, Siddhi should record the change rather than silently rewriting the previous observation.

Where the repository has undergone a history rewrite, Siddhi should preserve prior observations and identify that current history may no longer contain all previously observed commits.

Historical observations must be sufficient to explain why a prior portfolio report reached its conclusion, subject to the agreed retention policy.

## 13. Error handling and recovery

| Failure | Expected behavior |
|---|---|
| Repository path unavailable | Preserve prior evidence and mark the source unavailable |
| Invalid repository | Report a source-access failure without attempting repair |
| Authentication failure | Report insufficient access without exposing credentials |
| Git command failure | Record the failed operation and diagnostic |
| Remote provider unavailable | Preserve prior observations and mark refresh failure |
| History too large | Apply a configured bound or report incomplete coverage |
| Missing prior revision | Report that incremental collection cannot continue safely |
| History rewritten | Preserve prior observations and record the changed history context |
| Partial reference scan | Record which reference categories were observed |
| Unsupported object or metadata | Preserve available information and report the limitation |
| Interrupted scan | Record an incomplete run and permit safe retry |
| Persistence failure | Do not mark the scan successful |
| Repository changes during collection | Report inconsistent observations where detected |

Retries must be bounded. A repeated access or authentication failure should not trigger an endless loop.

Reprocessing the same revision range must not create duplicate logical commit records or artificial progress events.

## 14. Security and operational safeguards

The Git evidence adapter must:

- Use read-only commands and access scopes.
- Avoid executing hooks or repository-defined scripts.
- Avoid trusting repository configuration to define arbitrary commands.
- Use controlled command arguments rather than interpolating untrusted paths into a shell command.
- Restrict filesystem access to configured repositories.
- Avoid reading unrelated files outside the repository scope.
- Avoid logging credentials, tokens, or sensitive remote URLs.
- Respect the access permissions of private repositories.
- Apply limits to commit history, diff size, changed-path count, and execution duration.
- Treat commit messages and repository content as untrusted text.
- Prevent prompt-like text found in commits or files from overriding system instructions in AI workflows.
- Avoid sending full patches or sensitive source code to external AI unless explicitly authorized and permitted by policy.

The implementation must also decide whether diffs are retained, summarized, or retrieved only on demand. Full patch retention may create significant storage and confidentiality risks.

## 15. Testing requirements

The integration must be tested against representative repositories and histories, including:

1. A repository with a linear commit history.
2. A repository with merge commits and multiple branches.
3. A repository with annotated and lightweight tags.
4. Commits that add, modify, delete, and rename files.
5. A repository with no tags or no additional branches.
6. A repository with a shallow or incomplete history.
7. A repository with uncommitted working-tree changes.
8. A repository whose reference advances between scans.
9. A repository whose branch or tag is deleted or retargeted.
10. A repository whose history has been rewritten.
11. A repository with missing or unavailable prior revisions.
12. A remote API response with pagination or result limits.
13. An inaccessible private repository.
14. A failed scan followed by a successful retry.
15. Repeated ingestion of an unchanged revision range.
16. A repository with very large diffs or binary files.
17. A repository with misleading branch names or commit messages.
18. A repository containing prompt-like text in commit messages or files.
19. A project with Git evidence but no OpenSpec integration.
20. A project with OpenSpec completion claims but no corresponding verification evidence.

Tests must confirm that the adapter does not modify repositories, that collection is reproducible for fixed revisions and options, and that incomplete scans do not produce false deletion or completion claims.

## 16. Acceptance criteria

The initial Git evidence integration is ready when:

- Siddhi can resolve a repository through Vyasa or explicit configuration.
- The integration can collect a bounded set of Git observations using an approved read-only method.
- Commit and reference identities are preserved.
- Relevant changed-path evidence can be collected within configured limits.
- Each observation records its repository, revision context, timestamp, and collection scope.
- Snapshots can be compared deterministically.
- Incomplete history and partial scans are explicitly reported.
- Repeated ingestion does not create duplicate logical evidence.
- Repository modifications, checkout operations, and implicit fetches do not occur.
- Git evidence can be linked to portfolio entities without treating inferred mappings as confirmed facts.
- Reports distinguish Git activity from implementation verification.
- Git evidence can be correlated with OpenSpec, OKF, and verification artifacts without merging their authority.
- Routine collection and reporting work without an LLM.
- Historical evidence remains available according to the approved retention policy.

## 17. Implementation phases

### Phase 1 — Repository discovery and local inspection

Implement repository resolution, read-only access, source identity, current revision observation, and basic commit collection.

**Deliverable:** Siddhi can inspect an existing repository without checking it out or modifying it.

### Phase 2 — History and reference evidence

Implement bounded commit history, branch and tag observations, changed-path evidence, and snapshot persistence.

**Deliverable:** Siddhi can produce a traceable repository evidence snapshot.

### Phase 3 — Incremental refresh and comparisons

Implement revision-based incremental collection, reference change detection, comparison records, and recovery from incomplete scans.

**Deliverable:** Siddhi can report changes between observations without repeatedly processing the entire history.

### Phase 4 — Portfolio correlation

Link Git evidence to Vyasa projects, OpenSpec changes, OKF knowledge, and verification artifacts where reliable mappings exist.

**Deliverable:** Siddhi can report which source-control evidence relates to a goal and what further evidence is missing.

### Phase 5 — Strategic interpretation

Add optional external AI workflows for selected changes, evidence summaries, and goal-specific assessments.

**Deliverable:** Traceable interpretations that remain separate from source-control facts and approved portfolio decisions.

---

## 18. Open questions

| ID | Question | Why it matters |
|---|---|---|
| GE-001 | Should the initial release inspect only existing local repositories, or also query remote hosting APIs? | Determines access architecture |
| GE-002 | What is the authoritative repository identity supplied by Vyasa? | Prevents duplicate or incorrect repository mappings |
| GE-003 | Which Git providers must be supported initially? | Determines remote API and authentication requirements |
| GE-004 | What is the default history window for first-time ingestion? | Controls performance and storage |
| GE-005 | Should working-tree state and uncommitted changes be collected? | Adds potentially useful but sensitive local evidence |
| GE-006 | Should full diffs be stored, summarized, or retrieved on demand? | Controls privacy, storage, and analysis capability |
| GE-007 | Which branch and tag categories should be observed by default? | Determines coverage and noise |
| GE-008 | How should history rewrites and force-pushed branches be represented? | Preserves historical accuracy |
| GE-009 | Which explicit identifiers should be used to link Git evidence to OpenSpec changes and portfolio goals? | Avoids unreliable keyword-based mapping |
| GE-010 | What retention policy applies to commit metadata, patches, and snapshots? | Balances auditability, privacy, and storage |
| GE-011 | Should commit signature verification be included in the first release? | Adds trust-related evidence but requires defined semantics |
| GE-012 | What evidence is required before Siddhi can classify an engineering goal as achieved? | Prevents Git activity from being mistaken for successful outcomes |

## 19. Related documentation

- `vision.md`
- `scope-and-roadmap.md`
- `functional-requirements.md`
- `non-functional-requirements.md`
- `system-architecture.md`
- `architectural-decisions.md`
- `domain-model.md`
- `data-ownership.md`
- `data-model.md`
- `application-workflows.md`
- `source-integration.md`
- `vyasa-integration.md`
- `openspec-integration.md`
- `okf-integration.md`
- `scanning-and-evidence.md`
- `security-and-privacy.md`

## 20. Reference material

- [Git log documentation](https://git-scm.com/docs/git-log) — commit history, revision ranges, and path-based history queries.
- [Git show documentation](https://github.com/git/git/blob/master/Documentation/git-show.adoc) — inspection of commits, trees, tags, and other Git objects.
- [GitHub REST API: commits and comparisons](https://docs.github.com/en/rest/commits/commits) — an example of remote commit and comparison evidence, including changed-file information and API limits.

These references establish available Git and provider capabilities; they do not determine which provider or access method Siddhi must use.

**Document status:** Draft for review. The repository access method, collection bounds, retention policy, and goal-evidence acceptance rules must be agreed before this document is converted into implementation-level OpenSpec requirements.