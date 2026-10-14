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
