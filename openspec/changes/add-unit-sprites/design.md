## Context

地图底图已定案（add-map-composition），剩余与实机的视觉差距集中在单位层。资源侧已知：
- `DATA/DxAnim/` 53 文件：头 `{u32 总长; u32 块数(9); u32 44; u32 偏移表}`（01E 实测；
  EFCT 为 7 块嵌套子表，格式记忆里有案）。`##E.BIN`（01E..08E）疑按单位编号，E0A/E1A 特殊。
- `DATA/TACTICS/UNITPAL.BIN` = 70×1024B = 70 条 256×4B(BGRX, 0 号透明黑) 调色板。
- sim 侧：BattleUnit 有状态机（IDLE/MOVE/ATTACK/DEAD）与朝向（移动方向），渲染现为色块。

## Goals / Non-Goals

**Goals**: DxAnim 容器级+像素级格式定案（或显式开口）；帧资产管线；sim 精灵渲染+回退；数据驱动可魔改。
**Non-Goals**: 特效（EFCT）解码；攻击/受击特效播放；单位头像/UI 框（后续 change）；8 向朝向的
精确语义若数据推不出，用"移动方向→最近朝向"近似并记开口。

## Decisions

1. **容器解析复用 §2 档案容器惯例**（`{len; n; offs[]}`），块内结构按 01E 实测的
   `帧头数组 + 像素区` 假设族验证（帧宽高/stride 从块头推；8bpp 假设用直方图+调色板相关性验证，
   对照 UNITPAL 上色后视觉合理性）。多假设并用、目检裁决——沿用 add-map-composition 方法论。
2. **资产布局**：`assets/unit/<容器名>/<序列>_<n>.png` + `data/unit_sprites.json` 单一帧表
   （含调色板 id/锚点/朝向映射）。魔改约束：换 PNG/改表即生效，工具与 sim 都不写死常量。
3. **sim 集成**：main.gd 增 `_draw_sprites()`（在单位色块绘制处分支），帧推进用已稳定的
   `_accum`/LOGIC_STEP 时基；朝向由 `u.facing`（BattleUnit 新增，移动向量 8 向量化）驱动。
   动画序列映射表放 `data/unit_sprites.json` 的 `anim_map`（状态+朝向→帧前缀），不进代码。
4. **回退优先**：帧表缺序列/资产缺失 → 色块路径原样保留（无资产可运行约束）。
5. **阴影**：draw_ellipse 软阴影近似原版印章语义（43d270），不做逐像素复原。

## Risks / Trade-offs

- DxAnim 像素若为分块/行程编码，8bpp 直读会花屏 → 假设族验证阶段就要拦截，必要时只出容器
  结构分析、帧资产降级为开口项（不阻塞 sim 回退路径）。
- 锚点字段若不存在 → 默认"脚底=帧底中点"，视觉误差记开口。
- 01E..08E 只有 8 个编号 vs 30 职业/更多单位 → 单位↔动画映射表先按"battle_setup 可指定
  anim_id"处理，默认取 01E。

## Open Questions

（无——容器/像素疑点按上述方法论处理，推不出的一律显式开口，不需要用户裁决的点）
