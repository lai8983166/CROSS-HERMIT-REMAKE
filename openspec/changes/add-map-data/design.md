## Context

BIN 格式已定案（formats.md §5：16B 头 + 3×W×H u16 层，层语义待实机对照）；main.gd 现有
菱形格绘制与 HUD 可复用；数据管线分两轨——exe 内静态表走 table_export.py，游戏目录文件走
独立工具（.gitignore 对象），故地图导出独立成 `map_export.py`。

## Goals / Non-Goals

**Goals:**
- map01.json 完整承载三层逻辑数据（重制不再依赖游戏目录即可跑 sim）
- 渲染零美术依赖、纯 draw_*，60fps 无压力
- 坐标换算成为后续单位/寻路的公共 API

**Non-Goals:**
- 不解 MAP/MAP 纹理页、VPT（表现层后续 change）
- 不做多地图选择 UI（工具按编号导出，加载固定 map01）
- 不做层语义定案（terrain 值→草地/墙壁等命名留给实机对照 change）

## Decisions

1. **独立 `tools/map_export.py`** 而非并入 table_export：输入是游戏目录文件不是 exe 偏移，
   校验/输入/输出形态都不同；复用 `_meta` 惯例。备选（并入）会让 table_export 双职责。
2. **JSON 层用一维行优先数组**（非二维嵌套）：文件小（6144×3 int）、Godot 侧索引
   `y*cell_w+x` 一次乘加；二维数组在 GDScript 访问开销大。
3. **调色板 = terrain 值→颜色的数据表**（0=透明/空, 1..12 递进色相），放
   `prototype/data/terrain_palette.json`（魔改友好约束：代码不藏常量，改色=改 JSON）；
   层1 明度调制 `lightness ± value×2%`；层2 描边亮黄。全部为占位语义，实机对照后整表
   替换该 JSON。
4. **渲染分帧**：一次性 `_draw()` 画 6,144 格的 draw_polyline/draw_rect 数量级可控
   （实测同量级占位网格已达标），不加瓦片化/合并；若 profiling 不达标再引入
   RenderingServer 批量（记录为后备方案）。
5. **点击检测用数学反解**（world_to_cell）而非每格碰撞体：与 spec 的换算往返要求共用
   同一实现，避免两套坐标系漂移。
6. **悬停即回显 + 点击锁定**：悬停实时更新 HUD，点击把值固定显示（便于核对）——最低成本
   满足"点击回显"且更好用。

## Risks / Trade-offs

- [层语义未知导致颜色"不像地图"] → 占位调色板仅保证值可区分；语义定案后换表即可（决策 3）
- [全格 _draw 每帧重绘性能] → draw 调用 ~6k 次在 4.7 兼容渲染器可承受（占位场景已验证同类
  量级）；不行则升级 RenderingServer 批量（决策 4 后备）
- [JSON 体积]（map01 三层 ~74KB 压缩前）→ 入 git 可接受；全 50 张地图导出时再考虑二进制格式

## Migration Plan

纯新增 + main.gd 改造（保留速度档键）。回滚 = 还原 main.gd、删 map_export.py/map_data.gd/map01.json。
