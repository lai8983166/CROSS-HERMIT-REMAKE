## MODIFIED Requirements

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
