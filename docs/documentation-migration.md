# Documentation separation report

Date: 2026-10-28. Change: openspec-documentation-separation.
Branch: feature/openspec-documentation-separation-migrate-docs.

## Outcome and authority

- [Knowledge](../knowledge/index.md): standalone draft OKF v0.2 concepts.
- [Requirements](requirements/README.md): 12 draft packages owning all 106 IDs.
- Product conversion and implementation remain later work, after actual review.
- [Process change](../openspec/changes/openspec-documentation-separation/proposal.md):
  documents this migration and the validator correction, not product approval.

Knowledge has no dependencies on requirements, specifications, changes, or code.
Delivery references knowledge. Original requirements remain traceable when later
refined into specifications. Structural validity is neither owner approval nor
evidence of implemented product behavior.

## Source-to-destination registers

- [Product and architecture](migration-product-architecture.md) — eight documents,
  domain/architecture extraction, semantic decision mapping, original checksums.
- [Integrations](migration-integrations.md) — eight documents, source/analysis
  concepts and formats, original checksums, upstream uncertainties.
- [API and engineering](migration-api-engineering.md) — six documents, interface,
  persistence, security, diagnostics, practices and runbooks, preservation evidence.

All 22 old paths are short redirects. Detailed original bodies are retained as
[historical inputs](requirements/_source/README.md), not co-maintained guidance.
Seventeen archives match captured SHA-256 hashes directly. Five API archives have
surplus trailing newlines only; removing those to leave two EOF newline bytes
reconstructs the captured original hashes exactly. The API register documents
the discrepancy. No substantive detail was discarded.

## Reconciliation, not silent decisions

| Topic | Disposition |
|---|---|
| Conflicting historical ADR numbers | Semantic Decision filenames; historical ID-to-subject map retained; all extracted decisions draft |
| Technology and interfaces | Direction/proposal, not implementation evidence; actual Vyasa access contract unverified |
| HTTP/application boundary versus inherited MCP/Sheets wording | Workflow guidance aligned; no MCP server, sync subsystem, or provider automation mandated |
| Evidence terminology | Separate relationship certainty, sufficiency, freshness, processing, verification, and approval |
| Knowledge independence versus source ingestion | External formats may be inspected independently; local delivery references knowledge, never the reverse |
| Minimum goal fields and goal/project relationships | Package desk-review decisions; no silent cardinality/achievement approval |
| Plan revision and milestone membership | Historical mutation/reconstruction ambiguity remains explicit |
| Partial observation and publication | Capture may succeed partially; promotion boundary remains a reviewed contract decision |
| Health routes, authentication, operation recovery | Competing proposals retained; final contract deferred |
| Performance, retention, privacy, reproducibility | Proposed targets/policies require representative workload and owner decisions |
| Manual external handoff versus automated providers | Manual handoff recommended; automation not approved or required by migration |
| First useful release | Goal-to-evidence reporting recommended, not an approved release commitment |

## Review readiness

The 96 grill entries are **desk-review questions and recommendations**, not an
invented interview. Forty-one currently require decisions. Begin with the user's
desired first useful end-to-end outcome, then interrogate the selected package
one question at a time. Conversion must resolve or explicitly accept each
in-scope open decision and preserve its rationale.

The 117 scenarios are acceptance drafts. Some baseline IDs include several
obligations; one tagged scenario does not prove exhaustive acceptance coverage.
Detailed source catalogues still need reconciliation before implementation.

## Verification

The verifier now discovers heading/table baseline IDs and rejects unparsed,
missing, or duplicate baseline declarations. Scenario-free or invalid tagged
features cannot establish FR acceptance coverage. It no longer reports success
merely because the existing level-three headings were ignored.

All checks below were executed on 2026-10-28 after integration and review fixes.

| Check | Result |
|---|---|
| Workflow verification | PASS: schema, templates, change deltas, skills, knowledge, and requirements; no scratch change left |
| Knowledge verification | PASS: 46 concepts, zero errors and zero warnings |
| Requirement verification | PASS: 12 packages, 52 features, 117 scenarios, 96 grill entries, 41 decisions needed; all 50 FR/56 NFR IDs uniquely owned |
| Knowledge and requirement unit tests | PASS: 34 tests (14 knowledge, 20 requirements) |
| Skill synchronization unit tests | PASS: 6 tests |
| Schema end-to-end smoke | PASS: backend artifact chain, contract artifact, templates, skills, validation, and delta parsing |
| Skill references | PASS: 37 skills × 5 agents, zero failures |
| Migration change validation/show | PASS: openspec-documentation-separation validates and parses three process deltas |
| Archive audit | PASS with disclosed whitespace exception: 17 exact files plus five EOF-only variants recover all 22 captured original hashes |
| Redirect audit | PASS: all 22 old paths are short redirects, with no retained mixed draft bodies |
| Maintained Markdown links | PASS: 783 relative target occurrences resolve at audit time, excluding intentionally historical input links |
| Editor diagnostics | No errors in changed validator/test and workflow YAML files |

Independent review found two additional validator false-success paths: an absent
baseline and a tagged feature with no scenarios. Four new regression tests were
run first and failed (five failure reports including subtests); after the fixes,
all 20 requirement-validator tests pass. No unresolved review defect remains
within this migration's scope.

## Limits and Git state

- No product runtime, HTTP endpoint, adapter compatibility, database migration,
  security control, backup restoration, or performance behavior was executed or
  certified. The application remains a skeleton.
- No real stakeholder grill interview has occurred. Forty-one package choices
  still require decisions; numerical targets remain proposals.
- Historical input links and rendering markup intentionally remain uncorrected.
  External websites were not checked for current availability.
- Existing staged/unstaged source work was preserved. No staging, commit, push,
  merge, release, or archive was performed. The documentation working branch is
  feature/openspec-documentation-separation-migrate-docs; its eventual merge target
  is develop, after review and the normal synchronization/commit safeguards.