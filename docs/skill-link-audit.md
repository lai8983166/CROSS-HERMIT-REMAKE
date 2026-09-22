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

`0x466C80` 用单位序号 `param_2` 在 `0x610538 + param_2*8` 取 `data\\DxAnim\\*.bin` 路径，同时把 `param_2 + 8` 交给 `0x464D70` 选择动作表。因此现在可以通过 `python tools/unit_action_table.py 31 --archive C0A` 直接查询资源包的原版动作映射。十个映射是：B0A=9、B1A=10、A0A=11、A1A=12、C0A=13、C1A=14、E0A=15、E1A=16、D0A=17、D1A=18。

查询同时检查对应原始 BIN 中每个动画块/程序号是否真的存在，返回 `program_present` 与 `all_programs_present`。存在只代表素材可解析，不代表该单位在游戏中一定会施放这个技能。

C0A 等常规单位的 action 31 八方向指向 **block 1 的动画 6～10**，不是 block 0 的 151～155。D0A/D1A 共用动作表，但换用另一程序表，action 31 指向 **block 0 的 101～105**。对原始 BIN 的程序块数量检查也与此吻合：C0A block 1 有 31 条程序，D0A block 1 仅 1 条但 block 0 有 121 条。不过 E0A 的 block 1 只有 1 条程序，不能播放表中 action 31 对应的 6～10；查表结果不能单独证明动作可用。此前 `unit_sprites.json` 只导出了 block 0 时间线；后续需要按资源包对应的原版查表结果和该 BIN 实际程序数量选择动画块，不能给所有单位套用同一套动作号公式。
