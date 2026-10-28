# Non-executable acceptance draft; no runner or step definitions.
@FR-006
Feature: Explain meaningful portfolio revisions
  Scenario: Preserve the reason for a changed priority
    Given a goal with an existing priority
    When the owner changes its priority and supplies a rationale
    Then history identifies the prior and new priority and change time and rationale

  Scenario: Do not fabricate revision rationale
    Given a meaningful initiative or plan revision without a supplied rationale
    When the owner inspects its history
    Then the change and its time remain traceable without an invented rationale