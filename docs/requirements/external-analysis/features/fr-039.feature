# Non-executable acceptance draft; no runner or step definitions.
@FR-039 @NFR-019
Feature: Attributed external result import
  Scenario: Retain available external origin
    Given a structured external result with origin and model identity and generation time and input references
    When its assumptions and recommendations and uncertainty are imported
    Then the result retains that metadata and remains distinguishable from deterministic findings

  Scenario: Do not invent unavailable model metadata
    Given an otherwise usable structured result whose model or generation time is unavailable
    When the result is imported under the agreed structure
    Then unavailable metadata is not fabricated to imply stronger attribution