---
type: Technology
title: OpenSpec configuration and schema direction
description: Locally observed configurable artifact-schema conventions with unverified cross-version and target-project compatibility.
status: draft
generated: { by: GitHubCopilot/GPT-6.1-Sol, at: 2026-10-28T00:00:00Z }
---

# OpenSpec configuration and schema direction

Local format inspection shows YAML project configuration selecting a named schema,
with project context and artifact-specific rules. An inspected schema declares
a name, integer version, artifact identifiers, generated locations, template
references, instructions, and dependency lists. This establishes a configurable
artifact-graph direction, not a universal fixed filename catalogue.

The observed schema has a named backend specialization and version 1. That is a
schema declaration, **not an OpenSpec software version** or evidence that every
ingested repository uses that specialization. No local workflow is prescribed
for projects being ingested.

# Format versus source ownership

An ingested project owns its own behavioral declarations, artifact kinds, task
conventions, and archival state. Its schema/configuration provides interpretation
context. Siddhi's own development workflow does not confer authority over that
source or establish its schema. Independently authored engineering knowledge can
exist without source workflow cross-links.

An artifact dependency graph describes declared workflow order. A task marker,
artifact readiness indication, or archive location describes source state, not
successful execution or outcome achievement. Preserving configuration/schema
fingerprints alongside observations helps explain later interpretation changes.

# Access and compatibility direction

Supported machine-readable CLI output can resolve source semantics when available;
read-only files can retain source text and fingerprints. Neither mechanism is
automatically preferable for all operations. CLI availability, version, output
shape, exit/error behavior, scope, environmental schema resolution, and non-mutation
need confirmation. A hybrid also needs revision alignment between reads.

Project/user/packaged schema resolution may affect interpretation. Capture the
effective source and version when determinable; do not silently substitute an
unrelated default. Unknown custom artifacts can retain identity and metadata while
remaining semantically unsupported. Unknown schemas do not justify complete-coverage
claims based only on familiar filenames.

# Explicitly unverified assumptions

This local inspection does not establish the installed CLI's software version,
cross-version output stability, all supported schema-resolution mechanisms, the
standard schema's complete grammar, target projects' custom artifacts, or safe
automated validation commands. No universal parser support or executed adapter
conformance is claimed.

A useful compatibility matrix identifies actual target versions, schema names
and revisions, artifact kinds/grammars, task status conventions, archive/delta
coverage, access method, and unsupported interpretations. Representative fixtures
and demonstrated non-mutation are needed before asserting support. Missing source
IDs and moved declarations require a documented identity fallback rather than
content-similarity merging.

Related: [OpenSpec evidence architecture](../architecture/openspec-integration.md),
[technology index](index.md).