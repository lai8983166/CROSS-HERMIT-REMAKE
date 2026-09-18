## Purpose

把 MAP##.MAP 48 页 X1RGB555 纹理变成重制的世界底图：图集解码、世界布局定案（直角/行优先/恒等）、
sim 视图的贴图态与视口操作。三重定案证据（引擎公式 43eba0/43d9a0、BMP 页级匹配 0.57~0.92、
实机截图 NCC 复核）记录于 analysis/map_window_match.md 与 formats.md §5。

## Requirements

### Requirement: 图集解码
`tools/render_map_atlas.py` 从 MAP##.MAP 的 DX 纹理表（@+0x404，`{u32 表长; u32 count; u32 offs[count]}`，
每条目 12B 头 `"DX\2"+256×4` + 0x20000B X1R5G5B5 像素）解出 count 张 256×256 页，行优先拼合为
`assets/map##_atlas.png`。页起点检测 = 连续 256 u16 全 bit15 置位（严格门限）。

#### Scenario: 解码 MAP01
- **WHEN** 运行图集渲染工具
- **THEN** 产出 2048×1536 图集（48 页），页内容与实机画面逐块可对照

### Requirement: 世界图合成（恒等定案）
`tools/compose_map.py 01` 产出 `assets/map01_composed.png` 与元数据 json（projection、
verified_window、evidence、regen）。**世界图 == 图集恒等**（引擎绘制为全图线性 UV，
无页使用表/无素材复用），本工具留作管线锚点（后续雾/阴影烘焙的扩展点）。

#### Scenario: 再生成
- **WHEN** 运行 `python tools/compose_map.py 01`
- **THEN** 产出合成图与元数据；verified_window 来自实机验证结论（数据驱动，不在视图硬编码）

### Requirement: 视图贴图态与视口
main.gd 底图三态（T 循环）以合成图为贴图态；默认视口 = 元数据 verified_window；
支持滚轮缩放（以鼠标为中心）、中键拖拽平移、F 复位视口。合成图/图集缺失时回退纯数据视图并提示。

#### Scenario: 默认视口
- **WHEN** 窗口启动（合成图存在）
- **THEN** 初始视口对准实机验证窗口（≈引擎 1024×568 视口），非全图缩放

#### Scenario: 视口操作
- **WHEN** 滚轮/中键拖拽/F
- **THEN** 分别缩放/平移/复位，无错乱

### Requirement: 布局可验证
图集行优先布局的正确性可由仓库内资料复核：BMP 页级匹配、实机截图 NCC、引擎公式三方一致；
对照结论（差异=单位/水晶塔/阴影/UI 动态层缺失，非布局错误）记录于 analysis/map_window_match.md。

#### Scenario: 文档一致
- **WHEN** 查阅 formats.md §5 与 analysis/map_window_match.md
- **THEN** 布局定案、悬案清算（无页使用表/无尾部/镜像与 Morton 否定）均有据可查
