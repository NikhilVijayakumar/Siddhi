# Non-executable acceptance draft; no runner or step definitions.
@FR-024
Feature: Attributed verification artifacts
  Scenario: Ingest an existing verification result
    Given a supported existing test or build or release artifact with source and revision and timestamp
    When verification evidence is ingested
    Then its recorded outcome retains those available provenance fields

  Scenario: Preserve missing verification as unknown
    Given no supported verification artifact is available for a revision
    When verification evidence is retrieved
    Then verification is unknown or unavailable rather than a failed test or successful release