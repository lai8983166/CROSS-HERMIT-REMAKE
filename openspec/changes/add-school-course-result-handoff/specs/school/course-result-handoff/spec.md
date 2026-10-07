## Purpose

Complete MVP fields for the independent sourced school course example and expose the next story entry while preserving its calendar and evidence boundaries.

## ADDED Requirements

### Requirement: Sourced MVP recipient and count
The system SHALL select the first eligible settled student with the greatest strictly positive staged total in settled class order, increment only its MVP count with a cap of five, and reject unsupported input without partial output.

#### Scenario: Ordinary and tied recipients
- **WHEN** a supported confirmed course result is completed
- **THEN** its recipient and capped count match native execution, including first-in-class order for ties

#### Scenario: No eligible recipient
- **WHEN** no eligible assigned student has a positive staged total
- **THEN** the request is refused and owned fields remain unchanged

### Requirement: Once-only owned completion
The school example SHALL complete only its own confirmed frozen course result, validate the current revision and source rules, retain deep ownership, and apply count and handoff once even if delivered repeatedly or plans change later.

#### Scenario: Duplicate and stale request
- **WHEN** completion is delivered again or with a stale revision
- **THEN** a valid duplicate adds no count/revision/journal entry and a stale request changes nothing

### Requirement: Explicit story entry boundary
The system SHALL expose the sourced CH003 ADV request with Chapter016 entry for April week 4 and next task 7, while retaining date 4/4 and never claiming chapter completion or week advancement.

#### Scenario: MVP or confirmation waits
- **WHEN** native MVP input or result confirmation remains pending
- **THEN** no post-confirmation count or ADV request is produced

#### Scenario: Visible completion and restart
- **WHEN** the user completes the confirmed example and subsequently restarts it
- **THEN** the recipient/count and pending story entry are visible after completion and cleared by restart; the source new game remains isolated
