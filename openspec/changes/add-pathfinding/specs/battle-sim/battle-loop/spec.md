## MODIFIED Requirements

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
