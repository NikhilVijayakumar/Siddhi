# Non-executable acceptance draft; no runner or step definitions.
@FR-017
Feature: OpenSpec remains authoritative and unchanged
  Scenario: Ingest without source changes
    Given authoritative requirements and tasks and schemas and change artifacts
    When routine ingestion and analysis run
    Then their source contents remain unchanged

  Scenario: Report malformed source without repair
    Given an OpenSpec artifact cannot be parsed under its supported schema
    When ingestion reports the parsing failure
    Then the artifact is not rewritten or repaired as a side effect