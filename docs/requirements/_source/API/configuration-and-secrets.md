# Configuration and Secrets

**Project:** Siddhi — Portfolio Intelligence & Strategic Planning System  
**Document:** `configuration-and-secrets.md`  
**Status:** Draft for review  
**Scope:** Application configuration, environment-specific settings, credentials, secret storage, and configuration lifecycle  
**Implementation status:** Not yet verified in a running system

---

## 1. Purpose

This document defines how Siddhi manages application configuration and sensitive information across development, testing, and local production use.

Siddhi integrates with multiple systems, potentially including Vyasa, OpenSpec repositories, OKF knowledge stores, Git repositories, and external AI providers. These integrations have different configuration needs, permissions, and security risks.

The configuration system must allow these integrations to be enabled, disabled, and adjusted without requiring source-code changes or exposing credentials.

It must also support the planned separation between `siddhi-api` and `siddhi-desktop`, ensuring that the backend remains responsible for sensitive configuration and external-system access.

## 2. Design principles

### 2.1 Separate configuration from secrets

Ordinary configuration describes how Siddhi operates. Secrets grant access to systems or protect sensitive information.

Examples of ordinary configuration include:

- API bind address and port.
- Log level.
- Database location.
- Source refresh limits.
- Enabled integrations.
- AI-provider selection.

Examples of secrets include:

- API tokens.
- OAuth client secrets.
- Private keys.
- Database encryption keys.
- Credentials used to access private repositories or external services.

These categories must have different storage, access, logging, and export policies.

### 2.2 Keep configuration explicit

Every supported setting must have a defined name, type, default, validation rule, scope, and effect.

Configuration must not be inferred from arbitrary environment variables, undocumented filenames, or incidental repository contents.

Unknown settings should produce a clear diagnostic where appropriate, rather than silently changing application behavior.

### 2.3 Prefer secure local-first defaults

A fresh Siddhi installation should operate with the least privilege necessary.

It must not require an external AI provider, expose its API to the network, or grant access to private repositories merely to start the application.

Optional integrations should remain unavailable until configured and explicitly enabled.

### 2.4 Make effective configuration explainable

An operator should be able to determine which non-sensitive settings are active, where they originated, and whether they have been validated.

The application must never reveal secret values as part of configuration inspection.

### 2.5 Avoid unnecessary configuration frameworks

Use a small, typed configuration layer with clear validation and precedence rules. Do not introduce a distributed configuration service or elaborate secrets-management infrastructure without a concrete deployment requirement.

## 3. Configuration categories

Siddhi should distinguish the following categories.

| Category | Examples | Proposed storage |
|---|---|---|
| Application settings | Log level, API limits, feature switches | Typed configuration |
| Runtime settings | Bind address, port, process behavior | Launch configuration or environment |
| Persistence settings | Database path, backup location | Application configuration |
| Source settings | Source type, identifier, enabled state, refresh policy | Siddhi-owned persistent configuration |
| Integration credentials | Access tokens, client secrets | Secret store or approved secret injection |
| AI-provider settings | Provider, model, endpoint, timeout | Non-secret configuration |
| AI-provider credentials | API keys, provider tokens | Secret store or approved secret injection |
| User preferences | Display preferences, report defaults | Desktop settings or Siddhi API, according to ownership |
| Development/test settings | Mock providers, temporary paths, test credentials | Isolated test configuration |

The exact storage mechanism may vary by category. The effective configuration must still be validated through a consistent configuration interface.

## 4. Configuration sources and precedence

### 4.1 Proposed sources

The initial implementation may use:

1. Application defaults.
2. A system-level or installation-level configuration file, if needed.
3. A user-specific configuration file.
4. Environment variables for deployment and development overrides.
5. Explicit runtime arguments for settings that must be supplied at process startup.
6. Siddhi-managed settings changed through an authorized API or desktop workflow.

Secrets may also be supplied through a dedicated operating-system secret store or an approved deployment mechanism.

These sources should not all be supported automatically in the first release. The implementation should enable only those required by the deployment model.

### 4.2 Precedence

The application must define precedence for every setting category.

A proposed default for ordinary runtime settings is:

**Built-in defaults → configuration files → environment overrides → explicit startup overrides.**

Persisted application settings require separate treatment. A setting managed through Siddhi's API should not unexpectedly change because an unrelated configuration reload overwrites it.

Secrets should use an explicitly defined resolution policy rather than inheriting precedence blindly from ordinary settings.

If two active sources provide conflicting values, Siddhi should apply the documented precedence rule and make the winning source visible in a non-sensitive configuration diagnostic.

### 4.3 Configuration validation

At startup, Siddhi should validate:

- Required settings are present.
- Values have the expected types and formats.
- Numeric limits are within allowed ranges.
- File and directory paths are valid or can be created safely.
- The selected database location is usable.
- The API bind address follows the security policy.
- Enabled integrations have their required non-secret configuration.
- Secret references resolve when the integration requires them.
- Selected provider and model identifiers are supported by the configured adapter.

A missing optional provider credential must not prevent Siddhi from starting when external AI analysis is disabled.

Invalid security-critical settings must cause startup to fail safely or the affected capability to remain disabled with a clear diagnostic. The system must not silently fall back to an insecure setting.

## 5. Configuration ownership

Configuration must follow the same ownership boundaries as Siddhi's data model.

### 5.1 Application-owned configuration

Siddhi owns configuration for its own behavior, including:

- Database and backup paths.
- API runtime settings where the application is responsible for them.
- Logging and diagnostic levels.
- Ingestion limits and scheduling policies.
- Retention policies.
- Enabled source integrations.
- Analysis and reporting defaults.
- AI-provider selection and permitted workflows.

### 5.2 Source-specific configuration

Siddhi may retain the information required to identify and access a source, such as:

- Source type.
- Source instance identifier.
- Base URL or local root path.
- Enabled state.
- Read-only access policy.
- Refresh limits and timeout settings.
- Credential reference.
- Last successful validation status.

Siddhi must not claim ownership of the source's actual records merely because it stores the configuration needed to read them.

### 5.3 External-system configuration

Siddhi should not silently modify:

- Vyasa configuration.
- OpenSpec schemas or project configuration.
- OKF schemas or knowledge packages.
- Git remote configuration.
- Repository-specific credentials or hooks.
- CI/CD provider configuration.

Changes to these systems must follow their own authorized workflows. Siddhi's source integration is read-only by default.

## 6. Configuration file design

### 6.1 Format

A human-readable format such as TOML or YAML may be used for ordinary configuration. JSON is also acceptable where consistent with the selected implementation.

The format should support:

- Typed values.
- Explicit sections.
- Comments where useful.
- Schema validation.
- Stable naming conventions.
- Clear defaults.
- Migration or compatibility rules for configuration changes.

The choice of format is not yet confirmed.

### 6.2 Example configuration

The following is illustrative and does not establish the final schema:

```toml
[application]
environment = "local"
log_level = "INFO"

[api]
host = "127.0.0.1"
port = 0

[database]
path = "~/.local/share/siddhi/siddhi.db"

[ingestion]
default_timeout_seconds = 60
max_concurrent_runs = 2

[security]
allow_remote_bind = false

[external_analysis]
enabled = false
provider = "none"
```

In this example, port `0` means that the operating system may select an available port, if the implementation supports this behavior. The actual port must be reported to the authorized desktop launcher or client through a secure, documented startup mechanism.

No credentials, access tokens, or private keys belong in this file.

The example paths and values are placeholders. The final configuration must account for supported operating systems and the selected application lifecycle.

### 6.3 Configuration file handling

- Keep user-specific configuration in an application-controlled location.
- Restrict file permissions where settings could expose sensitive operational details.
- Do not place user configuration inside a repository by default.
- Do not overwrite an existing configuration during upgrades without a defined migration process.
- Validate configuration before applying it.
- Preserve a recoverable copy when a configuration migration could otherwise destroy user settings.
- Clearly distinguish generated defaults from user-edited configuration.

## 7. Secret management

### 7.1 Secret categories

Potential secrets include:

- Git hosting tokens.
- API keys for external AI providers.
- OAuth access and refresh tokens.
- OAuth client secrets.
- Credentials for external services.
- Encryption keys for protected local data, if required.
- Credentials for any future authenticated local API deployment.

Not every integration requires a secret. Local repository reads may rely on operating-system filesystem permissions, while private remote services may require an explicit credential.

### 7.2 Preferred storage

For a desktop installation, use a suitable operating-system credential store where available.

The implementation should evaluate native credential storage for supported platforms, including:

- Windows Credential Manager.
- macOS Keychain.
- Linux Secret Service or an equivalent supported credential service.

If a native secret store is unavailable, Siddhi must define an explicit fallback policy. It must not silently store plaintext credentials in the database, ordinary configuration files, logs, or source repositories.

For automated development and test environments, environment-based secret injection may be acceptable, provided values are not committed to version control or printed in logs.

The final secret-storage choice remains an architectural decision.

### 7.3 Secret references

Siddhi's ordinary configuration should store a reference to a secret rather than the secret value itself.

A secret reference should identify the relevant credential within the selected storage mechanism. Its format must not assume that every supported platform uses the same credential-store API.

Secret references should be scoped to the intended integration and source instance. Credential names must not expose the credential value.

### 7.4 Secret lifecycle

The system should support the lifecycle appropriate to each credential:

1. Create or supply the credential.
2. Store it using the approved secret mechanism.
3. Associate it with an authorized source or provider.
4. Validate it when validation is supported and explicitly requested or required.
5. Use it only for the intended operation.
6. Replace or rotate it when necessary.
7. Disable or remove the reference when access is revoked.
8. Confirm that obsolete credentials are no longer used.

Removing a secret reference from Siddhi does not necessarily revoke the credential at the external provider. Revocation must be performed through the provider's authorized workflow.

### 7.5 Secret exposure prevention

Secret values must not appear in:

- API responses.
- Application logs or exception messages.
- Generated reports.
- AI context packages.
- Debug dumps.
- Telemetry or diagnostic exports.
- Source-control commits.
- Unredacted configuration inspection.
- Routine backup manifests.

When an operation fails because a credential is invalid, report the affected integration and a safe diagnostic. Do not echo the submitted credential.

## 8. Secret access boundaries

### 8.1 Backend authority

The backend must be the authority for retrieving and using credentials.

The desktop frontend should not receive provider API keys merely because a user selects a provider or starts an analysis request.

The frontend may submit a credential through an explicitly authorized setup workflow if that is the selected design. The backend must validate and persist it using the approved secret mechanism, and responses must never return the stored value.

### 8.2 Integration-specific access

An integration adapter should receive only the credentials and configuration required for its operation.

For example:

- A Git adapter should not have access to an AI-provider key unless its operation genuinely requires it.
- An AI adapter should not receive unrelated repository credentials.
- A report generator should not receive raw secrets as part of its input context.
- A configuration-inspection endpoint should not expose secret values.

The implementation should avoid passing a global configuration object containing all resolved secrets through the entire application.

### 8.3 Local API protection

Binding the API to loopback reduces network exposure but does not, by itself, authenticate callers or prevent another local process from connecting.

The configuration and secret design must align with `api-design.md` and the future desktop integration design.

At minimum:

- Remote binding must be disabled by default.
- Any supported remote-binding mode must require explicit configuration and an appropriate security model.
- CORS restrictions must be explicit and must not be treated as authentication.
- The API must not expose secret values through generic settings endpoints.
- The desktop client must not rely on an undocumented shared secret embedded in its code.
- Startup configuration must not permit arbitrary filesystem or shell access through API parameters.

The local authentication mechanism remains an open architectural decision.

## 9. Source integration configuration

Each source configuration should have a stable identifier and a declared integration type.

A proposed source configuration includes:

| Field | Purpose |
|---|---|
| `source_id` | Stable Siddhi-owned identifier |
| `source_type` | Adapter type, such as Vyasa, OpenSpec, OKF, or Git |
| `display_name` | Human-readable label |
| `enabled` | Whether scheduled or requested operations may use the source |
| `connection_mode` | Supported local or remote access mode |
| `endpoint_or_path` | Non-secret connection location |
| `credential_reference` | Optional reference to a secret |
| `access_mode` | Intended access permissions |
| `timeout_seconds` | Per-source or inherited timeout |
| `refresh_policy` | Permitted scan or refresh behavior |
| `last_validation_status` | Last known configuration-validation outcome |
| `last_validation_at` | Time of the latest validation attempt |

This is a logical proposal, not a final database schema.

The system must distinguish configuration validation from source-data validation. A successful connection does not prove that the source is complete, current, or semantically correct.

### 9.1 Disabled and invalid sources

A disabled source must not be accessed by background ingestion.

An enabled source with invalid configuration must produce a clear, source-specific error. It must not silently fall back to a different source or broaden its filesystem access.

Existing evidence and historical snapshots should remain available when a source becomes unavailable or is disabled.

### 9.2 Filesystem path configuration

For local sources and repositories:

- Paths must be resolved and validated under the supported path policy.
- Access must follow operating-system permissions.
- User-supplied paths must not enable unintended traversal outside permitted locations.
- Missing paths must be distinguishable from permission errors.
- Siddhi must not create, delete, or modify arbitrary directories merely because a path appears in configuration.
- Repository scanning must remain read-only unless a separately approved capability explicitly changes that policy.

## 10. External AI-provider configuration

External AI analysis is optional and advisory.

Configuration should distinguish:

- Whether external analysis is enabled.
- The selected provider adapter.
- The provider endpoint, where applicable.
- The selected model identifier.
- Request timeout and retry limits.
- Output-size or token limits where supported.
- Data-disclosure policy.
- The secret reference for provider authentication.
- The allowed analysis workflows.

The application must not infer that a provider is approved to receive all portfolio data merely because a credential is present.

Before transmitting context, Siddhi must apply the approved disclosure policy and construct an explicit, purpose-specific context package.

A missing credential, provider outage, or invalid model selection must not prevent deterministic analysis from running.

Provider configuration changes should be traceable where they materially affect an analysis request. Analysis records should capture non-secret provider/model metadata and relevant template or policy versions, without logging credentials.

## 11. Configuration changes and reload behavior

Configuration changes may require different application behavior depending on their scope.

| Change type | Proposed behavior |
|---|---|
| Display preference | Apply immediately where practical |
| Log level | Reload safely if supported |
| Source enabled state | Apply to future ingestion runs |
| Source endpoint or path | Validate before activation |
| Credential replacement | Use the new credential after successful storage and validation policy |
| AI provider/model | Apply to subsequent requests |
| Database location | Require controlled restart or explicit migration workflow |
| API bind address or port | Require controlled restart unless the runtime explicitly supports safe rebinding |
| Security policy | Validate before applying; fail safely on invalid settings |

A configuration update must not leave the application in an ambiguous partially applied state.

Where an update affects a running operation, Siddhi should define whether the operation uses the configuration captured at its start or the newly active configuration. Long-running jobs should normally retain an identifiable configuration version or safe configuration snapshot for audit purposes.

Secrets must not be copied into historical configuration snapshots. Such snapshots may record the credential reference or a non-sensitive credential version identifier instead.

## 12. Configuration versioning and migration

Configuration files and persisted settings may evolve independently of the database schema.

The system must define a configuration schema version or another reliable mechanism for identifying incompatible configuration formats.

When configuration changes:

1. Detect the format version or legacy representation.
2. Validate the existing configuration.
3. Apply deterministic migrations where supported.
4. Preserve user-defined settings that remain valid.
5. Reject unsupported or ambiguous transformations with an actionable diagnostic.
6. Save the migrated configuration safely.
7. Record the effective version and migration outcome without exposing secrets.

Database migrations must not implicitly assume that every configuration file has also been migrated.

If configuration is stored in the database, its schema evolution must follow `persistence-and-migrations.md`. If configuration is stored in files, file-format migration and recovery rules must be documented separately.

## 13. Logging and diagnostics

Configuration diagnostics should help users resolve errors without revealing sensitive values.

A configuration report may include:

- Setting name.
- Effective non-secret value, when safe.
- Origin of the value.
- Validation status.
- Whether a secret reference is configured.
- Whether a required credential is available, without displaying it.
- Last validation time and safe error category.

The report must redact credentials, authorization headers, private keys, secret-bearing URL parameters, and sensitive local paths when the disclosure policy requires it.

Errors should identify the affected setting or integration and the corrective action where possible.

For example, a safe message might say:

> The configured Git source could not authenticate. Check the credential assigned to this source and confirm that it has the required read permissions.

It must not include the rejected token or a full request header.

## 14. Development, testing, and deployment

### 14.1 Development

- Provide an example configuration containing placeholders only.
- Keep actual credentials outside tracked source files.
- Provide clear setup instructions for optional integrations.
- Use separate local data directories for development and test environments.
- Avoid requiring live provider credentials for ordinary development.

### 14.2 Testing

Automated tests should use fake credentials, mock secret stores, and local test sources wherever possible.

Tests must not require production credentials or modify real user configuration.

Secret-handling tests should verify that values do not leak through API responses, logs, error messages, generated reports, or AI context construction.

### 14.3 Deployment

The deployment model must define:

- How configuration is supplied.
- Where the application stores user-managed settings.
- How secrets are supplied and retrieved.
- Which process owns the database and secret-store access.
- How configuration changes are applied.
- How diagnostics can be collected safely.
- What happens if the secret store is unavailable.

For the planned desktop deployment, the API should run with the least privilege necessary and should not inherit unnecessary environment variables or credentials from its parent process.

## 15. Acceptance criteria

The configuration and secret-management implementation is ready for its first usable release when:

1. All supported settings have documented types, defaults, validation, and precedence.
2. Configuration validation occurs before unsafe runtime behavior begins.
3. Ordinary settings and secrets have distinct handling policies.
4. No secret values are stored in ordinary configuration files or exposed in API responses.
5. Secret access is limited to the integrations that require it.
6. Optional integrations can remain disabled without preventing application startup.
7. Invalid source configuration produces an explicit error without unsafe fallback behavior.
8. Local repository access follows the configured path and read-only policy.
9. Provider credentials remain on the backend and are excluded from AI context packages.
10. Configuration inspection and diagnostics redact sensitive values.
11. Configuration changes have defined activation and restart behavior.
12. Configuration-format changes can be detected and safely migrated or rejected.
13. Configuration and secret-handling tests run without production credentials.
14. The default API binding does not expose Siddhi to the local network.
15. The implementation documents the selected secret-storage mechanism and its fallback policy.

## 16. Implementation sequence

### Phase 1 — Typed application configuration

- Define the configuration schema.
- Establish default values and precedence.
- Implement startup validation.
- Define user-specific configuration paths.
- Add safe configuration diagnostics.

### Phase 2 — Source configuration

- Persist source identities and non-secret settings.
- Implement source enable/disable behavior.
- Validate local paths, endpoints, and refresh limits.
- Add source-specific configuration diagnostics.

### Phase 3 — Secret storage

- Select the supported secret-store implementation.
- Implement credential references and lifecycle operations.
- Ensure credentials are injected only into authorized adapters.
- Add redaction and leakage tests.

### Phase 4 — External AI configuration

- Add provider and model settings.
- Implement provider credential resolution.
- Enforce data-disclosure policies.
- Ensure deterministic analysis remains independent of provider availability.

### Phase 5 — Desktop integration and operational hardening

- Define how the desktop client configures the backend.
- Establish the local API authentication and startup model.
- Verify permissions and data-directory behavior on supported operating systems.
- Test configuration upgrades, secret-store failures, and recovery.

This sequence is provisional and must be aligned with the first-release scope.

## 17. Open questions

| ID | Question | Why it matters |
|---|---|---|
| CS-001 | Which configuration format should be used: TOML, YAML, or another format? | Affects validation, comments, migration, and tooling. |
| CS-002 | Which settings belong in files, the database, or runtime environment variables? | Establishes clear ownership and precedence. |
| CS-003 | Which operating systems must the first release support? | Determines secret-store and filesystem implementations. |
| CS-004 | Which secret-store abstraction and fallback policy should be implemented? | Affects credential security and portability. |
| CS-005 | How will the Electron desktop client authenticate to the local API? | Binding to loopback alone is insufficient authentication. |
| CS-006 | Should the API process be launched and supervised by Electron or run independently? | Affects startup configuration, environment inheritance, and lifecycle. |
| CS-007 | How should credentials be entered, validated, rotated, and revoked through the UI or API? | Defines the operational credential lifecycle. |
| CS-008 | Which configuration changes require a restart? | Affects runtime consistency and user experience. |
| CS-009 | Should user configuration be included in backups, and under what redaction policy? | Affects restoration and sensitive-data exposure. |
| CS-010 | Which source connection modes are required initially: local filesystem, local service, remote API, or a subset? | Determines configuration complexity and permissions. |
| CS-011 | Is encryption at rest required for the database, backups, or both? | Depends on the security threat model. |
| CS-012 | Which AI providers and disclosure controls are in scope for the first release? | Determines provider configuration and data-handling requirements. |

## 18. Relationship to other documents

This document should be reconciled with:

- `system-architecture.md` — component boundaries and configuration ownership.
- `architectural-decisions.md` — database, deployment, and security decisions.
- `data-ownership.md` — authority and source-system boundaries.
- `source-integration.md` — adapter configuration and access policies.
- `vyasa-integration.md` — project-inventory connection settings.
- `openspec-integration.md` — repository and schema access.
- `okf-integration.md` — knowledge-source access and validation.
- `git-evidence.md` — local and remote repository access.
- `ingestion-and-snapshots.md` — refresh policy and operational limits.
- `external-analysis.md` — provider configuration, context disclosure, and advisory-only behavior.
- `api-design.md` — local API exposure and client authentication.
- `persistence-and-migrations.md` — persisted settings and configuration evolution.
- `security-and-privacy.md` — threat model, secret protection, and data disclosure.

Configuration must not override approved security constraints or silently change the authority of an external source.

## 19. Review status

This document establishes a proposed baseline for configuration and secret management. The storage mechanisms, supported platforms, and local API authentication model have not yet been confirmed.

Before implementation, resolve the secret-store strategy, configuration ownership and precedence, and the API process lifecycle. These choices should be recorded in the architectural decision register rather than embedded as undocumented implementation assumptions.




