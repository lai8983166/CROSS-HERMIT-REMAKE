## Purpose

把 MAP 纹理页（256×256 X1RGB555）离线渲染为 PNG 图集，产物入 git、工具可再生成。

**定性修正 (2026-09-18, 用户目检+缝分析触发)**: 缝分析实证页间不连续 (行/列优先缝差 5242~5769 vs 页内基线 990) — 图集是**贴图素材库** (引擎 UV 反复采样), 不是地图碎片拼图; "矩形平铺=世界布局"假设作废。世界画面合成 = BIN 层值驱动采样的后续 change (add-map-composition)。

## ADDED Requirements

### Requirement: 图集渲染工具
`render_map_atlas.py` 接收地图编号，读取 `MAP##.MAP`：按头部 `[pageX][pageY]` 取页数，页起点用行重复签名扫描定位（或已知偏移缓存），每页 256×256 X1RGB555 解码，行优先拼合输出 `prototype/assets/map##_atlas.png`（尺寸 = pageX×256 × pageY×256）。MAP01 产出 2048×1536。

#### Scenario: 渲染 MAP01
- **WHEN** 运行 `python tools/render_map_atlas.py 01`
- **THEN** 生成 2048×1536 PNG；与既有 `analysis/map01_atlas.png`（B 线验证产物）逐像素一致

#### Scenario: 非法输入
- **WHEN** MAP 文件缺失或头部页数与文件大小严重不符
- **THEN** 非零退出码与错误信息，不产出文件

### Requirement: 产物自描述
PNG 侧附 `map##_atlas.json`（页序、来源文件、渲染参数），消费方无需读原版格式。

#### Scenario: 元数据
- **WHEN** 图集生成
- **THEN** 同名 JSON 含 source、page_layout="row-major"、pixel_format="X1RGB555"、size 字段
