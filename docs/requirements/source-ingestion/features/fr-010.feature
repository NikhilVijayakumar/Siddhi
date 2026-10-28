# Non-executable acceptance draft; no runner or step definitions.
@FR-010 @NFR-011 @NFR-012 @NFR-016
Feature: Provenance-preserving normalization
  Scenario: Locate the origin of a normalized record
    Given a supported source record with a known revision and source event time
    When the record is normalized
    Then its queryable form retains the source reference and revision and distinguishes event time from ingestion time

  Scenario: Do not invent missing provenance or authority
    Given a source declaration without an available modification timestamp
    When the declaration is normalized
    Then it remains a source declaration and the unavailable timestamp is not fabricated