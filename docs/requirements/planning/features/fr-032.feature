# Non-executable acceptance draft; no runner or step definitions.
@FR-032
Feature: Preserved plan revisions
  Scenario: Retrieve a previous plan
    Given a recorded initiative plan
    When the owner revises it with a supplied rationale
    Then both versions and the supplied revision rationale remain retrievable

  Scenario: Protect an approved plan from advice
    Given an approved plan and a new external recommendation
    When the recommendation is imported
    Then the approved plan remains unchanged without an explicit plan revision