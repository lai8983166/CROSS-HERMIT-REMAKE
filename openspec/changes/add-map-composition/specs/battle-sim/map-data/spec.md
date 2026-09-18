## MODIFIED Requirements

### Requirement: sim 地图数据访问
`SimMapData` 加载 `map##.json` 并提供：维度只读、`layer(layer_name, x, y)` 格值、`cell_to_world(x, y)` / `world_to_cell(px)` 坐标换算。**换算为直角网格语义（add-map-composition 定案）**：格 (x,y) 占世界像素矩形 `[32x, 16y, 32, 16]`（对应地图 px 头 2048×1536 与引擎 `x>>21/y>>20` 线性整除证据），`cell_to_world` 返回格中心 `(32x+16, 16y+8)`；`world_to_cell` 为 `floor(px/32), floor(py/16)`。越界格访问返回 -1。

#### Scenario: 加载与格值
- **WHEN** headless 加载 map01.json 后读取 terrain(0,0) 与 (63,95)
- **THEN** 两值均为 JSON layers.terrain 中的合法值（0..12 域）

#### Scenario: 坐标换算往返
- **WHEN** 对任意格中心坐标 cell_to_world 后立即 world_to_cell
- **THEN** 回到原格坐标（全 64×96 网格成立）

#### Scenario: 越界
- **WHEN** 读取 layer("terrain", -1, 0) 或 (64, 0)
- **THEN** 返回 -1，不崩溃
