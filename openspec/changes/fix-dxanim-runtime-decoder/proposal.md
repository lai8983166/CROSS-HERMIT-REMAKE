## Why

当前 DxAnim 导出把 10B 指令中的打包描述符误当作 BMP 帧号，并把方向表的镜像位误当作
容器块号；因此单位移动虽然索引合法、测试全绿，实际播放的图片、方向和时长仍与原版不符。
共享解码器也被攻击特效使用，必须在继续目检和归档特效变更前修正数据模型。

## What Changes

- 按原版运行时链解码块0指令：提取每个逻辑帧最多四个 12 位描述符，经块4解析最终图片、
  偏移、绘制属性与时长，不再使用 `frame=-b` 的近似。
- 按移动调用方的动作号 `no=3` 和引擎方向表生成八向移动映射；动画号直达块0 #11～#15，
  表项第二字节低两位保留为水平/垂直镜像标志，不再伪造 `+5` 或块1路径。
- 为复合动画保留并行图层语义：opcode 1 生成块3子动画，禁止把子动画串行展平成单帧序列。
- 视图按动作/方向切换重置播放相位，并能绘制一个逻辑帧的多图层及各自偏移。
- 重新导出单位与攻击特效数据；用 A0A、B1A 原始字节到最终帧号的黄金样例覆盖方向、镜像、
  描述符、时长和边界回退。
- 修正文档中已被反汇编推翻的“no=2、+5、off=块1、块1串行展平”等结论。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `assets/unit-sprites`: 将 DxAnim 序列、八向移动选择和运行时播放契约改为与原版描述符链一致。

## Impact

- `tools/dxanim_lib.py`、`tools/unit_anim_export.py`、`tools/fx_export.py`
- `prototype/data/unit_sprites.json`、`prototype/data/attack_effects.json` 及对应导出资产
- `prototype/main.gd` 的序列选择、镜像、相位和多图层绘制
- `prototype/sim/tests/test_unit_sprites.gd` 与导出器侧黄金验证
- `docs/formats.md` 的 DxAnim 格式结论
- 进行中的 `add-attack-effects` 需在本变更完成后重新目检；本变更不处理独立的战斗双扣血问题
