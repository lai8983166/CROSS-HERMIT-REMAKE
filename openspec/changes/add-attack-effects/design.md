## Context

单位精灵与换色已落地。侦察（2026-09-18）：01E.BIN 与单位档同容器 9 块格式
（块0 #1..#121 = 9 记录播一次序列：首帧 dur20 + 6 系列帧；块5=帧数×8 ✓；
块6=98 帧 BMP；块7=6 张换色板）。battle.gd `_attack()` 现成挂点。

## Goals / Non-Goals

**Goals**: ##E 导出管线（解码库复用）；攻击 typed 事件流；视图播一次演出；
配置驱动（全局默认 + 职业覆盖）；回退完备。
**Non-Goals**: ##E 动画语义标注（哪档哪条=何种斩击/魔法，默认映射可配置，标注开口）；
特效换色（块7×6 的选择规则，开口）；受击闪白/击退等反馈（后续 change）；
魔法/技能特效区分（统一一个默认特效）。

## Decisions

1. **抽 `tools/dxanim_lib.py`**：容器解析（含空块/自洽校验）、BMP 帧解码、块0 记录
   解析（控制记录跳过规则）、块5 矩形/锚点——unit_anim_export 与 fx_export 共用。
   重构验证：unit 侧全量导出 diff 一致（管线不回退）。
2. **特效帧表并入 `_unit_sprites` 注册表**（attack_effects.json 与 unit_sprites.json
   同 schema）：`_frame_tex`/缓存/换色路径零改动即复用；特效档名与单位档名
   （如 01E vs A0A）天然不冲突。
3. **播一次语义**：视图按 `battle.frame` 快照事件 → 实例 {anim_id, cell, flip,
   born_frame}；绘制时 phase = (battle.frame - born_frame)×LOGIC_STEP，超过序列总长
   即不画（无需删除列表——帧号淘汰，停机回看也不残留）。事件只保留最近 N 条
   （N 取自配置，防长战内存涨）。
4. **事件即数据**：fx_events 字段含 from/to 格、hit、damage——MISS 也播（错位斩击
   是原版演出的一部分），特效选择不依赖 hit。
5. **锚点/翻转**：特效画布底中对目标格心（与单位同规则）；from→to 的 x 分量符号
   决定水平翻转。dy 不镜像（素材语义未定，开口）。

## Risks / Trade-offs

- ##E 语义未标注 → 默认 01E#1（9 帧斩击，首帧 dur20 视觉上是"定格起手"）；换档
  改 JSON 即可。
- 特效帧无内嵌调色板差异（块7=6 张为换色板）→ v1 用基色（BMP 内嵌），特效换色开口。
- battle.gd 增数组不动逻辑，确定性测试不受影响（事件由现有结算路径产生）。

## Open Questions

（无——语义标注/特效换色/dy 镜像均为显式开口，不阻塞）
