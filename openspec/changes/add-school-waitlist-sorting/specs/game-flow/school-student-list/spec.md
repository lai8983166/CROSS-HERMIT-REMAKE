# Spec Delta

## Purpose

提供来源明确的学校待命学生名单排序，使用户能在完成返回流程后调整浏览顺序，并确保学生成长、战果、日期以及班级信息不会因名单排序而改变。

## ADDED Requirements

### Requirement: Sourced student ordering
The system SHALL support descending level, ascending original job category, and descending sum of seven attributes for the waiting student list, preserving original exchange-sort tie behavior for numeric keys and input order within each category.

#### Scenario: Equal numeric keys displaced by a larger key
- **WHEN** levels for input students A, B, C are 10, 10, 20 and level ordering is requested
- **THEN** the list becomes C, B, A according to the original exchange operations

#### Scenario: Job categories are distinct from job IDs
- **WHEN** category ordering is requested
- **THEN** the original category table determines the order and students within one category retain input order

### Requirement: Guarded school publication
The system SHALL accept ordering only after sourced school boot completes and only for a validated waiting list and supported mode. It SHALL change only waiting order and its ordering mode in the shared catalog, without awarding rewards or advancing the calendar.

#### Scenario: Invalid or premature operation
- **WHEN** sorting is requested before school boot, with an unsupported mode, or with invalid waiting members
- **THEN** catalog, revision and journal remain unchanged

#### Scenario: Repeated current ordering
- **WHEN** a requested ordering produces the current order and mode
- **THEN** no additional catalog revision or journal entry is published

### Requirement: Window list follows shared state
The school page SHALL provide the three ordering choices, display the shared waiting list, preserve the selected student across ordering, and retain ordering when returning from result browsing. Restarting the demo SHALL start a fresh session.

#### Scenario: Change order and browse result
- **WHEN** the user selects a student, chooses category order and returns to the result page and back
- **THEN** the list retains category order and the same student remains selected without a second settlement

### Requirement: Bounded evidence disclosure
Evidence SHALL distinguish declared initial school data and stubbed menu input from executed original sorting instructions. Sorting SHALL NOT imply teacher assignment, scheduling, a live original-game witness or save-write authorization.

#### Scenario: Verify original commands
- **WHEN** sorting evidence is regenerated
- **THEN** the recorded native command consumers, job categories, input/output lists and write boundaries reproduce the frozen report
