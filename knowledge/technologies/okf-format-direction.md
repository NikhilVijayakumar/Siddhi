---
type: Technology
title: OKF format and local profile direction
description: Observed Markdown/frontmatter bundle conventions and the limits of extrapolating them to other OKF sources.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# OKF format and local profile direction

The locally inspected knowledge bundle declares OKF version 0.2 and uses Markdown
with YAML frontmatter. Its observed direction is a small base format plus an
explicitly stricter local profile, not a universal taxonomy for every source.
This observation describes local documents; it does not certify external tooling
or conformance of another bundle.

# Observed local conventions

- The bundle root declares a format version and navigates to section collections.
- Concept documents use `type`, `title`, `description`, `status`, and `generated`.
- The local profile maps type names to folders, including Architecture and Technology.
- Its status vocabulary is draft, stable, and deprecated.
- Generated attribution identifies an actor and time. Human verification is a
  separate claim and is not implied by an agent-created draft.
- Internal links express navigable relationships among independently meaningful
  concepts; external documentary dependencies are restricted by the local profile.
- The local profile adds independence rules and a 400-line bound per concept.

The stricter field set, folder taxonomy, status vocabulary, and line bound are
local policy observations, not claims about mandatory fields in every OKF source.
Neither a parseable YAML header nor a present attribution establishes truth.

# Reader implications

A source-aware reader separates base-format parsing from source-profile validation.
It preserves native type/status and unfamiliar metadata rather than discarding
everything outside the local vocabulary. A source may identify concepts by relative
path or by an explicit independent ID; actual identity semantics need confirmation.
Links can remain unresolved or cyclic without making every concept unreadable.

Generation, review, and verification metadata describe attributed events. Their
actor identity, scope, revision applicability, and trust meaning are not invented
by the importer. A successful structural check is not implemented capability,
production verification, or proof that the described architecture is current.

# Explicitly unverified assumptions

No universal OKF CLI, validation command, API/export schema, canonical identity
scheme, or supported extension set is established here. Other target bundles'
versions, profiles, validators, provenance semantics, and access methods remain
unverified. Public format descriptions alone would not demonstrate what an installed
source actually guarantees.

Before claiming compatibility, inspect representative source metadata and links,
the actual applicable format/profile, any supported validator's non-mutating
behavior, identity-on-move semantics, and revision signals. Record that supported
matrix separately from generic claims of being able to read Markdown.

Related: [OKF architecture](../architecture/okf-integration.md),
[technology index](index.md).