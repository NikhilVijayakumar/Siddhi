# Non-executable acceptance draft; no runner or step definitions.
@FR-050 @NFR-010 @NFR-045 @NFR-046 @NFR-047 @NFR-049 @NFR-054 @NFR-055 @NFR-056
Feature: Reliable configurable local operation
  Scenario: Operate locally using documented settings
    Given valid supported configuration specifying the SQLite location and no cloud connection
    When the service starts and stored portfolio information and reports are retrieved and the service shuts down
    Then local operations work and lifecycle and diagnostics follow documented procedures

  Scenario: Reject invalid required configuration
    Given a missing or invalid required environment setting
    When startup validates configuration
    Then an actionable safe error identifies the problem without requiring application source changes

  Scenario: Restore a consistent backup
    Given portfolio history and a backup made consistently with SQLite transaction and journaling behavior
    When the documented restoration procedure is tested with its schema context
    Then required records and relationships and historical decisions are recoverable

  Scenario: Preserve history when growth requires review
    Given snapshot and report retention causes measurable database growth
    When storage growth and retention cost are inspected
    Then durable decisions and plan revisions are distinguished from reconstructible caches and no history is deleted merely for convenience

  Scenario: Report interrupted work on lifecycle recovery
    Given a background operation was interrupted before service shutdown completed
    When the service restarts under the agreed recovery policy
    Then interrupted work is reported and database state remains consistent without unmanaged hidden work