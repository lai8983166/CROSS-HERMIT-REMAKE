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

### Requirement: Native first scene-unit animation and constructor completion
The system SHALL resume actual first scene-unit4500B0 through exact read-only animation loading, native metadata/palette/mask/texture/controller binding and file release, then finish4680B0 initial animation work, coordinates, cell accounting and defaults at natural453630. It MUST use finite ownership, reject assertions, declare GPU/vector primitives precisely, retain other mapped bytes and stop before remaining scene templates, deployment or VM.

#### Scenario: Ready school completes first scene NPC
- **WHEN** actual school execution reaches the first scene-unit archive request
- **THEN** a1a archive binding and original constructor tail complete, all file handles close and the native zero return at453630 is recorded without executing the next template or scene placement

#### Scenario: Refused school loads no scene-unit archive
- **WHEN** departure readiness refuses
- **THEN** no scene-unit animation allocation/load, constructor completion or cell mutation occurs

### Requirement: Independent first scene-unit constructor provenance
The system SHALL independently derive original archive/EXE metadata, texture/palette/mask, initial visible descriptor/program and constructor defaults, compare full work/record/scratch/cell/controller/resource bytes separately from frozen native output, reject unsupported inputs and preserve historical/runtime/save evidence. Declared palette-boundary loader calls MUST remain distinct from actual school execution.

#### Scenario: Verify actual NPC bytes and declared palette boundaries
- **WHEN** supported first NPC inputs and declared palette1/40 requests are independently decoded
- **THEN** every native binding input and complete actual constructor byte matches original source, with no live GPU, full35-template loop or final spawn claim

### Requirement: Native second scene-unit input preparation
The system SHALL resume actual453630 through original loading progress, ordinal1 template record derivation and4680B0 work/cache/controller prefix, stopping at its mode0 archive request before loading. It MUST use distinct finite controller ownership, preserve first NPC/current/persistent/resource bytes, and distinguish this boundary from complete scene constructors or deployment.

#### Scenario: Ready school requests second scene animation
- **WHEN** the first NPC has naturally returned
- **THEN** original progress and second record/work preparation select51e.bin with variant0/mode0 and stop before loading, while refusal cases do not enter

### Requirement: Independent scene cache lookup provenance
The system SHALL independently derive second record/prefix/progress and original466DA0 lookup semantics, compare complete bytes separately from frozen native output, and execute all35 source-selected keys under declared cache insertion inputs. It MUST verify signed fields, nonzero occupancy, first-match order, holes and full-table miss without claiming allocation, cache binding or full scene-loop completion.

#### Scenario: Verify ordered cache keys and boundary queries
- **WHEN** declared ordered keys and signed/duplicate/empty/full cache probes execute original lookup
- **THEN** pure source lookup matches native return pointers and unchanged cache bytes; missing-key insertions remain explicitly declared driver operations

### Requirement: Native second scene-unit constructor completion
The system SHALL resume the actual second scene-unit mode0 archive request through original read-only51e loading, metadata/texture/controller binding, file release and complete special-role387 constructor. It MUST enforce finite owned writes and retained prior/current/persistent/resource bytes, declare external primitives precisely and stop at natural453630 before ordinal2, deployment or VM.

#### Scenario: Ready school completes second scene unit
- **WHEN** actual school execution reaches51e variant0/mode0 loading
- **THEN** native binding and complete constructor return naturally with closed handles and verified special-role record/work/cell changes; refusal branches execute neither

### Requirement: Independent second scene-unit constructor provenance
The system SHALL independently derive51e archive/EXE mode0 palette, texture and initial-program/special-role constructor inputs, compare complete resource/controller/work/record/scratch/cell bytes separately from frozen native output, reject malformed or unsupported inputs and preserve historical/runtime/save evidence.

#### Scenario: Verify mode0 resource and special-role tail bytes
- **WHEN** original second scene-unit inputs are decoded
- **THEN** independent byte rules match all native binding and constructor outputs without claiming live GPU, complete scene loop, final deployment or VM execution

### Requirement: Native eight-unit scene batch and cache reuse
The system SHALL resume actual school execution through complete scene5 ordinals2–9 with original record/progress/cache/resource/constructor bodies. It MUST load only missing52e mode0 and50e variant1 archives, execute native cache hits without new allocation/loading/cache mutation, retain finite ownership and other mapped bytes, declare external primitives and stop at natural453630 after ordinal9 before deployment or VM.

#### Scenario: Ready school constructs eight more scene units
- **WHEN** the second scene unit has returned on the actual ready school CPU
- **THEN** ordinal2 and seven job383 units complete, six actual cache hits reuse the same owned controller/resources, and refusal cases execute none of this batch

### Requirement: Independent scene batch provenance
The system SHALL independently derive original job393/383 binding, action/program, special/hostile constructor and ordered cache/progress policy, compare complete bytes separately from frozen native output, reject malformed or unsupported inputs and preserve historical/runtime/save evidence.

#### Scenario: Verify every constructor and cache transition
- **WHEN** supported original scene batch inputs are decoded
- **THEN** every record/work/cache/controller/metadata/texture/palette/progress/scratch/cell byte matches independent source rules, without claiming the remaining25 constructors, deployment, VM or live GPU rendering
### Requirement: Remaining scene templates execute complete native constructors

The audit SHALL execute original scene5 ordinals10–34 after the verified first10 constructors, preserve inactive status11 behavior and original cache reuse, and stop at45363D after final progress before deployment. Source rules SHALL be decoded independently from original inputs and compared with separate immutable native fixtures, retaining prior runtime/save/history bytes.

#### Scenario: Inactive templates retain original animation defaults

- **WHEN** an original record has state0
- **THEN** its complete native constructor and resource binding execute with status11 and original action-dispatch behavior, without inventing an idle animation

#### Scenario: Full scene constructor loop reaches its final boundary

- **WHEN** a valid school branch completes all35 scene constructors
- **THEN** the audit captures exact final progress and retained bytes at45363D, with deployment and scene VM explicitly unexecuted

### Requirement: Native current-school formation placement

The audit SHALL resume the actual35-constructor CPU through its natural epilogue/caller and original468910 school branch, execute complete49A480 formation/terrain/occupancy placement and stop at468A49 before search-workspace allocation. It SHALL retain all other mapped bytes and distinguish this boundary from full deployment, VM or live graphical battle.

#### Scenario: Ready school obtains original formation coordinates

- **WHEN** all35 scene constructors have completed on the actual school CPU
- **THEN** source-selected active current students receive original record/work/grid coordinates and exact occupancy updates; refusal cases execute no placement

### Requirement: Independent formation placement provenance

The audit SHALL independently decode original formation grid, rotation, selection and terrain/occupancy inputs, compare full native output bytes separately from frozen evidence, reject malformed inputs and preserve historical/runtime/save evidence.

#### Scenario: Verify selection and placement bytes

- **WHEN** supported source placement inputs are decoded
- **THEN** every record/work/reservation/cell byte matches pure source rules, including retained unselected and deferred units, without claiming later search initialization or VM execution

### Requirement: Native deployment tail completion

The audit SHALL continue468A49 through original search workspace, unit/display indexes, scratch clearing and category linked lists to natural4534A1. It SHALL enforce finite writes and retain other mapped bytes. Actual checkpoint recovery SHALL require pinned identity and complete prior placement equality, publish provenance and distinguish inherited refusal fixtures from newly executed suffix cases.

#### Scenario: Ready checkpoint completes original deployment

- **WHEN** a trusted actual school checkpoint reproduces its immutable placement output
- **THEN** the original deployment tail returns zero naturally, with no next467AA0, scene VM or live GPU claim

### Requirement: Independent deployment byte provenance

The audit SHALL independently derive original allocation order, search/free-list pointers, category/state selection, work/display stores, scratch and descending category insertion; compare complete bytes separately from frozen native evidence, reject unsupported inputs and preserve historical/runtime/save evidence.

#### Scenario: Verify full deployment tail bytes

- **WHEN** supported current-scene inputs are decoded from original source
- **THEN** all buffers, wrappers, work, category nodes and scratch match source-derived bytes while existing runtime/UI and ten save fingerprints remain unchanged

### Requirement: Complete scene initialization and original opening request

The audit SHALL continue actual4534A1 through complete natural452FC0/4519C0 return after pinned placement/deployment equality. It SHALL explicitly distinguish bounded original453F10 driver updates from natural initializer execution, verify exact presentation/scheduler primitives and stop at phase5/script-work request without claiming event VM, work completion or live rendering.

#### Scenario: Actual initialized school reaches opening work request

- **WHEN** a trusted actual school CPU reproduces the previous placement and deployment
- **THEN** native timers/owner binding and initializer returns complete, original opening updates reach phase5 with request170=1, and all other mapped bytes remain unchanged

### Requirement: Independent complete opening byte provenance

The audit SHALL independently decode original signed timer decomposition, initializer stores, opening jump table, native increment and ordered rectangle/alpha inputs, compare complete output bytes and every canonical presentation hash, reject malformed/unsupported inputs and preserve historical/runtime/save evidence.

#### Scenario: Verify opening bytes and declared timer boundaries

- **WHEN** supported actual opening inputs and separately declared signed32 timer calls are decoded
- **THEN** source rules match every memory/presentation result without substituting native outputs as expectations or claiming script/world callbacks ran

### Requirement: Native opening request consumption and preflight entry

The audit SHALL reproduce pinned placement/deployment/opening on actual school checkpoints before declared499DA0 controller updates. It SHALL execute camera setup, request consumption and native180 delay, interleave original phase5 waiting and stop at the natural4551C0 selector0/sub1 entry before executing preflight or VM code. Finite writes and all other mapped memory SHALL be verified; the170 request SHALL be distinguished from direct VM execution.

#### Scenario: Actual entry controller reaches script preflight

- **WHEN** supported actual noninteractive opening state has request170=1 and completion171=0
- **THEN** 183 complete controller updates reach state6 with request consumed, 183 original phase5 calls continue waiting, and the next controller update stops at natural4551C0 before its first instruction

### Requirement: Independent entry control byte provenance

The audit SHALL independently decode original entry dispatch, camera clamping, native delay and selected preflight arguments, compare complete task/control/camera bytes and every update separately from frozen native evidence, reject unsupported inputs and preserve historical/runtime/save evidence.

#### Scenario: Verify complete entry control stores

- **WHEN** actual controller inputs are decoded from source
- **THEN** complete memory and natural pending-call arguments match independent rules while VM, runtime, UI and ten save fingerprints remain unchanged

### Requirement: Natural original script preflight and actual binding

The audit SHALL reproduce pinned parent stages before resuming natural4551C0. It SHALL execute original preflight VM, capture its return and continue actual selected script binding through controller return, with finite writes and exact declared external primitives. VM SHALL NOT be synthetically reset before execution. Playback/world/battle execution SHALL remain explicitly distinguished.

#### Scenario: Actual preflight selects original school script

- **WHEN** a trusted school CPU reproduces the pending preflight call
- **THEN** original register/condition/request/jump/END instructions select the actual0/1 segment, original binding activates it and controller returns naturally before playback

### Requirement: Independent preflight and VM binding bytes

The audit SHALL independently decode source nested headers, preflight opcodes and all reset/binding/register stores, compare complete captured bytes and opcode trace separately from frozen native evidence, reject malformed/unsupported inputs and preserve runtime/save/history.

#### Scenario: Verify preflight results and owned sparse resets

- **WHEN** supported actual source inputs are decoded
- **THEN** every VM/work/task/control/global/sparse-resource word matches source rules while all other mapped memory and ten save fingerprints remain unchanged

### Requirement: Actual normal script startup and native fade wait

The audit SHALL replay pinned actual parents before continuing selected0/1 normal playback under declared original VM and fade calls. It SHALL execute source startup setters, work wait and original sixty-count fade release, presentation-mode initialization and thirty-count delay; stop on the natural first board-on handler stack before its first instruction. Only exact declared presentation interfaces SHALL be skipped; no world callback or readiness result SHALL be fabricated.

#### Scenario: Normal branch reaches the first board request

- **WHEN** actual bank0/PC0 is selected and activated by the prior native binding
- **THEN** original normal playback completes107 VM/fade updates, with60 native fade counts and31 delay wait checks, then reaches4C5EA0 on its natural stack before board rendering

### Requirement: Independent normal startup memory and presentation provenance

The audit SHALL independently decode original script instructions, global/group setters, fade conversion/release and wait boundaries. It SHALL compare complete owned bytes, all updates/commands and exact presentation digests separately from frozen native evidence, reject malformed/unsupported inputs and preserve runtime/save/history.

#### Scenario: Source rules equal actual normal startup

- **WHEN** supported actual source inputs are modeled
- **THEN** complete task/control/work/VM/global/counter bytes, every update and pending board arguments match native execution while the full task wrapper, audio gating, dialogue/waves/world scheduling and graphics remain explicitly pending

### Requirement: Actual first board animation and readiness

The audit SHALL replay six pinned actual parents, resume the natural pending board handler and complete bounded native VM/layer/readiness updates. It SHALL execute active logical presentation updates and declare only exact terminal drawing interfaces. It SHALL stop at the following text-active handler before its first instruction, verify finite writes and retain all other memory without manufacturing readiness.

#### Scenario: First board becomes naturally ready

- **WHEN** the original selected script requests board4 on the preserved VM stack
- **THEN** source configuration maps it to layer7,47 completed updates animate and release the original wait, and the next VM call stops naturally at4C4DC0 for offset676 before text activation

### Requirement: Independent complete board provenance

The audit SHALL decode source board configuration, frame pieces, animation counters, alpha interpolation, readiness predicate and raw drawing arguments independently. It SHALL compare complete captured bytes, every update and every presentation digest, reject malformed or unsupported inputs, preserve runtime/save/history and distinguish terminal draw stubs from live rendering.

#### Scenario: Independent board rules equal native execution

- **WHEN** supported actual board inputs are modeled from original code and tables
- **THEN** all memory, update and drawing records match native evidence while text/font/GPU/full-task/audio/world/waves remain explicit subsequent dependencies

### Requirement: Natural first text preparation to font boundary

The audit SHALL replay seven pinned actual parents, resume the selected text-active call, complete its original VM return and execute first text lookup/split/record preparation to a natural CreateFontA API entry before its first instruction. It SHALL verify exact stack/font/text inputs, finite owned writes and retained bytes without substituting font/texture/width/readiness outputs.

#### Scenario: Actual first text reaches the font interface

- **WHEN** board4 is ready on the original selected script
- **THEN** original activation selects layer7, first opcode17 resolves text0 and prepares the first line/record, and the original indirect font call reaches its API entry with14 source-derived arguments

### Requirement: Independent original opening text catalog

The source model SHALL independently decode complete text preparation bytes, first line and font inputs, compare every native result, reject malformed/unsupported inputs and export the original ten Big5 opening texts with a bounded opcode17 sequence separately from native evidence.

#### Scenario: Complete text preparation and original ten entries

- **WHEN** supported original source headers, offsets and text are decoded
- **THEN** complete owned bytes, first text/split/font inputs match native execution and the compact runtime catalog contains the ten original source entries in verified instruction order

### Requirement: Read-only graphical opening dialogue preview

The existing current MAP05 preview SHALL offer a readable overlay for the ten source opening texts with previous/next/close controls and page position. Navigation SHALL NOT mutate model state, append commands, change save bytes or clear the adventure gate. It SHALL be labeled as a preview and SHALL NOT claim native font/layout/world or battle execution.

#### Scenario: Read and close opening dialogue over the current map

- **WHEN** a supported ready MAP05 projection is open
- **THEN** the opening preview displays all ten original texts in order, paging and Escape close safely, reopening starts at the first text, map controls remain usable and state/save/gate remain unchanged

### Requirement: Real host font and natural first text raster

The audit SHALL replay eight pinned actual parents and resume the natural CreateFontA call through real host GDI APIs. It SHALL execute original raster geometry and stop naturally at texture creation before GPU instructions, recording exact caller/arguments, host code page/font selection, finite writes, complete memory and cleanup. It SHALL NOT fabricate a font handle, metrics, texture success or dialogue readiness.

#### Scenario: First text produces a real offscreen raster

- **WHEN** the preserved original first-line font request is resumed
- **THEN** real GDI creation/measurement/drawing produce captured DIB bytes and original geometry reaches the pending texture call while GPU and full playback remain unexecuted

### Requirement: Independent raster conversion and isolated text timing

The audit SHALL independently decode source raster/texture geometry and pixel conversion and compare original CPU conversion on a declared memory surface. It SHALL separately probe original text fade/cadence/readiness with declared isolated records, compare every state/output, reject malformed inputs and preserve runtime/save/history.

#### Scenario: Conversion and counter branches are fully checked

- **WHEN** real captured raster bytes and bounded isolated timing cases are supplied
- **THEN** converted pixels/padding and every original counter/readiness state match independent source rules without claiming GPU upload or natural VM completion

### Requirement: Real32-bit Direct3D8 feasibility remains separate from natural VM continuation
The system SHALL independently verify original texture allocation and device dependencies and probe actual32-bit Direct3D8 resources without replacing native device0 or manufacturing texture success.

#### Scenario: Original dimensions and null-device boundary
- **WHEN** source-pinned bounded isolated texture cases execute original403B70/403BD0
- **THEN** power-of-two dimensions and full prepared CreateTexture arguments match independent rules
- **AND** device0 stops before null-vtable dereference without any COM call or GPU success

#### Scenario: Real host texture roundtrip
- **WHEN** a bounded32-bit helper creates a hidden windowed device and a managed format25 texture
- **THEN** source-derived dimensions, levels, usage and pool, actual HRESULTs/pointers/row pitch and complete uploaded/read-back pixels are recorded
- **AND** all resources are released and malformed requests rejected before platform calls
- **AND** probe success does not imply native renderer initialization, VM return, dialogue, waves or persistent state changes

### Requirement: Natural first text completes with a live real platform binding
The system SHALL bridge live owned32-bit Direct3D8 resources to the original first text call and keep source execution distinct from declared external-memory and API adapters.

#### Scenario: Original first text returns after real texture upload
- **WHEN** eight pinned parents replay and a real host device is explicitly bound before font continuation
- **THEN** original texture creation/descriptor/lock/conversion/unlock and text/VM caller return execute with actual platform results
- **AND** full regions, actual texture bytes/padding and retained memory match independent source rules
- **AND** owned GDI/COM/process resources close on success and failure
- **AND** original renderer startup, GPU drawing, text readiness, world scheduling and waves are not inferred

#### Scenario: Foreign or stale live resources are rejected
- **WHEN** a bridge request names an unsupported method, malformed buffer or dead/foreign pointer
- **THEN** no fabricated resource/result is returned and the request is refused with cleanup available

### Requirement: Natural consecutive second text prefix retains live first resources
The audit SHALL continue the actual first-text VM return while the real first texture is alive, observe original first-record readiness on actual bytes without altering the restored CPU/stack/state, and resume the next original opcode17 to the natural second font API entry. It SHALL compare complete memory and source-derived stack arguments, preserve old evidence/runtime/UI/saves, and close resources on success/failure. It SHALL NOT delay the selected VM for an invented first-line wait or claim that second font/texture creation, natural complete fade, GPU drawing or world/waves have executed.

#### Scenario: Consecutive text is prepared before first fade completes
- **WHEN** the first text naturally returns at PC238 with mode3/fade0
- **THEN** original first-record readiness is false and the next original VM update selects text index1 and prepares the next record on its natural font stack
- **AND** first texture pixels and all non-owned mapped memory are retained while the second font API remains unexecuted

#### Scenario: Missing live ownership or foreign writes refuse continuation
- **WHEN** a continuation has stale resource ownership, unsupported source state or writes beyond the finite second-row/header/stack/counter ranges
- **THEN** it fails without a fabricated font/texture/readiness result and cleanup remains mandatory

### Requirement: Natural second text completes with independent live textures
The audit SHALL support bounded independently owned real32-bit textures in a separate helper and continue the natural second font/raster/texture/cleanup/text/VM path. It SHALL preserve the complete first texture and independently verify second pixels, complete program regions and original two-row counter/terminal drawing inputs. Previous helper/evidence/runtime/UI/save bytes SHALL remain unchanged. It SHALL close every resource and refuse foreign, released, reused-address, malformed and invalid-lock requests. Actual GPU drawing/Present and full world/dialogue SHALL NOT be inferred.

#### Scenario: Two completed text records retain separate real resources
- **WHEN** the second original font call is resumed with the first actual texture still alive
- **THEN** a distinct real texture receives the original converted second raster, both complete readbacks match independent rules and the original text/VM caller returns with two records
- **AND** original counters and exact declared drawing inputs are verified while GPU drawing and later script/world execution remain pending

#### Scenario: Invalid ownership and multiple-lock cleanup
- **WHEN** a request references a foreign/released object, reuses a retired address, exceeds the resource limit or violates that texture lock state
- **THEN** it refuses without cross-object buffer changes and close unlocks/releases every remaining owned texture and device/window

### Requirement: Natural text wait and confirmation preserve live resources
The audit SHALL decode actual source opcode/wait dispatch tables and execute the original VM-driven text fade, cadence and readiness on two completed real textures. It SHALL hold the next confirmation gate without input, separately record a declared mouse confirmation pulse, and resume the original VM to the next source handler boundary. It SHALL independently compare complete per-update regions, exact terminal draw/arrow arguments, both full real texture readbacks, finite retained memory and cleanup; preserve historical/runtime/UI/save/REA bytes. Live input capture, GPU/Present, next-handler execution and full world/dialogue SHALL NOT be inferred.

#### Scenario: Text completes before confirmation is accepted
- **WHEN** the actual second-text return resumes with no input
- **THEN** original opcode50 waits through natural two-row fade/readiness and opcode51 remains waiting without input
- **AND** complete first/second texture bytes remain unchanged while original counters and terminal arrow inputs are verified

#### Scenario: Declared confirmation reaches the next command boundary
- **WHEN** a separately recorded bounded mouse-button pulse is provided at the held confirmation gate
- **THEN** original input query and confirmation return clear the wait without fabricated readiness and the next original handler's natural stack is captured before execution
- **AND** unsupported state, event values and out-of-range writes are refused with complete resource cleanup

### Requirement: Character layer prefix preserves live dialogue resources
The audit SHALL resolve configuration8 to its actual layer and independently derive original node/text-object initialization and nested font stack. It SHALL execute the natural confirmed opcode30 prefix with prior real textures alive, compare full regions and retain all non-owned memory. It SHALL stop before the first name-font API and distinguish decoded later image dependencies from executed loading or animation.

#### Scenario: Original character name font is reached
- **WHEN** the original confirmed handler entry is resumed
- **THEN** source configuration and initialization execute to the exact name-font request, both real texture readbacks remain unchanged and cleanup completes
- **AND** name raster, image loading, animation, GPU drawing and world scheduling remain unexecuted

### Requirement: Character name owns a third real texture
The audit SHALL continue the actual pending character-name font request with real GDI, original geometry and original texture upload/cleanup. It SHALL compare all complete regions, original stack and platform calls, converted pixels, retained prior textures and three-resource cleanup. It SHALL continue original resource selection/path construction to the natural image-loader call and stop before file/image loading. It SHALL preserve prior evidence/runtime/UI/saves and refuse unsupported parents, surfaces, ownership or writes.

#### Scenario: Character name completes before image loading
- **WHEN** the original character name request resumes with two live dialogue textures
- **THEN** a distinct real third texture receives the original converted name raster, original font cleanup executes and the natural image-loader call names sc004.bin/resource32
- **AND** file loading, image decoding, animation, third dialogue, GPU drawing and world scheduling remain unexecuted

### Requirement: Original character image completes with a fourth owned real texture
The audit SHALL execute the actual sc004 image-loader entry using real read-only Windows file APIs, original container/header/vector/texture/row-copy bodies and explicit bounded working-directory/heap/CRT adapters. It SHALL require an empty captured resource32 slot without patching prior resources, retain all three earlier textures, verify complete program/table/record bytes and all image pixels independently, and close every owned file/COM resource.

#### Scenario: Original scene image returns before animation
- **WHEN** the original sc004 loading entry resumes
- **THEN** pinned file bytes and source mode2 image produce a distinct real256x512 texture and original loaded flag/table/file release reach natural4CC0D2 return
- **AND** prior textures remain unchanged while subsequent animation, GPU drawing, third dialogue and world scheduling remain unexecuted

### Requirement: Bounded original character animation continuation
The audit SHALL execute original character delay, frame/background fades and both readiness predicates from the actual image-loader return, compare full state and terminal parameters independently, and preserve all four actual textures.

#### Scenario: Animation releases third-text prefix
- **WHEN** both original readiness predicates succeed after bounded VM updates
- **THEN** config8 selects layer5 and original text2 lookup/split/record setup reaches unexecuted CreateFontA with exact natural stack
- **AND** full rendering, third-text raster and world execution remain unclaimed

### Requirement: Third original live text and natural readiness
The audit SHALL complete layer5 text2 using actual GDI and an independently owned fifth actual texture, compare source-derived full state/pixels/calls and retain previous resources.

#### Scenario: Third text reaches readiness without skip input
- **WHEN** the original text handler completes and explicitly declared no-input VM updates continue
- **THEN** the third row naturally fades to mode1 and original all-object readiness releases opcode50 at PC290
- **AND** the following confirmation, GPU presentation and world scheduling remain unexecuted boundaries

### Requirement: Graphical current-adventure opening preview
The map preview SHALL render the original actor/frame assets and source-projected retained dialogue layers for ten ordered opening texts, with readable responsive layout and keyboard/button navigation.

#### Scenario: Graphical preview preserves school state
- **WHEN** a ready current squad opens and navigates the graphical opening at supported window sizes
- **THEN** source-selected characters/names/text banks appear with bounded fades and previous/next/finish/close controls
- **AND** school state, save bytes and mandatory adventure gate remain unchanged, including close/reopen and unsupported inputs

### Requirement: Current-school deployment and movement trial
The system SHALL expose a labelled MAP05 movement trial using the current ready student squad, verified current limits, source formation/passability and original directional sprites. It SHALL keep session commands transient, preserve school/save/gate state, and distinguish remake navigation from original world/AI execution.

#### Scenario: Current students move on the current map
- **WHEN** a ready supported fifth-week squad opens the trial and the player selects a student and a reachable free destination
- **THEN** source-derived deployment appears with current HP/MP, and deterministic movement follows a contiguous walkable path without overlapping students or reserved source cells
- **AND** pause, stop, recenter, zoom, pan and return remain usable

#### Scenario: Refusal and school return preserve progress
- **WHEN** the roster/loadout/assets are unsupported, a destination is blocked/occupied/outside/unreachable, or the trial closes
- **THEN** no persistent school/save commands, rewards or mandatory-gate clearing occur; invalid movement preserves the current command
- **AND** reopening after valid school edits uses the newly prepared student list, with formal adventure combat still unavailable

### Requirement: Correct original palette indirection
The presentation SHALL resolve original mode2 character palette selection through the actual table+1/loader-1 contract and SHALL compare current roles with the original binding evidence.

#### Scenario: Current student colors match original selected palettes
- **WHEN** current-school sprite assets are exported
- **THEN** original role3/4/9 use the captured palette variants and correct external/embedded mask choice; unsupported palette/source inputs refuse

### Requirement: Audited source combat inputs and isolated trial
The system SHALL independently verify original world admission boundaries and the current-role attack/defense input subset before presenting a current-school combat trial. Initial actors SHALL derive from source scene records and original presentation; deferred templates SHALL remain absent until their activation is verified.

#### Scenario: Source based current combat trial
- **WHEN** a ready supported school squad enters the isolated trial and issues an admitted attack against a source-initial enemy
- **THEN** derived current attack/defense values drive deterministic local health changes and original directional presentation, with pause/stop/return controls
- **AND** full original world/AI/waves/victory, school rewards and mandatory-gate clearing remain unclaimed and unchanged

#### Scenario: Invalid or protected targets refuse atomically
- **WHEN** a target or source/input is unsupported, absent, dead or protected, or the trial is closed/reopened
- **THEN** invalid attacks grant no damage or reward and closing discards transient combat while preserving school/save bytes

### Requirement: Original world mode and natural nested controller audit
The audit SHALL independently decode original mode-request effects and execute the actual current-school world prefix through its first nested entry-controller update, comparing full owned and retained bytes.

#### Scenario: Current opening state progresses inside world prefix
- **WHEN** the SHA-pinned actual school state reaches4678C0 with no pending mode request
- **THEN** the original callee returns naturally, the enabled entry controller performs its first native camera/state update, and execution stops before493630
- **AND** full world/AI/VM/opening completion and school persistence remain unclaimed

#### Scenario: Declared mode requests remain isolated
- **WHEN** separately declared supported requests execute on captured school memory
- **THEN** original UnitCtrl/map/task stores match independently source-derived complete bytes, and CPU/stack/owned memory are restored afterwards
- **AND** invalid mode requests refuse before execution and no probe grants gameplay or settlement authority

### Requirement: Original world time and map suffix
The audit SHALL execute the actual current-school world suffix through original time and map helper bodies, independently verify complete owned bytes and stop before49B180.

#### Scenario: Opening still updates map work
- **WHEN** the actual493630 call continues with opening enabled and event time disabled
- **THEN** the timer remains unchanged while original map pointer processing and double-buffer clear execute naturally
- **AND** full world tick, actions, AI, events and opening completion remain unclaimed

#### Scenario: Bounded input probes restore captured state
- **WHEN** separately declared supported clock and mouse inputs run
- **THEN** exact source-derived signed arithmetic, hover boundaries and owned buffer writes match original bodies, and complete captured inputs/context/stack are restored
- **AND** no live input or persistent school/reward authority is granted

### Requirement: Original visibility stamp and unit lists
The audit SHALL execute the actual opening-specific selection/visibility route and complete original display/category-list builders, independently verifying masks, predicates, sorting and full owned bytes.

#### Scenario: Original opening updates visibility and admitted lists
- **WHEN** actual school world state continues at49B180 with opening still enabled
- **THEN** the source-selected mask stamps current/history planes and original250-slot loops rebuild exactly admitted display/category lists, stopping before48CD90
- **AND** occupied deferred templates remain distinguished from record-state1 display candidates; no AI, activation waves or full world tick is claimed

#### Scenario: Verified private continuation checkpoints
- **WHEN** complete source/native/retention comparisons pass for a current-school case
- **THEN** a private checkpoint records exact CPU/memory state, source and parent identities with a published SHA for later bounded continuation
- **AND** checkpoints grant no runtime/save authority and malformed source/projection inputs refuse

### Requirement: Original paused command and unit suffix evidence
The audit SHALL restore verified private checkpoint provenance and independently verify the original empty queue, no-command input, selection normalization, closed cursor and complete paused unit loop without granting persistent or full-world authority.

#### Scenario: Actual paused opening continuation
- **WHEN** the three pinned school cases resume at48CD90 with empty queue and closed action/event/cursor/input gates
- **THEN** original bodies and all250 work tests execute with exact natural callers, full owned bytes match the independent source projection and retained memory is unchanged
- **AND** original action/animation/AI branches remain skipped and execution stops before490FC0

#### Scenario: Declared selection normalization inputs
- **WHEN** finite work selection bytes are temporarily bound for a source predicate probe
- **THEN** full source selection output is compared and CPU/stack/input bytes are completely restored
- **AND** these probes are not labelled real player input, command consumption or opening completion

### Requirement: Original paused world-tail return evidence
The audit SHALL verify the original post-unit suffix and complete first paused46B470 update against independent source byte projections, while distinguishing its declared audit-driver return from a full game task frame or enabled gameplay tick.

#### Scenario: Actual empty paused tail
- **WHEN** three verified school checkpoints continue at490FC0 with opening1, empty queues and idle effect animation PCs
- **THEN** the original post-unit routines, all ten effect updates and empty command forwarding execute with exact owned/retained bytes and natural inner calls
- **AND** original46B662 returns EAX0 to the existing declared driver with the root stack restored, without claiming opening/VM/AI completion

#### Scenario: Declared idle-effect counter boundaries
- **WHEN** finite signed-short counter values are explicitly bound in all ten effect slots
- **THEN** original466880/40A100 results match unsigned16 wrapping and the complete effect region
- **AND** CPU/stack/owned inputs restore exactly and no active animation, user command or gameplay progress is inferred

### Requirement: Natural second-world action admission evidence
The audit SHALL independently verify the next declared46B470 invocation through natural controller action enabling and the first student status dispatch, without substituting controller-only waiting for the enabled world updates.

#### Scenario: Controller state4 in original world order
- **WHEN** three verified first-paused-return cases invoke the next declared world update
- **THEN** original499DA0 consumes request170, sets action1/state5 and180 delay, then actual map/list/input calls match complete independent owned-byte projections
- **AND** the first occupied unit naturally executes the closed command-generation/empty work-queue/status preamble and stops before475D60 with exact caller/stack

#### Scenario: Continuation and refusal provenance
- **WHEN** actual full state is verified at the student handler entry
- **THEN** private CPU/all-memory checkpoints are pinned by immutable report/file identities and source/parent/case/owned-byte/stack checks
- **AND** unsupported current mode, pending transition, command queue or initial controller state is rejected without claiming activity/VM/AI completion

### Requirement: First enabled student initialization and animation evidence
The audit SHALL verify source-derived first-student initialization and actual original animation updates across bounded natural call boundaries without granting unexecuted world/VM/AI authority.

#### Scenario: Main pose and attached initializer
- **WHEN** three verified second-world cases resume the first mode25 student at475D60 phase0
- **THEN** original direction2/pose18 binding, two first-free88-byte attached pool nodes, source links/frames/layers and immediate steps match complete independent work/pool projections
- **AND** the handler/status preamble returns naturally to primary40A100 without stepping other units

#### Scenario: Original first animation update
- **WHEN** the verified initializer reaches the original main animation call
- **THEN** main and both linked frame waits plus five idle auxiliary controllers, completion and work counter match source byte projections
- **AND** execution stops before482A30 with exact stack, retained memory and private continuation provenance

### Requirement: First enabled student return and regeneration evidence
The audit SHALL independently verify the complete first enabled unit tail and its natural return, separating actual full HP/MP from declared depleted-value recovery probes.

#### Scenario: Actual first enabled student returns
- **WHEN** three pinned482A30 student cases continue with empty effect/damage queues and full health/magic
- **THEN** original six-controller scans, regen/death checks, source region statistics, vision and cell maintenance match full owned bytes and retained memory
- **AND** original46B760 returns naturally and execution stops before the next slot1 update

#### Scenario: Declared recovery boundaries restore
- **WHEN** finite HP/MP gaps, state1/2 and signed-short counters are explicitly bound for isolated472370 calls
- **THEN** original positive recovery/threshold/short-wrap/dead-HP results match independent source rules and full inputs/CPU/stack restore
- **AND** these probes are not presented as actual damage/healing, world advancement or persistent state

### Requirement: Following friendly and inactive unit evidence
The audit SHALL verify the remaining current friendly initializers and first inactive mode11 template handlers in natural world-loop order without granting unexecuted scene/world/VM authority.

#### Scenario: Remaining current friendly units
- **WHEN** verifiedslot1 cases resume with source jobs4/class6 and optionaljob9/class7 in mode25 phase0
- **THEN** original pose/attachments/animations and stationary unit tails match complete independent work/records/pool/region/vision bytes and natural returns
- **AND** original empty-slot tests stop before the first deferredslot215 unit instruction with a verified continuation

#### Scenario: First inactive mode11 handlers
- **WHEN** source state0 templates in slots215/216 enter mode11 phase0
- **THEN** original479F40 work flags6/7 clearing/phase advance and return1 skip subsequent animation/regen/map while records and map remain unchanged
- **AND** execution stops before scene217 without implying activation, AI/events or whole-world completion

### Requirement: First scene role406 unit evidence
The audit SHALL verify originalscene217 initialization, terminal animation and natural return with source-derived faction visibility, without granting unexecuted world/VM authority.

#### Scenario: Scene initializer and opening gate
- **WHEN** verifiedscene217 role406/group6 entersmode28 phase0 with opening1
- **THEN** original4761C0 flag/pose/phase initialization and480A60 early exit match source metadata and all owned/retained memory
- **AND** execution stops before the original main40A100 with a verified continuation

#### Scenario: Terminal animation and full unit return
- **WHEN** the source26E duration1 frame with terminalbit80 updates
- **THEN** original timer/endflag/return, five idle auxiliaries and empty effect/damage/regen/map tail match full source bytes and captured faction vision rules
- **AND** original unitret8 reaches the next218 entry before its first instruction, without claiming animation release, full world or opening/AI/VM completion

#### Scenario: Remaining inactive templates in natural loop order
- **WHEN** verified217 returns to the original218 unit entry
- **THEN** all22 source state0 mode11 units218–239 execute the original early-return handler with complete source byte/call/return/retention equality
- **AND** their records remain inactive and execution stops before scene240, without running their animation/regen/map or claiming world/VM completion

### Requirement: Remaining scene units and second world return evidence
The audit SHALL verify all ten remaining source mode2 units and the actual second46B470 function return without substituting disabled-action inputs or granting unexecuted outer-task/180/VM authority.

#### Scenario: All remaining occupied units
- **WHEN** verified240 cases continue with opening1/action1 and source four-class bindings
- **THEN** original mode2 initialization, terminal/nonterminal animation and empty tails/region/faction vision match full owned/retained bytes and natural ten-unit returns
- **AND** the original loop completes250 slots, clears current work and stops before490FC0 with the event gate closed

#### Scenario: Actual enabled world suffix returns
- **WHEN** verified post-unit CPU continues with its actual action1/state5 controls
- **THEN** original cursor/menu/hover, ten idle effects, inactive secondary slots and empty forwarding match source projection and original46B662 returns to the existing declared audit sentinel
- **AND** the bounded second world body completes while outer game-task/render/180 enabled updates and opening/VM/AI completion remain false

### Requirement: Third declared world prefix and delayed animation clearing
The audit SHALL distinguish the third natural enabled-world continuation from isolated ended-controller probes and retain complete source/state provenance.

#### Scenario: Third prefix and first phase1 student
- **WHEN** the verified second world return is followed by a declared next46B470 invocation
- **THEN** original state5 delay180→179, map/list/input and first phase1 student animation/tail match complete source projections and natural calls
- **AND** execution stops before slot1 with the third world body/180 interval/VM/AI still incomplete

#### Scenario: Ended scene controller clearing probes
- **WHEN** actual ended217/247/248 controllers are passed to isolated original40A100 calls
- **THEN** current PC clears on the next40A800 call and original40AB80 depth0 empty-child path leaves the shared pool unchanged
- **AND** full inputs, CPU and stack restore after each probe without claiming world advancement or attached-node release

### Requirement: Complete third declared enabled world body
The audit SHALL verify all remaining initialized/inactive units and the original third46B470 return without synthetic input or skipped world updates.

#### Scenario: Remaining units and actual ended-root clearing
- **WHEN** verified thirdslot1 CPU resumes with action1/opening1/delay179
- **THEN** all remaining friendly and scene animation/empty tails,24 inactive phase1 early exits, three ended-root PC clears and original250-slot loop match source-derived complete owned/retained bytes and natural calls/stack
- **AND** original loop clears current work and stops before490FC0 without activating templates, freeing attached nodes or executing audio

#### Scenario: Third body returns to existing declared driver
- **WHEN** the verified post-unit CPU continues its actual enabled closed-gate suffix
- **THEN** source ten idle counters2→3 and empty forwarding match full state and original46B662 returns naturally to the existing audit sentinel
- **AND** only the third bounded world body completes; original outer task/render,180 interval, opening/VM/AI and subsequent sound/node lifecycle remain incomplete

### Requirement: Consecutive initialized world updates4–6
The audit SHALL execute each declared original world call in sequence with complete source-derived initialized-state projections and retained-memory verification.

#### Scenario: Fourth and fifth worlds return
- **WHEN** pinned third-return cases continue through declared calls4/5
- **THEN** original controller delays179→178→177, full map/list/input,250-slot units and suffix/root returns match complete source state and natural calls/stack
- **AND** cleared root PCs remain zero and templates stay inactive without skipping enabled units or granting180/VM/AI authority

#### Scenario: Sixth attached sound opcode and next frame
- **WHEN** sixth update expires the actual2063 wait1 frame
- **THEN** original opcode2 sound59 dispatch reaches40B990→40D390, whose captured uninitialized+8 gate returns without backend playback, and the next source frame/state plus complete sixth return match independently derived bytes
- **AND** the audit preserves audio-manager state and records native sound-instruction execution separately from audible playback, full opening/AI and attached-node release

### Requirement: Consecutive regular animation frame transitions
The audit SHALL execute complete declared worlds7–15 in sequence and verify bounded source frame changes independently.

#### Scenario: Scene and attached regular frame changes
- **WHEN** verified sixth-return cases continue through every declared world7–15
- **THEN** original383 transitions at9/15 and2063 transition at11 match full source PC/timer/layer bytes and natural calls, with no same-call decrement of a newly selected regular frame
- **AND** complete prefix,250-slot loop,suffix,retained memory and natural return are verified without granting repeat execution, attached release, full180 interval or VM/AI authority

### Requirement: Continuous source animation lifecycle16–75
The audit SHALL verify all original declared worlds16–75 and distinguish terminal, clearing, repeat and pool release semantics.

#### Scenario: Main animation finishes and clears
- **WHEN** consecutive original calls reach source job5 duration40 terminal
- **THEN** world41 marks its root ended and world42 clears its PC through the original empty-child release path
- **AND** other active units,250 slots,prefix,suffix and retained memory remain independently verified

#### Scenario: Infinite source repeat and attached release
- **WHEN** calls65/73/74 execute the actual383 repeat and2100+job terminal lifecycle
- **THEN** original repeat127 jumps backward3 instructions and decrements the new first frame in the same call; child completion later unlinks from its root and clears only pool byte0 on the following update
- **AND** calls continue through75 with full losslessly retained owned bytes and no full180/VM/AI/outer-task completion authority

### Requirement: Continuous source opcode1 spawning76–118
The audit SHALL execute each declared original world76–118 and distinguish spawned main-archive children from persistent EFCT attachments.

#### Scenario: Original spawn reuses a freed slot
- **WHEN** world107 expires the source friendly regular frame and reaches opcode1
- **THEN** original40ADA0 uses first-free pool allocation/full reset, binds parent bank3/program1, links and immediately updates the child once with instruction layer0/1
- **AND** main opcode-loop countdown, visited-byte skip and the existing2063 update match full source bytes/natural calls/retention

#### Scenario: Existing attachment unlinks after the new child
- **WHEN** original worlds117/118 end then clear2063
- **THEN** original unlink updates the preceding spawned node+20 and frees only2063 pool byte0 while preserving root head and its live spawned child
- **AND** every intermediate world and full returned CPU are verified without granting full180/VM/AI/outer task authority

### Requirement: Bounded original main animation handoff
The audit SHALL execute every declared world119–126 from pinned118 in three actual-school cases, independently verify full source projections, original RNG/voice gate and nonpersistent child cleanup, preserve parent/runtime/save evidence and commit each completed stage locally.

#### Scenario: Source terminal and next-update phase handoff
- **WHEN** jobs3/4 reach source main terminal124 and execute125/126
- **THEN** prior completion drives original event125 and phase2, root cleanup recursively unlinks/frees only persistence0 spawned children, phase2 checks the real signed counter and advances to3, all owned/retained bytes and natural calls/CPU agree and no opening/VM/outer-task completion is inferred

#### Scenario: Native random stream with captured thread state
- **WHEN** original49AD90 attempts event125
- **THEN** original570FE0 updates the parent-bound CRT state, a declared5753B0 adapter only returns that existing block, source threshold/remap and exact original audio-manager guard agree, and altered state, omitted draws/calls, wrong recursive-free arguments, stale parent/checkpoint identity or missing world is refused

### Requirement: Continuous original pending mode and idle pose127–181
The audit SHALL execute every declared original world127–181 from pinned126 in three actual-school cases, verify source pending/current/previous mode and terminal idle-pose lifecycle, retain native RNG and prior evidence/runtime/save, and commit each completed stage locally without pushing.

#### Scenario: Pending mode is applied on the following update
- **WHEN** source mode25 phase3 requests2 then4751F0 executes next update
- **THEN** pending/previous/current mode, phase, flags, empty native path reset and source bank0/index4 pose1 bind agree with full independent bytes/natural calls/returns/retention, the one-tick terminal clears next update, and unsupported live path state or altered metadata is refused

#### Scenario: Job9 handoff and complete bounded waiting continuation
- **WHEN** the actual third friendly unit ends at128 and proceeds through129–133, followed by all worlds134–181
- **THEN** original voice draw count/threshold, recursive nonpersistent child release, pending/mode/pose lifecycle and383 repeat match source, no world is skipped, all returned CPU/checkpoints are verified, and delay1 does not grant zero-delay/VM/AI/outer-task or full180 completion authority

### Requirement: Original countdown zero and paused script boundary
The audit SHALL continue verified181 through original182 and183 and the next184 state6 prefix with independent source expectations, complete owned/retained bytes, original calls and CPU provenance. It MUST distinguish enabled1→0 from the following action0/state6 transition, verify all250 paused slots and frozen character counters/animations, and stop184 before the actual preflight entry4551C0. Script archive and entry identity SHALL be source pinned. Full preflight/playback/AI/outer-task and persistent settlement MUST remain unclaimed.

#### Scenario: Last delay decrement remains enabled
- **WHEN** original state5 sees delay1 on182
- **THEN** it stores0 and completes an enabled unit loop without changing state5

#### Scenario: Following zero test pauses units
- **WHEN** original state5 sees delay0 on183
- **THEN** it disables action and advances6 before the paused250-slot loop and natural46B662 return

#### Scenario: State6 reaches the actual script entry
- **WHEN** the next declared184 original controller queries the captured zero busy byte
- **THEN** it naturally calls4551C0 with0/1 and stops before its first instruction, retaining its real caller stack and source script

### Requirement: Continuous original preflight binding and paused return
The audit SHALL continue verified184 preflight entry through original five-command execution and natural return1, selected binding, controller state7 and complete paused worlds184/185. It MUST execute the original debug/music/audio/memset helper bodies, declare only platform/debug-check adapters, verify all owned/retained bytes, original calls/returns/CPU and immutable checkpoints, and preserve runtime/save/history.

#### Scenario: Actual preflight and selected binding
- **WHEN** the pending4551C0 original body executes on the captured school CPU
- **THEN** source opcodes167/8/166/11/19, sparse VM reset, native guarded cleanup and return1 agree,4549D0 binds0/1 and initializes task control, and the controller increments7 before its natural world return

#### Scenario: Paused world and status waiting
- **WHEN** worlds184/185 process action0 with selected task active
- **THEN** every250-slot loop and suffix is independently verified, character animation/counters remain frozen,185 queries native454C40 status1 and stays7, and no normal VM/task/render/AI completion is inferred

### Requirement: Original first selected-task initialization
The audit SHALL derive original task-script ordering and execute one declared454CF0 after verified185 through naturally nested457830, source input-buffer resets and inactive fade/board guards. It MUST declare only a bounded lstrlenA adapter reading existing captured empty text, verify full source stores/calls/CPU/retention, and MUST NOT sample or inject live input, skip task phases or claim a complete outer task/playback frame.

#### Scenario: Natural first task setup
- **WHEN** the selected task has script phase0/status1, empty captured text and inactive fade/board state
- **THEN** original454CF0 queries status, initializes its captured input manager through native resets, advances phase0→1 and naturally returns0 without executing playback VM

### Requirement: Native captured input reset and next task admission
The audit SHALL restore the verified first-task return, execute original425DE0 with a declared closed-IME result for its captured null context, execute the next phase1→2 task poll, reset through the same native function again and stop the following phase2 task at the unexecuted4CE8F0 entry. It MUST independently derive signed input flag handling, import identity and task phase branches; preserve complete owned/retained memory, source calls/stack/CPU and immutable checkpoints. No live OS response, full outer task, VM playback, rendering, AI or persistent completion SHALL be inferred.

#### Scenario: Original negative input request is consumed
- **WHEN** captured input flagFF and context0 enter original425DE0 with declared ImmGetOpenStatus(0)=0
- **THEN** original425E60(0) takes the inactive branch, no ImmSetOpenStatus call occurs, original425E3F clears the flag and the function naturally returns0

#### Scenario: Subsequent task phases reach normal playback entry
- **WHEN** the original phase1 task poll completes after native reset and the next reset precedes phase2
- **THEN** phase1 increments2 with original clears/guards, the next454CF0 naturally calls4CE8F0 with VM receiver and caller stack, and no VM instruction or full outer frame is counted as executed

### Requirement: First normal VM command and native overlay resource boundary
The audit SHALL continue the pinned normal VM entry through original opcode167, native overlay dispatch and stack object construction, then the actual resource binding to its unexecuted407AD0 draw call. It MUST independently verify all owned/retained memory, complete128-byte stack packet and SEH chain, original calls/ABI/CPU and immutable checkpoints. It SHALL preserve runtime/save/history and MUST NOT fabricate missing graphics resources, stub original helpers or claim a completed VM/task/render frame.

#### Scenario: First normal command and native display object
- **WHEN** the selected VM executes opcode167 from source offset452 on the retained task caller stack
- **THEN** source variable0/PC/counters agree, the natural4D29E0 kind1 dispatch executes original stack constructors, and the full native128-byte display object agrees before407870

#### Scenario: Captured texture binding uses the actual source index
- **WHEN** original407870 requests group20/index0 while captured count is1
- **THEN** original41F5A0 returns the existing record, source metadata and geometry/layer51 agree in the full packet, and execution stops before407AD0; no resource pointer or completed render frame is invented

### Requirement: Native captured draw gate and first VM/task returns
The audit SHALL continue the original pending407AD0 on the retained VM/task stack, verify the captured disabled render branch and all original cleanup helpers, execute remaining inactive VM maintenance and return through454D90, then complete the existing454CF0 suffix. It MUST verify all owned/retained bytes, source ABI/calls/CPU, fresh identities and immutable checkpoints without original-body substitutions or GPU claims.

#### Scenario: Disabled renderer and native cleanup
- **WHEN** the captured TASK+B28E word is0 and stack resources are inactive
- **THEN** original407AD0 returns1, the native destructor chain restores SEH0 and reaches4D024F with full packet and retained bytes verified, without GPU work

#### Scenario: First native normal VM and selected task return
- **WHEN** original VM resumes with ten inactive layers, five inactive secondary records, one inactive presentation object and twenty inactive resource records
- **THEN** all51 maintenance calls execute original bodies, VM returns1 to454D90 and inactive menu/fade/board task suffix returns0 with phase2/status1/PC8 preserved; full outer frame and later playback remain unclaimed

### Requirement: Native normal opening branch and complete captured fade
The audit SHALL resume verified task returns using explicitly declared original reset/task calls with inherited bounded platform responses. It SHALL execute the actual conditional PC44 path, variable/global/slot/pose commands and the60-update fade, preserving every original helper body, owned/retained byte and natural return. It MUST distinguish helper wait4 clearing, fade completion and the subsequent VM wait-clear poll, and MUST NOT infer GPU output, live input, full outer scheduling or persistent game progress.

#### Scenario: Actual opening path and original state commands
- **WHEN** the captured variable0=1 enters opcode8 at PC8
- **THEN** original comparison takes PC44, native variable/global/slot commands and both pose commands execute in order with source arguments, full state and additional wait-clear polls verified

#### Scenario: Complete native fade without forced endpoint
- **WHEN** original opcode117 starts duration60 using source fixed-point range38912
- **THEN** original x87 conversion derives the integer step, all60 task suffix updates and completion execute, and only the following VM poll clears wait4 before the next script command; full state/calls/CPU and immutable checkpoints agree without manual wait or alpha changes

### Requirement: Native normal display reset and old-counter timer
The audit SHALL continue verified fade_finish returns through original56 display initialization/query,20 text mode,12 timer setup and31 original timer polls, then reach the unexecuted27 handler on the natural retained VM/task stack. It MUST verify every intermediate owned state, original calls/ABI/return values, pending CPU/args and all retained bytes with immutable SHA-guarded checkpoints, without body stubs, manual waits, new OS responses or GPU/full-world claims.

#### Scenario: Original display reset and text mode
- **WHEN**56 evaluates literal2 and the next VM polls its presentation object
- **THEN** original4C76B0 records type2/state0/counter0/limit16,4C7AB0 naturally returns AL1 and clears the wait, and20 changes only source text-mode9228 with source/full state verified

#### Scenario: Timer30 completes on its31st poll
- **WHEN**12 initializes count0/limit30 and uses the opcode12 branch of4CCB90
- **THEN** polls1–30 retain wait1, poll31 stores31 and clears both1CD and wait, and a subsequent original task reaches unexecuted4C5EA0 with actual27 arguments and caller/CPU state; no character-body, text or outer-frame completion is claimed

### Requirement: Native character template and active presentation admission
The audit SHALL resume the pending27 handler on its retained original VM/task stack, verify template4/layer7 setup and native text-layout/show helpers, complete the actual handler return and overlay cleanup, then reach unexecuted4CA600 through original layer7 interpolation. Every source argument/ABI, critical return, complete owned state/CPU/stack and all retained bytes MUST agree with immutable SHA-guarded checkpoints; no additional root driver or body/platform substitution is allowed.

#### Scenario: Literal operands and original handler return
- **WHEN** the pending4C5EA0 receives the captured27 command
- **THEN** it keeps decoded0FFFFFFF operand values, applies original38-byte template4 and font/spacing/show settings on layer7, and naturally returns1 to4CED48 without completing VM/task or dialogue

#### Scenario: First active layer graphics call
- **WHEN** the VM advances toPC224/wait1 and finishes the existing overlay cleanup
- **THEN** inactive layers0–6 and native4CD850 execute before natural4CA600 admission; all five full argument words and real stack are retained before its first instruction, without claiming graphics-list/queue/GPU or full-frame completion

### Requirement: Native frame graphics and renderer-owner precondition
The audit SHALL resume4CA600 on the retained layer/VM/task stack, execute four native frame sprites through resource binding/disabled draw/cleanup, and verify each128-byte object and source call/ABI/return. It SHALL continue native rectangle admission and the actual40E2A0 prefix to the first read through captured owner0, preserving complete CPU/stack/effective address and immutable memory proof. It MUST NOT patch owner/gate, execute the invalid target read, invent a clipping result, or infer queue/debug/GPU/VM-task/dialogue/full-frame completion.

#### Scenario: Original four-piece frame return
- **WHEN** style1 graphics is entered at the verified4CA600 checkpoint
- **THEN** all four rows generate real sprite objects and complete native bodies, full objects/SEH/calls/ABI agree, and the list naturally returns24 with owned/retained memory unchanged

#### Scenario: Original renderer initialization is a precondition
- **WHEN** rectangle410310 calls40E2A0 using the captured manager whose owner is0
- **THEN** its prefix reaches40E2D0 before reading effective addressB278, all caller/CPU state is retained, and the original40D970/413500 initialization path is source-bound for subsequent work without patching current state

### Requirement: Isolated original renderer prerequisite execution
The audit SHALL source-bind renderer construction, owner/device binding, queue initialization and outer reset/draw order. It SHALL execute isolated original bodies with declared scratch state and bounded debug CRT allocation, verify full manager/queue/arena bytes and guarded writes, and preserve the retained VM checkpoint. It MUST NOT claim original D3D initialization, continuous VM progress, GPU output or a full outer frame from those probes.

#### Scenario: Native initialized queues and rectangle links
- **WHEN** isolated original construction and binding precede original queue initialization using declared successful allocations
- **THEN** the original4096-layer table and1MiB arena are initialized, native rectangle insertion and per-frame reset agree with source projections, and all unrelated bytes are retained

#### Scenario: Unsupported or exhausted renderer state
- **WHEN** a declared clip input is outside the original signed predicate or the arena has exactly24 bytes remaining
- **THEN** original clip rejection or the strict capacity debug-call boundary is observed without fabricating a debug response or GPU work

### Requirement: Live original windowed device startup prefix
The audit SHALL execute original windowed device startup helpers with live owned x86 Direct3D8 factory/device/surface results, verify complete source presentation/owner state, original calls and pending font-entry stack, and release all host resources. It MUST preserve original IAT and retained VM, reject foreign objects and fullscreen requests, and MUST NOT count platform success as GPU drawing or a full startup/outer frame.

#### Scenario: Original startup reaches font initialization
- **WHEN** declared hidden-window startup enters413450 with valid bounded dimensions and automatic device selection
- **THEN** original factory, device, capability, backbuffer, format andviewport logic execute with live results and naturally reach unexecuted415F50 before manager owner binding

#### Scenario: Foreign state and expired platform objects
- **WHEN** a request names a foreign device/surface, requestsfullscreen or follows resource cleanup
- **THEN** the bridge refuses it without performing the requested interface call and no released pointer is exported as a resumable checkpoint

### Requirement: Full original owner construction before font initialization
The audit SHALL execute original412E30 and its native array/subconstructors on declared dirty input with live32-bit DC/timer responses, verify the complete owner and finite source global mutations, and derive initial font pointers and render gate from original stores. It MUST NOT manually zero font slots or patch the retained VM.

#### Scenario: Native construction permits the first font cleanup
- **WHEN** dirtyA5 orCC owner state enters412E30 with inherited pinned timer globals
- **THEN** original subconstructors and loops return naturally, old fonts are0 andgate is1 by original stores, and all unrelated bytes plus SEH are retained

### Requirement: Original first font creation and static constructor admission
The audit SHALL continue the naturally pending415F50 after real device initialization on the constructed owner through realCreateFontA andGetObjectA, preserving actual60-byte LOGFONT and pending52AE11 stack. All live handles MUST be released, and no static font object, owner binding, queue or VM completion may be claimed.

#### Scenario: Actual font properties reach the internal font constructor
- **WHEN** native416140 consumes newly constructed null font slots and original52AFE6 reads the created font
- **THEN** realGetObjectA outputs60 bytes and execution stops before52AE11 on its natural device/LOGFONT/output-slot call without fabricated font objects

### Requirement: Original font factory and explicit cache-state boundaries
The audit SHALL execute the original static font factory and constructors with bounded declared CRT allocation responses and verify complete heap/owner/image/call-stack state. Inherited cache state MUST remain unchanged and an absent captured cache node MUST NOT be read. Empty-cache experiments MUST be explicitly distinguished from captured continuation, use owned live x86 device methods and stop before unresolved texture code.

#### Scenario: Inherited cache target is not captured
- **WHEN** the original lookup encounters inherited80A398=04D61D08 without mapped node memory
- **THEN** it stops before548D95 target read, retaining the head and all old evidence without inventing node contents

#### Scenario: Independent empty-cache native initialization
- **WHEN** an experiment declares only an empty initial cache head and bounded CRT memory
- **THEN** original font/cache constructors and real device AddRef/caps/creation queries execute to unexecuted52755E, full bytes and lifetime are verified, and no retained VM or texture completion is claimed

### Requirement: Original font-cache texture requirements and real resources
The audit SHALL resume the explicitly declared empty-cache CPU through original texture requirements and creation bodies with real owned x86 device/factory/texture/surface methods. It MUST retain original inherited debug target and source/IAT bytes, verify complete original calls/state/guards and release every additional interface reference. It MUST distinguish this experiment from inherited-cache recovery or retained VM progress.

#### Scenario: Requirements naturally return to texture creation
- **WHEN** original52755E receives the pending cache width/height/format inputs
- **THEN** native format selection, real platform queries and source dimension/mipmap rules return naturally to unexecuted5275D7 without a replacement D3DX result

#### Scenario: Actual texture and level surface reach sprite admission
- **WHEN** native5275D7 repeats requirements and the owned device accepts the resulting bounded texture parameters
- **THEN** actual CreateTexture/GetSurfaceLevel results reach the original cache fields and54864C returns to unexecuted52AE80; texture creation is verified but drawing/full font/VM completion is not claimed

### Requirement: Native sprite and first static font factory return
The audit SHALL continue the declared empty-cache experiment through original sprite construction, owned live x86 device/GDI calls and first static font factory returns, verifying all original object/heap/image/call-stack bytes and handle/reference lifetimes. It MUST preserve historical evidence and retained VM and MUST NOT infer state-block creation, drawing, complete415F50 or restored original upstream cache state.

#### Scenario: Sprite factory reaches real cache GDI admission
- **WHEN** original52AE80 allocates32 bytes and executes53C665/53BC06 with the current owned device
- **THEN** real device reference/caps/creation results determine full sprite flags and the original factory returns before CreateCompatibleDC executes

#### Scenario: Cache GDI setup returns the first font object
- **WHEN** original cache DC/bitmap/color/selection calls andCreateFontIndirectA succeed on bounded owned resources
- **THEN** original cache/font factories copy LOGFONT and return naturally through4162C0, owner+B270 receives the object and execution stops before416021 additional-slot work with no fabricated D3DX result

### Requirement: Additional font construction and atlas capability admission
The audit SHALL continue the independent first-font return through original additional-slot allocation, native face copy/construction and owner binding, then original atlas dimension selection and a real owned caps query. It SHALL verify complete memory/ABI/CPU and preserve historical/runtime/private VM bytes. It MUST distinguish allocation responses from executed original constructors and stop before unsupported texture creation.

#### Scenario: First additional slot receives its original object
- **WHEN** original416021 consumes source slot0 tables
- **THEN** original401000 copies FixedSys with native56CD90, initializes size12/flags1 and null resource fields, returns naturally and original caller stores owner+1090 before4010D0

#### Scenario: Atlas requirements reach an unexecuted resource call
- **WHEN** original4010D0 uses the newly constructed object and live device caps
- **THEN** original dimension/clamp logic prepares the exact CreateTexture call at40120C, with no texture/glyph/state-block/full-font or retained VM completion inferred

### Requirement: Original additional atlas resource and GDI preparation
The audit SHALL execute the pending original atlas texture call and subsequent native/GDI setup using fresh owned x86 helper versions, verify full original memory/ABI/CPU and all live resource lifetimes, and stop before the first glyph measurement. It MUST preserve historical/source/runtime/save/private VM bytes and distinguish this independent empty-cache experiment from retained VM advancement.

#### Scenario: Actual additional atlas texture reaches bitmap setup
- **WHEN** original40120C consumes its verified256-square/format26/pool1 arguments
- **THEN** the owned device creates an additional real texture, native memset/header stores execute and stop before CreateCompatibleDC with old cache resources intact

#### Scenario: Real GDI resources reach first glyph measurement
- **WHEN** original40127E continues with real DC/DIB/map mode/MulDiv/font/selection/color/alignment calls
- **THEN** native arithmetic and setup prepare the first character20 measurement at401491, all owned resources are cleaned and no glyph output/upload/additional-font/full-startup or retained VM completion is inferred

### Requirement: Original glyph generation and actual atlas upload
The audit SHALL execute all95 original measurement/drawing pairs and native UV stores, then original pixel conversion with owned real texture lock/unlock, full external-buffer transfer/readback and exact memory/ABI/CPU verification. It MUST declare GDI flush/snapshots and readonly texture readback as inspection-only, preserve prior evidence and retained VM, and stop before original cleanup/full-font completion.

#### Scenario: Original character loop fills the atlas
- **WHEN** the pending401491 CPU receives owned actual GDI measurements/drawing responses for characters32..126
- **THEN** original wrapping and x87 UV stores match all190 platform calls and the full object, actual DIB pixels are captured and401660 remains unexecuted

#### Scenario: Original pixel conversion reaches actual texture memory
- **WHEN** real LockRect provides its owned pitch/bits and original401660 continues
- **THEN** every one of65536 native-converted16-bit pixels and pitch padding matches source projection, real UnlockRect/readback verifies the complete buffer and execution stops4017B6 before original cleanup

### Requirement: Original first additional font cleanup and device-state return
The audit SHALL continue the existing original CPU through its three GDI cleanup calls and4010D0 return, then401810 vertex-buffer creation and both state-block recordings with actual owned x86 interfaces. It SHALL verify full native memory/ABI/CPU/resource lifetimes and preserve prior evidence. It MUST distinguish native/deferred/fallback cleanup, inspection-only queries and the independent empty-cache experiment from retained VM advancement.

#### Scenario: Native atlas initializer releases temporary resources and returns
- **WHEN** original4017B6 consumes its still-owned bitmap/DC/font locals
- **THEN** actual GDI deletion results and deferred lifetime are recorded, original4010D0 returns and its original caller reaches401810 without resource stubs

#### Scenario: First additional font completes device-state initialization
- **WHEN** original401810 executes on the same first additional font and owned device
- **THEN** actual8400-byte vertex buffer and two source-ordered state blocks reach original fields, full function returns to416101 and all external resources are released, with second font/full415F50/retained VM/drawing still pending

### Requirement: Original second additional font construction and admission
The audit SHALL continue the same independent empty-cache CPU after the first additional font return through native loop increment, separate second-slot construction and live caps preparation. It SHALL preserve all first-slot resources and full memory/ABI/CPU evidence, original helpers/history/runtime/save/private VM bytes, and stop before second atlas creation.

#### Scenario: Successful first font advances the original loop
- **WHEN** the retained independent CPU reaches416101 with first401810 result0
- **THEN** the original signed success test and loop increment select index1 at41603D without allocation or owner/image/heap mutation

#### Scenario: Separate second object binds and prepares its atlas
- **WHEN** original428A40 and401000 consume the index1 source tables
- **THEN** original ANSI copy and owner+1094 assignment create a distinct1656-byte object with size8/flags0, and native4010D0 plus actual caps reaches unexecuted40120C with the correct second output address; first-slot bytes/resources persist and no second atlas/full415F50/retained VM completion is inferred

### Requirement: Original second atlas creation and GDI preparation
The audit SHALL continue original second40120C through actual distinct owned texture creation and native/GDI setup to unexecuted401491 while preserving first-slot resources, complete native memory/ABI/CPU and historical evidence. Helpers SHALL be immutable new versions with honest resource ownership, auxiliary inspections and complete cleanup.

#### Scenario: Second real texture preserves first resources
- **WHEN** original second40120C consumes the second-slot output address
- **THEN** a distinct256-square/format26/pool1 texture is created, first texture/VB/tokens persist, original bitmap header executes and CPU stops before second DC creation

#### Scenario: Second GDI setup prepares its first glyph
- **WHEN** original code consumes actual second DC/DIB/MulDiv/font/selection/color responses
- **THEN** size8/flags0/rawANSI name produce height-11/weight400 font arguments and native locals reach first401491 measurement, full prior snapshots remain intact and no second glyph/upload/state/full-return/retained VM completion is inferred

### Requirement: Second native glyphs and uploaded atlas with explicit shadow retirement
The audit SHALL preserve the deleted first DIB snapshot, explicitly retire only its verified shadow mapping, and continue the same second-font CPU through all95 original glyph pairs/UV stores and65536 pixel conversions using actual owned x86 GDI and texture responses. It SHALL retain first persistent resources and complete memory/ABI/CPU/access evidence, distinguish inspections from native calls and stop before second cleanup/full font return.

#### Scenario: Deleted first DIB shadow becomes immutable retired evidence
- **WHEN** first native cleanup has released its temporary GDI objects and second setup reaches401491
- **THEN** exact old DIB shadow bytes/guards are preserved in a retirement ledger, only its declared mapping is unmapped, all other ranges and CPU remain unchanged, and no native game call is inferred

#### Scenario: Second glyph loop and native upload complete
- **WHEN** second95 actual GDI measurement/drawing pairs and real texture lock are admitted
- **THEN** original UV/native65536-pixel loops match dynamic metrics and complete buffers/pitch/access order, actual unlock/readback matches every pixel, old retired evidence and first resources remain intact and CPU stops4017B6 before second cleanup

### Requirement: Second original font cleanup and full initializer return
The audit SHALL execute the pending second font cleanup, real distinct VB/two state blocks and original two-slot loop/SEH/415F50 return on the same independent CPU, using immutable owned x86 helpers. It SHALL preserve both complete font objects/resources and pixel/retired evidence, verify every source ABI/CPU/memory boundary and clean all native/fallback resources honestly.

#### Scenario: Second font completes original cleanup and device state
- **WHEN** original second4017B6 consumes current GDI locals and then calls401810
- **THEN** actual second bitmap/DC/font deletion, distinct8400-byte VB and two exact30-call blocks store second resources and two distinct tokens while first resources remain valid

#### Scenario: Original font initializer returns to its real caller
- **WHEN** second401810 returns0 to416101 with loop index1
- **THEN** original increment selects index2, success/SEH restore/ret execute and reach unexecuted4134E3 with exact parent stack/CPU and unchanged complete objects; no413450 suffix/manager/queue/retained VM advancement is inferred

### Requirement: Continuous original startup caller manager and queue admission
The audit SHALL continue the verified independent font-return CPU through original413450 success handling,40D970 binding and40DAB0 allocation/zeroing, then original gamma generation to the unexecuted416CFA device call. It SHALL preserve the complete native prefix, all resources/snapshots and historical evidence and use only exact explicitly declared CRT allocation responses.

#### Scenario: Original owner and live device bind before queues
- **WHEN** original415F50 returns0 to4134E3
- **THEN** the original caller passes its constructed owner to40D970, copies its actual device through4142B0, then allocates and natively clears the4096-layer table and1MiB command arena with full CPU/ABI/buffer/guard verification

#### Scenario: Complete original gamma data stops before device invocation
- **WHEN** original queues return0 to413513
- **THEN** original416C40 writes three complete256-entry16-bit channels with value index shifted8, and416CC0 prepares device/flags1/ramp arguments before stopping at unexecuted416CFA; no device gamma change, full413450 return or retained VM advancement is inferred

### Requirement: Actual void gamma invocation and original startup return
The audit SHALL continue the same independent original startup CPU at416CFA using an immutable owned x86 device helper, execute the actual gamma method and both original returns, and preserve all prior native state/resources/evidence. It SHALL distinguish undefined EAX register bits from a void API status and restore externally owned gamma state during cleanup.

#### Scenario: Original gamma helper returns naturally
- **WHEN** both original fonts, manager queues and gamma table are complete at416CFA
- **THEN** a late actual method inspection preserves CPU and old maps except its declared method mapping, original flags1/ramp call executes on the owned device,416CC0 checks/unwind/ret4 reach413546 with exact ABI/CPU and full retained buffers, and no HRESULT is invented

#### Scenario: Original startup returns success with balanced external state
- **WHEN** original416CC0 returns to413546
- **THEN** original success0 and413450 epilogue/ret20 return to the declared root with original saved registers/stack restored, device/desktop gamma and all owned resources are restored/released, and real upstream/retained VM/GPU drawing completion is not inferred

### Requirement: Actual upstream renderer factory owner construction and admission
The audit SHALL execute both original412C70 and450570 allocation/owner-constructor prefixes on their real parent stacks with explicit scratch inputs and actual owned DC/timer responses. It SHALL preserve inherited globals, full owner/guards/output/CPU/SEH and all historical evidence, and distinguish each natural next-call boundary from factory success.

#### Scenario: Original factories allocate and construct their owner
- **WHEN** declared factory arguments enter either original root
- **THEN** original428A40 consumes one exact47648-byte declared CRT allocation, original412E30 completes all42 source calls and actual platform queries, and natural return restores the parent frame while output stays untouched

#### Scenario: Distinct real startup prerequisites remain visible
- **WHEN** each factory continues its original nonnull branch
- **THEN**412C70 reaches unexecuted413450 with window/1/1/dimensions, while450570 reaches unexecuted4500B0 with its inherited absent game context and original data literal; cache/global pointers remain unchanged, and no fabricated context/audio/device/factory success or retained VM progress is inferred

### Requirement: Original main-context construction and publication evidence
The audit SHALL execute original49DDC9 allocation tail,44FBB0 and49DE01 on an explicitly declared mid-WinMain frame using owned actual x86 system primitives, preserving complete allocation/backing guards, source image except exact native changes, parent stack and historical/private evidence. It SHALL distinguish isolated global publication from full WinMain and retained VM integration.

#### Scenario: Complete main-context creation without inherited pointer fabrication
- **WHEN** two independent dirty-backing cases execute the original allocation tail and complete constructor within fresh helper lifetimes
- **THEN** the original instruction publishes the newly constructed pointer, real event/critical-section resources are balanced, all native calls/returns/buffers are verified and old captured heaps/cache/retained VM remain unchanged
- **AND** zero-length directory memset preserves bytes outside actual subsequent API output; no save file is created

### Requirement: Original task initialization and actual duplicate-window admission
The audit SHALL continue the original constructed main-context CPU through32 task-slot resets, class-title initialization and actual x86 FindWindowA, verifying natural boolean conversion and source-selected branch while preserving full owned memory and history.

#### Scenario: Live duplicate-window outcome determines pending original body
- **WHEN** two independent cases replay the original constructor and query the original Cross Hermit class without changing any existing window
- **THEN** the original branch stops at unexecuted49E092 when a duplicate is observed, or executes command-line/configuration preparation to unexecuted450350 when none is observed
- **AND** no window body, fabricated query result, retained VM repair or reuse of expired resources is accepted

### Requirement: Original window geometry and partial class admission
The audit SHALL execute original450350 geometry and partial class preparation using actual owned x86 SetRect/AdjustWindowRect responses, exact source calls/stacks/full buffers, and preserve the unexecuted LoadIconA boundary and historical/runtime bytes.

#### Scenario: Actual no-duplicate startup reaches original icon prerequisite
- **WHEN** a fresh original prefix naturally takes the no-duplicate branch into450350
- **THEN** native geometry calls and seven class dword stores execute on the same CPU/helper lifetime, all five uninitialized class dwords and retained memory remain intact, and450416 stops before its import call
- **AND** icon157/resource5 identity is source-verified without interpreting the inherited instance scalar as a real module or claiming class registration/window creation
