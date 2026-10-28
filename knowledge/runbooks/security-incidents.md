---
type: Runbook
title: Credential exposure and disclosure response
description: Containment, issuer revocation, minimal evidence, scope assessment, recovery, and controlled resumption.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Credential exposure and disclosure response

Use this proposed procedure for leaked secrets, unauthorized local requests,
unexpected filesystem/network activity, stolen database copies, or unintended
provider disclosure. No incident tooling or automated containment is assumed.
Responsible organizational responders and actual notification obligations take
precedence over deployment assumptions.

# Contain

Identify instance, integration, credential reference, scope, and time window
without copying secret values. Disable affected access/capabilities where safe
and supported. Stop disclosure where possible; cancellation alone does not prove
transmission stopped. Preserve unrelated work only if its safety is established.

Do not publish raw diagnostic bundles, full context, authorization headers, or
database files. Restrict retained evidence to authorized investigators and the
minimum necessary scope.

# Revoke at the issuer

Revoke or rotate exposed credentials through the issuer's authorized workflow.
Removing references, deleting logs, or editing history does not revoke a valid
token. Review permissions/sessions and provision least-privilege replacements
through the approved store. Never reuse or send exposed values to support for
identification.

# Assess and preserve safe evidence

Record timestamps, request/operation IDs, affected capabilities, access/disclosure
categories, destination where appropriate, and relevant policy/config versions.
Distinguish observed facts from suspicions and missing diagnostics.

Assess source systems, owned records, reports, exports, backup copies, personal
information, and credentials that may have been exposed/modified. Transmission
is not presumed reversible; establish what recipients received and what deletion
controls actually exist. Evaluate organizational/legal notification needs with
the responsible authority.

# Recover and validate

Correct failed access, path, rendering, disclosure, or redaction controls. For
suspected modification, inspect provenance and use
[validated restoration](persistence-recovery.md) where needed. Do not erase
necessary evidence or rewrite historical decisions to hide the event.

Before resuming, verify denial of unauthorized access, source scope, issuer
revocation/replacement, safe diagnostics, and approved disclosure behavior. Use
synthetic regression data where possible. Resume deliberately, not as a restart
side effect.

# Closure

Record cause, observed impact, uncertainty, containment, issuer action, recovery,
validation, notifications, and follow-up controls. Set authorized retention and
cleanup for incident artifacts. No further alerts does not prove no exposure;
state investigative limits.

Related: [security](../architecture/security-and-privacy.md),
[credential lifecycle](../architecture/configuration-and-secrets.md),
[diagnostics](diagnostics.md).