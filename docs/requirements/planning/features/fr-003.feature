# Non-executable acceptance draft; no runner or step definitions.
@FR-003
Feature: Initiatives independent of repositories
  Scenario: Coordinate multiple goals
    Given two goals and no repository for the proposed work
    When the owner creates an initiative supporting both goals
    Then the initiative exists with both goal relationships and can hold a versioned plan

  Scenario: Retain a cancellation decision
    Given an initiative with existing project and dependency links
    When the owner cancels it with a recorded decision
    Then the cancellation and decision remain available with the initiative's context