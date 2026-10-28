# Non-executable acceptance draft; no runner or step definitions.
@FR-015
Feature: Attributed declared progress
  Scenario: Summarize supported declaration evidence
    Given supported task and change artifacts declare their completion states
    When a development-progress summary is generated
    Then the summary references the artifacts supporting each declared state

  Scenario: Keep completion separate from verification
    Given a task is declared complete but no independent verification evidence is available
    When progress is summarized
    Then declared completion is visible without claiming verified implementation