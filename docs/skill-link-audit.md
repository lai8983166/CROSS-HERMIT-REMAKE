# 技能编号关联审计（第一步）

`python tools/skill_link_audit.py 22 --unit C0A --direction N` 将同一个技能 ID 的攻击表行、演出表行、指定单位/朝向的动作映射，以及 EFCT 全局动画 ID 放在一份只读报告中。原始输入分别是 `prototype/data/attack_table.json`、`skill_visuals.json`、`unit_sprites.json`、`attack_effects.json`。必须指定单位资源包，以免误把某个单位的动作映射当成所有角色通用。

报告中的 `hit_effect` / `gameplay_effect_id` 是玩法效果编号，**不是** EFCT 动画编号。`effect_id_matches_attack` 只检查两份导出表的一致性，不证明效果分发语义。`targeting` 与 `target_filter` 保留原值，不在这里推断敌我性质。

状态含义：

| 状态 | 含义 |
| --- | --- |
| `exported` | 当前 Godot 资源 JSON 已包含这个动作方向或 EFCT 动画 |
| `valid_not_exported` | 全局 EFCT ID 在原资源程序块范围内，但尚未导出到 Godot |
| `not_exported` | 单位动作 ID 没有当前导出器提供的映射；不能据此断定原版没有该动作 |
| `no_exported_direction` | 动作有映射槽，但该单位该方向没有导出条目；可能是空槽，也可能仍需核实 |
| `outside_archive` | 全局 EFCT ID 越过目前解析到的程序块边界 |
| `none` | 表中编号为零 |

目前这个工具只审计已有导出链，**不**证明技能调度时序、EFCT 的施放位置、目标阵营、伤害生效时刻，也不替代实机差分。它的直接用途是定位编号关联的断点：例如技能 22 的 `2044`/`2029` 属于有效但未导出的 EFCT 动画，而 action 31 在当前单位动作导出中没有映射；action 13 的北向映射在 C0A 有、D0A 没有，因此不能跨单位直接套用。

## 原版动作号的两级查表

`python tools/unit_action_table.py 31 --type-index 0` 可直接从 `analysis/hermit_game.exe` 解出原版的动作/方向表。`0x464D70` 按单位类型索引取得动作表指针 `0x60E850[index]` 和程序表指针 `0x60F070[index]`。`0x465040` 再以 `action * 8 + 0x610510[direction]` 读动作表的二字节记录：第一字节是程序表索引，第二字节低两位是镜像标志。程序表的 16 位值高字节为动画块号、低字节为动画号，然后交给 `0x409FF0` 播放。

标准类型索引 0 的 action 31 八方向分别指向 **block 1 的动画 6～10**，不是 block 0 的 151～155。类型索引 17/18 共用动作表，但换用另一程序表，action 31 指向 **block 0 的 101～105**。现阶段没有证明这些运行时类型索引分别对应哪个 `A0A`～`E1A` 单位资源包，因此解析器要求显式输入 `--type-index`，不能把这两个编号体系直接合并。此前 `unit_sprites.json` 只导出了 block 0 时间线；要支持 action 31，先要查清运行时类型到资源包的关系，并让导出器能读取所需动画块。
