# Proposal: add-table-export

## Why

重制原型的战斗模拟器（`prototype/sim/`）需要等级/攻击/职业三张核心数值表，但目前这些数据只存在于
脱壳镜像 `analysis/hermit_game.exe` 的二进制里（地址已逆向归档于 `docs/REMAKE_BLUEPRINT.md` §7）。
需要一个导出工具把数据变成 Godot 可直接加载的 JSON，打通"逆向成果 → 原型数据"的管线。

## What Changes

- 新增 `tools/table_export.py`：按已知 VA 从 `analysis/hermit_game.exe` 读取并导出数据表
- 首期导出 3 张表到 `prototype/data/`：
  - `level_table.json` — 等级阈值表 `0x625300`（i32[50]，149,999→8,500,000）
  - `attack_table.json` — 攻击/技能表 `0x6C2DC8`×0x48（~360 条，字段图见 battle_mechanics.md §1.1）
  - `job_table.json` — 职业表 `0x6B2D88`×0x40（30 条）
- 每个 JSON 附溯源元数据（源 VA、条数、导出时间戳、字段说明指针）
- 字段名按蓝图 §7 的语义命名（未知字段保留 `u16_0xNN` 形式）

## Capabilities

### New Capabilities
- `data-pipeline/table-export`: 从脱壳镜像按地址导出重制数据表为 JSON 的工具能力

### Modified Capabilities
<!-- 无：本 change 不改动任何现有能力的行为 -->

## Impact

- 新文件：`tools/table_export.py`、`prototype/data/*.json`（3 个）
- 依赖：仅 Python 标准库 + 既有的 `analysis/hermit_game.exe`（已在 git 内）
- 不改动现有工具与文档；后续 sim 模块将消费这些 JSON
- 风险：攻击表条数上限需按相邻表边界推定（0x6D4E58 技能附属表之前），导出时做尾部全零截断校验
