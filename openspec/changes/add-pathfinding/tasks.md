# Tasks: add-pathfinding

## 1. 规则与寻路原语

- [ ] 1.1 `prototype/data/walk_rules.json`（默认 object≠0 阻断）+ SimMapData 增
       `is_walkable(x, y, rules)`。验证：GUT——默认规则下 object≠0 格不可走、
       object=0 可走；注入自定义 rules 后语义随表变化
- [ ] 1.2 `prototype/sim/pathfinding.gd`（class_name SimPath）：`find_path(map, rules,
       from, to, blocked := {})` → Array[Vector2i]（不含 from 含 to，不可达空）；
       邻居序固定 右/左/下/上。验证：GUT——直线长度、绕 U 形墙合法（逐格可走）、
       不可达空、同输入两次路径全等
- [ ] 1.3 目标退化：目标格阻挡/被占时返回到"目标四邻最近可达格"的路径。
       验证：GUT——目标为阻挡格时终点落在其可行邻居上
- [ ] 1.4 性能软护栏：GUT——MAP01 实数据上 1000 次跨图 BFS 用时 < 1s（Time.get_ticks_msec）

## 2. 战斗接入

- [ ] 2.1 battle.gd：加载 walk_rules；`_step_toward` 替换为 SimPath 首步步进
       （blocked = 其他存活单位占格）。验证：GUT——构造被墙隔开的 1v1，战斗仍能打完
       （路径绕行），日志 move 序列不含阻挡格
- [ ] 2.2 确定性回归：同种子两场日志全等（既有测试扩：新移动逻辑下重跑）。
       验证：test_determinism 仍绿
- [ ] 2.3 battle_setup.json 布阵核位：8 个初始格与寻路首步均不在阻挡格上。
       验证：GUT——setup 全员初始格 is_walkable

## 3. 验收

- [ ] 3.1 全量测试绿（新增 pathfinding 套件）。验证：runner 0 failures exit=0
- [ ] 3.2 窗口人工目检：单位绕开黄框障碍行进、不再同格重叠（用户确认）
- [ ] 3.3 提交 + README 增 walk_rules 魔改说明
