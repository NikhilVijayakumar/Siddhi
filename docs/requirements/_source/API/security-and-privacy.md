# Security and Privacy

**Project:** Siddhi — Portfolio Intelligence & Strategic Planning System  
**Document:** `security-and-privacy.md`  
**Status:** Draft for review  
**Scope:** Application security, data protection, privacy, threat mitigation, and security incident handling  
**Implementation status:** Not yet verified in a running system

---

## 1. Purpose

This document defines the security and privacy requirements for Siddhi, including its backend API, future desktop client, local database, source integrations, evidence store, reports, and external AI workflows.

Siddhi may process commercially sensitive project information, private repository metadata, unpublished plans, internal engineering knowledge, credentials, and strategic decisions. Some of this information may be valuable even when it does not contain personal information.

The system must protect this information against unauthorized access, accidental disclosure, unintended modification, and loss.

Security must be built into the architecture and operational workflows. It must not depend solely on users running Siddhi on their own machines or on the API being bound to localhost.

## 2. Security objectives

Siddhi must aim to provide the following properties.

| Objective | Requirement |
|---|---|
| Confidentiality | Only authorized components and users can access sensitive information. |
| Integrity | Records, evidence, decisions, and configuration cannot be silently altered or misrepresented. |
| Availability | Failures and hostile inputs must not unnecessarily corrupt the database or prevent recovery. |
| Least privilege | Each component receives only the access needed for its task. |
| Provenance | Stored evidence retains its source, acquisition context, and relevant timestamps. |
| Accountability | Important operations and failures produce safe, useful diagnostic records. |
| Privacy | Collect and disclose only information necessary for an explicit purpose. |
| Recoverability | Data can be restored without silently changing the meaning of historical records. |
| Transparency | Users can distinguish verified information, declared information, inference, uncertainty, and missing evidence. |

These objectives apply to normal operations, upgrades, background ingestion, report generation, and external AI analysis.

## 3. Security scope and trust boundaries

Siddhi contains several components that must not automatically trust one another.

### 3.1 Components and trust boundaries

**Desktop client**

The future Electron application is a user interface, not the authority for business rules or secret storage. It must not be trusted to enforce backend permissions by itself.

**Backend API**

The backend enforces access controls, validates inputs, applies domain rules, controls integrations, and mediates access to persistence and secrets.

**Local filesystem and repositories**

Repository files, configuration files, documents, Git metadata, and locally stored knowledge packages must be treated as potentially untrusted input. A repository may contain malformed files, unexpected links, hostile content, or secrets.

**External source systems**

Vyasa, OpenSpec, OKF, Git hosting providers, and verification systems are separate authorities. Their data may be stale, incomplete, inconsistent, or unavailable.

**Database and backups**

The SQLite database, journal/WAL files where applicable, exports, and backups contain potentially sensitive information. Local storage does not eliminate confidentiality or integrity risks.

**External AI providers**

A provider receives only the information deliberately disclosed to it. Its processing, retention, and access practices are outside Siddhi's direct control and must be evaluated before enabling a workflow.

### 3.2 Trust-boundary rule

Data crossing any boundary must be validated and assigned an appropriate trust classification.

Successful parsing does not prove that content is truthful. A valid OpenSpec artifact does not prove its implementation works. A source connection does not prove the source is complete. Text from a repository or external provider must never be treated as trusted instructions to the application or its agents.

## 4. Threat model

The initial threat model includes the following scenarios.

| Threat | Potential impact | Primary controls |
|---|---|---|
| Another local process calls the API | Unauthorized reading or modification | API authentication, authorization, narrow binding, request validation |
| Malicious repository content | Path traversal, resource exhaustion, misleading findings | Read-only access, bounded parsing, path restrictions, safe content handling |
| Secret leakage | Unauthorized repository or provider access | Secret-store integration, least privilege, redaction, rotation |
| Prompt injection in source material | External AI follows hostile instructions or discloses context | Treat content as data, isolate instructions, minimize context, validate outputs |
| Accidental AI disclosure | Confidential plans or code metadata leave the device | Explicit disclosure policy, user approval, data minimization |
| Database or backup theft | Exposure of portfolio and source information | Filesystem permissions, encryption decision, controlled backups |
| Database corruption or failed migration | Loss of data or application availability | Transactions, validated backups, migration safeguards |
| Forged or misleading evidence | Incorrect strategic conclusions | Provenance, source freshness, confidence and evidence classification |
| Unauthorized configuration change | Broader access or unintended disclosure | Configuration validation, protected settings, audit events |
| Denial of service | Slow or unavailable application | Input limits, timeouts, bounded jobs, resource controls |
| Log or report disclosure | Exposure of sensitive content | Redaction, access controls, output minimization |
| Compromised dependency | Execution or data exposure | Dependency management, vulnerability assessment, controlled updates |

This is an initial threat model. A formal security review must refine the attack surface after the backend lifecycle, authentication model, and desktop packaging are decided.

## 5. Security architecture

### 5.1 Backend enforcement

All security-sensitive operations must be enforced by the backend, including:

- Access to goals, plans, decisions, and historical records.
- Source configuration and refresh.
- Filesystem and repository access.
- Credential retrieval and use.
- Export and backup operations.
- External AI requests and disclosure approval.
- Changes to security-sensitive configuration.

The frontend must not be able to bypass these controls by constructing direct requests or modifying client-side state.

### 5.2 Separation of responsibilities

The API, application use cases, domain logic, persistence, and integration adapters should have clearly defined responsibilities.

- API routes validate requests and enforce access policy.
- Application use cases coordinate authorized operations.
- Domain logic enforces business invariants.
- Persistence handles database access and transaction boundaries.
- Integration adapters access only their assigned sources and credentials.
- External AI adapters receive only approved context packages.

Avoid granting every module access to a global object containing all credentials or unrestricted filesystem capabilities.

### 5.3 Read-only source integration

Read-only is the default access policy for external engineering sources.

Siddhi must not silently:

- Edit source repositories.
- Commit or push changes.
- Modify OpenSpec tasks or schemas.
- Rewrite OKF knowledge packages.
- Change Vyasa's inventory.
- Change external CI/CD configuration.
- Delete source records or external artifacts.

Siddhi-owned portfolio records may be edited through authorized workflows. External source records must remain under their source system's authority.

## 6. Local API and desktop security

### 6.1 Network exposure

The API should bind to loopback by default and should not expose itself to the local network or internet during ordinary desktop use.

Remote binding, if ever supported, must be an explicit deployment mode with its own authentication, authorization, transport-security, and threat-model requirements.

Binding to `127.0.0.1` is not sufficient authentication. Other local processes can potentially connect to a loopback service.

### 6.2 Authentication and authorization

The final authentication design remains an architectural decision.

Before the desktop client is integrated, the implementation must define:

- How the desktop client establishes an authorized connection.
- How the backend distinguishes authorized requests from arbitrary local requests.
- How credentials or session capabilities are issued and protected.
- How authorization is checked for sensitive operations.
- How credentials are invalidated when the client exits or the backend restarts, where applicable.
- How an unexpected or unauthorized caller is rejected.

Do not embed a reusable privileged secret in frontend source code and treat it as a secure authentication mechanism.

If the first release is intentionally single-user, that assumption must be documented. It must not be confused with protection against other local processes.

### 6.3 CORS and browser-facing controls

CORS must be restricted to the origins actually needed by the supported client. It is not an authentication or authorization mechanism.

The backend must validate request methods, content types, payload sizes, and state-changing operations. Browser-related protections should be applied where relevant to the actual client and deployment model.

### 6.4 API abuse controls

The API must impose appropriate limits on:

- Request-body size.
- Pagination size.
- Number of concurrent ingestion and analysis jobs.
- Job duration and retry attempts.
- Export size.
- External AI request size.
- Filesystem scanning scope.
- Any endpoint that can consume significant CPU, memory, storage, or network resources.

Limits must be configurable within safe bounds. Increasing a limit must not inadvertently disable the system's resource protections.

## 7. Filesystem and repository security

### 7.1 Path validation

Filesystem paths are security-sensitive inputs.

Siddhi must:

- Resolve and validate configured paths before use.
- Restrict scanning to authorized roots and explicit scopes.
- Prevent path traversal outside the permitted scope.
- Handle symbolic links and junctions according to an explicit policy.
- Avoid following links into unintended locations.
- Distinguish missing paths, permission errors, and invalid paths.
- Avoid writing files merely because an input path exists in a source artifact.

Where symlinks are permitted, the implementation must verify that their resolved targets remain within the authorized scope, accounting for race conditions where relevant.

### 7.2 Read-only repository access

Repository scanning must not modify working trees, check out branches, execute repository scripts, or run arbitrary build commands by default.

Git metadata and document content should be read through controlled interfaces. A repository's own instructions, scripts, or configuration must not automatically gain permission to execute code.

If a future capability requires build or test execution, it must be separately specified with an explicit execution boundary, permission model, and resource limits.

### 7.3 Malformed and hostile content

Source parsers must defend against:

- Extremely large files.
- Deeply nested documents.
- Malformed encodings.
- Unexpected file types.
- Archive expansion attacks if archives are ever supported.
- Excessive numbers of files or directory entries.
- Parser vulnerabilities and pathological inputs.
- Unexpected URLs or external references embedded in content.

The system should prefer bounded parsing and graceful failure over unbounded retries or memory consumption.

### 7.4 External URLs

A source document or repository must not be able to cause unrestricted network requests simply by containing a URL.

If URL fetching is supported, it must have an explicit allowlist or destination policy, reject unsafe schemes, prevent access to loopback/private-network or cloud metadata endpoints where applicable, and limit redirects and response sizes.

Server-side request forgery protections are particularly important if a future deployment allows remote source URLs to be configured.

## 8. Input validation and content handling

All input must be treated according to its origin and expected type.

### 8.1 API input

Validate request schemas, identifiers, enumerations, pagination parameters, date values, paths, URLs, and state transitions.

Use parameterized database operations. Never construct SQL statements by concatenating untrusted values.

### 8.2 Source content

Source content may contain arbitrary instructions, code, markup, links, or claims.

The system must preserve the distinction between:

- Application instructions.
- User-authored configuration.
- External source content.
- Model-generated suggestions.
- Verified evidence.
- Human-approved decisions.

Source content must not be allowed to modify application policy or authorize an operation merely by containing text that requests it.

### 8.3 Output encoding

Reports and UI content must safely render untrusted text. Do not execute embedded HTML, JavaScript, shell commands, or other active content originating from source documents or AI responses.

For Electron, the implementation must use appropriate content security controls and avoid enabling unnecessary Node.js capabilities in rendered web content.

## 9. Secrets and credential protection

Secret handling is governed in detail by `configuration-and-secrets.md`.

Security requirements include:

- No credentials committed to source control.
- No plaintext secrets in ordinary configuration files.
- No secrets returned by API configuration endpoints.
- No secret values in logs, exceptions, reports, or AI context packages.
- Credentials scoped to the integration that requires them.
- Least-privilege access tokens wherever supported.
- Clear credential replacement and revocation procedures.
- Safe handling of expired or invalid credentials.

Use an appropriate operating-system credential store where supported. If a fallback is necessary, document its security limitations and require an explicit policy rather than silently falling back to plaintext storage.

If a secret is exposed, the response must include revocation or rotation at the issuing provider, not merely deletion of the local reference.

## 10. Database, backups, and data integrity

### 10.1 Database access

The database must be stored in an application-controlled directory with appropriate filesystem permissions.

The backend should be the only application component that accesses the database directly. The frontend must use the API rather than opening SQLite files.

### 10.2 Integrity protections

- Use explicit transaction boundaries.
- Enforce database constraints and foreign-key relationships.
- Use versioned migrations.
- Preserve historical revisions and evidence provenance.
- Reject unsupported database schema versions.
- Protect the last-known-good source snapshot during failed ingestion.
- Avoid treating partially committed work as a completed operation.

### 10.3 Backup protection

Backups, database journal/WAL files, and exports may contain the same sensitive information as the main database.

The system must define backup access permissions, retention, storage location, and whether encryption is required.

Backup and restoration procedures must be tested. A backup that has not been validated should not be treated as a proven recovery mechanism.

### 10.4 Integrity versus truth

A cryptographic fingerprint can help detect changes to a captured artifact, but it does not prove that the original artifact was truthful or complete.

Similarly, a database constraint can enforce structural consistency without proving that an assessment or strategic conclusion is correct.

Siddhi must not equate storage integrity with factual verification.

## 11. Privacy and data minimization

### 11.1 Data minimization

Siddhi should collect and retain only the information needed for its declared portfolio-intelligence purposes.

It should not automatically ingest entire repositories or retain every source file simply because access is available.

Prefer targeted metadata, source references, bounded excerpts, fingerprints, and relevant evidence over indiscriminate content copying.

### 11.2 Personal information

Repository metadata, review notes, logs, and external AI responses may contain names, email addresses, usernames, or other personal information.

The system should avoid collecting personal data unrelated to the portfolio's purpose. Where personal data is required, its purpose, access, retention, and disclosure must be defined.

Applicable legal and organizational obligations depend on the actual deployment, data subjects, and jurisdictions. They must be assessed before production use; this document is not a legal determination.

### 11.3 Data classification

At minimum, classify data into operational categories such as:

- **Public:** explicitly approved for public disclosure.
- **Internal:** routine project metadata not approved for public release.
- **Confidential:** private repositories, unpublished plans, internal architecture, strategic assessments, or sensitive business information.
- **Restricted:** credentials, private keys, authentication material, and other data requiring especially narrow access.

These labels are a proposed handling model, not a claim that they match an existing organizational classification policy. They should be reconciled with the organization's actual policy before implementation.

Classification should drive access, export, logging, and AI disclosure rules. A source's accessibility does not make its content public.

### 11.4 Retention and deletion

Retention must be explicit for source snapshots, reports, logs, external AI requests, and backups.

Deletion must distinguish:

- Removing an active source connection.
- Removing a source from the current view.
- Retiring a Siddhi-owned entity.
- Expiring historical snapshots.
- Deleting stored content.
- Removing backups and exported copies.

A source becoming unavailable must not automatically delete historical evidence. Conversely, historical preservation must not become an excuse to retain sensitive content indefinitely.

Where deletion is required, the policy must account for database copies, exports, backups, and other stored representations.

## 12. External AI security and privacy

External AI analysis is advisory. It must not automatically approve decisions, change source systems, or execute recommendations.

### 12.1 Explicit disclosure

Before sending information to an external provider, Siddhi must apply an approved disclosure policy that considers:

- The provider and model.
- The intended analytical purpose.
- The information selected for the context package.
- The data classification of the selected information.
- The provider's configured data-handling terms and applicable organizational policy.
- Whether explicit user approval is required.

The presence of an API key does not constitute approval to transmit every portfolio record.

### 12.2 Context minimization

The context builder should include only information necessary for the requested analysis.

It must exclude:

- Credentials and secret references that reveal sensitive implementation details.
- Unrelated personal information.
- Entire repository contents where targeted evidence is sufficient.
- Unnecessary private file paths or internal endpoints.
- Data explicitly excluded by the disclosure policy.

The system should retain enough metadata to explain what categories of information were sent, to which provider, for what purpose, and under which policy or template version. It should not unnecessarily duplicate all transmitted content in logs.

### 12.3 Prompt injection

Repository documents, issue descriptions, requirements, and other source material may contain hostile instructions intended to manipulate an AI model.

Controls must include:

- Treating retrieved content as data rather than trusted instructions.
- Separating system-controlled instructions from source excerpts.
- Restricting the context to the current analysis purpose.
- Preventing model output from directly triggering privileged operations.
- Validating output structure and referenced evidence.
- Requiring explicit approval for consequential decisions or actions.

Prompt-injection defenses reduce risk but cannot guarantee that a model will never be manipulated. Sensitive workflows must therefore rely on least privilege, minimized disclosure, and controlled actions rather than prompt instructions alone.

### 12.4 Provider failure

If a provider is unavailable, rejects a request, or returns invalid output, Siddhi must preserve the request's outcome and report the failure safely.

Deterministic analysis must remain usable without external AI. A provider failure must not corrupt the portfolio database or replace valid historical findings with unverified output.

## 13. Evidence integrity and strategic decision safety

Siddhi's conclusions can influence engineering investment and portfolio priorities. Misleading evidence is therefore a security and integrity concern, even when no attacker is involved.

The system must distinguish:

- Source-declared facts.
- Observed source artifacts.
- Deterministic findings.
- Inferences and candidate matches.
- External AI recommendations.
- Human-approved decisions.
- Missing, stale, conflicting, or unverified evidence.

Each important finding should retain its provenance and relevant source or rule version.

A source's task status, a matching keyword, or the existence of a document must not automatically prove an intended outcome has been achieved.

Recommendations must not become approved decisions without an explicit authorized action. Decision rationale and revisions should remain traceable.

## 14. Logging, auditability, and diagnostics

Siddhi should record security-relevant events proportionately to the risks of a local-first portfolio system.

Potential events include:

- Application startup, shutdown, and failed initialization.
- Authentication failures and authorization denials, once authentication is implemented.
- Invalid or suspicious API requests.
- Source configuration changes.
- Credential addition, replacement, or removal, without recording the secret itself.
- Ingestion and export operations.
- Database migration and restore outcomes.
- External AI disclosure requests and their outcomes.
- Changes to sensitive security settings.
- Repeated resource-limit violations.

Log records should contain sufficient context to investigate an event without copying sensitive payloads unnecessarily.

### 14.1 Prohibited log content

Do not log:

- Passwords, API keys, access tokens, or private keys.
- Authorization headers or session secrets.
- Full database connection strings containing credentials.
- Entire repository documents or AI context packages by default.
- Unnecessary personal information.
- Unredacted provider responses that may contain sensitive source content.

### 14.2 Log integrity and availability

Logs should be protected against unauthorized reading and modification. They must be bounded to prevent disk exhaustion.

Diagnostic failures should not accidentally expose sensitive content or allow unsafe application behavior. Security-critical audit events must not be silently disabled by an ordinary log-level setting.

The system should distinguish operational logs, security events, and historical domain records; these have different retention and integrity needs.

See the [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) for supporting guidance.

## 15. Dependency and software supply-chain security

The application will depend on Python packages, frontend packages, database libraries, parsers, and potentially provider SDKs.

The project should:

- Pin or constrain dependencies using a documented dependency policy.
- Review dependency updates and known vulnerabilities.
- Avoid unnecessary dependencies and excessive privileges.
- Use lockfiles or an equivalent reproducible dependency-resolution mechanism.
- Scan dependencies using appropriate tools in CI.
- Keep credentials out of build logs and CI artifacts.
- Review security-sensitive dependency changes.
- Track the versions of critical components used in a release.
- Provide a process for addressing critical vulnerabilities.

Dependencies must not be installed dynamically from untrusted repository content during ordinary ingestion.

The initial release should define a reasonable vulnerability-handling policy without introducing heavyweight supply-chain infrastructure that is disproportionate to the product.

## 16. Security incident response

Siddhi needs a practical response process for exposed credentials, unauthorized access, corrupted data, and accidental disclosure.

### 16.1 Potential incidents

Examples include:

- A credential is committed to a repository or appears in a log.
- Confidential context is sent to an unintended AI provider.
- An unauthorized process accesses the local API.
- A malicious repository causes unexpected filesystem access.
- A database or backup is exposed.
- A source artifact or report is altered without authorization.

### 16.2 Response sequence

1. **Contain:** disable the affected integration, capability, or access path where safe.
2. **Protect credentials:** revoke or rotate exposed credentials at the issuing system.
3. **Preserve relevant diagnostics:** retain safe records needed to understand the incident without copying exposed secrets unnecessarily.
4. **Assess scope:** identify affected data, source systems, reports, credentials, and backups.
5. **Recover:** restore from a validated recovery point or rebuild affected derived data where appropriate.
6. **Validate:** verify access controls, data integrity, and source provenance before resuming operations.
7. **Document:** record the cause, impact, corrective action, and any required changes to security policy.

Deleting a local token reference alone is insufficient if the external credential remains valid.

The response process should also consider whether disclosure creates organizational or legal notification obligations.

## 17. Security testing and verification

Security controls must be tested rather than inferred from configuration or documentation.

### 17.1 API and authorization tests

- Unauthenticated or unauthorized requests are rejected under the selected security model.
- Sensitive operations cannot bypass backend authorization.
- Remote binding is disabled by default.
- CORS configuration is appropriately restricted.
- Invalid methods, content types, and oversized requests are handled safely.
- Error responses do not expose secrets or sensitive internals.

### 17.2 Filesystem and source tests

- Path traversal attempts are rejected.
- Symlink behavior follows the approved policy.
- Missing and inaccessible paths are handled distinctly.
- Repository scanning does not modify source content.
- Malformed or oversized files are handled within defined limits.
- Source documents cannot trigger arbitrary shell commands or unrestricted network requests.

### 17.3 Data and secret tests

- Secrets are absent from logs, reports, API responses, and AI context packages.
- Database permissions and backup protections follow the approved policy.
- Failed migrations and ingestion operations preserve recoverable state.
- Historical evidence retains provenance.
- Unauthorized configuration changes are rejected.
- Export and retention operations respect data classification.

### 17.4 External AI tests

- External AI is disabled by default until configured and enabled.
- Context disclosure follows the configured policy.
- Prompt-injection test cases cannot directly authorize privileged actions.
- Malformed model output is rejected or marked invalid.
- Provider failure does not corrupt deterministic results.
- Recommendations require explicit human disposition before becoming decisions.

### 17.5 Release readiness

Before a release, run the applicable automated tests, dependency checks, and security review. Record known limitations and unresolved risks.

A passing test suite is evidence of tested behavior, not proof that the system is free from vulnerabilities.

## 18. Acceptance criteria

The security and privacy baseline is ready for the first usable release when:

1. The trust boundaries and authority of each component are documented.
2. The local API has a defined authentication and authorization model.
3. The backend is the enforcement point for sensitive operations.
4. Filesystem access is restricted to authorized scopes and remains read-only for source integrations.
5. Secret storage, access, rotation, and redaction are implemented and tested.
6. Sensitive data is not automatically disclosed to external AI providers.
7. Prompt injection and untrusted source content are handled as security risks.
8. Database, migration, backup, and recovery procedures preserve integrity.
9. Logs and diagnostics avoid secret leakage and have bounded resource use.
10. Data classification, retention, export, and deletion rules are documented.
11. Security tests cover API access, path handling, secrets, ingestion, and AI disclosure.
12. Dependencies are managed through a documented update and vulnerability process.
13. A practical incident-response procedure exists for credential exposure and data disclosure.
14. Remaining security limitations are documented and explicitly accepted before production use.

## 19. Implementation sequence

### Phase 1 — Security foundations

- Finalize the threat model and data classification.
- Define local API authentication and authorization.
- Establish safe filesystem boundaries.
- Implement secure error handling and log redaction.
- Validate the configuration and secret-storage design.

### Phase 2 — Data protection

- Apply database access and backup protections.
- Verify transaction and migration recovery behavior.
- Define retention and deletion policies.
- Protect exported reports and diagnostic bundles.

### Phase 3 — Source integration hardening

- Test path validation, symlink handling, and bounded parsing.
- Confirm source adapters do not modify repositories.
- Restrict network access and external URL fetching.
- Add tests for malformed and hostile source content.

### Phase 4 — External AI protection

- Implement explicit context construction and disclosure policy.
- Add provider and workflow controls.
- Test prompt injection, invalid output, and provider failures.
- Ensure recommendations cannot automatically change approved decisions.

### Phase 5 — Release assurance

- Run dependency vulnerability checks.
- Perform an end-to-end security review of the backend and desktop boundary.
- Validate backup restoration and incident-response procedures.
- Document unresolved risks and production-readiness limitations.

The sequence is provisional and must be aligned with the agreed first-release scope.

## 20. Open questions

| ID | Question | Why it matters |
|---|---|---|
| SP-001 | Will the first release be strictly single-user and local-only? | Defines the initial authentication and authorization requirements. |
| SP-002 | How will Electron authenticate to `siddhi-api`? | Loopback binding alone does not authenticate callers. |
| SP-003 | Which operating systems must be supported? | Affects filesystem controls, credential storage, and packaging. |
| SP-004 | Is database and backup encryption required in the first release? | Depends on the data classification and threat model. |
| SP-005 | Which source content may be retained, and for how long? | Affects confidentiality, storage, and historical analysis. |
| SP-006 | Which data classifications and disclosure rules should be enforced for AI providers? | Determines whether sensitive data can leave the device. |
| SP-007 | Which external AI providers are permitted, and under what data-handling terms? | Affects privacy and deployment approval. |
| SP-008 | Should the first release support remote URLs, remote repositories, or only local sources? | Determines network attack surface and SSRF exposure. |
| SP-009 | What is the policy for symbolic links and repository submodules? | Affects scan scope and filesystem isolation. |
| SP-010 | Which security events must be retained, and for how long? | Balances investigation value, privacy, and storage. |
| SP-011 | Which dependency scanning and vulnerability response practices are proportionate for the project? | Defines ongoing supply-chain assurance. |
| SP-012 | What incident notification obligations apply to the intended deployment? | Depends on organizational and legal requirements. |

## 21. Relationship to other documents

This document must be reconciled with:

- `system-architecture.md` — component boundaries and trust boundaries.
- `architectural-decisions.md` — approved security and deployment decisions.
- `data-ownership.md` — source authority and data boundaries.
- `configuration-and-secrets.md` — configuration precedence and secret lifecycle.
- `persistence-and-migrations.md` — database integrity and recovery.
- `source-integration.md` — adapter access and validation rules.
- `vyasa-integration.md` — inventory integration and read-only access.
- `openspec-integration.md` — requirements-source handling.
- `okf-integration.md` — knowledge-source handling.
- `git-evidence.md` — repository access and evidence provenance.
- `ingestion-and-snapshots.md` — source snapshot consistency.
- `external-analysis.md` — provider use, context minimization, and advisory-only behavior.
- `api-design.md` — API exposure, authentication, and error handling.
- `deterministic-analysis.md` — evidence classification and reproducibility.

Security controls must preserve the system's core design principles: source authority remains with source systems, evidence is distinct from inference, external AI is advisory, and consequential decisions require explicit authorization.

## 22. References

- OWASP Foundation, [Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html).
- OWASP Foundation, [Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html).
- OWASP Foundation, [REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html).

These references provide general security guidance. They do not replace validation against Siddhi's actual implementation, the organization's policies, or applicable legal requirements.

## 23. Review status

This document establishes a proposed security and privacy baseline. It does not claim that Siddhi has been penetration-tested, that all controls have been implemented, or that the system is production-ready.

The most important unresolved dependency is the local API authentication and process-lifecycle design. Resolve that alongside `api-design.md` and `configuration-and-secrets.md` before integrating the desktop client. Then validate filesystem boundaries, secret handling, and AI disclosure controls against the actual code and supported deployment environments.






