## Purpose

地图逻辑层的基础可视化：把三层格值以占位视觉（调色板+明度+描边）渲染到窗口，并提供点选回显——sim 第一个"能看见"的界面，供数据核对照用。

## Requirements

### Requirement: 三层占位渲染
主场景加载 map01.json 并渲染全图菱形格：每格底色 = 层0(terrain) 值经固定调色板映射；层1(variant) 非零时按值微调明度（可视觉区分变体）；层2(object) 非零时格子加亮色描边。渲染覆盖全部 64×96 格，帧率可交互（≥30fps 窗口模式）。

#### Scenario: 全图渲染
- **WHEN** 窗口运行主场景
- **THEN** 可见 64×96 格完整地图，不同 terrain 值呈现不同底色，object 格有描边标记

### Requirement: 点选回显
鼠标点击/悬停格子在 HUD 显示：格坐标 (x, y) 与三层值 terrain/variant/object。屏幕外点击无效。

#### Scenario: 点击回显
- **WHEN** 点击某个 object≠0 的格子
- **THEN** HUD 显示该格 (x,y) 与三层值，object 值与 JSON 数据一致

### Requirement: 渲染不依赖美术资产
本能力仅使用程序化绘制（draw_*），不加载任何原版纹理——保证 sim 在无素材仓库状态可运行。

#### Scenario: 无资产运行
- **WHEN** assets/ 目录为空时运行主场景
- **THEN** 地图渲染与回显功能完全正常
