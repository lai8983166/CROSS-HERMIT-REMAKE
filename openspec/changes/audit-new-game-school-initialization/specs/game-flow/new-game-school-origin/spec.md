# Spec Delta

## Purpose

Establish a reproducible school origin from the original new-game initializer, with explicit teacher provenance, owned session data and separate raw initialization and school preparation states for later interactive grouping.

## ADDED Requirements

### Requirement: Source bound school origin
The system SHALL construct the audited school subset from verified original initialization calls, member template fields and relationship data. The origin SHALL have date4/0, teacher101 and students3/4/9 in group0, reset pending, empty course buffers, and the original raw/derived field lifecycle.

#### Scenario: Fresh origin
- **WHEN** verified source rules construct a new school origin
- **THEN** the teacher and student lists, initial placement and source profiles are produced without consuming expected output checkpoints

#### Scenario: Inconsistent rules
- **WHEN** an initialization call, profile, relationship or source binding is changed
- **THEN** construction is refused without publishing a snapshot

### Requirement: Explicit school data preparation
The system SHALL keep origin construction separate from course unlocking, group reconciliation and rating. Preparation SHALL use the source date and teacher domain, preserve profiles and date, and expose every defined phase without claiming full menu execution.

#### Scenario: Prepare the initialized group
- **WHEN** the origin is prepared for school data operations
- **THEN** courses are evaluated, raw member count and selection are reconciled, derived fields are rated, and the teacher remains101

### Requirement: Owned repeat safe session
The system SHALL own deep copies of source rules, snapshot and journal, publish initialization and preparation only once per session, reject stale preparation revisions, and leave legacy returned campaigns unchanged. School readiness, live witness and persistent write flags SHALL remain false.

#### Scenario: Repeated or stale request
- **WHEN** initialization is repeated with conflicting input or preparation is requested against a stale revision
- **THEN** no new state or journal entry is published

#### Scenario: Independent sessions
- **WHEN** callers alter an exposed view or initialize another session
- **THEN** existing source rules, state and journal are unaffected
