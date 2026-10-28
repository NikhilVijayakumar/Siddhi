# Non-executable acceptance draft; no runner or step definitions.
@FR-022
Feature: Supported revision observations
  Scenario: Collect available revision evidence
    Given the authorized source supports commits and branches and tags and timestamps and changed paths
    When revision evidence is collected
    Then available observations retain their source and exact revision context

  Scenario: Qualify limited history
    Given source access exposes only a limited history without some changed-path details
    When revision evidence is reported
    Then unavailable evidence is qualified without implying complete repository coverage