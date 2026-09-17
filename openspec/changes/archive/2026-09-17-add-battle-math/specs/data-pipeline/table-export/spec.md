## ADDED Requirements

### Requirement: 导出 ENGAGE 表
导出工具支持 `engage` 表：从 `0x6E4528` 读取 i32[51]（每级 ENGAGE 时长，单位分钟），写出 `prototype/data/engage_table.json`（`{_meta, rows}`，行含 level 与 minutes）。

#### Scenario: 导出 engage 表
- **WHEN** 运行 `python tools/table_export.py engage`
- **THEN** 生成 51 行 JSON：level 0 的 minutes=0、level 1..5 均为 5940、level 6 为 5760、level 50 为 540；首值不符 5940 段特征时报错退出

#### Scenario: 纳入 all
- **WHEN** 运行 `python tools/table_export.py all`
- **THEN** engage 与 level/attack/job 四表一并生成
