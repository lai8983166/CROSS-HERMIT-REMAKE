# Spec Delta

## Purpose

为学校编班提供来源明确的教师登记和班级派生数据，区分全局名单、班级原始槽位、可用成员及评级，并以隔离回放核对这些字段，作为后续编班操作的前置条件。

## ADDED Requirements

### Requirement: Sourced teacher registration
The isolated data module SHALL replay the sourced teacher117 registration and its direct helper placement variant, updating teacher roster and availability once. Already available teachers SHALL NOT be registered or placed again.

#### Scenario: Chapter012 registration repeated
- **WHEN** the sourced teacher117 command is delivered twice
- **THEN** the teacher appears once and the second delivery leaves the data unchanged

### Requirement: Teacher-aware group reconciliation
The isolated data module SHALL rebuild waiting lists and clear unavailable teachers/students, teacherless student slots and duplicate student assignments in original group/slot order. It SHALL preserve unrelated bytes and catalog fields.

#### Scenario: Class loses its teacher
- **WHEN** a group contains an unavailable teacher and available students
- **THEN** teacher and student slots clear and the students remain in the waiting list

#### Scenario: Student appears in two classes
- **WHEN** two valid teacher-led groups reference one student
- **THEN** the first assignment survives and the later assignment clears

### Requirement: Defined group ratings
The isolated data module SHALL rebuild teacher/student roster indices and report the original group state, directed relationship mean and threshold rank. It SHALL expose work fields only in branches that initialize them.

#### Scenario: Asymmetric relationships
- **WHEN** a teacher and students have different directed relationship values
- **THEN** the mean includes every ordered distinct pair and truncates toward zero before ranking

#### Scenario: Missing or empty teacher-led class
- **WHEN** a class has no teacher or no students
- **THEN** the state is respectively0 or1 and uninitialized work fields are excluded

### Requirement: Evidence and refusal boundaries
The module SHALL reject unsupported identities, contradictory global rosters, duplicate assigned teachers, missing relationships and invalid work fields without changing inputs. Evidence SHALL distinguish sourced opcodes, direct helper calls, declared initial groups and stubbed presentation from live school interaction.

#### Scenario: Current return demo remains unchanged
- **WHEN** isolated teacher/group replay is tested
- **THEN** the current teacherless campaign demo and its frozen outputs remain unchanged, without full-school or save authority
