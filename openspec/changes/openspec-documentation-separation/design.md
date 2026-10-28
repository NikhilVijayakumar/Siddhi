# Design

Classify mixed drafts into standalone knowledge and package-owned behavioral
intent. Preserve original bodies under docs/requirements/_source/ before replacing
their original paths with redirects. These inputs are historical evidence, not
a second maintained source of truth. Keep the two existing requirement baselines
as identifier registries while packages add ownership, acceptance examples, and
explicit unresolved decisions. Product details remain draft pending review.

Extract focused concepts rather than mechanically copying large source files.
Retain historical proposed schemas and endpoint catalogues in source inputs until
the owning product change reconciles them. Do not silently decide between them.

Knowledge never links back to input drafts or delivery artifacts. A migration
register outside the bundle records source-to-destination mappings and unresolved
ADR numbering. Draft Decision concepts use semantic names rather than adopting
conflicting historical ADR identifiers.

Update inherited MCP/Sheets-specific workflow language to describe Siddhi's
HTTP/application/adapters boundary without promising new runtime capabilities.
Test baseline discovery red-first, then add heading/table matching. Check all
106 IDs, source preservation, profile metadata, independence, and links.

Review identified two additional false-success cases within the same verification
boundary: missing baseline files and tags on scenario-free features. Treat absent
registries as errors and derive FR coverage only from well-formed features with
at least one scenario. Regression tests must reproduce both failures first.

## Knowledge References

- knowledge/practices/knowledge-and-delivery-separation.md — classification and safe migration.

## Open decisions

First useful product release, real Vyasa contract, access policy, snapshot
publication unit, retention budgets, numerical targets, and provider automation
are not settled by this process change. Package grill logs record them as such.