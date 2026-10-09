## Purpose

Extend the playable fourth-week school slice into the fifth-week workroom and school planning while preserving earned growth and saved progress. Keep source evidence, remake interaction, and the unimplemented next settlement boundary explicit.

## ADDED Requirements

### Requirement: Source verified fifth week school entry
The system SHALL verify workroom, CH002, school dispatch and school data initialization on the same original CPU that completed the current fourth-week course and fifth-week Chapter018. It MUST retain explicit input, presentation and scheduler boundaries and MUST NOT substitute another campaign's snapshots.

#### Scenario: Actual fifth week continuation
- **WHEN** native Chapter018 produces pending state8 on 4/5
- **THEN** continuation consumes that request once and records workroom control, CH002 and school initialization with before/after data and source hashes

#### Scenario: Waiting prevents later stages
- **WHEN** the workroom continue input or CH002 readiness is unavailable
- **THEN** school preparation does not execute and earned records remain intact

### Requirement: Durable workroom and school planning
The system SHALL allow entering the workroom and then fifth-week school once, retaining current member growth, relationships, equipment, MVP and fourth-week review. Fifth-week members SHALL be editable using verified movement. Courses SHALL be viewable but selection MUST be refused while the source mandatory adventure gate is active. Second settlement MUST remain unavailable in this change.

#### Scenario: Enter and edit new week
- **WHEN** the player enters school after the fifth-week workroom
- **THEN** the calendar shows 4/5, current members and attributes carry forward, and class movements update only the fifth-week plan and mandatory adventure prevents direct course selection

#### Scenario: Repeat or invalid commands
- **WHEN** an entry command repeats or a command is premature, malformed or chooses an unavailable course
- **THEN** it is idempotent or refused atomically without granting growth, advancing the date or changing the saved command history

### Requirement: Compatible atomic saves
The system SHALL preserve v1/v2/v3 save loading with their original fingerprints and state verification, and save workroom and fifth-week plans in a new version with strict command replay. Failed load or write MUST preserve current memory and the existing recoverable saves.

#### Scenario: Old fifth week progress migrates
- **WHEN** a genuine v3 partial Chapter018 or completed exit save is loaded
- **THEN** its exact progress and earned records restore before any new workroom or school command runs

#### Scenario: Restore edited school plan
- **WHEN** the player saves in the workroom or after fifth-week class edits and relaunches
- **THEN** the correct screen and exact plan restore, without replaying the fourth-week reward into the fifth-week records

### Requirement: Graphical workroom navigation
The system SHALL show a source-derived workroom background and clear actions to enter school, review the prior course, save or preview battle. The fifth-week school SHALL show usable member controls and viewable locked courses and communicate the next settlement boundary. Restart and skip confirmations and battle return SHALL retain their existing behavior.

#### Scenario: Use workroom controls
- **WHEN** the player finishes fifth-week dialogue and chooses to enter the workroom
- **THEN** source-derived workroom art and entry controls appear, and entering school opens fifth-week planning

#### Scenario: Battle round trip and review
- **WHEN** the player reviews fourth-week results or enters and returns from battle during the new continuation
- **THEN** the fifth-week location and plan remain available and no date, reward or class edits are lost

### Requirement: Source verified mandatory adventure preparation
The system SHALL derive departure readiness and round teacher/student lists from current fifth-week classes using source-verified conditions and adventure records. Preparation MUST preserve all school records and MUST NOT execute battle, grant rewards or clear the mandatory gate.

#### Scenario: Prepare current classes
- **WHEN** at least one source-valid adventure class is ready and no nonempty invalid class exists
- **THEN** preparation shows the current teachers, students, class indices and source scene selection without changing school or save state

#### Scenario: Incomplete class prevents departure
- **WHEN** a teacher has no student or no class qualifies
- **THEN** preparation reports not ready and preserves the current plan and rewards

### Requirement: Graphical departure preparation
The system SHALL allow viewing fifth-week mandatory adventure preparation from school, showing source adventure and scene identities and current member portraits. Returning to class editing and reopening MUST recompute from current classes. Actual battle execution MUST remain visibly unavailable until its next chain is implemented.

#### Scenario: Edit and reopen preparation
- **WHEN** the player views preparation, returns to edit classes and opens it again
- **THEN** the screen reflects the updated current members, offers school save/load/review navigation and does not substitute the independent battle preview roster

### Requirement: Source verified school to first round handoff
The system SHALL verify native school commit, source group request10, native state10 construction and first-round preparation on the current fifth-school CPU checkpoint. It MUST distinguish native configuration scalar and roster writes from unresolved resource loading and combat-unit derivation, and MUST NOT claim playable battle, rewards or mandatory-gate clearance.

#### Scenario: Current squad enters source round preparation
- **WHEN** current classes satisfy source readiness and the confirmed-menu input boundary is supplied
- **THEN** native school commit updates the adventure ledger, the resumed source group requests10, and the consumed native preparation task transfers current students to configuration5 and requests16 while role records, MVP and calendar remain unchanged

#### Scenario: Invalid squad never commits
- **WHEN** current classes fail readiness
- **THEN** neither commit nor request10 occurs and the complete school, role and adventure ledger state remains unchanged

### Requirement: Pure current school handoff projection
The system SHALL derive a handoff from current school and its adventure ledger using independent validated source inputs. The projection MUST match native ledger and first-round defined outputs, preserve member order and input ownership, and MUST NOT mutate the player's saved plan or add persistent commands.

#### Scenario: Project edited or waiting members
- **WHEN** a supported current school and ledger are projected
- **THEN** the output contains the native-equivalent committed ledger, ordered students, source configuration and request sequence, with combat unit readiness explicitly false

#### Scenario: Malformed or unsupported handoff inputs
- **WHEN** source rules, ledger or school data are malformed or outside the verified subset
- **THEN** projection refuses atomically without changing input, save, calendar or rewards
