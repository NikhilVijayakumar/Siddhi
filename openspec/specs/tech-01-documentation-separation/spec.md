# tech-01-documentation-separation Specification

## Purpose
Keeps reusable knowledge, draft behavioral intent, and delivery artifacts separate and traceable, so each can change without silently rewriting the others.

## Requirements

### Requirement: Independent knowledge ownership

The documentation workflow SHALL maintain reusable concepts in a profile-compliant OKF bundle independently of delivery artifacts, following knowledge/practices/knowledge-and-delivery-separation.md.

#### Scenario: Extract a mixed draft

- **GIVEN** a draft containing reusable explanation and behavioral obligations
- **WHEN** its content is classified
- **THEN** reusable knowledge has no dependency on requirement, specification, or implementation artifacts
- **AND** behavioral intent remains in draft requirement material with knowledge references

### Requirement: Preserve intent and uncertainty

The migration SHALL preserve all 106 existing baseline identifiers, uniquely assign their package ownership, retain lossless historical input, and keep unresolved decisions explicitly unapproved.

#### Scenario: Review migration traceability

- **GIVEN** the original 50 FR and 56 NFR identifiers
- **WHEN** migration completeness is checked
- **THEN** each identifier has exactly one owning package
- **AND** every FR has a tagged acceptance scenario
- **AND** retained historical draft bodies can be located from their old paths
- **AND** no interview response or human approval is fabricated

### Requirement: Detect actual baseline coverage

The requirement validator SHALL recognize baseline identifiers in both supported table rows and Markdown headings, require both baseline files, and SHALL report missing ownership rather than passing an unparsed baseline. Feature tags SHALL establish acceptance coverage only when the feature contains a valid scenario.

#### Scenario: Heading-based baseline lacks packages

- **GIVEN** FR and NFR baselines using level-three headings
- **WHEN** validation runs without packages
- **THEN** every baseline identifier is reported as unowned

#### Scenario: Existing table-based baseline

- **GIVEN** baseline identifiers in the supported table format
- **WHEN** validation runs
- **THEN** existing ownership and feature-tag checks still apply

#### Scenario: Missing baseline file

- **GIVEN** either baseline file has been deleted or is absent
- **WHEN** validation runs
- **THEN** validation reports the missing baseline file as an error

#### Scenario: Feature contains no scenario

- **GIVEN** an FR-tagged feature with no scenarios
- **WHEN** validation runs
- **THEN** the feature is rejected and cannot establish acceptance coverage
