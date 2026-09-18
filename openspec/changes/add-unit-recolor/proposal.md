## Why

add-unit-sprites 落地后单位已是原版精灵，但实机中**同模不同色**（阵营/单位变体配色），
sim 里全部档只有基色。侦察已定案关键事实：
- 块7[0] == 身体帧内嵌调色板（逐字节 dist=0），即基色就是换色表的第 0 张；
- 块7[1..39] 为换色表（约 180/256 索引变色，头部索引 8..15/32..59 集中变色）；
- 视觉验证：40 张表 = 同角色 40 套配色（第 1 行=装备大改变体，其后=头盔/盾色轮换，
  #9=黑影红边特殊版）——正是实机敌我同模不同色的来源。

把换色表接进 sim（运行时重映射 + JSON 配置），是缩小"和实机差距"观感收益最大的一步。

## What Changes

- **逆向补遗**：块7 结构定案写入 formats.md §10（40 张/单位档全档一致、[0]=基色、
  [9]=黑影特殊；引擎侧选择字段仍开口）。块8 与帧类型相关性弱（0.43 vs 0.17），语义保持开口。
- **导出**：`tools/unit_recolor_export.py` → `prototype/data/unit_recolors.json`
  （每档 40×256 RGB 表 + 预览图 `assets/unit/<档>/_recolors.png`，目检选色用）。
- **sim 换色渲染**：main.gd 帧纹理按 (档, 帧, palette_id) 缓存重映射 ImageTexture
  （基色 RGB 精确匹配 → 换色表替换，纯 GDScript 数据变换）；battle_setup.json 每单位
  `palette_id`（默认 0=基色）；越界/缺表 → 基色回退。
- **阵营默认配色**：battle_setup 红蓝阵营各指定默认 palette_id（数据驱动，可改）。

## Capabilities

### New Capabilities
- `assets/unit-recolor` — 块7 换色表导出与数据格式（JSON 可魔改）

### Modified Capabilities
- `assets/unit-sprites`（sim 精灵渲染 requirement 扩展）— 精灵按 palette_id 换色渲染

## Impact

- 新增 `tools/unit_recolor_export.py`、`prototype/data/unit_recolors.json`
- `prototype/main.gd` 纹理缓存路径扩展（重映射分支）；`battle_setup.json` 增 palette_id 字段
- 测试补：换色表加载/重映射正确性/越界回退
- 风险：帧内嵌调色板 ≠ 块7[0] 的帧（特效帧）不适用精确匹配 → 仅对身体帧重映射，
  匹配失败的像素保持原色（渲染正确性不受损）
