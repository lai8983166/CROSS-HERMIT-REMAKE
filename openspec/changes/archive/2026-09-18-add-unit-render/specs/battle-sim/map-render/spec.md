## MODIFIED Requirements

### Requirement: 三层占位渲染
主场景加载 map01.json 并渲染全图菱形格：每格底色 = 层0(terrain) 值经固定调色板映射；层1(variant) 非零时按值微调明度（可视觉区分变体）；层2(object) 非零时格子加亮色描边。渲染覆盖全部 64×96 格，帧率可交互（≥30fps 窗口模式）。

**变更**: 保留全部既有行为，另需在地图之上绘制战斗层——存活单位以阵营色菱形标示（死亡变暗、撤退半透明），头顶绘制 HP 条与 ENGAGE 条；地图渲染性能要求不变。

#### Scenario: 全图渲染
- **WHEN** 窗口运行主场景
- **THEN** 可见 64×96 格完整地图，不同 terrain 值呈现不同底色，object 格有描边标记，战斗单位覆盖其上

#### Scenario: 战斗状态可视化
- **WHEN** 战斗进行中
- **THEN** 每个存活单位头顶可见双条（HP 红/ENGAGE 蓝），HP 变化与移动可肉眼追踪；dead 单位暗色遗留、withdrawn 单位淡出

### Requirement: 点选回显
鼠标点击/悬停格子在 HUD 显示：格坐标 (x, y) 与三层值 terrain/variant/object。屏幕外点击无效。

**变更**: 点击命中单位时，HUD 额外显示该单位摘要（阵营/职业/等级/HP/MP/ENGAGE/状态）；格子回显行为保留。

#### Scenario: 点击单位
- **WHEN** 点击一个存活单位
- **THEN** HUD 同时显示其所在格三层值与单位摘要，数据与 battle_setup + 派生值一致

#### Scenario: 战斗结束显示
- **WHEN** 一方全灭
- **THEN** HUD 显示胜负阵营与总 tick 数，`R` 键以新种子重开
