## Context

数据表地址/结构已全部逆向归档（`docs/battle_mechanics.md` §1/§1.1、`docs/character_growth.md` §3.2、
`docs/REMAKE_BLUEPRINT.md` §7），镜像 `analysis/hermit_game.exe` 在 git 内（节表 raw==VA，即
文件偏移 = VA − 0x400000）。消费方是 Godot 4 原型（`prototype/sim/`，尚未实现）。

## Goals / Non-Goals

**Goals:**
- 单文件工具、零第三方依赖（Python 标准库），可重复执行（幂等覆盖输出）
- 字段命名与逆向文档一一对应，未知字段不丢数据
- 输出对 Godot 4 `JSON.parse_string` 零处理直接可用

**Non-Goals:**
- 不做全量 17 张表（后续 change 按需扩 `TABLES` 注册表）
- 不导出需要交叉引用才有意义的表（如课程表习得率 → 留给消费方组装）
- 不做 C# 生成 / Godot Resource (.tres) 导出（JSON 足够，避免工具依赖 Godot）

## Decisions

1. **表驱动注册**：`TABLES = {"level": TableSpec(...), ...}`，每张表声明 VA/条数/步长/解码器。
   追加表 = 加一个注册项 + 一个解码函数。优于 if-else 长链，后续 change 扩表零侵入。
2. **攻击表条数推定**：上界 = `(0x6D4E58 − 0x6C2DC8) // 0x48`（下一已知表地址），
   从尾部向前截去全零条目。备选（按引用扫描统计最大 id）留作交叉校验注释，不进首期逻辑——
   简单上界+截断已满足 spec 的量级校验。
3. **字段命名**：以 `battle_mechanics.md` §1.1 字段图的语义名（snake_case）为准；未定名字段
   输出 `u16_0x22` 式原名。不做"猜名"，避免重制代码绑死在错误语义上。
4. **`_meta` 放根级**：Godot 侧 `data["_meta"]` / `data["rows"]` 分离，遍历时跳过 `_meta` 即可。
   备选（旁挂 .meta.json）会制造双文件同步问题，弃。
5. **时间戳用文件 mtime 链**：`_meta.exported_from` 记镜像 SHA1 前 8 位而非时间——时间戳会让
   重复导出产生无意义 diff，哈希能真正回答"数据来自哪次镜像"。

## Risks / Trade-offs

- [攻击表真实条数与截断推定不符] → spec 已要求异常量级报错；导出后人工抽查 entry0/1/2 与
  文档已知值（+0x40 = 40/16000/36000）核对
- [未来表地址因镜像重抓而漂移] → `_meta.source_va` 溯源 + 工具校验 magic（如 level 表首值
  应为 149999），漂移立即报错而非静默错位
- [字段语义文档后续修订] → `naming_ref` 指针直指文档章节，重导出即同步；不改 JSON 结构

## Migration Plan

新增文件，无存量迁移。回滚 = 删除 `tools/table_export.py` 与 3 个 JSON。
