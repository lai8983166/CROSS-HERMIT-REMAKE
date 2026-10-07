# Spec Delta

## Purpose

Provide source-backed course growth and skill learning for students in an assigned teaching class. Expose the result once in the independent declared-date course example while preserving calendar and other school sessions.

## ADDED Requirements

### Requirement: Source course growth
The system SHALL compute course packets, capped growth pools, skill learning and recalculated attributes/levels using validated source rules and the declared random seed. Waiting students SHALL remain unchanged and unsupported inputs SHALL refuse without mutation.

#### Scenario: Assigned teaching class
- **WHEN** a valid teaching class with an available course settles
- **THEN** its students receive source-matching packets, skills, attributes and levels

#### Scenario: Waiting student
- **WHEN** a student is outside the settled class
- **THEN** that student's complete growth record remains unchanged

### Requirement: Once-only owned settlement
The system SHALL settle the declared4/4 example atomically under a current integer revision. Repeat completion SHALL preserve data and revision; stale or unsupported requests SHALL leave all owned state and journal unchanged.

#### Scenario: Repeat completion
- **WHEN** the completed example is asked to settle again with its current revision
- **THEN** no additional growth or journal entries are published

#### Scenario: Stale request
- **WHEN** a request uses an old revision or unsupported rules
- **THEN** no student or school field is changed

### Requirement: Course settlement example window
The system SHALL expose a labeled course settlement action and student changes in the independent example. Completion SHALL keep its date fixed, preserve the original new-game and returned campaign, and reset only through the active example restart.

#### Scenario: Complete and navigate
- **WHEN** the user completes an example course and switches schools
- **THEN** the result is retained in the example and other school data remains unchanged
