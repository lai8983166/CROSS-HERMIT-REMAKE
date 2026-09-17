# Proposal: add-map-data

## Why

战斗模拟器的第一个可视化里程碑：sim 已具备数值层（add-battle-math），现在把 MAP01 的逻辑格数据
（已逆向定案的 16B 头 + 3 层 u16 格，formats.md §5）接进来并渲染——完成后窗口里第一次出现
原版地图的完整地形数据视图，同时为后续寻路/单位/贴图 change 打好数据地基。

## What Changes

- 导出：`tools/map_export.py`（独立工具，不动 table_export 的 exe 表职责）——解析
  `CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/MAP/MAP01.BIN`，产出 `prototype/data/map01.json`
  （`{_meta: {px_w,px_h,cell_w,cell_h,page_x,page_y,source}, layers: {terrain, variant, object}}`）
- sim：`prototype/sim/map_data.gd`（SimMapData：加载/格值访问/行列↔世界坐标换算）
- 可视化：`main.gd` 从占位网格改造为 MAP01 渲染——层0 地形类别调色板上色、层1 变体明度微调、
  层2 物件格子描边标记；点击格子回显坐标与三层值（HUD 文本）
- 不含：寻路、AI、单位、纹理贴图、多地图切换 UI（后续 change）

## Capabilities

### New Capabilities
- `battle-sim/map-data`: 地图逻辑层数据的导出、加载与数据访问（格值/维度/坐标换算）
- `battle-sim/map-render`: 地图层的基础可视化渲染与点选回显（占位视觉，非原版贴图）

### Modified Capabilities
<!-- 无：不改动既有能力的行为 -->

## Impact

- 新文件：`tools/map_export.py`、`prototype/data/map01.json`、`prototype/sim/map_data.gd`、
  地图渲染相关脚本
- 修改：`prototype/main.tscn`/`main.gd`（占位网格 → 地图渲染）
- 依赖：MAP01.BIN（游戏目录，.gitignore 内——导出 JSON 入 git，工具可重跑）
- 地形调色板是**占位语义**（层值→颜色的临时映射），语义定案待实机截图对照（formats.md §5 开口项），
  本 change 只保证"值可区分、图可辨认"
