# Proposal: add-pathfinding

## Why

战斗循环已运行但单位直线步进**穿墙**（object 障碍无视）。接入可行走规则 + BFS 寻路，
单位行为从"物理演示"升级为"绕障行军"——同时把可行走语义做成数据（BIN 三层语义未定案，
实机对照后改 JSON 即生效，不改代码）。

## What Changes

- `prototype/data/walk_rules.json`：`{blocked_terrain: [], blocked_variant: [], blocked_objects: "nonzero"}`
  ——三层值→阻挡的规则表（占位默认：object≠0 即阻挡）
- `prototype/sim/pathfinding.gd`（SimPath：BFS 最短路；输入地图+规则+动态占格集；
  输出路径或首步方向；不可达返回空）
- `battle.gd`：`_step_toward` 改为沿 BFS 路径步进；目标/相邻格被存活单位占用时把占格
  计入阻挡重算（挤死则原地等一步）
- 单位碰撞：移动前检查目标格占用
- 不含：原作 VPT 导航图解析（重制重新生成，蓝图 §4.4 已定）、移动速度/地形代价差异、对角移动

## Capabilities

### New Capabilities
- `battle-sim/pathfinding`: 可行走规则（数据驱动）与 BFS 寻路——含动态占格、不可达语义，纯函数可测

### Modified Capabilities
- `battle-sim/battle-loop`: 移动行为从直线步进改为 BFS 绕障行军（含单位碰撞）

## Impact

- 新文件：`walk_rules.json`、`sim/pathfinding.gd`、`sim/tests/test_pathfinding.gd`
- 修改：`battle.gd`（移动逻辑）、`battle_setup.json`（如需挪初始位避开障碍格）
- 风险：BFS 每步重算（8 单位 × 6,144 格）在 30Hz 逻辑帧的开销——按需缓存（决策记录）
