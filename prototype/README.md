# prototype/ — Godot 4 复刻原型

默认入口: school_playground.tscn（图形化学校养成试玩，2026-10-09）。独立4月第4周会话支持编班、选课、成长与MVP，再播放Chapter016/017的109页原版剧情，完成后一次推进到4月第5周。Chapter018有126页，结束后可进入原版BG002_B职务室、阅读Chapter205的32页巡逻班对白，再调整第五周教师与学生。点击「必修冒险 · 出发准备」显示当前队伍，实际冒险战斗暂未开放，授课保持锁定。存档version4兼容version1/2/3，十项指纹未改。

本轮恢复上轮真实CPU检查点，完整复核学校学生落点后，从468A49执行搜索结构、单位/显示索引、scratch与分类链表，部署函数468910以零值自然返回4534A1。三组就绪样本实际执行新尾段；两组拒绝明确沿用上轮不可变证据，没有重跑全部上游。下一467AA0、事件VM和本周图形战斗尚未完成。

独立原EXE规则核对7块589824字节缓冲、完整搜索包装器、所有非空单位工作区、分类链表及scratch，保留原落点/占格/记录/资源。Python193项、Godot62套件409项、严格规格30项通过；355个历史/运行时/界面/素材文件和十项v4存档指纹保持原字节。本轮画面未改。

[本轮部署尾段验收](../analysis/school-deployment-tail-final-20261011/README.md) · [来源边界](../docs/school_deployment_tail.md) · [前轮学生落点](../analysis/school-formation-placement-final-20261011/README.md) · [地图查看](../analysis/school-scene-resources-final-20261009/README.md) · [试玩操作](../docs/school_playground.md)。75项完成，仅为已规划阶段，本地提交未push。下一步继续467AA0、调用者初始化和事件VM，再接实际单位位置与学校阵容图形战斗。

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
