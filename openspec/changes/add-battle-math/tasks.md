# Tasks: add-battle-math

## 1. 数据与依赖

- [x] 1.1 `tools/table_export.py` 注册 `engage` 表（i32[51] @0x6E4528，行 = {level, minutes}，
       magic 校验：minutes[0]==0 且 minutes[1]==5940 且 minutes[50]==540）。验证：
       `python tools/table_export.py all` 后四个 JSON 齐全且 engage 值符合
- [x] 1.2 测试框架就位（GUT 9.3/9.6 在 4.7.2 无头挂起 → 自研 runner: sim/tests/test_base.gd
       断言基类 + test_runner.gd 发现/汇总/退出码, 见 design 决策 6 修订）。验证：
       `~/bin/godot --headless --path prototype -s res://sim/tests/test_runner.gd` 输出汇总 exit=0

## 2. sim 模块

- [x] 2.1 `prototype/sim/tables.gd`：加载并缓存 `res://data/*.json`（level/attack/job/engage），
       暴露 `job(id)` / `attack(id)` / `engage_table()`。验证：headless 脚本取 job 0 与
       attack 0 字段与 JSON 一致
- [x] 2.2 `prototype/sim/unit.gd`（class_name SimUnit）：七属性/职业/等级/HP/MP 现值与上限/
       回避/装甲/魔抗/精神抗性 字段 + 构造默认值。验证：GUT 构造测试（缺省防御字段为 0，
       全字段可读回）
- [x] 2.3 `prototype/sim/derive.gd`：`derive_unit(u) -> Dictionary` 按蓝图 §2 公式与
       job_table 系数算 HP/MP/精神上限（clamp 1..999 等，整数截断）。验证：GUT 锚点
       (耐10力10敏10, hp_coef=100)→50；全 1 属性 + hp_coef=1 → 1
- [x] 2.4 `prototype/sim/battle_math.gd`：`physical(atk, def, rng)`（MISS=-1、倍率档≥150、
       防御削减、钳位语义）、`magic(base, resist, mod)`、`fixed(v)`。验证：GUT 锚点三则
       （200 命中→200 伤；MISS 场景；10−20→0）+ 确定性测试（同种子两次一致）
- [x] 2.5 `prototype/sim/engage.gd`：`engage_seconds(level, mod_h, mod_s)` 读表计算，
       clamp(1, 356400)。验证：GUT 锚点 lv1→356400、lv50→32400、lv50+mod_h=1→36000 (32400+3600)

## 3. 集成验收

- [x] 3.1 GUT 全量绿：headless 运行全部测试退出码 0，汇总行写进提交信息。验证：
       `~/bin/godot --headless --path prototype -s addons/gut/gut_cmdln.gd -gdir=res://sim/tests -gexit`
- [ ] 3.2 公式↔文档交叉核对：把 battle_math/derive/engage 的每个公式旁注文档章节指针，
       提交前人工过一遍符号与端点。验证：代码内注释含 `# 见 battle_mechanics.md §3.1` 式引用
       不少于 5 处
- [ ] 3.3 提交（信息含测试汇总），blueprint §6 资产表加一行 sim 现状
