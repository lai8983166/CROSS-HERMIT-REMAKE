# Design

## Context

现有 Godot 重制已实现九月第 4 周的单次课程规划、结算、确认与剧情推进（见 `add-school-course-planning`, `add-school-course-settlement`, `add-school-story-week-continuation`）。这些是**独立示例**，验证了单周的原版规则，但未实现连续循环。

M2 要求从 10 月推进到 3 月共 30 个日历周位，可操作周按原版包含排课、授课/冒险、结算、转职判定、剧情推进。现有代码中：
- `prototype/sim/school_course_planning.gd`: 课程安排逻辑
- `prototype/sim/school_course_settlement.gd`: 单次授课结算
- `prototype/sim/school_course_confirmation.gd`: 确认阶段（职业进度、关系、MVP）
- `prototype/sim/week_settlement_replay.gd`: 周推进逻辑（仅九月第 4→5 周）
- `prototype/data/job_table.json`: 职业表（30 个职业，含转职条件）

约束：
- 行为对等验收：同存档同操作下，数值、转职结果、关系与原版一致
- 证据体积：每个 change 新增证据 ≤256 MiB
- 不改原存档、既有 Godot 代码所有权

## Goals / Non-Goals

**Goals:**
- 实现 10 月至 3 月 30 个日历周位的循环推进逻辑
- 每周结算时刷新转职资格（基于职业熟练度、等级、任务完成）
- 多周累积成长、关系、职业进度，与原版对等
- 周进度持久化（保存/读取）
- 提供可操作的学年循环试玩场景

**Non-Goals:**
- 不实现 4 月及之后的月份（属于 M2 之后）
- 不实现完整剧情系统（M4）
- 不实现所有 45 张战斗地图（M3）
- 不改变现有九月试玩的验收标准

## Decisions

### 0. 先从九月第 5 周存档跨入十月，核对返校与读档。
1. 周循环状态机
使用显式状态机管理周推进：`planning → execution → settlement → story → next_week`。每个状态对应一个可验证的检查点，避免跳步或重复结算。

**Why:** 现有 `week_settlement_replay.gd` 只验证单次推进，状态机让连续循环可测试、可回滚。

**Alternatives considered:**
- 隐式推进（每个模块自行触发下一步）：难以验证中间状态，调试困难。
- 事件驱动：增加复杂度，当前规模不需要。

### 2. 转职资格判定模块
新增 `prototype/sim/school_job_eligibility.gd`，读取 `job_table.json` 中的转职条件（职业熟练度阈值、等级要求），在每周结算后计算每个学生的可转职列表。

**Why:** 职业表已存在，转职判定是 M2 明确要求但当前缺失的功能。

**Data source:** `job_table.json` 含 30 个职业的系数、AI、技能，但转职条件字段（如 `group`, `series_b`）语义需逆向验证。若黑盒观察不足，创建针对性的逆向 change（遵循 roadmap 规则）。

### 3. 多周累积验收
每周结算后生成快照（学生属性、技能、关系、职业进度），与原版对照文件对比。对照文件来源：
- 单周：复用现有 `school_course_settlement_evidence_v1.json`
- 多周：新建 `school_year_loop_evidence_oct_nov.json`，记录 10 月第 1 周至 11 月第 1 周的原版执行结果

**Why:** 单周对等不保证多周对等（累积误差）。分阶段验收降低调试成本。

### 4. 持久化格式
扩展现有 `school_playground_legacy_v*.json` 格式，增加字段：
- `current_week`: `{year, month, week}`
- `job_eligibility`: 每个学生的可转职列表
- `accumulated_mvp`: 累积 MVP 计数

**Why:** 复用现有存档迁移机制（version1→version2），避免破坏九月试玩的存档。

### 5. 实现顺序
0. 先从九月第 5 周存档跨入十月，核对返校与读档。
1. 周循环状态机（无转职，复用现有结算）
2. 转职资格判定模块
3. 多周累积验收（10 月→11 月）
4. 持久化
5. 完整 30 个日历周位试玩场景

**Why:** 状态机是基础，转职是新功能，验收锁定行为，持久化保障可用性，场景是交付。

## Risks / Trade-offs

**[Risk]** 转职条件的原版规则未完全验证
→ **Mitigation:** 若 `job_table.json` 中的字段语义不明，先用黑盒测试（原版存档 + 已知转职案例）推断规则；若仍无法确定，创建针对性逆向 change，范围限定在转职判定函数。

**[Risk]** 多周累积误差（浮点精度、RNG 分支）
→ **Mitigation:** 每周结算后立即对比快照，误差出现时二分定位到具体周；RNG 使用固定种子回归测试。

**[Risk]** 证据体积超限（30 个日历周位 × 多案例）
→ **Mitigation:** 对照文件只记录关键检查点（10 月第 1 周、11 月第 1 周、3 月第 5 周），中间周只在发现问题时补充；完整原版执行日志保持本地，Git 只收快照与 SHA。

每个周位依据原版日期分派和事件结果判定是否开放学校操作。影响周推进或学生状态的事件纳入该段验收。

## Open Questions

1. **10 月至 3 月是否有月度特殊事件？** 需黑盒观察或查阅现有文档确认。
2. **转职执行时机：** 是否在周结算时自动转职，还是玩家手动触发？需参考原版 UI 流程。
3. **3 月第 5 周之后：** 是否直接结束学年，还是触发特殊剧情？属于 M2 边界确认。
