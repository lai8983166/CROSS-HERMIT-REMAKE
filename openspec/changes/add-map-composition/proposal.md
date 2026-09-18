# Proposal: add-map-composition

## Why

add-battle-assets 的缝分析把图集定性为**贴图素材库**（非地图碎片），当前贴图态是"素材平铺"——
用户看到的就是错位的存储顺序。真正的原版画面 = BIN 三层（疑贴图索引）驱动图集采样、逐格
合成世界布局。做完这步，sim 底图才是真正的 MAP01，叠加态对齐检查也随之有效。

## What Changes

- **映射逆向**（核心）：解出 `层值 → 图集 UV` 的对应——
  - 分析 MAP01.MAP 文件头的 255×4B 索引表与 53×(u16,u16) 步长表的结构语义
  - 结合 BIN 层值域（terrain 0..12 / variant / object）与图集页内贴片几何（32×16 菱形带？）
  - 多假设并用（直接索引/表走查/行列锚定），以渲染目检与回退 BMP 宏观相关度评分
- `tools/compose_map.py`：按定案映射把 64×96 格逐格贴片 → `prototype/assets/map01_composed.png`
  （世界布局，菱形交错排布，可再生成）+ 元数据
- `main.gd`：贴图态底图改用合成图；素材库平铺图（map01_atlas.png）降级为调试视图（T 循环第四态
  或并入文档说明）
- 三层语义**定案或收敛**：能定的写进 `docs/formats.md` §5；数据推不出的明确标注"需实机截图对照"
- 不含：高度/立体渲染（原作 D3D 有地形起伏——本 change 只做平面贴片）、其余 49 张地图批量、动画贴片

## Capabilities

### New Capabilities
- `assets/map-composition`: BIN 层值 → 图集采样 → 世界布局合成图的工具链与映射规则（数据驱动、可再生成）

### Modified Capabilities
- `battle-sim/map-render`: 贴图态底图改用合成图；叠加态对齐检查在此之后才具验收意义

## Impact

- 新文件：`tools/compose_map.py`、`prototype/assets/map01_composed.png`(+json)
- 修改：`main.gd`（贴图态来源）、`docs/formats.md`（三层语义收敛）
- 依赖：既有 atlas 工具/产物 + map01.json 三层数据
- 风险：映射可能无法纯数据推出（表语义不明时）——验收允许"部分定案+标注开口"，但合成图
  宏观结构必须与回退 BMP 对应（可辨认布局），否则不达标
