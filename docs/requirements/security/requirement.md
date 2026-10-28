# Access, privacy and untrusted-content boundaries

- **Status:** Draft; NOT approved for implementation.
- **Owns:** FR-049, NFR-021, NFR-022, NFR-023, NFR-025, NFR-026, NFR-027, NFR-039

## Scope and outcomes

| Baseline | Observable acceptance outcome |
|---|---|
| [FR-049](../functional-requirements.md#fr-049--enforce-access-boundaries) | Filesystem and repository access stays within configured authorized locations/mechanisms; imported instructions cannot override policy or grant access. |

## Out of scope

Implicit network-wide API exposure, source writes caused by routine processing, executing repository instructions, automatically selected authentication technology and general-purpose agent command execution. A future write-enabled workflow requires separate explicit authorization and specification.

## Data and integration boundaries

Source documents, paths, metadata and external outputs are untrusted data. Configuration establishes permitted roots and access mechanisms; source content cannot enlarge them. Credentials remain separate from synchronized metadata, retained source payloads, logs and reports. Local deployment is not itself proof of secure browser or client access.

## NFR responsibilities

- [NFR-021](../non-functional-requirements.md#nfr-021--least-privilege-access): least-privilege configured paths and operations, read-only ingestion where practical.
- [NFR-022](../non-functional-requirements.md#nfr-022--local-api-exposure): no external-interface exposure by default; explicitly design loopback, browser/CORS and unauthorized-local-request protection.
- [NFR-023](../non-functional-requirements.md#nfr-023--secret-management): no hardcoded/committed/logged/reported credentials; secure per-integration configuration.
- [NFR-025](../non-functional-requirements.md#nfr-025--untrusted-source-content): embedded instructions cannot change policy, authorize reads or trigger actions.
- [NFR-026](../non-functional-requirements.md#nfr-026--safe-diagnostics): errors, logs and diagnostics exclude secrets, unpublished work and unnecessary private details.
- [NFR-027](../non-functional-requirements.md#nfr-027--controlled-write-operations): ordinary reads and analysis cannot publish or mutate repositories; future writes have explicit boundaries.
- [NFR-039](../non-functional-requirements.md#nfr-039--security-testing): test input validation, containment, secret leakage, unauthorized operations and malicious source content.

## Cross-package dependencies

- [source-ingestion](../source-ingestion/requirement.md) and evidence packages: authorized non-mutating reads.
- [external-analysis](../external-analysis/requirement.md): owns NFR-024 disclosure minimization; security supplies trust/access enforcement.
- [api-operations](../api-operations/requirement.md): safe errors, diagnostics and client-boundary enforcement.
- [persistence-recovery](../persistence-recovery/requirement.md): local settings and private retained data.
- [engineering-quality](../engineering-quality/requirement.md): reproducible security/failure fixtures; this package owns security test coverage obligations.

## Unresolved questions

Authorized filesystem roots and symlink policy, local-client authentication, browser/origin policy, credential storage, remote-access exceptions, diagnostic redaction and future write authorization remain open. Recommended first release: goal-to-evidence report, NOT an approved release choice. See [grill log](grill-log.md).

## Acceptance drafts

Features are non-executable acceptance drafts, with no runner or step definitions. They do not constitute a completed threat model or passing security tests.

## Knowledge References

- `knowledge/architecture/security-and-privacy.md` — trust, access, disclosure and non-mutation.
- `knowledge/architecture/configuration-and-secrets.md` — credential/configuration separation.
- `knowledge/architecture/api-boundary.md` — local HTTP trust boundary.
- `knowledge/architecture/observability.md` — redacted diagnostic context.
- `knowledge/practices/testing-and-validation.md` — adversarial fixtures.
- `knowledge/practices/knowledge-and-delivery-separation.md` — security choices need explicit review.