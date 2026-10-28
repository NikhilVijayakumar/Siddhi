# Non-executable acceptance draft; no runner or step definitions.
@FR-013 @NFR-003
Feature: Correct incremental processing
  Scenario: Avoid reparsing unchanged content
    Given reliable source identity and a revision or content hash matching processed input
    When incremental refresh evaluates that content
    Then unnecessary reparsing is avoided without changing the normalized meaning

  Scenario: Detect changed content despite unchanged time
    Given source content changed while its timestamp stayed the same or became unreliable
    When refresh uses available stronger revision or content evidence
    Then changed content is processed correctly rather than skipped solely because of the timestamp