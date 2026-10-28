# Non-executable acceptance draft; no runner or step definitions.
@FR-042
Feature: Focused authorized repository investigation
  Scenario: Request and validate a focused investigation
    Given stored evidence cannot answer a defined question and a coding agent is authorized for the investigation
    When the question-focused structured investigation result is returned
    Then the result is validated before it is ingested as investigation evidence

  Scenario: Keep routine operations independent of investigation
    Given no authorized coding-agent investigation is available
    When routine source parsing and defined-rule reporting are requested for stored supported inputs
    Then those routine operations do not require the investigation workflow