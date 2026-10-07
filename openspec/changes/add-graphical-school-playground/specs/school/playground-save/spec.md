## Purpose

Preserve an isolated school playground across launches while validating recovered choices against the same source rules and preventing corrupt saves from partially replacing live state.

## ADDED Requirements

### Requirement: Versioned validated recovery
Playground saves SHALL record a version, context, source-rule fingerprints and bounded supported commands; restoration MUST rebuild a candidate session and validate its final state before publishing it.

#### Scenario: Restore completed teaching
- **WHEN** a valid saved sequence containing grouping, courses, growth, confirmation and MVP is restored
- **THEN** the school state, growth, counts and pending chapter match the saved state with no extra settlement

#### Scenario: Reject incompatible or malformed save
- **WHEN** a save has changed rules, an unsupported version, invalid commands, excess size or a mismatched state digest
- **THEN** restoration fails without changing the active session

### Requirement: Recoverable local writes
The playground SHALL save successful changes locally using a temporary file and replacement with a recoverable previous copy; failed writes SHALL be reported and SHALL not be described as saved.

#### Scenario: Corrupt current save
- **WHEN** the current file is invalid and a valid previous copy exists
- **THEN** the player can recover that previous copy and is told that recovery occurred

### Requirement: Explicit restart and session isolation
Restart SHALL require a confirmation interaction before replacing saved playground progress, and playground saves SHALL not mutate native evidence, original game saves or the existing research sessions.

#### Scenario: Cancel restart
- **WHEN** the player cancels the restart confirmation
- **THEN** both current progress and its saved copy remain intact
