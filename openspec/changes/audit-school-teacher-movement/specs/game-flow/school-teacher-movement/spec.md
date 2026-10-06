# Spec Delta

## Purpose

提供来源明确的教师移动与工作表投影，保留教师替换、交换、学生回待命、工作字段清理和即时/整理状态之间的原版区别，作为后续编班交互的数据前置条件，不授予实机或存档权限。

## ADDED Requirements

### Requirement: Teacher placement replacement and exchange
The isolated operation SHALL place or replace waiting teachers and move or exchange assigned teachers using sourced release behavior. An unoccupied destination SHALL return the source class students to waiting; an occupied destination SHALL preserve class student assignments.

#### Scenario: Move to an empty class
- **WHEN** an assigned teacher is released over an empty class
- **THEN** that teacher moves and the previous class students return to waiting

#### Scenario: Exchange teachers
- **WHEN** an assigned teacher is released over another assigned teacher
- **THEN** teachers exchange while student slots remain with their classes

### Requirement: Immediate teacher side effects remain sourced
The operation SHALL preserve held membership, clear the sourced work fields on release, apply original activity and sorting behavior, and keep immediate derived fields distinct from later reconciliation and rating.

#### Scenario: Release outside classes
- **WHEN** an assigned teacher is released outside teacher slots
- **THEN** that teacher and source students return to waiting, source work clears and sourced sorting applies

### Requirement: Teacher work list refresh
The isolated work projection SHALL select enabled and unblocked teacher records in source slot order, classify them using original template fields, emit category ordinal rows and calculate page limits. Clearing selection SHALL empty active lists and reset pages without inventing inactive rows.

#### Scenario: Pagination boundary
- **WHEN** one category has eleven enabled and unblocked records
- **THEN** it exposes eleven ordered rows with zero-based ordinals and a page limit of one

#### Scenario: Blocked work
- **WHEN** a work record is disabled or blocked
- **THEN** it contributes no active row

### Requirement: Validation and compatibility
The module SHALL reject unsupported teachers, invalid source selection, inconsistent rosters, malformed work records and altered source rules without modifying input. Existing campaign, student movement, sorting UI and frozen evidence SHALL remain unchanged.

#### Scenario: Teacher source changed
- **WHEN** the teacher ID no longer matches the declared source location
- **THEN** the operation refuses without a new snapshot

#### Scenario: Isolated scope
- **WHEN** teacher movement or work refresh succeeds
- **THEN** it does not grant current-campaign teacher provenance, course execution, live-school or save authority
