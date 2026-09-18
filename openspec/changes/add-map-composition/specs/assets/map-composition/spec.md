## Purpose

把"图集=贴图素材库"的定性转化为可执行合成：解出 BIN 层值到图集贴片的映射，逐格合成世界布局图——sim 的真·原版底图，以及三层语义的定案载体。

## ADDED Requirements

### Requirement: 层值→贴片映射
合成工具内建一份**数据驱动的映射规则**（层值 → 图集页内贴片坐标），规则来源为对 MAP01.MAP 头部索引表（255×4B）与步长表（53×(u16,u16)）的结构分析；映射可整体替换（JSON/常量表），改映射不改合成逻辑。

#### Scenario: 映射可执行
- **WHEN** 以默认映射运行合成
- **THEN** 每个非零层值格都能取到图集内一块确定贴片（越界/缺映射值记日志并跳过）

### Requirement: 世界布局合成
`compose_map.py` 读取 `data/map01.json` 三层 + `assets/map01_atlas.png`，按映射逐格贴片为菱形交错世界布局，输出 `assets/map01_composed.png`（含元数据 json）。宏观结构与游戏回退 BMP 对应：按"道路/建筑/开阔区"可辨认布局评估。

#### Scenario: 合成 MAP01
- **WHEN** 运行 `python tools/compose_map.py 01`
- **THEN** 产出合成图与元数据；与回退 BMP 缩略相关度 ≥ 0.5（超过素材平铺基线的可辨性）

#### Scenario: 宏观布局可辨
- **WHEN** 人工比对合成图与回退 BMP
- **THEN** 能辨认出对应的大块结构（如同一片建筑群/道路走向），用户确认

### Requirement: 三层语义收敛
映射定案过程产生的新认知写入 `docs/formats.md` §5（哪层选贴图/变体/物件）；数据无法定案的部分明确列为开口项（需实机截图对照），不猜测。

#### Scenario: 文档更新
- **WHEN** change 完成
- **THEN** formats.md §5 的 BIN 三层描述被更新为"定案语义"或"收敛假设+开口标注"之一
