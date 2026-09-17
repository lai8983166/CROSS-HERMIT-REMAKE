# Tasks: add-battle-assets

## 1. 图集工具

- [x] 1.1 `tools/render_map_atlas.py`：编号参数 → 读 MAP##.MAP 头 [pageX][pageY] →
       签名扫描页起点（dist=512 相关>30% + 连续性自校验）→ X1RGB555 解码行优先拼合 →
       `prototype/assets/map##_atlas.png` + `map##_atlas.json` 元数据。
       验证：MAP01 产物与 analysis/map01_atlas.png 逐像素一致（PIL diff == 0）
- [x] 1.2 护栏：文件缺失/页数与大小严重不符 → 报错退出零产出（临时坏文件验证）

## 2. 场景接入

- [x] 2.1 main.gd：加载图集纹理（缺失→数据态+HUD 提示）；`T` 键三态循环；
       叠加态 = 贴图 + 数据层 alpha 0.45。验证：窗口 `--quit-after 300` 无错误，
       人工 T 切三态、叠加态格子与贴图对齐（黄框落在纹理图案边缘）
- [x] 2.2 性能回归: 后台遮挡窗口被 DWM 节流 ~13fps 为基准假象 (与绘制内容无关已二分验证,
       逻辑层 0.05ms/tick); 前台帧率以用户目测为准 (task 3.2)

## 3. 收尾

- [x] 3.1 全量测试绿 + assets/README（来源/再生成/坐标系说明）。
       验证：runner 0 failures；README 含再生成命令
- [ ] 3.2 用户目检：窗口认出原版 MAP01（与 analysis/map01_atlas.png 同图）、三态切换、
       战斗照常进行。验证：用户确认
- [x] 3.3 提交 cd258f6 (含 atlas PNG/JSON/README)
