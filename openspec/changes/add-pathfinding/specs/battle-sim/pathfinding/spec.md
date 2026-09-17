## Purpose

数据驱动的可行走规则与 BFS 最短路：给定地图三层值、阻挡规则与动态占格，输出绕障路径——为战斗移动与未来 AI 提供统一的寻路原语。

## ADDED Requirements

### Requirement: 可行走规则数据驱动
阻挡规则由 `data/walk_rules.json` 定义：三层的"阻挡值集合"（`blocked_terrain`/`blocked_variant` 为数组，`blocked_objects` 支持 `"nonzero"` 或数组）。默认规则 = object 层非零阻挡。SimMapData 暴露 `is_walkable(x, y, rules)`；改 JSON 不改代码即可改变通行语义。

#### Scenario: 默认规则
- **WHEN** 以默认规则查询 object≠0 的格子
- **THEN** 不可行走；object=0 且其余层不在阻挡表的格子可行走

#### Scenario: 自定义规则
- **WHEN** 把某 terrain 值加入 blocked_terrain 后重新加载
- **THEN** 该 terrain 的格子变为不可行走，无需改代码

### Requirement: BFS 最短路
`find_path(from, to)` 返回从 from 到 to 的格坐标序列（不含 from，含 to），满足四连通、每格可行走；四连通等距下 BFS 即最短。路径确定性：同输入恒同输出（邻居扩展顺序固定）。

#### Scenario: 直线可达
- **WHEN** 无障碍、同行两格寻路
- **THEN** 返回逐步直达路径，长度 = 距离

#### Scenario: 绕 U 形障碍
- **WHEN** 起终点之间被凹形阻挡墙隔开
- **THEN** 返回绕过开口的合法路径，不含任何阻挡格

#### Scenario: 不可达
- **WHEN** 目标被完全围死
- **THEN** 返回空数组（调用方原地等待）

### Requirement: 动态占格
寻路可接收"额外临时阻挡格"集合（存活单位所占格）；目标格本身被占时路径终点退化为相邻可达格。战斗移动消费该接口实现单位不重叠。

#### Scenario: 占格绕行
- **WHEN** 最短路被一个存活单位占据
- **THEN** 路径绕开该格仍可达目标

#### Scenario: 单位不重叠
- **WHEN** 战斗中两单位路径相交
- **THEN** 任意时刻不存在两单位同格
