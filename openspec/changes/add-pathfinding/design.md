## Context

battle.gd 现为 `_step_toward` 直线步进（穿障碍、可同格）；地图层 SimMapData 与规则数据管线就绪。
64×96 = 6,144 格，BFS 最坏全图扫描在 GDScript 数组上 <1ms 量级，30Hz 逻辑帧内 8 单位足够。

## Goals / Non-Goals

**Goals:**
- 寻路原语独立可测（不依赖 Battle），战斗只消费
- 可行走语义 100% 数据驱动（walk_rules.json），实机对照后换表即改行为
- 路径确定性（固定邻居扩展序）→ 不破坏整场确定性

**Non-Goals:**
- 不解析原作 VPT 导航图（蓝图 §4.4：重制重新生成）
- 不做 A* / 地形代价 / 对角移动（64×96 四连通 BFS 足够；代价权重等实机语义定案再说）
- 不做推挤/交换（占格=临时阻挡，挤死等待）

## Decisions

1. **BFS 而非 A***：格量小、四连通等距、GDScript 实现简单；`PackedInt32Array` 做环形队列 +
   `visited`/`prev` 两个 PackedInt32Array（idx = y*cell_w+x），零 Dictionary 哈希开销。
   A* 的收益（少扫格）在此规模无感。
2. **邻居扩展序固定为 右/左/下/上 (dx=+1,−1,dy=+1,−1)**：保证同输入同路径（确定性回归依赖）。
   序本身无优劣，写死后不做配置。
3. **每步重算路径，不缓存**：占格每 tick 变，缓存失效逻辑比重算贵。8 单位 × BFS(<1ms) × 30Hz
   ≈ 240 次/秒 — 余量充足。若未来单位数 ×10 再引入增量重算（记录为后备）。
4. **目标被占的退化**：BFS 以目标格为终点；目标格本身占/阻挡时改求"目标的四邻中最近可达者"
   （一次性多源 BFS：把目标邻格都入初始队列）。战斗层无需特判。
5. **规则求值放 SimMapData.is_walkable(x,y,rules)**：规则 Dictionary 由调用方加载缓存
   （walk_rules.json → Battle 持有），地图层不读文件——保持 SimMapData 纯内存。
6. **移动节拍不变**：仍是 `frame % move_interval` 走一格，BFS 只改"走哪格"——确定性回归的
   唯一风险点是路径分歧，由决策 2 钉死。

## Risks / Trade-offs

- [每 tick 重算的 GDScript 性能] → 决策 3 已估余量；测试加"1000 次 BFS < 1s"软护栏
- [object≠0 就阻挡的占位规则可能过严（黄框密集处单位寸步难行）] → 布阵挪到开阔区 +
  规则可改 JSON；实机对照后校正
- [挤在窄口互等形成活锁] → 接受（等一步）；死锁由 ENGAGE 计时兜底结束战斗

## Migration Plan

新增 2 文件 + battle.gd 移动段替换。回滚 = 还原 battle.gd、删 pathfinding/walk_rules。
