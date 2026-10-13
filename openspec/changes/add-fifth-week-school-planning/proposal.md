# Proposal

## Why

第五周剧情已可阅读并保存，但结束后只能停在职务室入口。需要延续同一批成员与成长，进入职务室，再开放第五周学校编班，并按原版必修冒险顺序准备出发。

## What Changes

- 沿当前 4/4 授课到 4/5 Chapter018 的同一原版 CPU，验证实际 state8、CH002、state9 与学校初始化前缀。
- 保存职务室停留和进入学校的独立命令，保留已完成成长、关系、MVP与剧情；迁移原有 v1/v2/v3 试玩存档。
- 增加使用原版背景的职务室画面，提供进入学校、回顾、存档和战斗预览。
- 开放第五周五班成员调动与课程查看；必修冒险完成前禁止选课，不清除来源gate。
- 根据用户2026-10-08的继续指令沿原版路线推进：核对学校出发就绪与参战名单准备，显示由当前班级生成的必修冒险准备画面。已完成准备页阶段不执行战斗、第二轮成长或后续剧情。
- 根据2026-10-09继续推进指令，延伸到原版学校提交、pending10消费、场次配置/参战学生传递及pending16；实现当前队伍的纯交接接口。该交接阶段将4DAB10误标为资源装载；后续原指令核对表明它只是工作区清零。
- 本轮继续执行4DAB10工作区重置和4B9340→4B93C0完整战术记录派生，导出独立职业/技能规则，接当前角色的战术输入与上限/ENGAGE纯计算。真正场景资源装载位于后继战术构造，保持待接边界，不把记录派生称为可操作战场。

## Capabilities

### New Capabilities

- `school-fifth-week-planning`: 第五周职务室到学校的可保存续接，以及保留成长的班级规划、课程限制与必修冒险出发准备。

### Modified Capabilities

无。学校前置能力目前保存在已完成未归档的 change specs 中，主 specs 尚无学校能力。

## Impact

原版审计工具、SchoolPlayground 与学校会话、职务室资源导出和 Godot 图形界面、存档兼容测试与验收文档。仅本地 Git 提交，不改写原版存档，不 push。

## Tactical startup extension (2026-10-09)

Continue actual pending16 dispatch and native outer tactical construction with explicit unresolved graphics/UnitCtrl subcomponents, source script-work setup and startup normalization up to the first resource request. Capture common resource and independently declared current-scene start-resource selection probes, resolve local file identities without claiming their loader/VM/world has run. Display already verified current-role HP/MP on graphical departure cards. World construction, enemies/events and executable battle remain subsequent stages.

## Native resource loading extension (2026-10-09)

Continue the same current-school pending16 pipeline through original path composition, file loader and texture-container traversal for common/TactStart05/Gybc_00, then load the source-selected current scene script. Stop before the first tactical phase update. File/heap/CRT and DirectX upload remain explicit external primitives; UnitCtrl construction remains unresolved. Export an independent byte-derived resource catalog and verify all parsed entries, exact script selection, refusal cases and persistent retention. No battlefield or actual battle is claimed.

## UnitCtrl and logical scene map extension (2026-10-09)

Continue actual pending16 through native logical UnitCtrl, AI/animation/event linked lists and generic appearance-table construction. Continue natural startup through phase0 into phase2 and source-selected logical scene map loading, stopping at the scene graphics request. Export independently decoded current-map inputs and original texture preview with source/pixel provenance. Graphics/fonts/audio remain declared primitives; enemy/event/VM placement and playable battle remain subsequent stages.

## Native scene resources and graphical current-map preview (2026-10-09)

Continue naturally from the verified scene graphics request through original MAP texture traversal, BMP minimap/fog preparation and VPT loading/rebasing, stopping before the following unit-art reset/initialization entry. Export independent original minimap/pathfinding inputs and separate native fixtures. Add an interactive current MAP05 preview to the graphical departure screen with pan/zoom and state-preserving return. This preview contains no invented squad/enemy placement or executable battle; unit assets, t0005 VM, scene events and placements remain the following dependencies.

## Unit reset and effect animation metadata extension (2026-10-10)

Continue the paused original school CPU through467EB0 work reset, original relation setup and text-cache request loops, then466000 effect controller construction and exact read-only Efct.bin loading/metadata copy. Text rasterization and existing graphics objects remain explicitly declared boundaries. Stop at the effect texture binding entry before accepting a fabricated animation object. Independently decode text-table inputs and effect animation/container metadata, verify original pointers, retained records and refusal cases, and preserve the current graphical map/save behavior. Current/enemy work construction, scene VM and placement remain later dependencies.

## Effect texture and work initialization extension (2026-10-10)

Continue actual school CPU through original effect texture slot selection, all Efct texture/header records and effect work/initial animation setup. Declare GPU upload explicitly and reject unexpected assertions: source4660FC selects slot100, bypassing the dynamic-slot assertion dialog. Stop at the following mapcom resource request before current/enemy work. Independently verify every texture entry and effect work/program input; preserve historical/save/UI evidence and commit each stage locally.

## Map common resource and first current-unit input (2026-10-10)

Continue the actual paused school CPU through read-only mapcom.bin loading and native top-level/nested pointer traversal. Follow original current-record preparation and the first source-selected 176-byte unit-record copy, stopping before4680B0 constructs its work. Verify only original state/recovery fields may change in current records, retain persistent roles/MVP/date and prior effects, independently decode the map common container and preparation/selection policy, and preserve old runtime/save evidence. Full current/enemy construction, VM and placement remain subsequent dependencies.

## First unit work and animation cache request (2026-10-10)

Continue the actual first4680B0 input through finite work clearing, record binding/sentinels, initial status and original animation-cache lookup/allocation/controller construction. Follow original job/palette selection and stop at the natural unit animation resource request before file loading. Independently decode every initialized work/record byte, status template and job/cache/controller input; retain current global records, persistent data, previous map/effect bytes and runtime/save evidence. The constructor tail, unit animation resources, remaining current/enemy work, VM and placement remain following dependencies.

## First unit animation resource binding (2026-10-10)

Resume the actual school CPU at the first unit-art request, load the exact source-selected archive read-only and execute original metadata copying, selected palette/mask lookup, complete texture record/header traversal, controller mode setting and temporary file release. Stop before467147 binds animation work into the selected unit, preserving its work/copied record and previous map/effect resources. Independently verify all archive/texture/palette inputs, native records and bounded ownership; retain historical/runtime/save evidence. GPU remains a declared primitive and this stage does not complete the unit constructor or place units.

## First unit constructor completion (2026-10-10)

Finish the first source-selected4680B0 constructor on the actual school CPU, including initial action/program binding, pre-placement coordinates, logical cell accounting and remaining status/scratch defaults. Stop at the natural caller4533FA before the next unit, independently verify complete work/record/scratch/cell bytes from original source, and preserve previous resources, runtime/save and history. This completes one constructor; remaining current/enemy units, scene VM, actual placement and graphical battle integration remain subsequent work.

## Complete current-unit construction (2026-10-10)

Continue the actual school CPU from the first constructor return through both current-record selection loops and remaining unit constructors. Execute original loading-progress updates with explicit graphics/scheduler primitives; load exact original job6/7 archives and retain native cache/metadata/texture ownership. Stop at453540 before enemies. Independently verify selection/order, cache/resource/initial-work bytes and every retained object; preserve runtime/save/history and commit completed stages locally.

## Scene-unit template records (2026-10-10)

Continue453540 scene-selected template preparation. Scene5 contains35 templates, including NPC/friendly, active enemies and deferred event waves; do not label all templates deployed enemies. Execute first4DA450/4DA5F0/4DFC20/4E0A00 on the actual school stack and stop before enemy-loop4680B0. Separately derive all35 records on the original CPU with explicitly declared driver calls, independently verify full numeric/scene overlays, preserve prior units/resources/runtime/save/history and commit stages locally. Full enemy work/assets/placement/VM remain subsequent stages.

## Scene-unit work prefixes (2026-10-10)

Continue the actual first scene-unit4680B0 through NPC status/template and job/palette/cache/controller construction, stopping at its natural animation file request before loading. Separately execute all35 scene5 constructor prefixes with declared isolated records/cache inputs; inventory exact source-selected archives without claiming that the actual full loop, textures, constructor tails, placement or VM ran. Verify complete initialized bytes independently, preserve runtime/save/history and commit each completed stage locally.

## First scene-unit animation and constructor completion (2026-10-10)

Resume the actual first scene-unit animation request, load/bind its exact a1a archive and finish4680B0 through initial program, coordinates, cell accounting and defaults. Stop at natural453630 before scene-loop progress/next template. Independently verify metadata, every texture/palette/mask input and complete work/record/scratch/cell bytes; label separately declared palette-boundary calls, retain prior/runtime/save/history and commit stages locally. Other34 templates, placement and VM remain subsequent work.

## Second scene-unit input and cache policy (2026-10-10)

Continue the actual first NPC return through original progress and the second template record/work prefix, stopping before its mode0 animation load. Independently verify the complete next record/prefix/progress bytes and retained first NPC/current resources. Separately run original cache lookup for all35 ordered template keys with explicitly declared cache insertions, plus signed/duplicate/empty/full-table probes. This establishes lookup policy, not completed remaining constructors, cache binding or deployment. Commit native/source/acceptance stages locally.

## Second scene-unit complete constructor (2026-10-10)

Continue the actual second scene-unit51e variant0/mode0 request through read-only archive loading, native binding and complete special-role387 constructor. Independently derive resource/palette-mode and complete work/record/scratch/cell bytes, retain prior NPC/current/resources and runtime/save/history. Stop at natural453630 before ordinal2. Commit native/source/acceptance stages locally.

## Scene-unit batch and actual cache reuse (2026-10-11)

Continue the original school CPU through ordinals2–9: special-role393 mode0 and seven job383 variant1 units. Execute each complete constructor and actual native cache reuse, load only the two missing archives, and stop at453630 after ordinal9. Independently verify all record, prefix, binding, tail, progress and cache bytes. Retain prior resources/runtime/saves/history and commit native/source/acceptance stages locally. The remaining25 templates, deployment, VM and graphical battle remain subsequent work.

## Remaining scene constructors (2026-10-11)

Continue ordinals10–34 on the original CPU, including the24 inactive status11 records and one active role406. Execute missing resource loads and native cache reuse; stop at45363D after the final original loading-progress call, before the loop epilogue and subsequent deployment. Derive inactive action-skipping from original code, verify all complete bytes independently, preserve existing reports/runtime/saves and commit stages locally. Deployment, VM and graphical battle remain following work.

## Current-school deployment positions (2026-10-11)

Continue the actual35-constructor CPU through its natural epilogue/caller into468910 and complete49A480 school formation placement. Stop at468A49 before search-workspace allocation; independently verify original formation rotation, terrain/occupancy filtering, selected-unit records/work/cell changes and all retained bytes. Keep VM, later deployment initialization and graphical battle as explicit subsequent dependencies. Commit native/source/acceptance stages locally.

## Native deployment completion (2026-10-11)

Continue468A49 through both search-workspace constructors, current-category unit/display indexes, scratch clearing and category linked lists, stopping at natural468910 return4534A1. Resume trusted private actual CPU checkpoints only after pinned identity and complete immutable placement equality checks; publish checkpoint provenance separately from inherited upstream refusal evidence. Independently verify every owned buffer, wrapper, work and linked-list byte and retain runtime/save/history. Event VM, next467AA0 and graphical battle remain subsequent stages. Commit each completed stage locally.

## Scene initialization return and opening request (2026-10-11)

Continue actual4534A1 through native timer/owner binding and complete452FC0/4519C0 return. Execute original453F10 opening updates under an explicit bounded driver on that actual state, including native415040 increments and exact declared rectangle presentation, until phase5 emits script-work request170=1. Independently verify complete timer/task/global bytes and every presentation parameter; distinguish driver updates from a full world scheduler or executed event VM. Preserve runtime/save/history and commit native/source/acceptance stages locally.

## Opening request consumption and preflight entry (2026-10-11)

Continue actual opening state into original499DA0 under declared controller updates. Verify camera setup, request consumption and native180-tick waiting, interleave original phase5 waiting and stop at the natural4551C0 preflight call with selector0/sub1 before its first instruction. The170 request belongs to entry control rather than directly to the VM. Preserve source/VM/runtime/save/history and commit native/source/acceptance stages locally. Full world-loop scheduling, preflight VM execution, script binding and graphical battle remain following work.

## Actual script preflight and selected VM binding (2026-10-11)

Continue the natural pending4551C0(0,1) call after complete pinned parent replay. Execute original nested script lookup, preflight VM/register/condition/jump/END and cleanup, capture natural preflight return, then actual caller selection and selected script binding through controller return. Stop with controller7 and active selected VM before normal playback updates. Declare exact C-string/tick/debug/audio/clear primitives without changing existing globals or simulating world work. Independently verify full memory, source script spans and opcode trace; preserve runtime/save/history and commit native/source/acceptance locally.

## Normal opening script and native fade continuation (2026-10-12)

Continue the pinned actual selected0/1 VM from bank0/PC0 under explicitly declared original4CE8F0 and497AA0 calls. Execute startup variable/global/group settings, original work wait/release and sixty-count fade, native presentation-mode setup and thirty-count delay. Complete107 updates, then stop naturally at the first4C5EA0 board-on handler before its first instruction. Declare only exact overlay/layer/object/fade/resource presentation interfaces; do not replace world readiness or manufacture callbacks. Independently compare complete memory and every update/command/presentation digest, preserve runtime/save/history and commit native/source/acceptance locally. Full task/audio gating, board rendering, dialogue and waves remain following dependencies.

## First dialogue board and native readiness (2026-10-12)

Continue the natural pending first board-on call and its original VM caller. Execute the active layer's native update and native readiness predicate under declared bounded VM calls, stopping at the following text-active handler before its first instruction. Decode original board configuration and frame-piece inputs; declare exact terminal sprite/rectangle calls, retaining logical animation, readiness and object updates. Independently compare complete memory, every state and presentation digest; preserve runtime/save/history and commit native/source/acceptance locally. Text layout, font/GPU execution, full task/audio/world scheduling and waves remain subsequent work.

## Text activation, first font request and visible opening preview (2026-10-12)

Continue the natural text-active call, complete its original VM return and execute the first text lookup/split/object preparation to the natural CreateFontA entry before any font API instruction. Independently verify complete owned bytes and stack-derived first text/line/font arguments. Export the original selected opening's ten Big5 text entries and their opcode17 sequence independently for a read-only dialogue overlay in the existing Godot MAP05 preview. Preview navigation must not append commands, change school/battle state or save files, or clear the adventure gate. Keep original font/texture/layout/world/wave execution boundaries explicit and commit native/source/UI/acceptance stages locally.

## Host-backed font raster and text timing (2026-10-12)

Resume the natural first font call with real Windows GDI rather than a fake handle. Execute original text-copy, context binding, measurement, bitmap setup, shadow/foreground drawing and geometry stores to natural texture creation entry. Explicitly distinguish current host ANSI code page/font fallback and offscreen GDI from original GPU or live-game witnessing. Independently decode geometry and pixel conversion; execute original pixel conversion and text fade/readiness as declared isolated probes on real captured raster bytes and bounded input cases. Verify complete memory, strict call arguments, resource cleanup and unsupported inputs. Commit each completed stage locally, then run source/model/UI/spec acceptance and preserve runtime/save/history.

## Real32-bit Direct3D8 platform feasibility (2026-10-12)

Trace the original renderer factory/device initialization and texture allocation contract. Independently execute original signed-WORD power-of-two size selection and null-device boundary on declared isolated records. Build a bounded32-bit helper using the real installed Direct3D8 runtime to create a hidden windowed device and managedA1R5G5B5 texture, upload/read back independently verified original CPU pixels, and release all resources. Report real pointers, HRESULTs, actual format/dimensions/row pitch and host provenance without replacing the existing zero device or claiming natural original graphics/VM continuation. Commit source/platform/acceptance stages locally; preserve prior evidence/runtime/saves.

## Live real-device bridge and first text completion (2026-10-12)

Keep real32-bit Direct3D8 objects alive in an owned helper process across bounded calls. Declare the live host device as a platform binding in the existing renderer device slot; this is not original renderer startup or a fabricated pointer. Continue the real-GDI first-line frame through original texture creation, descriptor, lock, original pixel upload, unlock, GDI cleanup, line-count completion and VM return. Independently verify complete regions and pixel rows; retain GPU drawing/readiness/world/wave boundaries and commit bridge/native/source/acceptance stages locally.

## Natural next opening text (2026-10-12)

The selected script contains consecutive opcode17 entries at offsets684 and690. Continue the actual first-text VM return with its real texture still alive to the second text lookup/split/record preparation and natural font API entry. Observe the original first-record readiness predicate separately without changing its CPU/stack/state. Do not delay the VM until first-line fade completion or claim single-line timing is the selected script cadence. Independently compare complete bytes/stack/source arguments, preserve prior evidence/runtime/UI/saves, and commit native/source/acceptance stages locally. Multiple text textures, natural fade/readiness after those entries, world/waves and actual rendering remain subsequent dependencies.

## Natural second text completion (2026-10-13)

Extend real owned32-bit texture resources to bounded multiple concurrent objects in a separate helper while retaining the prior helper/evidence. Continue the actual second font call through real GDI, independent raster and lock mirrors, original texture upload/cleanup/record count and natural VM return. Execute the resulting original two-row update with exact declared terminal drawing, preserve complete first texture pixels and all non-owned memory, derive independent geometry/pixels/counters/stack effects, and commit bridge/native/source/acceptance stages locally. Actual GPU drawing/Present, later text/waits/world/waves and full dialogue remain subsequent work.

## Natural dialogue waits and confirmation (2026-10-13)

Decode actual dispatcher tables for selected opcode50/51, independent of misleading decompiler case labels. Continue the two completed real textures through natural VM-driven fade/cadence/readiness, then hold the confirmation gate without input. Execute original mouse/key query helpers on the captured zero event buffers; separately declare a bounded mouse-button pulse and continue through the real confirmation return to the next source command boundary. Independently compare every update's complete regions, actual texture retention, terminal draws, wait/arrow effects and resource cleanup. Commit source/native/source/confirmation/acceptance stages locally and preserve old evidence/runtime/UI/saves/REA. No live input capture, GPU/Present, portraits, world/waves or full dialogue is inferred.

## First character layer dependency (2026-10-13)

Continue the confirmed opcode30 entry by decoding its actual configuration index, layer, name and image resource references. Execute the original prefix to its first new name-font request with live prior textures; independently compare complete memory and natural stack. Preserve later name raster/image loading/animation as explicit subsequent work, and publish source/native/regression stages with local commits.

## Character name raster and live texture (2026-10-13)

Continue the actual character name font request through real host GDI and original geometry, then upload to a third owned real texture and execute name cleanup. Continue the actual source caller through bounded path construction to original image loader entry. Independently compare complete regions, stack, COM, pixels and cleanup; preserve later file/image decode, animation, third dialogue and world/GPU as subsequent dependencies. Commit source/raster/upload/comparison/acceptance separately.

## Original character image loading (2026-10-13)

Continue actual4CDE10 for pinned sc004.bin. Execute original file loader/container/header bodies using real owned Windows read-only file APIs, bounded declared working-directory/heap/CRT adapters, original texture vector construction and a fourth live real texture. Compare source DX header, full pixels, program/table/record states and resource ownership independently. Complete image-loader return before subsequent layer animation/presentation, preserve all earlier artifacts and commit source/file/upload/comparison/acceptance stages locally.

The next bounded continuation executes opcode30 return, layer5 delay/frame/background animation and both source readiness predicates with all four actual textures alive, then activates config8 and prepares text2 to its natural unexecuted font entry.

Continue the natural layer5 text2 font entry through actual host GDI, fifth real texture and original one-line fade/readiness, retaining all four previous textures and stopping before the next confirmation instruction.
