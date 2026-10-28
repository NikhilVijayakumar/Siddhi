# Non-executable acceptance draft; no runner or step definitions.
@FR-019
Feature: Knowledge availability without correctness claims
  Scenario: Summarize qualified knowledge coverage
    Given a project's knowledge includes accessible and inaccessible and unlinked and stale artifacts
    When knowledge availability is assessed for a goal-related capability
    Then the summary identifies those availability limitations with their basis

  Scenario: Avoid certifying knowledge from presence
    Given a readable concept whose practical applicability has not been assessed
    When available knowledge is summarized
    Then presence is not reported as proof of correctness or completeness or applicability