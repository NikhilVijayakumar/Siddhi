---
type: Architecture
title: Configuration and secret boundaries
description: Typed setting ownership, proposed precedence, scoped credentials, activation, and configuration evolution.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Configuration and secret boundaries

Configuration describes behavior; secrets grant access. They need different
storage, resolution, inspection, export, and recovery policies. This is proposed
architecture, not confirmation of a settings interface, credential store, local
authentication mechanism, or reload implementation.

# Categories and ownership

| Category | Examples | Proposed authority |
|---|---|---|
| Runtime | Binding, port, process behavior | Validated launch configuration |
| Application | Logging, limits, enabled capabilities | Typed application settings |
| Persistence | Database and backup location | Controlled local configuration |
| Source | Stable ID, endpoint/root, refresh policy | Backend-owned connection metadata |
| Provider | Adapter, model, timeout, disclosure policy | Backend-owned non-secret settings |
| Credentials | Tokens, private keys, session material | Approved secret mechanism |
| Preferences | Display and report defaults | Explicit client/backend ownership |

Retaining a source endpoint does not authorize changing its records, repository
configuration, hooks, schemas, or inventory. Default integration access is
read-only. Disabled sources are not accessed by background work; historical data
remains available with its freshness limitations.

# Typed settings and proposed precedence

Every setting needs a name, type, default, safe range, owner, origin, sensitivity,
validation, activation behavior, and compatibility policy. Unknown or conflicting
settings need useful diagnostics rather than hidden behavior.

The proposed low-to-high runtime order is built-in defaults, installation/user
files, environment overrides, explicit startup arguments. Support only needed
sources; specify merge order if multiple files are enabled. TOML, YAML, and JSON
remain candidates, not an established file schema.

Persisted user-managed settings are a separate category: reload must not silently
overwrite an authorized saved preference. Decide per setting whether a launch
override temporarily masks persistence or rejects conflicting sources. Safe
inspection shows the winning origin and effective value.

Secrets have their own resolution policy, not inherited ordinary precedence.
Do not silently substitute credentials after resolution failure. Availability
can be reported without revealing values.

# Validation and defaults

Validate types, ranges, path permissions, database usability, binding policy,
enabled integration settings, provider/model support, and required references
before unsafe activation. Invalid security-critical values fail safely or disable
the affected capability, never trigger insecure fallback. An absent optional
provider key must not block local deterministic operation.

Default to loopback, disabled remote exposure/external disclosure, and bounded
concurrency, timeouts, retries, inputs, and retention. Actual numeric defaults
need measurement and policy approval. If ephemeral ports are supported, report
the assigned endpoint to the authorized launcher through a secure handshake.

Resolve roots under an explicit traversal/symlink policy. Distinguish missing
paths from denied access. A configured path does not authorize creating, deleting,
or scanning unrelated directories. Do not keep user data in source repositories
by default. Protect configuration files that reveal operational details.

# Credential storage and lifecycle

Native desktop stores are candidates: Windows Credential Manager, macOS Keychain,
and Linux Secret Service. Supported platforms and abstraction remain unresolved.
If no approved store is available, require an explicit fallback decision; never
silently persist plaintext in ordinary settings or tables. Isolated automation
may use approved environment injection with leak controls.

Ordinary configuration retains scoped credential references, not values. Backend
resolution supplies only what the current adapter needs. Avoid a global object
containing all resolved secrets. Clients do not receive provider keys merely to
select providers or request analysis.

The lifecycle is supply, store, associate, validate where authorized, use, rotate,
disable, and remove. Replacement must not leave partially applied associations.
Removing a reference does not revoke an external credential; revocation occurs
at the issuer. Never embed privileged reusable client secrets or use token URLs.

# Activation, versioning, and recovery

Classify updates as immediate, future-operation-only, or restart-required. Log
level may be reloadable; database location and binding normally need controlled
restart or migration. Validate before activation and apply coherent versions
atomically. Long operations normally retain their starting non-secret settings
identity rather than silently changing behavior mid-run.

Configuration evolution differs from database evolution. Detect format version,
validate old values, transform deterministically, preserve valid user settings,
save safely, and reject unsupported/ambiguous transformations. Keep a recoverable
copy for destructive file updates. Historical snapshots contain safe policy
versions or credential references, never resolved secrets.

# Inspection, backups, and diagnostics

Safe inspection shows name, safe effective value, origin, validation, restart
need, reference presence, and last check time. Redact headers, keys, secret URL
parameters, private paths, and sensitive endpoints, including at debug level.

Backup policy must explicitly identify included non-secret configuration.
Restoring SQLite does not restore OS credentials, issuer revocation state, or
launch settings. Revalidate restored associations without automatic disclosure
or broader source access. A configured provider is not approval to send all data.

# Open choices and validation

Confirm platforms, locations/format, category-specific precedence, store failure
behavior, client authorization/supervision, reload semantics, encryption, and
provider/disclosure policy. Test conflicting origins, insecure values, unavailable
stores, rotation, disabled sources, upgrade failure, and synthetic-secret leakage.

Related: [API boundary](api-boundary.md), [security](security-and-privacy.md),
[persistence](persistence.md), [diagnostics](observability.md),
[credential incidents](../runbooks/security-incidents.md).