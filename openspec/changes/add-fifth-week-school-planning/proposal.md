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

Render the already verified opening character/text layers in the Godot map preview. Project all ten source pages with original actors/frame art/layout, bounded visual timing, keyboard/button navigation and unchanged school/save/gate state.

## Current-school field interaction (2026-10-14)

Continue toward the playable current-squad battle by first exposing a separately labelled, read-only MAP05 deployment/movement trial. Export source terrain/formation and original current-student idle/walk art; carry current student identities and verified limits. Teacher remains a class leader. This bounded interaction does not invent enemy activation, waves, victory or persistent settlement. Verify model and actual window controls and commit source/model/UI/acceptance stages locally.

## Extended overnight battle integration (2026-10-14)

The user authorizes multiple consecutive rounds. Correct the discovered original character-palette indirection before adding combat. Independently audit the original world/controller gates and current attack/defense derivation; compare bounded native probes with source rules. Export source initial active scene actors and directional art, then extend the isolated current-school trial with explicit attack/health and source-positioned opponents under declared remake scheduling. Keep original full world/VM/waves, authoritative victory and persistent rewards/gate clearing as unresolved until verified; never fabricate their completion. Verify graphical and save compatibility and commit each completed stage locally.

## Original world mode continuation (2026-10-14)

Continue the actual admitted world prefix through4678C0 and the first naturally nested499DA0 entry-controller update, stopping before493630. Independently decode mode request consumption and its UnitCtrl/map/task flags; execute separately declared mode probes on captured school memory with full restoration, never label these as original opening completion. Compare exact source-derived stores, stack and retained bytes, preserve the current playable trial/save/evidence and commit source/native/acceptance stages locally. Full world/action/AI/events remain subsequent dependencies.

## Original map/time world suffix (2026-10-14)

Continue the captured493630 world stack through the original clock gate and map update, stopping at49B180 before its first instruction. Decode complete source timer, double-buffer clearing and map-pointer/input stores, verify actual-school retained memory and separately declared timer/mouse probes with exact restoration. Preserve graphical trial/save evidence and commit source/native/acceptance stages locally; full world/action/AI/events remain later dependencies.

## Original selection/vision and unit-list suffix (2026-10-14)

Continue49B180 through the opening-specific visibility stamp and original display/category list builders, stopping before48CD90 command-queue processing. Independently decode source masks, activity/status/relation predicates, viewport inclusion and original sorting/tie behavior; compare full owned buffers and actual current/scene rows. Preserve trial/save/history and save verified private next-boundary checkpoints with pinned provenance for faster subsequent bounded audits. Commit source/native/acceptance stages locally; full world/action/AI/events/VM remain later work.

## Original paused command/input/unit suffix (2026-10-14)

Restore the pinned verified private48CD90 checkpoint, execute the original empty queue, no-command input/selection normalization, closed cursor reset and all250 work-slot tests through46B618. Independently project full owned memory, per-unit vision and cell bookkeeping; prove skipped action/animation/AI branches under actual opening gates. Preserve runtime/save/history and commit source/native/acceptance stages locally. Nonempty command consumption and enabled actions remain later dependencies.

## Original paused world tail (2026-10-14)

Continue the verified490FC0 CPU through the source post-unit cursor/menu/hover, ten idle effect slots, five inactive secondary slots and empty command-forwarding queue. Independently verify all owned bytes, natural inner stack and original46B470 return to its existing declared audit driver. Complete this first paused UnitCtrl update only; do not equate it with an enabled gameplay tick, full task frame or opening VM completion. Verify declared counter wrap probes with full restoration and commit source/native/acceptance locally.

## Original second update and first student action admission (2026-10-14)

Continue the verified first paused world return using a separately declared next46B470 invocation. Execute its original controller state4 branch in natural world order, consume request170, enable action34, set state5 and native180 delay, then original timer/map/list/empty input prefix and first occupied unit command/status dispatch to475D60 entry. Preserve task/event/AI/VM completion boundaries; do not skip the required enabled-unit updates during the180 interval. Verify whole owned bytes, source refusal rules, private next-boundary provenance and local source/native/acceptance commits.

## First enabled student initialization and animation (2026-10-15)

Continue the verified475D60 CPU through its source phase0 initialization: direction2, pose18, two source-backed attached animations, cell scratch and phase1. Verify main pose binding first, then original shared-pool allocations/links/immediate attached steps and handler/status return to primary40A100, then main/two-attached/five-idle animation updates to482A30. Decode program/table/sprite fields independently from source archives/EXE and compare full work/global pool plus retained memory. Pin verified continuations, preserve runtime/save/history and commit each source/binding/attachment/animation/acceptance stage locally. Further unit processing, enabled180 ticks, opening VM/AI and settlement remain unresolved.

## First student update return and regeneration (2026-10-15)

Continue the verified482A30 actual CPU through six empty effect scans, six empty damage-event scans, empty damage queue, full HP/MP regeneration/death guard, source MAP05 region statistics, vision and cell maintenance. Verify the original first46B760 return and next slot1 admission, stopping before its first instruction. Independently source-project full work/record/region/vision/occupancy and source class mask; execute finite declared regeneration thresholds/status/short-wrap/dead-HP probes with full restoration. Preserve runtime/save/history, pin next CPU and commit source/native/acceptance stages locally. Later units, nonempty effects/damage, full world/180 updates/VM/AI remain unresolved.

## Following friendly units and first deferred templates (2026-10-15)

Continue the verified next-slot1 CPU through all remaining current friendly mode25 initializers, original animations, empty-queue tails and map statistics, then through first inactive mode11 slots215/216 to unexecuted scene slot217. Derive per-job source archives/pose/attachment differences, validate whole work/record/pool/region/vision/retained memory and natural unit/loop calls. Preserve runtime/history/save and commit each source/native/deferred/acceptance stage locally. Complete second-world return remains subsequent work after the scene-specific handlers.

## First scene unit initialization and return (2026-10-15)

Continue pinnedscene217 job406/group6 mode28 CPU through original status initialization, opening-gated387–406 post-handler, terminal-frame animation, empty effect/damage/regen tail and source region/vision gates, then natural return before218. Derive source26E metadata/pose/terminal bit and actual faction relation policy. Verify whole owned/retained state, pin initialization/return checkpoints and commit source/initializer/complete-unit/acceptance locally. Other units, full world/180 updates/VM remain future work.

Extend this continuation through the remaining22 contiguous inactive mode11 slots218–239 using the already decoded early-return handler, verify each natural call/record gate and full state, and stop before active scene240. No template activation or full-world completion is inferred.

## Remaining scene units and first enabled world return (2026-10-15)

Continue pinned240 through all ten remaining scene mode2 units, independently verify four source archives/poses, opening phase gate, terminal/nonterminal animation, empty tails, region totals and faction vision, then stop before post-unit490FC0. Execute original closed-gate suffix/ten idle effects/secondary skip/empty forwarding and real46B662 return to the existing declared audit sentinel. Pin unit-loop/whole-function continuations; preserve runtime/history/save and commit source/unit-loop/return/acceptance locally. This closes the second declared46B470 body, not the outer game task,180 enabled updates or opening VM.

## Next enabled update and delayed animation clearing (2026-10-15)

Continue the pinned second46B470 return with an explicitly declared third invocation. Verify state5 delay180→179 and the complete original map/list/input prefix to first phase1 student, then its next animation/full unit return to unexecutedslot1. Independently derive ended-controller clearing; run isolated original40A100 on actual ended scene217/247/248 state with full CPU/stack/memory restoration, without claiming those probes advance the world. Preserve runtime/save/history and commit source/prefix/unit/acceptance locally. Remaining units, attached frame sound commands,180 complete updates and VM/AI remain future work.

## Complete third enabled world body (2026-10-15)

Continue verified third-worldslot1 through all remaining occupied units and250-slot loop, derive initialized friendly frame countdowns, phase1 inactive early exits and actual ended217/247/248 root clearing, then original enabled suffix and natural46B662 return to the existing audit sentinel. Verify source metadata/records/relations, all owned/retained bytes and natural calls/stack; pin unit-loop/return checkpoints and commit source/native/return/acceptance locally. Inspect the upcoming2063 source sound opcode and forwarding call without claiming audio execution. Full180 interval/VM/AI/outer task and attached-node lifecycle remain future work.

## Consecutive enabled updates4–6 and source sound opcode (2026-10-15)

Generalize initialized world projections for declared natural46B470 calls4–6 from the verified third return, preserving cleared roots, phase1 inactive templates, complete prefix/250-slot loop/suffix and180 countdown. Execute4/5 consecutively, then sixth2063 expiry through original opcode2 sound59,40B990 and captured uninitialized40D390 early exit, followed by the next source frame and complete world return. No backend audio stub or fabricated playback is accepted. Verify full state/calls/stack/retention, pin fifth/sixth returns and commit source/two-world/sound-world/acceptance locally. Opening VM/AI, full180 interval and attached-node release remain future work.

## Consecutive source frame changes7–15 (2026-10-15)

Continue verified sixth-return cases through every original declared world7–15, verifying383 source first/second frame expiry and2063 next regular frame. Decode bounded frame0 stepping and the upcoming383 repeat instruction, retaining complete owned/retained state, native calls and private checkpoint provenance. Commit source, worlds7–9, worlds10–15 and acceptance locally. Actual repeat execution, attached-node release, full180 interval/VM/AI and outer task remain later work.

## Consecutive animation lifecycle16–75 (2026-10-15)

Continue every declared original world16–75 from the verified fifteenth return in three batches16–42/43–65/66–75. Verify friendly and attached frame transitions, job5 terminal/next-update root clearing,383 source infinite repeat and actual2100+job child terminal/unlink/pool-free. Preserve complete original state/calls/retention and all history/runtime/save. Losslessly compress large hex buffers per world to bound report memory while retaining every owned byte. Commit source, each native batch and acceptance locally; full180/VM/AI/outer-task remain later work.

## Consecutive source child spawning76–118 (2026-10-15)

Continue every original declared world76–118 from verified75. Verify friendly visible frames through106, original opcode1 at107 reusing the first freed pool slot, class-specific bank3/program1 binding/immediate child step and source layer semantics, then subsequent updates through2063 terminal117 and non-head unlink/free118. Preserve all prior evidence/runtime/save, compact full-byte evidence and natural calls/CPU/retention. Commit source,76–106,107,108–118 and acceptance locally; main terminal/phase transition, full180/VM/AI/outer task remain future work.

## Main animation handoff119–126 (2026-10-15)

Continue every original declared world119–126 from verified118. Verify jobs3/4 terminal124, following phase1 voice request125, original captured CRT random state/LCG and guarded audio manager, recursive root cleanup of nonpersistent spawned nodes and phase2 counter threshold126. Job9 terminal128/129, later pending-mode commit/new pose,180 interval, VM/AI and outer task remain subsequent work. Preserve old evidence/runtime/save and commit source,119–124,125–126 and acceptance locally without push.

## Pending mode and idle-pose continuation127–181 (2026-10-15)

Continue every original declared world127–181 from verified126. Verify phase3 pending2/flag stores, next-update mode25→2 commit and native empty path reset, source pose1 binding and duration1 terminal/next clearing,383 repeat128, and job9 terminal128/voice129/recursive release/phase2/pending/new pose132/clear133. Then verify every enabled original world134–181 to delay1 before the next controller boundary. Preserve old evidence/runtime/save and commit source,127–128,129–133,134–181 and acceptance locally without push; full180 completion, controller handoff/VM/AI/outer task remain subsequent.

## Countdown zero and paused handoff continuation (2026-10-15)

Continue from the verified181 return through original declared worlds182 and183. Verify the last1→0 decrement while enabled, then the following zero-test/action0/state6 transition and complete paused250-slot bookkeeping/suffix. Continue the next declared world184 only through the actual state6 predicate to the unexecuted script-preflight entry4551C0, preserving the natural stack and captured script identity. Preserve history/runtime/save; commit source,182,183,184 boundary and acceptance locally without push. Script preflight body, selected playback, AI and outer task remain later dependencies.

## Continuous original preflight and task entry (2026-10-16)

Continue the verified184 pending4551C0 CPU through native five-command preflight, original no-op debug/music/audio guards, actual selected4549D0 binding and state7 controller return. Complete184 and the next declared185 paused world, verifying unchanged characters and original task status query. Independently derive the next original454CF0 task-script setup, declare one call after185 and complete native phase0→1 with a bounded read-only lstrlenA adapter on the already captured empty text buffer. Preserve historical/runtime/save evidence and commit source, preflight, binding,184,185, task-source, task-input boundary and acceptance separately locally. Full outer task frame, OS input sampling, playback/AI/rendering and settlement remain pending; no helper-stub or synthetic VM result is accepted.

## Native captured input reset and next task polls (2026-10-16)

Continue the pinned first-task return through a declared original425DE0 input reset, native phase1→2 task poll, another original reset and the following task prefix to its unexecuted normal playback4CE8F0 entry. Derive the original49E540 caller and IMM32 import identity from preserved descriptors. Declare a closed-IME response solely for the captured null context; do not sample live input or claim this is a complete OS/main/outer task frame. Preserve historical/runtime/save bytes, verify all three cases and commit each source/native/acceptance stage locally without push.

## First normal VM command and native presentation binding (2026-10-16)

Continue the pinned normal4CE8F0 entry on its original454D90 caller stack. Execute first opcode167, then native overlay dispatcher/stack object constructor and actual source resource query. Trace every argument through both dispatchers:51 is the layer and the actual resource index is0. Verify native binding of the captured group20 entry and stop before the original407AD0 draw body, without fabricated resources or replacement drawing helpers. Preserve history/runtime/save and commit source, command, constructor, resource-boundary and acceptance stages separately locally without push.

## Native draw gate, cleanup and first VM/task return (2026-10-16)
Continue the exact pending407AD0 checkpoint. The captured TASK+B28E render gate is0, so verify its original early return without claiming GPU output; execute original destructor chain and unwind SEH. Execute all51 inactive native VM maintenance calls and return through the retained454D90 caller. Then execute the existing task suffix with captured WORK+2434 inactive menu guard, fade and board to its declared return. Preserve all prior evidence/runtime/save and commit each bounded stage locally without push.

## Continuous normal opening branch and fade (2026-10-17)
Continue from the verified first-task return through explicitly declared input-reset/task invocations, using only inherited closed-null-IME and captured-empty-string adapters. Follow the actual opcode8 comparison to PC44, opcode5 variable reset,165/163 global bit/word writes, two113 slot flags and two136 pose commands including their extra wait-clear polls. Execute117 fade start, all remaining countdown updates and the following VM wait-clear poll to PC184 before opcode56. Verify every actual task/VM return, source state/calls/ABI and full owned/retained memory without changing live input, renderer gates, original saves or Godot; commit nine bounded stages locally without push.

## Normal display reset, text mode and timer continuation (2026-10-17)
Continue immutable vm-flow fade_finish task returns through explicitly declared original reset/task pairs. Execute56 setting presentation type2/state0, its actual wait1 query/clear,20 text-mode0,12 timer30 and all31 native timer polls. Continue the next declared pair only to the natural unexecuted27 handler4C5EA0 with original arguments/VM/task stack. Preserve complete intermediate state, native bodies, source ABI/returns and all retained memory; commit source, each bounded native phase and acceptance separately locally without push. No live input/GPU/outer-world/character body or dialogue completion is inferred.

## Original character command and first active presentation admission (2026-10-17)
Continue the immutable vm-panel character_entry CPU on its real VM/task stack. Execute the three typed operands and template4/layer7 setup, original text-layout/show helpers and full27 handler return, then the existing overlay/draw-gate cleanup and inactive layers0–6. Execute layer7's native interpolation and stop before first4CA600 graphics-list body. Verify complete source ABI/arguments/critical returns, all61 owned ranges and retained bytes with12 fresh checkpoints. No additional reset/task root, OS response, resource/queue stub, GPU or dialogue completion; commit source, four native phases and acceptance locally without push.

## Original graphics list and renderer-owner precondition (2026-10-17)
Continue immutable vm-character layer_entry on its real layer/VM/task stack. Execute4CA600's four frame pieces through complete4CBDB0 construction/binding/disabled draw/destruction and natural list return. Execute remaining native alpha/rectangle to unexecuted40E2A0, then its actual prefix only to the first read through captured null renderer owner at40E2D0. Verify four full128-byte packets, source calls/ABI/returns,61 owned ranges and outside bytes with9 fresh checkpoints. Bind original owner initializer40D970 and caller413500 as the next prerequisite. No owner/gate patch, invalid target read, clipping result, queue/debug/GPU or VM/task/dialogue completion; commit source, three native phases and acceptance locally without push.

## Isolated renderer prerequisites (2026-10-17)
Derive original manager construction, owner/device binding, queue allocation and per-frame reset ordering. Execute isolated native prerequisite experiments with explicit owner/device/dimensions/gate inputs and a bounded debug-CRT allocation response. Verify full manager/queue bytes, rectangle linked-list insertion, reset and source overflow/rejection branches. These experiments do not repair or advance the retained vm-graphics owner_read CPU; complete D3D initialization and real outer scheduling remain prerequisites. Preserve history/runtime/saves and commit each completed stage locally without push.

## Live original device startup prefix (2026-10-17)
Execute original413450 windowed startup from explicitly declared scratch owner state, through original factory/device setup, capabilities, backbuffer description, format selection and viewport to unexecuted415F50 font initialization. Supply only live owned x86 Direct3D8 interface responses through a separate hidden-window process, retaining original import target and original helper bodies. Validate complete owner bytes/CPU/calls and release all external resources; do not patch pending VM or claim rendering/Present/full startup completion.

## Full owner construction before font startup (2026-10-17)
Resolve the font cleanup prerequisite by executing original412E30 and all native subconstructors on declared dirty owner bytes and inherited pinned source globals. Reuse live device startup only after real construction, then execute original415F50/416140/CreateFontA/4162C0/52AFE6/GetObjectA to unexecuted52AE11. Real32-bit GetDC/QPC/QPF/GDI responses remain owned in a new small helper; no manual old-font zeroing, owner/gate repair, static font-body stub or retained VM advancement. Preserve and locally commit each stage.

## Static font allocation and cache prerequisite (2026-10-18)
Continue the independent52AE11 CPU through original allocation wrapper/font constructor and captured cache lookup. Preserve inherited80A398 and stop before its absent heap node is read. Separately declare an empty-cache experiment, construct the original176-byte cache and use real owned x86 AddRef/caps/creation-parameter responses to the unexecuted52755E texture-requirements body. No imported fake old cache, silent global repair, texture success or retained VM progress is accepted. Commit source, bridge, inherited boundary, empty-cache prefix and acceptance locally.

## Native cache texture requirements and creation (2026-10-18)
Continue the independently declared empty-cache CPU through original52755E/527234/format selection, real DebugSetMute and owned device/factory queries, then original5275D7/CreateTexture/GetSurfaceLevel to unexecuted52AE80 sprite factory. Verify full heap/image/owner/stack/live identities and balanced texture/surface/factory/device references. Preserve inherited-cache missing-memory boundary and retained VM without claiming full font startup, drawing or outer scheduling. Commit each source/bridge/native/acceptance stage locally.

## Sprite and complete first static font return (2026-10-18)
Continue the verified independent empty-cache CPU from52AE80 through original32-byte sprite construction and real device capability/creation queries, then real cache GDI DC/bitmap/setup/CreateFontIndirectA and original factory returns to416021 after owner+B270 stores the font object. Preserve full objects/padding/guards/image/CPU/ABI and release every owned GDI/COM reference; no state-block/drawing/full415F50/retained VM completion is inferred. Commit source, platform, sprite, font-return and acceptance locally.

## Additional font-slot construction and atlas admission (2026-10-18)
Continue the independent empty-cache first-font CPU at416021 through original1656-byte allocation/401000/native CRT face copy and owner+1090 binding. Then execute4010D0 dimension selection and a real owned device caps query to unexecuted40120C CreateTexture. Preserve both prior font/cache objects and source/owner/stack/heap guards. This bounded batch does not complete either additional font, upload glyphs, create state blocks, return415F50 or advance the retained VM. Commit source, constructor, atlas admission and acceptance separately locally.

## Additional font atlas texture and GDI preparation (2026-10-18)
Continue the independent declared empty-cache CPU from40120C through real owned additional atlas texture creation, native bitmap-header initialization and real bounded GDI DC/DIB/map mode/MulDiv/font/selection/color/alignment preparation. Stop before the first glyph measurement import at401491; no glyph rasterization, pixel upload, state blocks, full extra font/415F50 or retained VM completion. Fork immutable helpers, verify full objects/image/stack/lifetimes and commit source/device/texture/GDI/native/acceptance separately locally.

## Original glyph rasterization and atlas upload (2026-10-19)
Continue the independent empty-cache CPU from401491 through all95 original character measurements/draws and native UV stores, then real atlas LockRect, original65536-pixel conversion and real UnlockRect with exact external-memory transfer/readback. Fork immutable owned GDI/device helpers, explicitly distinguish inspection-only GdiFlush/DIB snapshots/readback from native calls, and stop4017B6 before original cleanup. No state blocks, full4010D0/415F50, second font or retained VM completion. Commit source/GDI/raster/device/upload/acceptance separately locally.

## Original atlas cleanup and first additional font device state (2026-10-19)
Continue the independent empty-cache CPU from4017B6 through original bitmap/DC/font deletion and4010D0 return, then actual401810 vertex-buffer creation and both complete state-block loops to416101. Use fresh immutable owned GDI/device helper versions, distinguish deferred bitmap deletion/inspection/fallback cleanup, validate full native objects/ABI/CPU/lifetimes and preserve all historical/runtime/save/private VM bytes. No second extra font, complete415F50, retained VM or drawing/Present completion. Commit source/GDI/native-cleanup/device/native-VB/native-states/acceptance separately locally.

## Second additional font loop, construction and atlas admission (2026-10-19)

Continue the independent empty-cache CPU at416101 through the original success test and loop increment, then a separate guarded1656-byte allocation,401000 native ANSI face copy and owner+1094 binding. Execute second4010D0 size/scale/caps preparation to unexecuted40120C. Keep the completed first additional font, static font/cache/sprite, full image/owner/stack and pixel snapshots intact. Derive both-loop exit/415F50 return statically without claiming it executes. Reuse unchanged owned x86 helpers for the existing caps operation; no second texture/GDI/upload/state blocks/full startup or retained VM advancement. Commit source, loop, construction, admission and acceptance separately locally without push.

## Second atlas texture and GDI preparation (2026-10-19)
Continue the independent original second-slot CPU at40120C using fresh immutable x86 helpers. Keep first atlas/VB/two tokens alive while creating a distinct second256-square/format26/pool1 texture. Execute native bitmap-header stores and second GDI setup with size8/flags0/rawANSI face to unexecuted401491. Verify full objects/memory/CPU/ABI/lifetimes, preserve historical/runtime/save/private VM bytes, and commit source/platform/native/acceptance separately locally without push. Second glyphs/upload/VB/blocks/full415F50 return and retained VM remain pending.

## Second glyph generation and pixel upload (2026-10-19)
Continue the independent original second font at401491. Explicitly retire only the proven-deleted first DIB shadow after byte verification, preserving its immutable snapshot and keeping the first texture shadow/resources. Fork immutable owned x86 GDI/device helpers for second95 measurement/draw pairs and second LockRect/native65536-pixel conversion/UnlockRect/readback; verify dynamic metrics/UV/full memory/ABI/CPU/access order. Stop4017B6 before original second cleanup/VB/state blocks/full415F50 return. Preserve historical/runtime/save/private VM bytes and commit source/platform/retirement/native/acceptance separately locally without push.

## Second font cleanup, device state and full font initializer return (2026-10-19)
Continue the independent second4017B6 CPU through actual original bitmap/DC/font deletion,4010D0 return, second8400-byte VB and two complete state blocks. Execute the original loop index1→2, success result0, SEH restore and415F50 ret to unexecuted4134E3. Use new immutable owned helpers, preserve both fonts/resources/full objects/pixel snapshots/retired evidence and historical/runtime/save/private VM bytes. Record all four boundaries on one continuous trajectory within each of two fresh helper lifetimes, avoiding independent replays for each stage report; verify and commit source/platform/each native boundary/acceptance separately locally without push. Original413450 suffix/manager/queues/upstream and retained VM remain later work.

## Original startup caller manager, queues and gamma admission (2026-10-19)
Continue the independent empty-cache CPU from the original415F50 return at4134E3, through its actual success branch,40D970 owner/device binding and40DAB0 queue initialization. Supply only two explicitly declared debug-CRT allocations, execute original full zeroing, then generate all768 gamma entries and stop before original416CFA device call. Preserve complete prefix/resources/owner/image/stack/guards and historical/runtime/save/private VM evidence. Record the three boundaries within each same live trajectory; commit source, each native boundary and acceptance locally without push. Gamma device execution, full413450 return, upstream integration and retained VM remain pending.

## Original gamma invocation and complete startup return (2026-10-19)
Continue the independent original416CFA CPU through actual owned x86 void SetGammaRamp and416CC0 ret4, then413450 success0/epilogue/ret20 to the declared root return. Fork an immutable device helper, expose the actual gamma method only after the verified prior boundary, capture undefined EAX bits without inventing HRESULT, and inspect/restore prior device and desktop gamma during helper cleanup. Verify the entire native prefix, new source ABI/CPU/full memory and same helper lifetimes. Commit source, platform, native gamma return, complete startup return and acceptance locally without push. Real upstream cache/outer scheduling/retained VM and GPU drawing remain pending.
