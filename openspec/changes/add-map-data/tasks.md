# Tasks: add-map-data

## 1. 导出

- [ ] 1.1 `tools/map_export.py`：参数=地图编号（`01`），读
       `CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/MAP/MAP##.BIN`，16B 头解析 + 尺寸校验
       （文件大小==16+6×格数）+ 3 层 u16 解码 → `prototype/data/map##.json`。验证：
       map01.json 的头字段 (64/96/2048/1536/8/6)、三层长度 6144、terrain 层 0 值占比 ≈2/3
- [ ] 1.2 损坏输入护栏：构造尺寸不符的假 BIN（临时文件）运行工具 → 非零退出 + 报错信息。
       验证：stderr 有信息、目标目录无新 JSON

## 2. sim 数据层

- [ ] 2.1 `prototype/sim/map_data.gd`（class_name SimMapData）：加载 map JSON、
       `cell_w/cell_h` 等维度、`layer(name,x,y)`（越界 -1）、`cell_to_world/world_to_cell`
       （32×16 菱形，含格心偏移）。验证：GUT——加载 map01 后 terrain(0,0)==JSON 值、
       全网格换算往返、越界 -1 三则
- [ ] 2.2 换算实现与 main.gd 既有 ORIGIN/菱形画法对齐（同一 cell_to_world 驱动绘制）。
       验证：肉眼——渲染网格与原占位网格同构（等距同形）

## 3. 渲染与交互

- [ ] 3.1 `data/terrain_palette.json`（占位调色板 13 色，数据驱动）+ main.gd 改造：SimMapData 加载 map01 → 全图渲染（
       variant 明度微调、object 亮黄描边）。验证：窗口运行 `--quit-after 120` 无脚本错误，
       人工看一眼全图着色分层可辨
- [ ] 3.2 悬停/点击回显：HUD 显示 (x,y)+三层值（点击锁定）。验证：人工点击 object≠0 格，
       HUD 值与 JSON 抽查一致；无资产（assets 空）状态功能正常
- [ ] 3.3 回归：sim 测试全绿（`-s res://sim/tests/test_runner.gd`，新增 map_data 套件）。
       验证：汇总 0 failures, exit=0
- [ ] 3.4 提交 + prototype/README 更新（运行方式/map01.json 来源/调色板占位说明）
