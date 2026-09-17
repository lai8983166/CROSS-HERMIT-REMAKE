# Proposal: add-battle-math

## Why

重制原型的核心里程碑是战斗模拟器，其第一步是把已逆向定案的战斗数值规则（蓝图 §4.1/§4.2、
character_growth §1.3/§2）落成可运行、可测试的 Godot 代码。数据表已由 add-table-export
导出（attack/job），现在补齐公式层与 ENGAGE 表数据，使 sim 具备"输入属性 → 输出战斗数值"的
完整能力。

## What Changes

- 新增 `prototype/sim/` 第一批模块：
  - `unit.gd`（SimUnit：七属性/职业/等级/HP/MP/回避/装甲/魔抗 等战斗字段）
  - `derive.gd`（战备合成：HP/MP/精神 上限公式，职业系数读 `data/job_table.json`）
  - `battle_math.gd`（伤害三式：物理命中残量/倍率档/防御削减、魔法抗性、固定伤害；可注入 RNG）
  - `engage.gd`（ENGAGE TIME 计算，表驱动）
- `tools/table_export.py` 新增 `engage` 表导出（i32[51] @0x6E4528，分钟/等级）
- 引入 GUT 测试框架（vendor 至 `prototype/addons/gut/`）+ `sim/tests/` 锚点测试
- 不含：AI、寻路、演出、UI、地图（后续 change）

## Capabilities

### New Capabilities
- `battle-sim/combat-math`: 战斗数值核心——单位战斗字段模型、派生上限、伤害/命中公式、ENGAGE TIME 的可测实现

### Modified Capabilities
- `data-pipeline/table-export`: 新增 engage 表（0x6E4528, i32[51]）导出要求

## Impact

- 新文件：`prototype/sim/*.gd`（4 个）、`prototype/sim/tests/`、`prototype/addons/gut/`（第三方 vendor）、`prototype/data/engage_table.json`
- 修改：`tools/table_export.py`（TABLES 注册 + engage 解码器）
- 依赖：既有 `data/attack_table.json`、`data/job_table.json`；GUT（Godot 4 兼容版本）
- 公式保真约束：整数运算、C 语义截断（/100 向零取整）、钳位与原作一致（HP 1..999 等）
