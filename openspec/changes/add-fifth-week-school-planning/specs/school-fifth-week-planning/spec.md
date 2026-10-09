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

### Requirement: Source verified current student combat derivation
The system SHALL execute the original first-round work reset and complete current-student combat record derivation on the actual fifth-school CPU checkpoint, retaining roles, calendar, growth and MVP. It MUST distinguish prepared combat records from a constructed battlefield and retain pending16 as an explicit boundary.

#### Scenario: Prepare actual current students
- **WHEN** the source first-round preparation receives a ready current squad
- **THEN** it resets the exact source work range and derives records from ordered current student job, attributes, level and loadout before requesting16, without substituting demo units

#### Scenario: Invalid class cannot derive units
- **WHEN** source readiness refuses the squad
- **THEN** work reset, combat derivation and request16 do not occur and all persistent records remain unchanged

### Requirement: Pure current role combat limits
The system SHALL assemble owned current-student inputs and calculate source-equivalent HP, MP, recovery fields and engagement limits for the verified no-item subset using independent source tables. It MUST refuse unsupported inputs and expose its partial-record projection boundary without changing saved plans, rewards or mandatory gate.

#### Scenario: Current growth and equipped skills affect combat limits
- **WHEN** a supported current-school squad is queried
- **THEN** current carried-forward attributes, job, level and equipped skill effects produce native-equivalent limits in current member order with copied output and unchanged v4 save state

#### Scenario: Unsupported loadout or source data
- **WHEN** a role has an unverified item, malformed fields or incompatible source tables
- **THEN** projection refuses atomically without claiming a complete combat record or constructed battle

### Requirement: Source verified tactical startup boundary
The system SHALL consume actual pending16 and execute native outer tactical construction and script-work initialization with explicitly declared subcomponent boundaries. It SHALL verify current-unit startup normalization and first resource request, and keep separately invoked scene-resource selection probes distinct from natural startup. It MUST retain persistent records and MUST NOT claim loaded resources, enemies or a constructed battlefield.

#### Scenario: Ready squad starts tactical task
- **WHEN** source first-round preparation requests16
- **THEN** native dispatch constructs the outer task, initializes its source script work and normalizes current student records before stopping at the common-resource loader boundary

#### Scenario: Unready school never creates a tactical task
- **WHEN** readiness refuses departure
- **THEN** no tactical allocation, dispatch or resource request occurs

### Requirement: Graphical current student combat limits
The system SHALL show source-verified current student HP and MP in graphical departure cards. It MUST recompute from current owned roles, report unavailable values when unsupported, preserve saves and keep actual battle visibly unavailable.

#### Scenario: Edit and restore current squad
- **WHEN** the player changes classes, waits a student or restores a fifth-week save
- **THEN** departure cards show the correct current members and derived HP/MP without mutating growth, save commands or mandatory gate

#### Scenario: Unsupported combat derivation
- **WHEN** current combat inputs or source limits are unsupported
- **THEN** the preparation page reports unavailable combat values, retains usable return/save navigation and does not substitute demo limits

### Requirement: Source verified tactical resource loading
The system SHALL continue actual pending16 startup through native path composition, file-buffer loading and texture-container traversal before loading the source-selected current-scene script. File, heap, CRT, empty graphics table, GPU and audio boundaries MUST be declared. It MUST preserve persistent roles, date and MVP, and MUST NOT claim an initialized battlefield.

#### Scenario: Current squad loads natural startup resources
- **WHEN** the current school is ready and native startup proceeds
- **THEN** common, current TactStart, dialogue texture and the source-selected scene script are loaded from original bytes in natural order, all texture entries are accounted for, handles close and execution stops before the first tactical phase update

#### Scenario: Unready squad loads nothing
- **WHEN** school readiness fails
- **THEN** no tactical resource buffer, texture entry or scene script is loaded

### Requirement: Independent tactical resource provenance
The system SHALL export byte-derived container inputs and script selection independently of native output fixtures and verify source hashes, exact entry offsets/types/dimensions and finite memory bounds. Existing saves and historical evidence MUST remain unchanged.

#### Scenario: Compare native entries with original bytes
- **WHEN** supported original resource files are audited
- **THEN** each native texture record matches the independently decoded source entry and the selected script identity matches the original scene table

#### Scenario: Malformed resource refusal
- **WHEN** container sizes, offsets, entry types or source identities are inconsistent
- **THEN** validation refuses the resource without accepting fabricated battlefield data

### Requirement: Native logical UnitCtrl and scene map initialization
The system SHALL execute native logical UnitCtrl, linked-list and vector initialization and the original generic appearance-grid construction on actual ready current-school CPU branches. It SHALL continue natural tactical phases to source-selected logical map loading and stop at the next scene graphics resource request. It MUST retain finite memory bounds and explicit graphics/font/audio/random primitives without claiming enemy/event/VM placement or playable battle.

#### Scenario: Ready current squad initializes logical scene map
- **WHEN** native pending16 startup proceeds from a ready current school
- **THEN** original logical constructors and appearance-grid code execute, phase0 transitions naturally to phase2, and source-selected logical map and cleared map scratch buffers have verified ownership while roles/date/MVP remain unchanged

#### Scenario: Refused school initializes no scene map
- **WHEN** school readiness fails
- **THEN** UnitCtrl, appearance grid and logical map allocation do not execute

### Requirement: Independent current map and original texture provenance
The system SHALL export current scene map selection and logical map bytes independently from native output fixtures. It SHALL decode the original map texture container selected by the source table and validate entry offsets, dimensions and pixels with strict malformed-input refusal. Existing saves and historical reports MUST remain unchanged.

#### Scenario: Verify current scene map resources
- **WHEN** the selected original scene map files are decoded
- **THEN** metadata matches native logical map ownership and original texture pixels form an inspected source preview, without substituting demo units or a fabricated battlefield

#### Scenario: Reject inconsistent map data
- **WHEN** map header, container offsets, texture dimensions or source identities differ
- **THEN** export refuses the input without accepting scene placement or modifying saves

### Requirement: Native current scene resource initialization
The system SHALL continue actual current-school CPU branches naturally through current MAP/BMP/VPT read-only loading, original texture/minimap headers, fog calculation and pathfinding section rebasing. It MUST declare GPU/renderer primitives and bounded allocations, retain current/persistent records and stop before following unit-art initialization.

#### Scenario: Ready squad loads scene resources
- **WHEN** natural tactical phase2 reaches the verified scene graphics request
- **THEN** all three scene resource buffers, texture records and pathfinding relocations match original bytes, handles close, and execution stops at the following unit-art reset entry

#### Scenario: Refused school loads no scene resources
- **WHEN** readiness refuses departure
- **THEN** no scene texture, minimap, fog or pathfinding data is loaded

### Requirement: Graphical current scene map preview
The system SHALL provide a pan/zoom preview of the independently verified current scene map from a supported ready departure plan. It MUST retain school state, saves and mandatory gate, provide usable return, and MUST NOT invent unit/enemy placement or enable battle.

#### Scenario: Inspect and return from current map
- **WHEN** a ready player opens the current-map preview, pans or zooms and returns
- **THEN** original MAP05 pixels render within the viewport and the same squad, state and saved commands remain

#### Scenario: Unready or unsupported departure
- **WHEN** current departure readiness or scene identity is unsupported
- **THEN** the current-map action refuses without changing school/save state or substituting the standalone demo

### Requirement: Native unit reset and effect metadata preparation
The system SHALL continue the actual current-school CPU from the scene-resource pause through original unit work reset, relation setup, text-cache requests and effect animation file/metadata preparation. Text rasterization and unresolved graphics objects MUST be declared boundaries. It MUST preserve current/persistent records, use bounded allocations and stop before effect texture binding rather than fabricating a loaded animation or battlefield.

#### Scenario: Ready school prepares unit reset and effect metadata
- **WHEN** the actual ready scene-resource continuation reaches467EB0
- **THEN** original work reset and text request loops execute, the original effect controller and exact Efct.bin file/metadata pointers are prepared, handles close and execution stops before41EBF0 texture binding

#### Scenario: Unready school prepares no unit assets
- **WHEN** school readiness refuses departure
- **THEN** no unit reset, text requests, effect allocation or file load occurs

### Requirement: Independent unit text and effect provenance
The system SHALL independently decode original text pointer tables and effect container offsets/metadata, separate from frozen native outputs. It MUST validate source identity, each request and copied section pointers, retain historical evidence and save fingerprints, and reject malformed input without claiming effect rendering or squad placement.

#### Scenario: Compare native preparation to source bytes
- **WHEN** supported original text and effect inputs are decoded
- **THEN** every requested string/destination and effect metadata byte/pointer matches the original source, while current graphical map behavior remains unchanged
