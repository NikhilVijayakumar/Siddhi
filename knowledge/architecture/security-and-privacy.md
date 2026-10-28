---
type: Architecture
title: Security and privacy trust boundaries
description: Backend authorization, hostile source handling, least privilege, data minimization, disclosure, and incident principles.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Security and privacy trust boundaries

Local portfolio information includes private project metadata, unpublished plans,
personal identifiers, credentials, and strategic decisions. Local hosting does
not establish confidentiality or authorize every process. This draft proposes
controls, not implemented authorization, penetration testing, a legal compliance
determination, or production readiness.

# Assets, threats, and enforcement

| Boundary or asset | Threat | Design response |
|---|---|---|
| Client to backend | Unauthorized requests or modified client | Backend authentication, authorization, validation |
| Repository to parser | Traversal, active content, oversized malformed input | Read-only scoped access, bounded parsing |
| Backend to provider | Disclosure or prompt injection | Approved minimal context, isolated instructions, validated output |
| Database/backups | Theft, corruption, failed upgrades | Permissions, transactions, validated recovery |
| Configuration/secrets | Broader access or credential leakage | Protected updates, scoped resolution, redaction, rotation |
| Reports/diagnostics | Sensitive output or misleading certainty | Safe rendering, minimization, provenance |
| Dependencies | Compromise or unsafe parser behavior | Controlled resolution, review, vulnerability response |

Routes check caller policy; application services enforce operation authority and
domain invariants across entry points. Persistence/adapters receive only needed
capabilities. Frontend permissions are not backend enforcement. External records
remain under source authority; read-only ingestion does not edit repositories,
inventory, knowledge packages, schemas, hooks, or CI configuration.

# Authentication and authorization remain open

Loopback is proposed default binding, not authentication. Define client handshake,
session/capability issuance, storage, expiry, restart/exit invalidation, and
operation authorization before integration. Single-user describes the audience,
not immunity to other local callers. Do not embed reusable privileged client
secrets or place credentials in URLs.

Protect sensitive reads as well as writes: diagnostics, exports, backups, paths,
and historical records. Narrow CORS to intended origins; it cannot replace caller
authorization. Remote binding needs explicit policy, transport protection, and
a reviewed deployment model, not an accidental setting.

# Untrusted filesystem, documents, and network input

Resolve roots under an explicit symlink/submodule policy and enforce containment
when opening files, accounting for races where relevant. Distinguish missing
paths from denied access. A source location is not unrestricted filesystem
authority. Scans do not check out branches, run hooks/build commands, install
dependencies, commit, push, or modify source artifacts.

Bound file counts, bytes, nesting, parsing time, archive expansion if supported,
retries, and output sizes. Unsupported versions and malformed input produce
explicit limited outcomes. Source instructions are data, not application policy.
Declared completion is not independent verification.

Embedded URLs do not authorize network requests. Supported fetching needs scheme
and destination policy, redirects/response limits, and protection against access
to private/loopback/metadata endpoints where inappropriate. Validate configured
endpoints too; indirect references must not broaden authorized scope.

Validate API schemas and state transitions, use parameterized SQL, and encode
untrusted output safely. Do not execute embedded HTML, JavaScript, shell fragments,
or model suggestions. Desktop rendering needs content isolation without needless
privileged runtime access.

# Secrets, storage, and resource protection

Use an approved credential store with scoped backend resolution. No plaintext
fallback in ordinary configuration, API echo, or secret-bearing logs, reports,
context, diagnostic bundles, and manifests. Revoking leaked credentials requires
issuer action, not merely deleting a local reference.

Restrict database, journal/WAL, backup, export, and temporary-file permissions.
Encryption at rest is an unresolved threat-model choice; ordinary SQLite is not
assumed encrypted. Transactions and migration safeguards protect the last usable
state. Hashes establish byte identity, not truth of captured claims.

Limit bodies, pages, jobs, scan scope, exports, provider calls, durations, retries,
and storage. Bounds stay safe under reconfiguration. Rotation prevents diagnostics
becoming a denial of service.

# Classification, retention, and deletion

Public, internal, confidential, and restricted are proposed categories, not an
adopted organizational policy. Accessibility is not public-disclosure approval.
Personal names, emails, usernames, and notes need a purpose and minimized collection;
applicable obligations depend on deployment and jurisdiction.

Define access, retention, export, and deletion per class/category. Disabling a
source, retiring an entity, expiring payload history, and deleting backups differ.
Preserve historical explanation where permitted, but not indefinite sensitive
retention by default. Account for exported, backup, and temporary copies.

# External analysis safety

A key does not approve transmission. Select provider, purpose, allowed context,
classification, handling terms, and required human approval before disclosure.
Exclude secrets, unnecessary paths, unrelated personal data, and indiscriminate
repository payloads. Retain safe policy/template and origin metadata.

Separate trusted instructions from retrieved excerpts; bound context and validate
output shape/evidence references. Prompt defenses cannot guarantee immunity, so
model output has no direct privileged action path. Advice requires explicit
authorized human disposition. Provider failure must not corrupt local records
or disable independent deterministic processing.

# Audit, supply chain, and response

Record safe denied-access, sensitive-setting, credential-lifecycle, disclosure,
export, migration, and recovery events without secret values. Audit needs cannot
be silently disabled by ordinary log verbosity. Avoid full payload/SQL parameter
dumps. Protect and bound logs separately from durable domain history.

Constrain dependencies, resolve reproducibly, review critical updates, assess
known vulnerabilities, and keep build credentials out of artifacts. Repository
content cannot trigger package installation during ingestion.

Contain incidents, revoke/rotate credentials, preserve minimal safe evidence,
assess scope/notification obligations, recover, validate, and record corrective
actions. See the [incident runbook](../runbooks/security-incidents.md).

# Validation and unresolved policy

Test allowed/denied access, malformed/oversized input, path escapes, read-only
scans, synthetic-secret leakage, disclosure denial, hostile model text, resource
bounds, backup permissions, and recovery. Passing tests cover tested conditions,
not absence of vulnerabilities. Resolve authorization, platforms, remote/symlink
scope, classification, encryption, disclosure, retention, audit, vulnerability
response, and incident obligations before production use.

Related: [configuration](configuration-and-secrets.md), [API boundary](api-boundary.md),
[persistence](persistence.md), [observability](observability.md),
[validation practice](../practices/testing-and-validation.md).