## Purpose

地图逻辑层的基础可视化：把三层格值以占位视觉（调色板+明度+描边）渲染到窗口，并提供点选回显——sim 第一个"能看见"的界面，供数据核对照用。

## Requirements

### Requirement: 三层占位渲染
主场景以**底图层 + 战斗层**两级渲染。底图层三态（`T` 键循环）：①纯贴图（assets 图集）②贴图 + 数据层半透明叠加（terrain 调色板/object 描边，alpha 约 0.45）③纯数据色块（现状行为）。数据层的 terrain 调色板/variant 明度/object 描边规则不变；贴图缺失时自动回退③并提示。渲染覆盖全图，帧率可交互（≥30fps）。

#### Scenario: 三态切换
- **WHEN** 窗口运行中按 T
- **THEN** 底图在 纯贴图→叠加→纯数据 间循环，单位/HUD 不受影响

#### Scenario: 贴图缺失回退
- **WHEN** assets 图集不存在时启动
- **THEN** 自动使用纯数据视图并在 HUD 提示，无报错

#### Scenario: 战斗状态可视化
- **WHEN** 战斗进行中（任一底图态）
- **THEN** 单位/双条/死亡淡出正常显示于底图之上

### Requirement: 点选回显
鼠标点击/悬停格子在 HUD 显示：格坐标 (x, y) 与三层值 terrain/variant/object。屏幕外点击无效。

**变更**: 点击命中单位时，HUD 额外显示该单位摘要（阵营/职业/等级/HP/MP/ENGAGE/状态）；格子回显行为保留。

#### Scenario: 点击单位
- **WHEN** 点击一个存活单位
- **THEN** HUD 同时显示其所在格三层值与单位摘要，数据与 battle_setup + 派生值一致

#### Scenario: 战斗结束显示
- **WHEN** 一方全灭
- **THEN** HUD 显示胜负阵营与总 tick 数，`R` 键以新种子重开

### Requirement: 渲染不依赖美术资产
本能力仅使用程序化绘制（draw_*），不加载任何原版纹理——保证 sim 在无素材仓库状态可运行。

#### Scenario: 无资产运行
- **WHEN** assets/ 目录为空时运行主场景
- **THEN** 地图渲染与回显功能完全正常
