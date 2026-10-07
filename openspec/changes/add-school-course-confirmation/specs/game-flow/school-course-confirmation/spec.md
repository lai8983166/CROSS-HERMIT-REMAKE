# Spec Delta

## Purpose

Provide source-backed confirmation of career progress, weekly activity history and relationships after course growth in the independent declared-date school example.

## ADDED Requirements

### Requirement: Source confirmation fields
The system SHALL derive confirmation fields from validated source rules and the settled roster, matching native execution for assigned and waiting students, career boundaries, relationship clamps and moved classes, without consuming expected snapshots at runtime.

#### Scenario: Assigned and waiting students
- **WHEN** a validated example course has grown its participating students
- **THEN** confirmation increments all enrolled students' current career progress, records course or waiting activity at the declared date and applies native directed relationship updates

#### Scenario: Invalid input
- **WHEN** source rules, date, roster or records are invalid
- **THEN** confirmation refuses without modifying input or published state

### Requirement: Atomic once-only confirmation
The system SHALL confirm a completed example settlement once with a current integer revision, publish all fields and ratings atomically, use the captured settlement roster despite later plan edits and return deep copies.

#### Scenario: Confirmation and duplicate
- **WHEN** confirmation is delivered twice to the same completed example
- **THEN** only the first valid delivery changes state, revision and journal

#### Scenario: Captured context and independent sessions
- **WHEN** the plan is edited after settlement, or a source-new-game session attempts confirmation
- **THEN** confirmation uses the original settled roster in the example and rejects the source-new-game request while preserving all other sessions

### Requirement: Visible bounded confirmation
The system SHALL offer a confirmation-fields action after example growth, show career/history/relationship changes, preserve completion on navigation and reset it only on explicit example restart, while stating that the calendar and save have not advanced.

#### Scenario: Real input and restart
- **WHEN** the user clicks confirmation, navigates away and back, then restarts the example
- **THEN** changes appear once, remain visible across navigation and are cleared for the new example
