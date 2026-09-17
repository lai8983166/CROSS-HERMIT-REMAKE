## Purpose

把已逆向定案的战斗地图逻辑层数据（MAP*.BIN：尺寸头 + 3 层 u16 格）变成重制可加载的 JSON 与 sim 内的数据访问层，作为寻路/单位/渲染的公共地基。

## ADDED Requirements

### Requirement: 地图逻辑层导出
导出工具接收地图编号（如 `01`），解析对应 `MAP##.BIN`：16B 头 `[px_w px_h cell_w cell_h 256 256 page_x page_y]` + `cell_w×cell_h` × 3 层 u16，写出 `prototype/data/map##.json` = `{_meta:{px_w,px_h,cell_w,cell_h,page_x,page_y,source_bin}, layers:{terrain,variant,object}}`（层数组按行优先，长度=格数）。头部长度校验不符（文件大小 ≠ 16 + 6×格数）时报错退出。

#### Scenario: 导出 MAP01
- **WHEN** 运行 `python tools/map_export.py 01`
- **THEN** 生成 `prototype/data/map01.json`：cell_w=64、cell_h=96、px 2048×1536、page 8×6；三层各 6,144 项；层值分布与 formats.md §5 记录一致（terrain 层 0 值约 2/3）

#### Scenario: 损坏输入
- **WHEN** BIN 尺寸与头部长度推定不符
- **THEN** 非零退出码 + 明确错误信息，不产出 JSON

### Requirement: sim 地图数据访问
`SimMapData` 加载 `map##.json` 并提供：维度只读、`layer(layer_name, x, y)` 格值、`cell_to_world(x, y)` / `world_to_cell(px)` 菱形格坐标换算（格 32×16px，与既有 main.gd 坐标系一致）。越界格访问返回 -1。

#### Scenario: 加载与格值
- **WHEN** headless 加载 map01.json 后读取 terrain(0,0) 与 (63,95)
- **THEN** 两值均为 JSON layers.terrain 中的合法值（0..12 域）

#### Scenario: 坐标换算往返
- **WHEN** 对任意格心坐标 cell_to_world 后立即 world_to_cell
- **THEN** 回到原格坐标（全 64×96 网格成立）

#### Scenario: 越界
- **WHEN** 读取 layer("terrain", -1, 0) 或 (64, 0)
- **THEN** 返回 -1，不崩溃
