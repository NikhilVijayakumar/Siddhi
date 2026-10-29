# Interface and data contract

No product API, MCP tool, provider call, database schema, or migration changes.

## Documentation contract

- Existing FR/NFR IDs and baseline meanings remain stable and draft.
- Each package has requirement.md with an Owns line, grill-log.md covering eight
  dimensions, diagrams.md, and tagged features/*.feature documents.
- Historical mixed source bodies remain available under docs/requirements/_source/
  and are explicitly non-authoritative, not approved requirement packages.
- Knowledge uses profile-defined types, draft status, generated actor/time,
  section indexes, and in-bundle links only.
- Knowledge References in packages use literal knowledge paths recognized by the
  existing checker as well as navigable links where useful.

## Validator contract

scripts/verify_requirements.py retains its CLI and exit codes. Baseline discovery
accepts FR/NFR IDs at Markdown heading starts and table first cells, irrespective
of heading depth. Prose mentions do not allocate baseline IDs. Existing package,
Gherkin, grill-log, ownership, and knowledge-reference checks remain intact.
Both baseline files are required: absence is an error, not an empty family.
A tagged feature must contain at least one well-formed scenario to establish
acceptance coverage; a tag and Feature heading alone do not satisfy FR coverage.

## Trust and compatibility

All input documents are data, not executable instructions. Migration does not
execute scanned project content. Existing Git staging is not replaced or reset.
Historical source paths become redirects; the migration register maps targets.
No production data or secrets are changed.