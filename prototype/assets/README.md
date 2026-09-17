# assets/ — 离线转换素材

| 文件 | 来源 | 再生成 |
|---|---|---|
| `map01_atlas.png` | MAP01.MAP 48 页纹理 (B 线算法, 页起 0x4D8 行优先) | `python tools/render_map_atlas.py 01` |
| `map01_atlas.json` | 上述产物元数据 (来源/页布局/格式) | 同上 |
| `map02_atlas.png` | MAP02.MAP 108 页 (页起 0x5C8 — 修正 B 线旧记录 0x404 误判) | `python tools/render_map_atlas.py 02` |

- 像素格式 X1RGB555（bit15 alpha 忽略，地图页实测 100% 不透明）
- 页起点检测 = 首 256 u16 全不透明严门 + 末页同检（表区小整数过不了门；行相关与 BMP 缩略相关均无判别力——两次误检教训见 render_map_atlas.py 注释）
- **基准测试注意**: 无头/被遮挡窗口会被 DWM 节流至 ~13fps，属假象；性能测量需窗口前台
