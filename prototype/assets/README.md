# assets/ — 离线转换素材

| 文件 | 来源 | 再生成 |
|---|---|---|
| `map01_atlas.png` | MAP01.MAP 48 页纹理 (B 线算法, 页起 0x4D8 行优先) | `python tools/render_map_atlas.py 01` |
| `map01_atlas.json` | 上述产物元数据 (来源/页布局/格式) | 同上 |
| `map02_atlas.png` | MAP02.MAP 108 页 (页起 0x5C8 — 修正 B 线旧记录 0x404 误判) | `python tools/render_map_atlas.py 02` |

- 像素格式 X1RGB555（bit15 alpha 忽略，地图页实测 100% 不透明）
- 页起点检测 = 首 256 u16 全不透明严门 + 末页同检（表区小整数过不了门；行相关与 BMP 缩略相关均无判别力——两次误检教训见 render_map_atlas.py 注释）
- **基准测试注意**: 无头/被遮挡窗口会被 DWM 节流至 ~13fps，属假象；性能测量需窗口前台

## 定性 (2026-09-18 缝分析)

图集 = **贴图素材库**，非地图碎片拼图（行/列优先缝差 5242~5769 vs 页内基线 990，任何矩形拼法不连续）。
世界画面 = BIN 三层(疑贴图索引)驱动 UV 采样 → 见后续 add-map-composition。

## 直角投影定案 (2026-09-18, add-map-composition)

- **图集即世界图**（2048×1536 == px 头），格 (x,y) = 像素矩形 [32x,16y,32,16]
- 证据：引擎线性整除 (x>>21/y>>20) + BMP 宽高比 + iso 8 朝向相关全灭 (≤0.113 vs 0.488)
- `map01_composed.png` = 直角世界图（现与图集恒等；后续层烘焙扩展点）；再生成 `python tools/compose_map.py 01`
- 原"菱形坐标投影"为误读，已在 SimMapData/main.gd 修正；"菱形观感"来自贴片绘制
