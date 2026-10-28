# Non-executable acceptance draft; no runner or step definitions.
@FR-027
Feature: Explicit finding classifications
  Scenario: Preserve the baseline finding distinctions
    Given agreed rules and fixtures representing confirmed relationship and candidate match and identified gap
    And fixtures representing missing evidence and unresolved evidence and stale or unavailable input
    When the findings are classified
    Then each applicable distinction and its rule basis remains visible

  Scenario: Do not turn missing evidence into a gap
    Given a capability cannot be assessed because the relevant source is inaccessible
    When a goal comparison is classified
    Then unavailable or missing evidence is visible without a demonstrable absence claim