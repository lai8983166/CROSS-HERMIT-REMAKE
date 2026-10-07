# Spec Delta

## Purpose

Allow the source-backed school to plan class courses using the teacher's available source courses and original adventure/teaching mode rules. Keep planning separate from course execution, calendar progression and original saves.

## ADDED Requirements

### Requirement: Source class modes and assignments
The system SHALL assign an available teacher course to a taught class in teaching mode and reproduce original category/key/course/ordinal fields and rating. Requests outside the available teacher list SHALL fail without changes.

#### Scenario: Select available course
- **WHEN** a taught class in teaching mode selects an available course
- **THEN** the class shows the sourced course and updated rating

#### Scenario: Adventure class
- **WHEN** course assignment is requested for a class in adventure mode
- **THEN** the request is refused without writes

### Requirement: Owned planning transactions
The system SHALL derive planning inputs from owned school state, enforce integer current revisions and publish successful changes atomically. Repeated unchanged actions SHALL preserve the revision.

#### Scenario: Stale selection
- **WHEN** an assignment carries an old revision or unavailable course
- **THEN** snapshot and journal remain unchanged

### Requirement: Explicit course example and navigation
The system SHALL retain the original4/0 school and separately expose a visibly labeled4/4 course example using declared date input and source unlock rules. Course navigation SHALL preserve each independent school and SHALL not execute a week or course settlement.

#### Scenario: Example course selection
- **WHEN** the user opens the4/4 example, switches a class to teaching and selects a course
- **THEN** the course appears in that class while the original school state remains unchanged
