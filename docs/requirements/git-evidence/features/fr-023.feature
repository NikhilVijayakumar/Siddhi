# Non-executable acceptance draft; no runner or step definitions.
@FR-023
Feature: Activity is supporting evidence only
  Scenario: Describe activity within its scope
    Given revision observations for a defined repository interval
    When the system summarizes activity
    Then activity is presented as scoped supporting evidence

  Scenario: Avoid activity-only delivery claims
    Given many recent commits and an active branch without outcome verification
    When progress evidence is summarized
    Then those observations are not treated as proof of meaningful progress or successful delivery