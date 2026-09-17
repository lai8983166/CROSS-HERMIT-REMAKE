# Proposal: add-battle-assets

## Why

观感里程碑：战斗模拟器逻辑已完整（公式/循环/寻路），但画面是占位色块。把 MAP01 的**原版纹理**
接进来——B 线逆向已验证的 48 页图集渲染算法工具化后，战斗背景立刻变成原作地图，sim 首次
"看起来像那个游戏"，同时保留数据层视图用于核对。

## What Changes

- `tools/render_map_atlas.py`：解析 `MAP##.MAP`（页定位=行优先，B 线已实证）→
  `prototype/assets/map##_atlas.png`（pageX×256 × pageY×256，X1RGB555 解码）
- `main.gd`：图集作为底图接入既有烘焙纹理管线；`T` 键三态切换
  **[纯贴图 → 贴图+数据层半透明叠加 → 纯数据色块]**；单位/战斗/HUD 层永远在最上不受影响
- `prototype/assets/README.md`：素材来源与再生成命令
- 不含：单位形象（原作单位是 D3D 3D 模型，无 2D 帧可提——占位菱形保留，立绘/模型方案后续
  独立 change）、UI 皮肤、音频、地图卷动

## Capabilities

### New Capabilities
- `assets/map-atlas`: 原版 MAP 纹理图集的离线渲染工具与产物（页定位/解码规则固化，可再生成）

### Modified Capabilities
- `battle-sim/map-render`: 底图层三态（贴图/叠加/数据），贴图缺失时自动回退数据视图

## Impact

- 新文件：`tools/render_map_atlas.py`、`prototype/assets/map01_atlas.png`（~2-4MB PNG 入 git）、
  `prototype/assets/README.md`
- 修改：`main.gd`（底图来源与 T 键）
- 依赖：MAP01.MAP（游戏目录，.gitignore）——产物 PNG 入库后 sim 不依赖游戏目录
- 风险：图集是"表现图"而非"逻辑图"，格坐标系与贴图像素的对齐（32×16 菱形 vs 矩形页）需在
  叠加态校验——数据层与贴图层坐标同源（同一 world 坐标系），理论上自然对齐
