# Security desk review

Desk review only, no interview or user confirmation. A goal-to-evidence report is the recommended first-release goal, NOT an approved release choice. Threat-model and local-client policy decisions below remain open.

Deep review 2026-10-29: every question now records the options considered, the trade-off, and a resolution. `Recommended` means a recommendation is on record and may be adopted by a draft specification; `Decision needed` means the answer needs an owner threat decision that the documents cannot supply.

## Intent

**Q1. Can repository text authorize a wider filesystem read?**
- **Options:** follow instructions found in sources; treat source text as data only; strip anything that looks like an instruction.
- **Trade-off:** following text hands authority to content; stripping is unreliable and lossy; treating everything as data keeps the boundary absolute.
- **Recommendation:** Treat all source and imported output as data; only configured authorization can grant access.
- **Why:** Instructions embedded in evidence cross no legitimate trust boundary.
- **Resolution:** No content read by Siddhi can change its configuration, roots, credentials or operations. Authorization exists only in machine-local configuration.
- **Status:** Recommended
- **Feeds:** FR-049, NFR-025
- **Knowledge:** `knowledge/architecture/security-and-privacy.md`, `knowledge/concepts/evidence-semantics.md`

## Scope

**Q2. Which roots and symlink-resolution rules define authorized repository access?**
- **Options:** prefix string comparison; realpath containment; allow anything the user can read.
- **Trade-off:** string prefixes are defeated by `..` and symlinks; allow-anything ignores least privilege; realpath containment is checkable and explainable.
- **Recommendation:** Agree approved roots and containment behavior using canonical-path and escape fixtures before implementation.
- **Why:** A textual path prefix alone does not establish safe containment.
- **Resolution:** Configured roots only. Each access resolves the real path and requires it to remain inside an approved root after resolution; symlinks escaping a root, junctions and case-variant tricks are refused with an inaccessible result, not a crash.
- **Status:** Recommended
- **Feeds:** FR-049, NFR-021; filesystem access policy
- **Knowledge:** `knowledge/architecture/security-and-privacy.md`, `knowledge/architecture/source-adapters.md`

## Behaviour

**Q3. Can ordinary ingestion publish a repaired source file?**
- **Options:** repair the source; report and leave it; copy the repair into a local cache.
- **Trade-off:** repairing crosses authority; leaving it loses a fix; a local cache repair helps the user without touching the source but must never look authoritative.
- **Recommendation:** Do not write or publish as a side effect of reading or analysis.
- **Why:** A source diagnostic is not permission for mutation.
- **Resolution:** Ingestion never writes to a source location. Diagnostics describe the defect and location. No cache repair is performed in the first slice.
- **Status:** Recommended
- **Feeds:** NFR-027; source authority contract
- **Knowledge:** `knowledge/architecture/source-adapters.md`, `knowledge/concepts/evidence-semantics.md`

## Data

**Q4. Where should integration credentials live and how should they be redacted?**
- **Options:** committed config; environment or OS credential store; encrypted database rows.
- **Trade-off:** committed config leaks; an OS store adds platform work; encryption in the database moves the key problem rather than solving it.
- **Recommendation:** Confirm secure machine-local credential handling and explicit redaction rules; exclude secrets from committed settings, payload history and diagnostics.
- **Why:** Local-first operation does not prevent accidental disclosure through artifacts.
- **Resolution:** First slice stores no integration credentials at all (local repository reads only). Values arrive through environment or machine-local settings, are never returned by an API, never written to logs, and errors name the setting rather than its value.
- **Status:** Recommended
- **Feeds:** NFR-023, NFR-026; secret management policy
- **Knowledge:** `knowledge/architecture/configuration-and-secrets.md`, `knowledge/architecture/security-and-privacy.md`

## Integration

**Q5. How should loopback clients and browsers be authorized?**
- **Options:** no authentication on loopback; a shared local token; full user accounts.
- **Trade-off:** loopback-only is reachable by any local process and by browser pages; a local token blocks cross-origin drive-by requests cheaply; accounts are disproportionate here.
- **Recommendation:** Keep non-external binding by default and decide authentication/origin policy from actual local clients and threats.
- **Why:** Loopback is not automatic protection from unauthorized local or browser requests.
- **Resolution:** Recommended default pending owner decision: bind `127.0.0.1`; require a generated local token for mutating operations; restrict `Origin`/CORS to the desktop client. The owner's threat acceptance is what closes this.
- **Status:** Decision needed
- **Feeds:** NFR-022; local HTTP access model
- **Knowledge:** `knowledge/architecture/api-boundary.md`, `knowledge/architecture/security-and-privacy.md`

## Architecture

**Q6. Should every adapter implement an independent interpretation of access authority?**
- **Options:** each adapter decides; one shared policy applied by all adapters; the caller decides.
- **Trade-off:** per-adapter decisions drift and one permissive adapter defeats the rest; a shared policy is uniform but must still permit source-specific mechanisms.
- **Recommendation:** Apply consistent configured access policy across adapters while preserving source-specific permitted mechanisms.
- **Why:** One permissive adapter can bypass otherwise correct portfolio boundaries.
- **Resolution:** A single authorization service resolves roots, containment and read-only rules; adapters may differ in how they read a source but not in what they are allowed to reach.
- **Status:** Recommended
- **Feeds:** FR-049, NFR-021, NFR-025
- **Knowledge:** `knowledge/architecture/source-adapters.md`, `knowledge/architecture/security-and-privacy.md`

## Acceptance

**Q7. What negative cases must demonstrate boundary enforcement?**
- **Options:** happy-path access tests; only unit tests of the path helper; end-to-end negative fixtures through the real entry point.
- **Trade-off:** happy-path tests prove nothing about refusal; unit tests can pass while an adapter bypasses the helper; end-to-end negatives test the boundary that matters.
- **Recommendation:** Exercise path escapes, unauthorized requests, prompt-like content, accidental writes and secret-bearing failures with controlled fixtures.
- **Why:** Happy-path reads cannot prove refusal or redaction behavior.
- **Resolution:** Fixtures: `../` and symlink escapes; a mutating request without a token or with a foreign origin; a source file containing instruction-like text; a read-only source that must remain byte-identical; a failure carrying a credential-shaped string that must not appear in the error.
- **Status:** Recommended
- **Feeds:** NFR-039, NFR-026, NFR-027
- **Knowledge:** `knowledge/practices/testing-and-validation.md`, `knowledge/architecture/security-and-privacy.md`

## Ambiguity

**Q8. What would authorize a future remote exposure or write-enabled integration?**
- **Options:** infer permission from a recommendation; reuse the local token; require a separate explicit decision and boundary.
- **Trade-off:** inference and token reuse extend reach without review; a separate decision is slower but proportionate to the risk.
- **Recommendation:** Require a separately defined explicit configuration/authorization decision and operation boundary rather than infer permission from a recommendation.
- **Why:** Broader reach and mutation introduce new consequences and trust boundaries.
- **Resolution:** Remote binding, remote credentials and any write to a source each require their own change with an explicit decision record, threat review and configuration switch that defaults off.
- **Status:** Recommended
- **Feeds:** NFR-022, NFR-027; future exposure and write policy
- **Knowledge:** `knowledge/architecture/security-and-privacy.md`, `knowledge/practices/knowledge-and-delivery-separation.md`
