## Purpose

把 DxAnim 块7 换色调色板（40×256/单位档，[0]=基色==身体帧内嵌）变成重制可用的
换色数据：导出 JSON + sim 运行时重映射，实现实机"同模不同色"（阵营/变体配色）。

## ADDED Requirements

### Requirement: 换色表导出
`tools/unit_recolor_export.py` 从单位档块7 导出 `prototype/data/unit_recolors.json`：
每档 40×256 RGB 数组（含 0 号透明语义标注）+ 每档预览图 `assets/unit/<档>/_recolors.png`
（基帧 × 40 色，供目检选 palette_id）。换色表与帧表分离存放，互不耦合。

#### Scenario: 全档导出
- **WHEN** 运行导出工具
- **THEN** 10 档各 40 条调色板，条目数与块7 头一致；预览图可辨认 40 套配色差异

#### Scenario: 数据可替换
- **WHEN** 手改 unit_recolors.json 中某条 RGB 后重载
- **THEN** sim 渲染按新表换色（数据驱动）

### Requirement: sim 换色渲染
配了 palette_id 的单位，其精灵帧按 (档, 帧, palette_id) 重映射后渲染：基色像素
（=块7[0] 条目）精确匹配替换为换色表对应条目；重映射纹理缓存复用。palette_id
越界、换色表缺失、或像素无匹配 → 保持基色（渲染不报错不出花屏）。

#### Scenario: 换色生效
- **WHEN** battle_setup 两单位同 anim_id 不同 palette_id
- **THEN** 窗口中两单位配色不同，且与本档预览图对应格子观感一致

#### Scenario: 回退
- **WHEN** palette_id 超出该档调色板数或 unit_recolors.json 缺失
- **THEN** 渲染基色，战斗逻辑与精灵动画不受影响
