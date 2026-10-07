# prototype/ — Godot 4 复刻原型

默认入口: `school_playground.tscn`（图形化学校养成试玩，2026-10-08）。四位原版角色头像、五班编成、课程卡片、成长与MVP结果，使用独立4月第4周会话。点击「授课安排」选课，再按底部按钮依次结算、确认、评选MVP。自动保存，顶部可保存/读取/确认重开；本段完成后停在待接入剧情，日历不推进。

[操作与存档说明](../docs/school_playground.md) · [最终截图与验收](../analysis/school-playground-final-20261008/README.md)。全量56套件371项通过。

「战斗预览」打开旧 `main.tscn`（MAP01底图、红蓝实时互殴、点选、速度档及研究窗口），右上返回学校试玩。研究窗口的新局/旧返回数据与默认试玩独立。直接运行旧场景：`~/bin/godot --path prototype res://main.tscn`。

操作: `[1/2/3]` 速度 `[空格]` 暂停 `[R]` 新种子重开；点击单位看摘要、点击空地锁格看三层值。

数据来源: `python tools/map_export.py 01` → `data/map01.json`（游戏目录不入库，JSON 入库）。
调色板: `data/terrain_palette.json`（占位语义，直接改颜色即可换肤/魔改）。
可行走规则: `data/walk_rules.json`（占位=object≠0 阻挡；实机对照后改表即改通行语义）。

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

## 战后返回基线 (2026-10-05)

`sim/tests/test_battle_campaign_replay.gd` 已使用实际Battle终局和明确提供的原版场景5回放输入，验证共享目录的评分/成长包/战利品→角色战果→剧情入学→完整周结算→职务室→学校数据初始化。两条源子程序11/8路径的完整角色与学校快照均与同CPU原版报告一致，重复送达不重发奖励或结算；本地伤害、HP和winner不代替原版事件/结果输入。

运行全部离屏测试：

```bash
~/bin/godot --headless --path prototype -s res://sim/tests/test_runner.gd
```

当时39套件284项Godot测试通过；Python279项已于返回变更13/13验收时通过。主窗口“返回流程演示”变更3/3完成：选择两条源路线之一，运行本地战斗、确认战果，再浏览学校学生名单和详情。可重开或返回默认战斗，操作说明见 [返回流程演示](../docs/campaign_return_ui.md)。这是有来源的数据演示，教师课程、编班/排课、完整战术VM和存档仍未开放，完整学校就绪标记保持false。完整来源及边界见 [战斗返回审计](../docs/battle_return_audit.md) §57–69。
