# prototype/ — Godot 4 复刻原型

入口: `main.tscn`（**战斗模拟器**：MAP01 底图 + 红蓝两队实时互殴 + 单位点选 + 速度档）。

操作: `[1/2/3]` 速度 `[空格]` 暂停 `[R]` 新种子重开；点击单位看摘要、点击空地锁格看三层值。

数据来源: `python tools/map_export.py 01` → `data/map01.json`（游戏目录不入库，JSON 入库）。
调色板: `data/terrain_palette.json`（占位语义，直接改颜色即可换肤/魔改）。

## 目录

| 目录 | 用途 |
|---|---|
| `sim/` | 战斗模拟器模块（tables/unit/derive/battle_math/engage 已就位），按 openspec change 逐个扩展 |
| `sim/tests/` | 测试（自研 runner）：`~/bin/godot --headless --path prototype -s res://sim/tests/test_runner.gd`（改 class_name 后先 `--import`） |
| `data/` | 表导出 JSON（tools/table_export.py 产出）+ 地图逻辑层 + 文本池 |
| `scripts_gen/` | YBC32→GDScript 转译输出（**不手改**，工具再生成） |
| `assets/` | 离线转换素材（PNG/OGG） |

## 规格锚点（docs/REMAKE_BLUEPRINT.md）

- 格 = 32×16 px 菱形；MAP01 = 64×96 格（2048×1536 px）
- 速度档 1/2/3 ↔ `Engine.time_scale`
- 数据只读 JSON，运行时不解析原版格式

## 运行

本机 Godot 4.7.2 (winget: `GodotEngine.GodotEngine.Mono`)，bash 包装器 `~/bin/godot`：

```bash
~/bin/godot --path prototype            # 窗口运行
~/bin/godot --headless --path prototype --quit   # CI/无头校验
~/bin/godot --path prototype --quit-after 60     # 渲染 60 帧自退 (验证通过, RTX 3060 Ti)
```

exe 直达路径 (cmd 用):
`%LOCALAPPDATA%\Microsoft\WinGet\Packages\GodotEngine.GodotEngine.Mono_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_mono_win64\Godot_v4.7.2-stable_mono_win64_console.exe`
