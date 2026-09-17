## Purpose

把数值层与地图层串成可运行的实时战斗循环：单位按状态机行动、普攻按原作公式结算、ENGAGE 计时强制撤退、胜负可判定——整体可离屏确定性回放，作为后续 AI/技能/寻路的宿主。

## Requirements

### Requirement: 战斗单位状态机
BattleUnit 持有格坐标、阵营、HP/MP 现值、ENGAGE 剩余秒与状态（idle/move/attack/dead/withdrawn）。状态迁移唯一由战斗控制器驱动；dead/withdrawn 为终态。ENGAGE 剩余以秒计，随战斗时间递减。

#### Scenario: 状态初始化
- **WHEN** 依 battle_setup.json 构造单位
- **THEN** HP/MP 上限来自 SimDerive 派生，ENGAGE 初始 = SimEngage 表值，状态 = idle

#### Scenario: ENGAGE 耗尽撤退
- **WHEN** 单位 ENGAGE 剩余降至 0 且未死亡
- **THEN** 状态迁至 withdrawn，不再参与战斗与目标选择

### Requirement: 战斗循环 tick
Battle 每 tick（固定逻辑步长，速度档只改逻辑频率不改结果）：存活单位选最近敌方 → 射程外**沿 BFS 最短路绕障行军**（每 N tick 一格，可行走规则与占格见 pathfinding 能力；被占/不可达则原地等待）→ 射程 1 内发起普攻 → 用 BattleMath.physical 与攻击表条目结算（MISS/伤害如实生效）→ HP≤0 阵亡。一方全灭（含撤退）即结束，产出胜负阵营与 tick 数。

#### Scenario: 普攻结算走原作公式
- **WHEN** 一次攻击发生
- **THEN** 伤害/MISS 由 BattleMath.physical（含攻击表条目的威力/命中与双方派生防御值）计算，HP 相应扣减

#### Scenario: 绕障行军
- **WHEN** 单位与目标之间有阻挡格
- **THEN** 移动路径避开阻挡格仍逐步接近目标；全程不与阻挡格或其他存活单位重叠

#### Scenario: 胜负判定
- **WHEN** 一方全部 dead 或 withdrawn
- **THEN** 战斗结束，胜方为另一方（双方同时清空为平局）

### Requirement: 整场确定性
战斗的全部随机性来自注入的种子 RNG；同种子 + 同 setup 连续运行两场，逐事件的日志序列（移动/攻击/伤害/死亡/撤退/胜负）完全一致。

#### Scenario: 同种子回放一致
- **WHEN** headless 下以 seed=42 运行同一场战斗两次并比对事件日志
- **THEN** 两次日志逐条相同，胜负与 tick 数相同

### Requirement: 布阵数据驱动
参战单位（属性/职业/等级/阵营/初始格位）全部来自 `data/battle_setup.json`；改 JSON 即改阵容，不改代码。

#### Scenario: 无代码改阵容
- **WHEN** 修改 battle_setup.json 中某单位职业后重跑
- **THEN** 该单位 HP 上限与攻击条目随职业表变化
