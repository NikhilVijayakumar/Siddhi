# Non-executable acceptance draft; no runner or step definitions.
@FR-018
Feature: Attributed OKF inventory
  Scenario: Expose supported package information
    Given a supported OKF package with metadata and concepts and decisions and links and declared validation status
    When the knowledge inventory is retrieved
    Then the available information is exposed with source references and declared validation attribution

  Scenario: Preserve absent validation as unknown
    Given a supported package with no declared validation information
    When its inventory is retrieved
    Then validation availability is reported without inventing successful validation