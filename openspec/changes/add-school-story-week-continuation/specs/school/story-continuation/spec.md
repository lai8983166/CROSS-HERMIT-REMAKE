## Purpose

Let a school playground player continue from course results through the original fourth-week scenes and reach the next verified calendar state without losing progress.

## ADDED Requirements

### Requirement: Source-traceable continuation
The continuation SHALL use the original Chapter016 and Chapter017 dialogue order and speaker selection, with source hashes. Its isolated native evidence MUST distinguish executed control flow from presentation and scheduler boundaries.

#### Scenario: Course-following chapter completion
- **WHEN** the audited course result enters Chapter016 and Chapter017 reaches END
- **THEN** the continuation records the actual state7 request and preserves course growth and MVP results.

### Requirement: Graphical dialogue controls
The player SHALL be able to enter the story after course results, read original dialogue with scene imagery and speaker labels, advance, revisit previous text, return to results and confirm skipping.

#### Scenario: Revisiting and skipping
- **WHEN** a player returns to the previous text or confirms skipping the remaining dialogue
- **THEN** revisiting does not change school records, and skipping completes the same bounded story once.

### Requirement: Durable validated reading progress
Saving and loading SHALL preserve the exact story cursor and completion state. Invalid replay, mismatched resources or malformed save data MUST leave the current state unchanged. Valid existing version1 playground saves SHALL migrate without losing school results.

#### Scenario: Restart during the second scene
- **WHEN** a player saves during the second scene and restarts
- **THEN** the same text, school records and MVP count are restored.

#### Scenario: Existing completed course save
- **WHEN** a valid version1 save is loaded
- **THEN** its original course state is restored and the new story remains available.

### Requirement: Once-only next-week arrival
After story completion the playground SHALL project the verified 4/4 to 4/5 week body once, including source unlock and cleanup changes. It MUST retain course results, persist arrival and state the next school setup boundary without enabling unsupported fifth-week courses.

#### Scenario: Duplicate advance and navigation
- **WHEN** the player advances to the next week, saves, visits battle preview and returns
- **THEN** the date remains 4/5, growth and MVP counts are unchanged, and a repeated advance cannot settle another week.
