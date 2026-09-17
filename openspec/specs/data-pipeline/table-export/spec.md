## Purpose

从已逆向定位的脱壳镜像数据表导出重制可用的 JSON，打通逆向成果与原型数据层之间的管线，使游戏数值无需手工誊抄。

## Requirements

### Requirement: 按地址导出数据表
导出工具接收表名（或 all），从 `analysis/hermit_game.exe` 的既定 VA 读取原始字节并解码为带命名字段的结构化条目，写入 `prototype/data/<table>.json`。首期支持：`level`（等级阈值 i32[50] @0x625300）、`attack`（攻击/技能 ×0x48 @0x6C2DC8）、`job`（职业 ×0x40 @0x6B2D88，30 条）。

#### Scenario: 导出等级表
- **WHEN** 运行 `python tools/table_export.py level`
- **THEN** 生成 `prototype/data/level_table.json`，含 50 个阈值条目，首项 149,999、末项 8,500,000，与 `docs/character_growth.md` §3.2 的数值一致

#### Scenario: 导出攻击表
- **WHEN** 运行 `python tools/table_export.py attack`
- **THEN** 生成 `prototype/data/attack_table.json`，每条含 battle_mechanics.md §1.1 已定名字段（mp_cost、cast_frames、recovery_frames、power_a、level_points 等），未知字段以 `u16_0xNN` 原样保留

#### Scenario: 导出职业表
- **WHEN** 运行 `python tools/table_export.py job`
- **THEN** 生成 `prototype/data/job_table.json`，恰好 30 条职业记录

#### Scenario: 全量导出
- **WHEN** 运行 `python tools/table_export.py all`
- **THEN** 上述三张表一次性全部生成

### Requirement: 溯源元数据
每个导出的 JSON 必须自带 `_meta` 对象：源 VA、条目步长、条数、字段命名依据（文档指针）、工具版本。镜像缺失或地址越界时，工具以非零退出码报错并指明缺失文件，不产出半成品 JSON。

#### Scenario: 镜像缺失
- **WHEN** `analysis/hermit_game.exe` 不存在时运行导出
- **THEN** 工具打印明确错误信息并以非零码退出，`prototype/data/` 无新增文件

#### Scenario: 元数据完整
- **WHEN** 任一表导出成功
- **THEN** JSON 根级 `_meta` 含非空 `source_va`、`stride`、`count`、`naming_ref` 字段

### Requirement: Godot 可加载
导出的 JSON 必须是合法 UTF-8、无注释、无尾逗号，能被 Godot 4 的 `FileAccess.get_file_as_string` + `JSON.parse_string` 直接解析。

#### Scenario: Godot 解析
- **WHEN** 在 Godot 4 中解析任一导出文件
- **THEN** `JSON.parse_string` 返回非 null Dictionary/Array

### Requirement: 条目数推定与校验（攻击表）
攻击表无独立长度字段，导出时须以下一已知表（0x6D4E58 技能附属表）为上界，并向后截去连续全零哑条目；截断结果须落在外部文档宣称的量级（数百条）内，否则报错拒绝导出。

#### Scenario: 尾部全零截断
- **WHEN** 攻击表导出
- **THEN** 末条不是全零记录，且总条数 ≤ 上界推定值；若截断后条数异常（<10 或 >4096），工具报错退出
