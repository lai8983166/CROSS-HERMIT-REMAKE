# Design

## Context

见 proposal.md。已有第四周会话不可变的结果是迁移存档的重放基础；第五周出口保存在单独 continuation 字段。旧职务室和学校前缀审计有可复用的 API 边界，但其上游日期与成员不同。

## Goals / Non-Goals

Goals: 扩展实际 4/5 同一 CPU 的 state8→CH002→state9→学校数据前缀；保留旧会话作为成长回顾，创建独立第五周规划会话，复用已经验证的调动、解锁与查看操作；核对原版4A7D30就绪与4A6A10参战准备，提供当前队伍的出发准备页；继续核对学校提交和state10场次交接，并提供当前班级的纯交接投影。

Non-Goals: 不模拟原版完整任务调度器、音视频或所有职务室菜单；不执行第二次成长、冒险战斗或第五周后续剧情。准备/交接数据与已实际执行的战斗分开，必修gate保持有效。

## Decisions

- 将现有三个边界 hook 的阶段处理提取为无继承副作用的 helper，沿现有第五周 CPU 调用；不多重继承两个不同上游初始化器。
- 先记录 native before/after 与有限写范围，再用 source rules 对当前成员计算学校数据。fixture 仅用于测试，不作为运行时目标快照。保留动态成长、关系、班级；原版前缀是否重置字段由实际证据决定。
- 第四周 session 保持不变，增加 fifth_session 与 workroom/school continuation；界面选择 active planning session。旧成长回顾继续从第四周 session 读取。
- 新存档版本增加规则指纹。迁移逐版本验证原有 state hash；v3 迁移使用捕获于模型修改前的两个真实 fixture（剧情中、出口）。保留精确 CRLF/LF alias。
- 职务室使用独立 source background/catalog；不生成仿制游戏美术。返回、保存、战斗预览沿用当前事务机制。

- 出发准备由当前第五周school snapshot纯计算生成，读取独立来源规则并验证；不把native fixture复制到运行时，不改角色/日历/gate，不发奖励。准备页为当前班级的可重复查看投影，不新增持久命令或改变version4存档指纹；修改班级后重算。
- 原版同一CPU前缀继续执行4A7D30与4A6A10，保留就绪条件和defined rating/round字段，覆盖原班、换班、成员待命与教师孤班。原准备阶段未执行战斗状态10。新增阶段继续执行实际学校提交、恢复已捕获的group协程、消费pending10和场次准备；菜单确认输入、调度器、配置资源和战术单位派生仍逐项声明边界。

## Risks / Trade-offs

- 原版学校前缀处理多个共享缓冲区 → 在独立 CPU 中限定写范围，比较所有当前角色与学校字段，拒绝意外 growth/date/MVP 写入。
- 旧存档 hash 随新增 state 字段改变 → 保存原有 v3 state 构建路径，只给 v4 添加字段。
- 新一周课程可能更多 → 必修冒险完成前只查看实际当前教师可用课程；素材名称缺失时采用描述性名称，声明命名来源。
- 原版菜单正文未完整执行 → 将学校数据准备与原版菜单可操作性分开标记，图形规划由重制项目提供。

## Migration Plan

捕获 v3 fixture；验证并提交 source audit；实现原子续接和 v4 重放；接图形职务室与第五周规划；完成兼容、窗口与视觉验收。新功能仅在用户主动进入职务室/学校时执行。可回退本轮 commits，既有 v1/v2/v3 fixture 与源规则均保留。

## 2026-10-09 departure handoff extension

- Capture the source group coroutine register/stack checkpoint at its existing menu boundary; after native readiness, execute 4A1920 with explicit confirmed-menu input, resume that actual coroutine with return code8, then let its own 4A6A10/request10 execute. Never synthesize request10 or round-table outputs.
- Consume the actual pending10 with the original dispatcher/constructor and execute 4B8FF0 using its source-prepared table. Configuration scalar loading, roster/counts and request16 are native. Resource loading4DAB10 and unit derivation4B9340 remain explicit unresolved boundaries; combat_units_ready stays false.
- Fork isolated branches from the same captured fifth-school checkpoint for initial, waiting and fifth-class squads; invalid readiness executes no commit. Record adventure ledger before/after independently from school/role snapshots, enforce finite writes and date/role/MVP retention.
- Export source table inputs separately from test fixtures. Implement a pure handoff projection taking current school plus its owned adventure ledger and validating source rules. It does not add saved commands, consume the player plan, change v4 fingerprints or expose an executable battle action.

## Native combat record extension

The prior 4DAB10 resource boundary name is incorrect: its original body only clears 0x8093F8..0x809692. Preserve old reports and supplement the corrected classification. Continue source4B8FF0 through that reset and original4B9340/4B93C0/4DB340/4DD510, including native CRT floating-to-integer conversion, with writes limited to declared current-student record destinations, stack and the exact work reset. Retain persistent roles/calendar/MVP and refuse unexpected item handlers. Pending16 remains unconsumed; resource loading and tactical world construction are separate.

Export source job records, equipped-skill table inputs and engagement schedule independently of fixtures. Add a pure current-role input and native-equivalent HP/MP/recovery/ENGAGE projection for the verified no-item subset; use actual carried-forward job/attributes/level/equipped skills, never output fixtures or demo defaults. It is a partial runtime projection, not the full0xB0 combat record nor a live battle. Verify actual squads plus declared isolated attribute/level/skill counterfactuals, malformed inputs and unchanged v4 state.

## Tactical startup boundary and visible current limits

Native dispatcher16 and outer451170 execute with bounded allocated task/script-work buffers. Graphics and UnitCtrl subconstructors, font API, scheduler and C++ vector construction are named external boundaries; no fabricated map or enemy object. Execute source startup452040/452130 and stop before resource loader4500B0. Source451BF0/451D10 start-resource selection is a separately labelled probe of the same current scene, not a claim that the common-resource loader completed. Resolve relative filenames against existing original files read-only, preserving exact hashes. Historical combat reports remain unchanged; the actual current skills go through4DCF00 (+52), while4DD510 consumes item slots (+62), correcting the earlier design wording.

Graphical departure cards read the current pure combat-limits API and show student HP/MP only. Teachers remain class leaders; missing/unsupported limits show an unavailable status rather than demo defaults. No new saved command, fingerprint, battle action or gate/reward mutation. Verify dynamic waiting/reordering/restored saves and rendered card/detail layout.

## Native resource buffers and scene script

Subclass the frozen startup audit without modifying historical evidence. Execute4500B0/42AE20/42AC50 and texture-table/container/header bodies against read-only original bytes. Bind declared file APIs only after actual ready handoff; validate arguments, exact lengths, closed handles and finite writes. Declare an initially empty isolated graphics texture table because previous graphics constructors were boundaries. Execute source texture entry constructors using a bounded C++ iterator primitive; record BMP/DX headers and no-texture markers, while GPU creation/upload and sound remain explicit boundaries. Continue natural451670 through common, TactStart, dialogue texture and current-scene script loading; stop at4519C0 before phase update. Export byte-derived inputs separately from native output fixtures, preserving all v4 save rules. UnitCtrl/map/enemy/event initialization remains pending.

## UnitCtrl logical construction and first scene phase

Extend the resource audit without altering frozen evidence. Execute4653D0 and its logical child constructors, list bodies and generic65x65 appearance-grid function. Expose existing Unicorn hook handles for a bounded batch of the expensive original grid code: verify its static direct control-flow graph, suspend outside the instruction callback, retain finite forbidden-write hooks, intercept only declared CRT/heap primitives and record actual final bytes. Never replace the grid with another campaign snapshot or a Python grid output. All other functions retain instruction/write guards. Native vector constructors run outside emulation hooks with preserved outer stack/context.

Continue naturally from4519C0 phase0 through451F50/4538D0 to phase2, with explicit deterministic CRT random and audio boundaries. Execute source map path selection43A640, native file loading and logical map scratch creation, then stop at43A920 next graphics resource request. Record map ownership, initialized scratch buffers, current records and source paths without claiming VM/enemy/event initialization. Independently decode the selected original map and its texture container at source offset0x404; validate pixel/entry/header provenance instead of applying the older atlas-start heuristic. No v4 save or runtime command changes.

## Scene resources and current-map presentation

Subclass the logical map audit and continue on its paused original stack. Preserve old reports. Bind only exact read-only scene MAP/BMP/VPT paths, bounded separate resource allocations, the declared empty texture slot92, GPU creation/upload/lock and renderer boundaries. Execute original map texture and minimap header bodies, original fog-buffer calculation and VPT section rebasing, retaining persistent/current records. Stop at467EB0 before unit-art reset; do not fake font/effect/unit objects to reach a later VM. Run the same three ready and two refusal school branches.

Independently parse source BMP pixels and VPT section offsets/relocation arrays; compare initialized pointers/buffers against native outputs. Export the exact original map atlas into runtime assets with a source manifest, preserving v4 fingerprints. Add a full-screen pan/zoom map viewer reachable from a validated ready current scene5 departure projection. Opening, dragging, zooming, fitting and closing cannot append commands, write saves, clear gates or construct battle units. Verify input, bounds, refusal, pixel provenance and actual rendered captures.

## Unit reset and effect metadata continuation (2026-10-10)

Subclass the immutable scene-resource audit and resume its actual stack at467EB0. Execute source reset/relation bodies and text-cache loops, recording every table pointer, original string byte sequence, font handle and destination. Execute408E30 color initialization;405160 platform text rendering remains a labelled success-return boundary with no fabricated pixels, GPU object or dimensions. Keep prior unresolved graphics constructors explicit.

Execute466000/464C60/409900/41EAD0 effect controller initialization, source binding464D70, source path/load464DE0/409B70 and metadata copy/pointer selection. Use a separate finite pool for the 15MB original effect file and metadata; enforce ownership, exact file arguments, closed handles and protected current/persistent records. Stop before41EBF0 effect texture binding. Independently export effect container offsets and metadata prefix, plus original text tables, separate from fixed native fixtures; do not advance current/enemy units or use these outputs as a playable-world snapshot. Re-run relevant native/source/model/spec validation and verify save/historical bytes, then commit each completed stage locally.

## Natural effect binding continuation (2026-10-10)

Subclass the frozen unit-assets audit. Resume41EBF0, execute41EC40/41F0E0 and all1959 texture record/header bodies with finite allocation and native vector constructors outside hooks. Source4660FC already selects slot100 (previously described as a kind field); verify its declared isolated empty prior bytes. This source selection bypasses41EFD0 and its unconditional debug dialog. Reject every assertion rather than supplying an unused dialog-ignore input. GPU creation/upload remains a primitive and no pixel/GPU objects are fabricated.

Continue native source release of the original Efct buffer, effect work construction, first animation selection and descriptor/duration initialization. Execute the43A510 request prefix and stop at4500B0 before mapcom loading. Guard protected roles/current records and retained metadata; export every texture header and work fields separately from input bytes/programs, with no current/enemy or scene VM claim. Use original-source texture parsing with an independently bounded1959-entry container rather than weakening the historical580-entry resource parser. Preserve all old evidence and runtime saves/UI.

## Map common and first current-record continuation (2026-10-10)

Subclass the frozen effect audit and resume4500B0 on its natural stack. Execute43A510 completely using the existing read-only Win32/CRT boundaries and a separate finite retained mapcom buffer. Verify four top-level and33 nested pointers against independent original offsets; retain opaque payloads without assigning unproven semantics. Follow4531A8 preparation branches with source header inputs: restrict current-record writes to state+0F and recovery+24 and compare every resulting byte to an independently decoded policy. Persistent roles, MVP/date and all retained effect objects remain unchanged.

Execute the first source4533E0/453467 copy primitive with exact176-byte source/destination/index, then stop at4680B0 entry without supplying a success-return constructor. Record the naturally selected record, order inputs and copied bytes. Refusal school branches allocate/load/copy nothing. Full work construction, enemy derivation, VM and placement remain outside this stage. Verify source provenance, malformed data and guard refusals, existing Godot model/specs/save/UI evidence and commit each completed stage locally without pushing.

## First work constructor prefix (2026-10-10)

Subclass the frozen map common audit and resume its natural4680B0 stack. Execute the work/status helpers and original467020 job/palette logic, finite512-entry cache search, first free-slot allocation and464C60 controller construction/binding. Heap/CRT/debug-log operations are explicit primitives with exact caller/argument ownership. Stop at4500B0 called by464EB0 before loading the source-selected unit file; do not return success for the incomplete4680B0 constructor.

Guard only the selected0x520 work, its176-byte copied record, declared animation-cache slots/counter, one finite84-byte controller, stack and SEH. Compare persistent/current global records and all retained map/effect allocations before/after. Record complete raw work/record/controller bytes, source table pointers/values, prior cache/counter and natural file arguments. Independent EXE rules derive expected bytes and reject unsupported categories/IDs instead of inventing enemy/status/graphics state. Validate three ready/two refusal cases, malformed/guard refusal and old source/model/spec/save/UI bytes; commit each completed stage locally without pushing.
