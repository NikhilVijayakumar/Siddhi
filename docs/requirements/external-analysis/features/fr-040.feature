# Non-executable acceptance draft; no runner or step definitions.
@FR-040 @NFR-019
Feature: Structural and reference validation
  Scenario: Keep a valid import advisory
    Given an external result conforms to the expected structure and references available inputs
    When validation completes
    Then the result remains a recommendation rather than verified fact

  Scenario: Identify invalid structure and unsupported references
    Given an imported result is incomplete or malformed or cites an unsupported reference
    When result validation runs
    Then the applicable validation problems are identified without accepting unsupported claims as facts