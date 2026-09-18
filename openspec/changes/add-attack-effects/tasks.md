# Tasks: add-attack-effects

## 1. 导出管线

- [ ] 1.1 抽 tools/dxanim_lib.py（容器/BMP/块0 记录/块5 锚点），unit_anim_export
       改调用。验证：unit 侧全量导出与重构前 diff 一致
- [ ] 1.2 tools/fx_export.py：01E → assets/fx/01E/ + data/attack_effects.json
       （PLAY 播一次序列挑选）。验证：帧数与容器一致、PLAY 引用界内
- [ ] 1.3 formats.md §10 补 ##E 播一次序列结构行。验证：无待定表述

## 2. 事件与播放

- [ ] 2.1 battle.gd：fx_events typed 数组 + _attack 挂点（from/to/hit/damage）。
       验证：既有测试全绿（逻辑零改动）
- [ ] 2.2 main.gd：特效表并入注册表 + 播一次绘制（锚点目标格心/方向翻转/帧号淘汰）。
       验证：窗口攻击时目标格播斩击一次
- [ ] 2.3 配置：attack_effects.json {effects, default} + battle_setup 职业覆盖。
       验证：改 default 即换特效；删表无报错

## 3. 回归与验收

- [ ] 3.1 测试：特效表加载/PLAY 序列有效/事件字段/回退 + 全量 runner 绿。
       验证：0 failures
- [ ] 3.2 用户目检：攻击命中目标格播原版斩击，播完消失。验证：用户确认
- [ ] 3.3 提交 + 归档
