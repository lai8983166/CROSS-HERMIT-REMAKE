# 原场景4终局选择

`connect-original-terminal-selection`接续[自主致死](battle_lethal_combat.md)。输入为已接受案例的完整38拥有区，而非只抄死亡标记；新增首根前声明为场景4、正常/到时时间、T0004原文件、VM/脚本工作区和一致的任务内嵌UnitCtrl布局。它是明确的完整内存输入实验，不是恢复旧CPU、原加载或原生外层并行调度同寿命。

原432100先检查脚本忙/网络门，执行430FE0单位统计，然后按场景4调用433720。无敌对存活优先，再检查经过时间和己方伤亡；否则先检查是否到时，再检查己方全灭。原454AB0/454AF0选择条件/终局脚本，原455060/4214F0实际读取T0004两级目录，原4551C0执行条件VM，原4549D0绑定终局脚本及暂停字段，原454AF0最终从原表60CA7C写TASK+174。未手填选择，也未把条件VM固定返回真。

本次条件路径为原opcode167读工作模式、8比较、166设返回、11跳转、19结束；独立解释器从原字节推导五条指令、分支和结果。终局展示脚本只绑定，尚未推进其对白、淡入淡出或任务退出；之后另有明确473860根，把实际选择及原交战计数写入结果页。奖励发放仍待验。

正常剩余时间36000与到时0均为声明输入，经过时间0；不能称原战斗计时已接通。原任务调用以`TASK+190`作为UnitCtrl，因此本实验将任务前缀放在当前CTRL前190字节，并将反向任务指针指向它；旧独立TASK内存保持。任务前缀原输入、字段声明和所有其它38区字节均可检查。

原代码191000字节和IAT页前后逐字节核对，不改原导入目标。lstrcmpA通过原地址调用实际Windows接口；GetTickCount首次实际采集，完整新实例重放明确使用该采集时间。原VM的14..55线程标志字段包含主9400区以外的short，按原地址声明拥有并逐字段开放写入；没有跳过初始化。原音频停止体40D120执行已有空接口分支，不使用固定结果桩。

独立预测范围为场景条件、五条条件指令、目录选择、完整任务前缀、战斗记录保持及整个结果页；全VM内部字节、所有拥有内存/57项CPU/每条原指令和写入由完整重放核对，不冒称独立逐字节VM/世界模型。无需解锁或OS输入，不改Godot、冻结工具、存档和私有检查点。R3/R4/R5/R6均未整体完成，2026-11-20目标不变。

## 重放

输出路径必须未存在：

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.battle_terminal_selection_emulation --out analysis/battle-terminal-selection-source-v3-20261025.json.gz
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.battle_terminal_selection_verification --report analysis/battle-terminal-selection-source-v3-20261025.json.gz --out analysis/battle-terminal-selection-proof-v1-20261025.json
```

早期未知依赖/拥有范围/布局/根返回观察问题均留存explore诊断；正式来源v3附原代码/IAT身份，v1/v2为先前完整执行采集，不能混为全部正式验证已通过。

## 实测结果

八例共327779条原指令、126367次原写入、35条条件VM指令和14次实际Windows API叶调用。45拥有区、57项所记录CPU、完整调用与每条原PC/写入的新实例重放全部一致；34项专项和71项相关回归通过（105项）。前驱702项为已冻结基线，本轮没有重跑全部661项旧世界回归。

| 交战快照 | 正常计时选择/脚本 | 到时选择/脚本 |
| --- | --- | --- |
| 敌方死亡 | 1 / 2 | 1 / 2 |
| 玩家死亡 | 5 / 14 | 4 / 11 |
| 玩家保命阈值1 | 0 / 无终局请求 | 4 / 11 |
| 中性且双方存活 | 1 / 2 | 1 / 2 |

无敌对存活的判定先于到时，因此敌方死亡和中性案例的到时对照仍选1；有敌对时，到时先于玩家全灭，故玩家死亡的到时对照选4。正常玩家存活/敌对存活保持0。结果整理同时保留实际玩家击杀1/贡献20或死亡1，己方分数分别20/0。

正式[source-v3](../analysis/battle-terminal-selection-source-v3-20261025.json.gz)、[独立规则与完整重放](../analysis/battle-terminal-selection-proof-v1-20261025.json)、[最终验收](../analysis/battle-terminal-selection-acceptance-v1-20261025.json)。选择生成已验不等同终局演出、奖励或R5整体完成。
