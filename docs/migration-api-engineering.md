# API and engineering migration register

Date: 2026-10-28. Scope: six API/engineering drafts, standalone draft knowledge,
operational runbooks, and old-path redirects. Extraction is not approval of any
route, schema, authentication mechanism, operational policy, or release gate.
No application behavior was implemented or verified by this documentation work.

## Preservation evidence and completed redirect state

All six old API paths are now short redirects, with no retained draft bodies or
duplicate redirect blocks. API design was already replaced after an exact-byte
comparison; its archive still matches the previously recorded original SHA-256.

Before replacing the other five originals, a read-only comparison verified that
`archive.rstrip(b'\n') + b'\n\n'` equals the complete original bytes for each.
Their only discrepancies are surplus EOF newline bytes: three for configuration
and five each for the other four. **These five archives are not byte-exact.**
Their substantive source bodies are exact; reconstructing each original requires
removing surplus EOF newlines to leave exactly two final newline bytes. Original
and current archive hashes and byte counts are recorded below. No substantive
mismatch was found, and the configuration archive contains no sentinel line.
No archive was edited during this redirect-completion pass; normalization was
performed only in memory for read-only comparison, never written to disk.

All archives are **historical, unreconciled, non-authoritative** inputs. Their
future-tense claims and relative links are historical text, not maintained
contracts. Use the [requirements guide](requirements/README.md) for behavioral
reconciliation. Knowledge and owning packages remain draft, not approved behavior.

## Complete old-to-new mapping

| Old document | Standalone draft knowledge | Draft owning packages | Historical archive | Old-path state |
|---|---|---|---|---|
| [API/api-design.md](API/api-design.md) | [API boundary](../knowledge/architecture/api-boundary.md), [observability](../knowledge/architecture/observability.md), [vertical slices](../knowledge/practices/vertical-slices.md) | [api-operations](requirements/api-operations/), [persistence-recovery](requirements/persistence-recovery/), [security](requirements/security/), [engineering-quality](requirements/engineering-quality/) | [API/api-design.md](requirements/_source/API/api-design.md) | Redirect; exact archive preservation verified |
| [API/configuration-and-secrets.md](API/configuration-and-secrets.md) | [Configuration/secrets](../knowledge/architecture/configuration-and-secrets.md), [security](../knowledge/architecture/security-and-privacy.md), [credential incidents](../knowledge/runbooks/security-incidents.md) | [api-operations](requirements/api-operations/), [security](requirements/security/), [persistence-recovery](requirements/persistence-recovery/) | [API/configuration-and-secrets.md](requirements/_source/API/configuration-and-secrets.md) | Redirect; normalized archive preservation verified |
| [API/persistence-and-migrations.md](API/persistence-and-migrations.md) | [Persistence](../knowledge/architecture/persistence.md), [recovery runbook](../knowledge/runbooks/persistence-recovery.md), [testing](../knowledge/practices/testing-and-validation.md) | [persistence-recovery](requirements/persistence-recovery/), [security](requirements/security/), [engineering-quality](requirements/engineering-quality/) | [API/persistence-and-migrations.md](requirements/_source/API/persistence-and-migrations.md) | Redirect; normalized archive preservation verified |
| [API/security-and-privacy.md](API/security-and-privacy.md) | [Security/privacy](../knowledge/architecture/security-and-privacy.md), [configuration](../knowledge/architecture/configuration-and-secrets.md), [incident response](../knowledge/runbooks/security-incidents.md) | [security](requirements/security/), [api-operations](requirements/api-operations/), [engineering-quality](requirements/engineering-quality/) | [API/security-and-privacy.md](requirements/_source/API/security-and-privacy.md) | Redirect; normalized archive preservation verified |
| [API/observability-and-diagnostics.md](API/observability-and-diagnostics.md) | [Observability](../knowledge/architecture/observability.md), [diagnostic runbook](../knowledge/runbooks/diagnostics.md), [recovery](../knowledge/runbooks/persistence-recovery.md) | [api-operations](requirements/api-operations/), [persistence-recovery](requirements/persistence-recovery/), [security](requirements/security/), [engineering-quality](requirements/engineering-quality/) | [API/observability-and-diagnostics.md](requirements/_source/API/observability-and-diagnostics.md) | Redirect; normalized archive preservation verified |
| [API/testing-and-validation.md](API/testing-and-validation.md) | [Testing/validation](../knowledge/practices/testing-and-validation.md), [vertical slices](../knowledge/practices/vertical-slices.md), [recovery runbook](../knowledge/runbooks/persistence-recovery.md) | [engineering-quality](requirements/engineering-quality/), [api-operations](requirements/api-operations/), [persistence-recovery](requirements/persistence-recovery/), [security](requirements/security/) | [API/testing-and-validation.md](requirements/_source/API/testing-and-validation.md) | Redirect; normalized archive preservation verified |

## Original and current archived SHA-256 inventory

Hashes cover raw bytes, including EOF whitespace. For the five newline-only
variants, the original hash is also the hash of the in-memory normalized archive.
API design needs no normalization. These replace the obsolete pre-repair archive
inventory; the current configuration archive no longer contains a sentinel.

| Historical archive | Original bytes | Original SHA-256 | Current archived bytes | Current archived SHA-256 | Extra EOF newline bytes |
|---|---:|---|---:|---|---:|
| [API/api-design.md](requirements/_source/API/api-design.md) | 37091 | 95ccb852bf7276cb7bdfffab3cb6b510b86733f93d899e699727badc821b4df0 | 37091 | 95ccb852bf7276cb7bdfffab3cb6b510b86733f93d899e699727badc821b4df0 | 0 |
| [API/configuration-and-secrets.md](requirements/_source/API/configuration-and-secrets.md) | 29223 | d7ca06c3b18484374ee949f411955981f7df34f70972db6dda70b727b096e5d7 | 29226 | fd9b315e38720e61b623bd9bf668bb55f240f6f2a544781a802f626fc1421b01 | 3 |
| [API/observability-and-diagnostics.md](requirements/_source/API/observability-and-diagnostics.md) | 29077 | afae05d9e3700e205582478f64edbe6e67c537d80fe47b01e07bcd2868f21296 | 29082 | e6627c5fddd53147d11f47ef650ed9da558f8eb747a1fbded28ea99c4588b131 | 5 |
| [API/persistence-and-migrations.md](requirements/_source/API/persistence-and-migrations.md) | 32811 | 50bdac5f36bb4fd3b8f5f3d5260e72e706187c0bde62a6b4834cc859aa632e91 | 32816 | a21b30d98a22d5fbb7932cb7413d4857ef8f61ad7b7a307842a86ab645118e51 | 5 |
| [API/security-and-privacy.md](requirements/_source/API/security-and-privacy.md) | 35692 | 1a7d594901bf029b806cab80f65423da2029277514d073f80c1b37973335133c | 35697 | 975737c31faa24029c053ca916b14fd5f1e63ee8cd7e457786b0e799d03e4942 | 5 |
| [API/testing-and-validation.md](requirements/_source/API/testing-and-validation.md) | 36307 | cccc774ed037f13bbd6bd3974a2e17939ee3c9287230bd502ed0bad8268984da | 36312 | 0acd2a5c8a028b1a5d79d6e81f6bf309eed4d5ebcb090c60bc78c0bf79525f21 | 5 |

## Extracted coverage and independence

Five Architecture concepts cover transport/domain ports, validation/errors,
asynchronous operations, config precedence, scoped secrets, transaction and
migration safety, backup restoration, authorization, hostile inputs, privacy,
health/readiness, correlation, redaction, and diagnostic integrity.

Two Practice concepts cover layered unit/contract/integration/persistence/security
and recovery tests, deterministic fixtures, evidence limits, performance
measurement, and coherent vertical slices rather than horizontal scaffolding.
Three Runbooks cover safe triage, isolated validated restoration, and credential
or disclosure incident response. Practice navigation preserves the existing
knowledge-and-delivery-separation entry; runbooks have their own index.

All ten concepts use draft status and profile metadata with generated.by
`GitHubCopilot/GPT-6.1-Sol` and timestamp `2026-10-28T00:00:00Z`. They depend only
on in-bundle knowledge, contain no behavioral identifier dependencies, and claim
no implemented HTTP/API schema. Their focused texts replace neither behavioral
ownership nor implementation verification.

## Unresolved reconciliation and design decisions

1. **Routes and contracts:** reconcile versioned versus unversioned health and
   readiness, system info/status, generic versus resource-specific operations,
   report resources, field naming, pagination, request/error models, validation
   status mapping, versioning, deprecation, and generated-client distribution.
2. **Authentication and authorization:** choose local client handshake,
   session/capability issuance, storage, expiry/revocation, process supervision,
   sensitive-read/action permissions, minimal unauthenticated health, and remote
   client support. Loopback and CORS are not authorization.
3. **Configuration and secrets:** settle platforms, file formats/locations,
   setting-category precedence, saved versus launch overrides, store abstraction
   and failure fallback, credential rotation, activation/restart, and secure
   endpoint discovery. No plaintext fallback is inferred.
4. **Retention, privacy, and recovery:** choose retention separately for payloads,
   snapshots, provenance, decisions, reports, AI context/responses, operation
   records, logs, backups, exports, and diagnostics. Resolve deletion obligations,
   reproducibility, classification, encryption, disclosure approval, provider
   terms, and incident notification.
5. **Performance and bounds:** define representative source formats, portfolio
   size, hardware, latency/duration targets, memory/storage budgets, body/page
   limits, scan scope, concurrency, retries/timeouts, metric cardinality, and
   diagnostic bundle bounds. No numerical target is adopted.
6. **Jobs and side effects:** identify asynchronous actions, durable acceptance,
   stage/status transitions, interruption detection, resume versus fail policy,
   cancellation guarantees, duplicate provider submissions, idempotency scope,
   payload matching/retention, and concurrency preconditions. A running marker
   or absent completion event does not prove success.
7. **Persistence evolution:** select access/migration libraries, connection/journal
   policy, publication scope, staging, immutable/revisioned records, lock/ledger
   semantics, upgrade range, restore promotion, backup schedule/location, and
   export versus full-backup scope. Binary downgrade is not rollback; a backup
   file is not proof of recoverability.
8. **Validation and release:** decide mandatory automated layers, source variants,
   platform/live checks, fixtures, dependency response, CI cadence, quarantined
   test treatment, and explicit release risk acceptance. Readable scenarios and
   checklists alone do not establish executable coverage.

## Completion scope and checks

This redirect-completion pass owns only seven remaining Integration redirects,
one Architecture redirect, five remaining API redirects, and this register:
**13 redirect replacements and one register update**. The completed source
integration and API design redirects were not edited. Archives, requirements,
knowledge, scripts, workflows, application code, and Git state were not written.

Read-only checks before replacement confirmed exact archived body suffixes for
all seven Integration drafts and the Architecture decision draft, including the
original hashes in their respective migration registers. For API design, the
archive hash matches the prior exact-preservation record. For the other five API
drafts, full normalized-byte comparison passed before removal of the originals;
all differences were EOF newline bytes only. No runtime/API, production security,
or recovery verification is implied. Final redirect length, duplicate-body,
link-target, archive-hash, and editor-diagnostic checks are reported separately
when run; previous combined-bundle/index results are not asserted as current.

## Final read-only validation results

- **PASS:** all 13 replaced originals are short redirects (9–10 lines each),
  each with one title and no old draft body or duplicate redirect blocks.
- **PASS:** all 14 relevant archive hashes match the captured preservation
  evidence: seven Integration archives, one Architecture archive, and six API
  archives. Five API archives reconstruct the captured original bytes and hashes
  exactly after in-memory EOF normalization; they remain non-byte-exact on disk.
- **PASS:** obsolete blocked/pending replacement claims are absent.
- **PASS:** editor diagnostics report no errors in the 14 edited files.
- **LINK CHECK:** 148 link occurrences checked; 134 resolve. The remaining 14
  all target the [requirements guide](requirements/README.md), which does not
  exist at check time and is outside this pass's write ownership. The agreed
  guide destination is retained; no requirements file was created or edited.
  These counts describe the redirects and register before this results section
  added one further occurrence of the same guide link.
- No archive, terminal, or Git writes were performed. Runtime/API behavior,
  security controls, recovery, and combined knowledge verification were not run.