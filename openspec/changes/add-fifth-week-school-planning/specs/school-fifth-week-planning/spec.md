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

### Requirement: Native effect textures and work initialization
The system SHALL continue actual current-school CPU through source-selected effect texture slot, original texture/header records, metadata retention/file release and effect work/initial animation setup. GPU MUST be declared. Source slot100 selection MUST bypass dynamic-slot search and its assertion dialog; unexpected assertions MUST fail. It MUST stop at the following mapcom request and preserve roles/current records without claiming current/enemy placement or battlefield rendering.

#### Scenario: Ready school initializes effect textures and work
- **WHEN** the actual ready unit-assets checkpoint reaches41EBF0
- **THEN** every original effect texture entry and work record is verified, the original file releases only after binding, and execution stops at the next mapcom resource request

#### Scenario: Unready school initializes no effects
- **WHEN** current school readiness fails
- **THEN** no effect texture slot, work or animation setup executes

### Requirement: Independent effect texture provenance
The system SHALL independently validate original effect image records and initial animation/program/work inputs, separate from frozen native outputs, with malformed data refusal and historical/save/runtime retention.

#### Scenario: Match original effect image and work data
- **WHEN** supported effect resources are decoded
- **THEN** all native offsets, headers, dimensions, work/program pointers and initial duration/descriptor fields match independent original bytes

### Requirement: Native map common and first current-unit input
The system SHALL resume actual school execution through mapcom loading, four top-level and33 nested pointer selections, original current-record preparation and the first source-selected176-byte record copy. It MUST stop before4680B0 work construction, allow current writes only to source state/recovery fields, retain persistent roles/MVP/date and effects, and label file/heap/CRT boundaries without claiming battle placement.

#### Scenario: Ready school reaches first unit constructor input
- **WHEN** the actual ready effect checkpoint resumes at4500B0
- **THEN** mapcom loads read-only into a finite retained buffer, all handles close, current preparation matches original policy, and the copied first record reaches4680B0 without executing its body

#### Scenario: Unready school reaches no map common input
- **WHEN** school readiness refuses departure
- **THEN** no mapcom request, allocation, preparation or current-record copy occurs

### Requirement: Independent map common and current preparation provenance
The system SHALL decode original mapcom offsets and executable preparation/selection constants independently from native evidence, reject malformed containers, verify all copied/prepared bytes and retain historical/runtime/save fingerprints.

#### Scenario: Compare native map common and selected record to original inputs
- **WHEN** supported original inputs are independently decoded
- **THEN** each retained pointer and first selected/copied record matches original bytes and policy, while full current/enemy work, VM and placement remain pending

### Requirement: Native first unit work and animation cache request
The system SHALL resume actual4680B0 through work clearing/record binding/sentinels/status initialization and source job/palette/cache lookup, finite controller allocation/construction/binding. It MUST stop at the natural unit animation file request before loading, preserve current global/persistent/map/effect bytes, restrict writes to the selected work/copied record/cache/counter/controller and declare primitives without claiming a completed constructor or unit appearance.

#### Scenario: Ready school reaches the first unit art request
- **WHEN** the actual ready map common checkpoint resumes4680B0
- **THEN** initialized work/status/cache/controller bytes and source-selected resource arguments are recorded, and execution stops at4500B0 called by464EB0 without returning constructor success

#### Scenario: Unready school initializes no current work
- **WHEN** departure readiness refuses
- **THEN** no current work, animation-cache allocation or unit art request occurs

### Requirement: Independent first unit work provenance
The system SHALL independently derive original work/status/controller bytes and job/palette/cache/resource inputs from EXE source bytes, separate from frozen native output, with unsupported/malformed input refusal and historical/runtime/save retention.

#### Scenario: Compare complete first work prefix to original source
- **WHEN** supported original source inputs are decoded
- **THEN** every initialized work/copied-record/controller byte and natural file argument matches original rules, while resource loading and the constructor tail remain unexecuted

### Requirement: Native first unit animation resource binding
The system SHALL resume the actual first unit-art request through read-only archive loading, native metadata copy and palette/mask selection, complete texture/header traversal, temporary source release and controller mode setting. It MUST retain finite ownership, reject assertions, declare GPU primitives and stop before selected unit animation-work binding while retaining previous work/record/cache/map/effect/persistent bytes.

#### Scenario: Ready school loads first unit animation
- **WHEN** the actual ready school CPU resumes4500B0 called by464EB0
- **THEN** source d1a.bin loads with exact bytes and closed handles, its retained metadata/texture records and selected palette/mask inputs are verified, and execution stops at467147 without completing4680B0 or placing a unit

#### Scenario: Unready school loads no unit animation
- **WHEN** current school readiness refuses departure
- **THEN** no unit animation file, metadata or texture records are allocated or loaded

### Requirement: Independent first unit animation provenance
The system SHALL independently decode original archive/EXE metadata, texture and palette/mask inputs separately from frozen native evidence, compare every initialized byte and upload input, reject malformed resources and preserve historical/runtime/save rules.

#### Scenario: Verify original unit animation binding
- **WHEN** supported original unit animation bytes are independently decoded
- **THEN** retained pointers/controller fields, complete texture records and pixel/palette/mask inputs match the original sources without claiming GPU rendering or finished unit construction

### Requirement: Native first unit constructor completion
The system SHALL resume467147 on the actual school CPU, execute initial animation action/program binding and the remaining4680B0 coordinate, cell-accounting, scratch and status initialization, stopping at its natural4533FA return. It MUST restrict writes to finite original ownership and preserve copied/global records, persistent data and retained resource bytes. Constructor coordinates MUST be distinguished from later scene placement.

#### Scenario: Ready school completes exactly its first constructor
- **WHEN** the actual ready school CPU resumes after first unit resource loading
- **THEN** the original constructor returns zero at4533FA with complete work/scratch/cell bytes recorded, before other unit constructors, scene VM or468910 placement execute

#### Scenario: Refusal creates no completed unit
- **WHEN** school departure readiness refuses
- **THEN** no first unit constructor completion, animation work binding or map cell mutation occurs

### Requirement: Independent first unit constructor provenance
The system SHALL derive initial action/direction/program and constructor defaults independently from original EXE/archive inputs, compare complete resulting work/record/scratch/cell bytes separately from frozen native cases, reject unsupported inputs and preserve historical/runtime/save evidence.

#### Scenario: Verify complete first constructor bytes
- **WHEN** supported original pre-constructor inputs are decoded
- **THEN** independent rules match the actual three-ready/two-refusal native outcomes without claiming final spawn positions, live GPU output or a completed battle world

### Requirement: Native complete current-unit construction
The system SHALL continue actual4533FA through both original current-record loops, loading-progress updates and remaining4680B0 constructors with exact read-only supported job archives and finite cache/controller/texture ownership. It MUST stop before453540 enemies, retain previous units/resources and current/persistent records, reject assertions and declare graphics/scheduler primitives explicitly.

#### Scenario: Ready school completes every selected current unit
- **WHEN** the actual school CPU resumes the first constructor return
- **THEN** original selection/order, copies, archive/cache handling and complete work initialization run for every current record before453540, with no enemy construction, scene placement or VM execution

#### Scenario: Refusal creates no current-unit batch
- **WHEN** school departure readiness refuses
- **THEN** no current-unit loop continuation, additional resources or work constructors execute

### Requirement: Independent current-unit constructor provenance
The system SHALL derive selection/order/progress/cache/job/palette/archive and constructor results independently from original source for supported jobs6/7/10, compare complete bytes separately from immutable native cases and preserve historical/runtime/save evidence. Declared cache reuse tests MUST be identified separately from actual school witnesses.

#### Scenario: Verify complete current units and cache ownership
- **WHEN** supported original current-record inputs are decoded
- **THEN** selected indices and every initialized work/record/controller/metadata/texture/palette/cell byte match the source, unsupported inputs are rejected and no final scene placement or live GPU output is claimed

### Requirement: Native scene-unit record preparation
The system SHALL continue actual453540 through scene5 template selection and original4DA450 first record derivation, stopping before enemy-loop4680B0. It MUST declare separate all35 template driver calls, bound writes to the selected record and exact transient profile scratch, retain all other current/persistent/resource bytes and distinguish templates from deployed enemies.

#### Scenario: Actual school prepares first scene-unit record
- **WHEN** the actual current-unit constructors have completed
- **THEN** original scene/count/index selection and profile/numeric/overlay conversion prepare the first176-byte record at index249 without starting its unit-work constructor

#### Scenario: Refused school has no scene-unit record
- **WHEN** departure readiness refuses
- **THEN** no453540 continuation or scene-unit record derivation runs

### Requirement: Independent scene-unit record provenance
The system SHALL decode original template/profile/job/archetype/formula/normalization/overlay inputs independently, compare complete176-byte records for all35 declared scene5 templates and the actual first record, reject unsupported inputs and preserve historical/runtime/save bytes.

#### Scenario: Verify scene templates without claiming deployment
- **WHEN** original scene5 templates are transformed under their declared character inputs
- **THEN** every record byte matches independent source derivation and active/deferred/NPC fields remain distinct from unexecuted unit construction, placement and VM/event scheduling

### Requirement: Native scene-unit work prefix preparation
The system SHALL resume the actual first scene-unit4680B0 through original category/status/template, job/palette/cache and controller initialization, stopping before natural animation loading. It MUST bound selected work/record/cache/counter/controller ownership, retain other mapped bytes and distinguish separately declared all35 isolated prefix calls from actual scene-loop completion, constructor tails, placement and VM.

#### Scenario: Ready school requests first NPC animation
- **WHEN** actual scene5 first record preparation has completed
- **THEN** original NPC status and scene template branches execute, a finite controller is initialized and the source-selected file request is recorded without loading the archive or completing4680B0

#### Scenario: Refused school prepares no scene work
- **WHEN** departure readiness refuses
- **THEN** no scene-unit work prefix, cache/controller allocation or animation request executes

### Requirement: Independent scene-unit work provenance
The system SHALL independently decode original work/controller stores, category/status/template overlays and job/palette/cache selection for all35 scene5 templates, compare full initialized bytes and resource arguments separately from frozen native output, reject unsupported inputs and preserve historical/runtime/save evidence.

#### Scenario: Verify source-selected scene work and resources
- **WHEN** original scene5 records are constructed under explicitly declared isolated inputs
- **THEN** all initialized bytes and mode0/1/2 animation arguments match source-derived rules, exact archives are inventoried read-only and no deployed scene or loaded native animation is claimed
