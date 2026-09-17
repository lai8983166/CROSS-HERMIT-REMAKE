## Context

公式语义全部来自逆向定案（`docs/REMAKE_BLUEPRINT.md` §2/§4.1/§4.2、`docs/character_growth.md`
§1.3/§2、`docs/battle_mechanics.md` §3/§8），数据消费沿用 add-table-export 建立的
`{_meta, rows}` JSON 约定。sim 尚无代码（prototype/ 仅有占位 main）。

## Goals / Non-Goals

**Goals:**
- 公式层与数据层解耦：纯函数 + 注入 RNG，headless 可测
- 数值保真：整数运算、C 语义截断（向零）、钳位端点与原作一致
- 每个公式带文档锚点测试（值取自逆向档案已验证的边界）

**Non-Goals:**
- 不复刻原作 44B 属性快照/0x4C 修正缓冲的内存布局——sim v1 用显式参数与 Dict 表达
- 不做 AI/寻路/演出/地图（后续 change）
- 不做平衡性调整（数值照抄，改平衡属于未来独立 change）

## Decisions

1. **模块划分**：`unit.gd`(数据) / `derive.gd`(派生) / `battle_math.gd`(伤害) / `engage.gd`(时间)
   四个静态类（`class_name` + `static func`），互相无场景依赖。优于单文件大杂烩——后续 AI/寻路
   change 可独立挂靠。
2. **RNG 注入**：公式签名收 `rng: RandomNumberGenerator`（调用方持有并播种）。
   Godot `RandomNumberGenerator.randi() % n` 与原作 `rand() % n` 同为整数均匀分布，模拟语义
   足够；不复刻 MSVC rand 算法（重制不需要比特级一致）。测试用固定种子。
3. **整数截断**：Godot int 为 64 位且 `/` 向零截断，与 C int32 一致；中间量不溢出 64 位
   （原作量级 ≤ 8.5M×系数），无需模拟回绕。钳位统一 `clampi`。
4. **MISS 语义**：返回哨兵 `MISS = -1`（伤害值域非负），调用方判负数。优于抛枚举——sim
   阶段保持轻量。
5. **表加载**：`sim/tables.gd` 单点负责加载 `res://data/*.json` 并缓存（静态 Dictionary）；
   位置换算（如 minutes→秒）写在消费者（engage.gd）而非导出器——导出保持"原作单位原样"。
6. **测试框架 (实施中修订 2026-09-17)**：原计划 vendor GUT 9.x，实测 9.3.0 与 9.6.1 在
   Godot 4.7.2 headless 下均报错后挂起（class 注册/兼容性问题；另查明 `_init` 报错会使
   SceneTree 永不退出，即"挂起"的机制）。改用原备选：自研轻量 runner
   （`sim/tests/test_base.gd` 断言基类 + `test_runner.gd` 发现/汇总/退出码），满足 spec 的
   headless 可跑 + 退出码要求。GUT 若未来兼容可整体替换（测试文件仅依赖自家基类 API）。
7. **魔法式简化建模**：v1 按 spec 场景实现 `d = 基础×(100−魔抗+修正)/100`；原作 4826F0 的
   状态附加/多段细节留待需要时扩展（文档锚点已注明）。

## Risks / Trade-offs

- [公式细节与原作有出入（如 MISS 区间 (4,94] 的边界）] → 测试锚点直接抄逆向文档的数值结论；
  存疑处标注 TODO 与文档指针，不做无声猜测
- [GUT vendor 体积/升级] → 一次性拷贝不引 submodule，升级=整目录替换；.gitignore 不忽略它
- [伤害公式参数在原作里来自 44B 快照聚合] → sim v1 参数显式传入，聚合层（装备/技能修正）
  属于未来 change，届时在 derive.gd 扩展

## Migration Plan

纯新增（sim/ 4 文件 + tests + addons/gut + engage 导出）。回滚 = 删除上述文件与
`table_export.py` 的 engage 注册段。
