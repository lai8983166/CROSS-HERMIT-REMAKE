# Spec Delta

## Purpose

Provide usable grouping for the school roster established by the original new-game initializer. Preserve source-backed movement behavior, coherent owned state and independent navigation without requiring the user to operate the original executable.

## ADDED Requirements

### Requirement: Source scoped grouping
The system SHALL support moves of teacher101 and students3/4/9 within the source new-game roster, matching separately observed original movement, cleanup and rating phases.

#### Scenario: Teacher moves to an empty class
- **WHEN** teacher101 is moved from its class to another empty class
- **THEN** the original class students return to waiting and the final class counts and indices are coherent

#### Scenario: Student swaps an occupied position
- **WHEN** a student moves onto another student in a taught class
- **THEN** the two positions exchange according to source behavior

### Requirement: Atomic owned commands
The system SHALL derive command sources from owned prepared school state and publish all successful movement phases at one revision. Invalid, unsupported or stale requests SHALL preserve state and journal.

#### Scenario: Stale version
- **WHEN** a member move uses an earlier revision
- **THEN** the request is refused without partial changes

### Requirement: Operable school window
The system SHALL expose the new school roster, five class rows and waiting members from the main window. Users SHALL move members by clicking a member then its target, cancel selection, navigate back and restart the school session explicitly.

#### Scenario: Window grouping
- **WHEN** the user selects a student and clicks waiting
- **THEN** the roster and class counts refresh from the published session

#### Scenario: Navigation and battle isolation
- **WHEN** the school window is open and the user presses battle restart or changes class membership
- **THEN** battle state remains unchanged; closing and reopening preserves the school session
