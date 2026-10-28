# Security desk review

Desk review only, no interview or user confirmation. A goal-to-evidence report is the recommended first-release goal, NOT an approved release choice. Threat-model and local-client policy decisions below remain open.

## Intent

**Q1. Can repository text authorize a wider filesystem read?**
- **Recommendation:** Treat all source and imported output as data; only configured authorization can grant access.
- **Why:** Instructions embedded in evidence cross no legitimate trust boundary.
- **Status:** Recommended
- **Feeds:** FR-049, NFR-025

## Scope

**Q2. Which roots and symlink-resolution rules define authorized repository access?**
- **Recommendation:** Agree approved roots and containment behavior using canonical-path and escape fixtures before implementation.
- **Why:** A textual path prefix alone does not establish safe containment.
- **Status:** Decision needed
- **Feeds:** FR-049, NFR-021; filesystem access policy

## Behaviour

**Q3. Can ordinary ingestion publish a repaired source file?**
- **Recommendation:** Do not write or publish as a side effect of reading or analysis.
- **Why:** A source diagnostic is not permission for mutation.
- **Status:** Recommended
- **Feeds:** NFR-027; source authority contract

## Data

**Q4. Where should integration credentials live and how should they be redacted?**
- **Recommendation:** Confirm secure machine-local credential handling and explicit redaction rules; exclude secrets from committed settings, payload history and diagnostics.
- **Why:** Local-first operation does not prevent accidental disclosure through artifacts.
- **Status:** Decision needed
- **Feeds:** NFR-023, NFR-026; secret management policy

## Integration

**Q5. How should loopback clients and browsers be authorized?**
- **Recommendation:** Keep non-external binding by default and decide authentication/origin policy from actual local clients and threats.
- **Why:** Loopback is not automatic protection from unauthorized local or browser requests.
- **Status:** Decision needed
- **Feeds:** NFR-022; local HTTP access model

## Architecture

**Q6. Should every adapter implement an independent interpretation of access authority?**
- **Recommendation:** Apply consistent configured access policy across adapters while preserving source-specific permitted mechanisms.
- **Why:** One permissive adapter can bypass otherwise correct portfolio boundaries.
- **Status:** Recommended
- **Feeds:** FR-049, NFR-021, NFR-025

## Acceptance

**Q7. What negative cases must demonstrate boundary enforcement?**
- **Recommendation:** Exercise path escapes, unauthorized requests, prompt-like content, accidental writes and secret-bearing failures with controlled fixtures.
- **Why:** Happy-path reads cannot prove refusal or redaction behavior.
- **Status:** Recommended
- **Feeds:** NFR-039, NFR-026, NFR-027

## Ambiguity

**Q8. What would authorize a future remote exposure or write-enabled integration?**
- **Recommendation:** Require a separately defined explicit configuration/authorization decision and operation boundary rather than infer permission from a recommendation.
- **Why:** Broader reach and mutation introduce new consequences and trust boundaries.
- **Status:** Decision needed
- **Feeds:** NFR-022, NFR-027; future exposure and write policy