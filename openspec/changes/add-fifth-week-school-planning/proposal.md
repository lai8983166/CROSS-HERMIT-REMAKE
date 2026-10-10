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
