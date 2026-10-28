# Non-executable acceptance draft; no runner or step definitions.
@FR-009 @NFR-031
Feature: Verified format parsing
  Scenario: Parse a supported layout using its verified format
    Given artifacts using different explicitly supported versions and layouts
    When their applicable parsers process them
    Then interpretation follows each verified format rather than one assumed repository layout

  Scenario: Refuse silent version fallback
    Given an artifact declares an unsupported version and another is malformed
    When parsing is attempted
    Then unsupported and invalid outcomes are reported without treating either as valid supported input