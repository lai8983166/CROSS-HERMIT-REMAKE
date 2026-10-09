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
