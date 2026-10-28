---
type: Practice
title: Knowledge and delivery separation
description: Separate reusable knowledge from behavioral intent, agreed behavior, and implementation evidence.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# Knowledge and delivery separation

Knowledge describes domain meanings, architectural boundaries, rationale, and
reusable engineering practices. It remains meaningful independently of any
particular delivery effort. A knowledge bundle is not an implementation-status
register or a catalogue of acceptance obligations.

Behavioral intent describes an actor's observable outcomes and constraints.
Agreed behavior refines that intent into scenarios and contracts. Implementation
and verification provide evidence about whether that behavior exists.

# Dependency direction

Delivery material references reusable knowledge. Knowledge references only other
knowledge concepts or external publications, never delivery material or source
code. Traceability to historical inputs belongs in a separate delivery audit.

Conversion refines intent rather than deleting its history. Stable identifiers
and decision rationale remain useful after more precise behavior is agreed.

# Drafts and uncertainty

Extracting a statement does not approve it. Agent-authored concepts remain draft
until reviewed; a human verification record requires actual human confirmation.
Unknown interfaces, conflicting alternatives, and proposed numerical targets
remain explicitly unresolved. Familiar tools are not automatically chosen tools.

# Migration safety

Classify statements, not whole files. Mixed documents can contain reusable
explanations, behavioral obligations, illustrative designs, and unanswered
questions. Retain a lossless historical input separately while extracted content
is reconciled. Label historical inputs non-authoritative so they do not compete
with maintained content.

Checks distinguish structural completeness from semantic approval and from
executable verification. A scenario document is not a passing application test.