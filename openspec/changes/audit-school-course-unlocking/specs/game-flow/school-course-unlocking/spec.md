# Spec Delta

## Purpose

Provide reproducible course availability from original date thresholds and teacher masks, with isolated data operations that preserve the declared campaign state and expose their evidence boundary.

## ADDED Requirements

### Requirement: Date and source bound availability
The system SHALL scan source work IDs in ascending order, unlocking only previously locked entries whose month-times-six-plus-week threshold has been reached and whose category and key are nonzero. It SHALL distribute each entry to all marked teacher slots without consulting roster availability.

#### Scenario: Date threshold and unavailable teacher
- **WHEN** a marked course reaches its source date and its teacher is absent from the declared roster
- **THEN** its teacher work record is inserted and its global flag is set without changing the roster

#### Scenario: Invalid and unassigned templates
- **WHEN** a reached template has a zero category or key, or has no marked teachers
- **THEN** the invalid template stays locked and a valid unassigned template becomes globally unlocked without adding records

### Requirement: Head insertion and repeat safety
The system SHALL insert newly unlocked courses at the head, shifting only enabled, blocked, work ID, metadata and progress fields. Opaque physical slot bytes SHALL stay in place. Repeated or earlier-date calls SHALL retain already unlocked records.

#### Scenario: Several courses and existing progress
- **WHEN** several courses unlock for a teacher who already has records
- **THEN** the new courses appear in reverse source ID order, existing defined fields retain their order, and new progress is zero

#### Scenario: Repeat call
- **WHEN** the same state is processed again at the same date
- **THEN** no duplicate course is inserted

### Requirement: Validated isolated operation
The system SHALL bind template rules to the audited source, reject malformed states and projected counts over 100 before publishing a result, deep-copy supported output, and preserve date, roster and unrelated metadata. All school readiness, live witness and persistent write authority flags SHALL remain false.

#### Scenario: Capacity refusal
- **WHEN** any teacher would exceed 100 physical records
- **THEN** the entire operation is refused without an after state or input mutation

#### Scenario: Provenance boundary
- **WHEN** original initialization call bytes or Chapter012 joining evidence are reported
- **THEN** they do not authorize adding a teacher to the current declared campaign roster
