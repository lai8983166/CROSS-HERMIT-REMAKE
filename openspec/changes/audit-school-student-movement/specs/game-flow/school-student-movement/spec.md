# Spec Delta

## Purpose

提供来源明确的隔离学生移动操作，保留原版释放、教师门槛、交换、自动排序与后续整理之间的区别，作为未来学校编班交互的数据基础，不混同实机学校或存档写入。

## ADDED Requirements

### Requirement: Waiting students enter or replace a class slot
The isolated operation SHALL place a waiting student into a teacher-led target slot on release, returning an occupant to waiting when necessary and applying the sourced waiting sort.

#### Scenario: Replace an occupied slot
- **WHEN** a waiting student is released over a teacher-led occupied student slot
- **THEN** that student takes the slot and the occupant joins the sorted waiting list

### Requirement: Class students move exchange or return to waiting
The operation SHALL move class students to empty slots, exchange occupied slots, or return them to waiting on release outside eligible teacher-led slots, including teacherless target classes.

#### Scenario: Teacherless target
- **WHEN** a class student is released over a teacherless class
- **THEN** the source slot clears and the student returns to sorted waiting

#### Scenario: Cross-class exchange
- **WHEN** a class student is released over another teacher-led occupied slot
- **THEN** the two students exchange their slots

### Requirement: Held drag and cleanup checkpoints remain distinct
The operation SHALL preserve assignments while held, reproduce immediate defined drag changes on release, and expose separately sourced reconciliation and rating checkpoints. Undefined rating work words SHALL remain excluded.

#### Scenario: Button remains held
- **WHEN** the selected student is over an eligible class slot but release has not occurred
- **THEN** selection feedback may change but memberships and drag identity remain unchanged

#### Scenario: Immediate count versus cleanup
- **WHEN** a class student moves and the original immediate count is stale
- **THEN** the immediate checkpoint retains that value and the later reconciliation recomputes it

### Requirement: Refusal and compatibility boundaries
The operation SHALL reject malformed or contradictory source selections, unsupported identities, invalid sorting inputs and missing required relations without modifying input. Existing campaign return, sorting UI and frozen outputs SHALL remain unchanged.

#### Scenario: Stale source slot
- **WHEN** the selected identity no longer matches its declared source slot
- **THEN** the operation returns refusal without a new snapshot

#### Scenario: Isolated evidence
- **WHEN** a supported student movement is replayed
- **THEN** it grants no live-school, campaign-teacher or save-write authority
