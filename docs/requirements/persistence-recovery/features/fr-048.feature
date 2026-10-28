# Non-executable acceptance draft; no runner or step definitions.
@FR-048 @NFR-037
Feature: Controlled database evolution
  Scenario: Upgrade a representative previous schema
    Given a database at a supported earlier schema version with portfolio history
    When controlled migrations complete successfully
    Then the new schema version is identifiable and the required data and history remain consistent

  Scenario: Report a failed migration safely
    Given a representative earlier database and a migration that fails
    When database evolution is attempted
    Then the failure is explicitly reported and no successful upgrade is falsely recorded over an inconsistent state