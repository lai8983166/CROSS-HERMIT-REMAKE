## Why

地图底图已三重定案（add-map-composition），但实机画面与 sim 视图的剩余差距主要来自**单位层**：
sim 里单位还是程序化色块，实机是带朝向动画的精灵。缩小"和实机差距"最直接的一步就是把
DATA/DxAnim/ 的单位动画与 UNITPAL.BIN 调色板解出来，让 BattleUnit 显示原版精灵。

## What Changes

- **逆向定案**：DxAnim 容器格式（`DATA/DxAnim/*.BIN` 53 文件，头 `{u32 总长; u32 n块; 偏移表}`；
  `##E.BIN` 疑按单位编号、E0A/E1A 特殊、EFCT 特效）——块结构、帧像素格式（疑 8bpp 索引 +
  UNITPAL 70×256 调色板绑定）、朝向/帧序列组织。定案写入 docs/formats.md 新 §。
- **导出工具** `tools/unit_anim_export.py`：DxAnim 容器 → `prototype/assets/unit/*.png`（帧序列，
  含元数据 json：帧尺寸/锚点/朝向表/调色板 id——锚点从数据推，推不出记开口）。
- **sim 渲染**：`BattleUnit` 增加精灵渲染路径——按朝向（移动方向）与状态（待机/移动/攻击/死亡）
  选帧序列循环；保留色块回退（无资产可运行约束不变）。
- **脚底阴影**：椭圆软阴影（近似 43d270 印章语义），精灵落地感。

## Capabilities

### New Capabilities
- `assets/unit-sprites` — DxAnim 解码/导出管线与精灵资产格式（数据驱动：帧表/锚点/调色板映射全部 JSON）

### Modified Capabilities
- `battle-sim/unit-render`（现 map-render 内"战斗状态可视化"的扩展）— 单位由色块升级为
  原版精灵帧动画 + 阴影，色块降级为回退路径

## Impact

- 新增 `tools/unit_anim_export.py`、`prototype/assets/unit/`、`prototype/data/unit_sprites.json`
- `prototype/sim/battle_unit.gd` / `prototype/main.gd` 渲染路径扩展；测试补帧选择/回退用例
- 风险：DxAnim 帧像素若非简单 8bpp（如行程编码/分块），导出器需多假设对比——容器级（头/偏移）
  与像素级分开定案，像素级推不出时按开口处理、先上锚点居中的近似渲染
