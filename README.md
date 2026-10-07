# 超魔法大战 (Cross Hermit) 研究工作区

2002 年 EnterBrain 出品的 SRPG+养成游戏，2004 年光谱资讯繁体中文版。
本工作区用于**私下研究**：黑盒规则逆向 + 素材格式分析 + 复刻原型（Godot）。

## 当前状态 (2026-10-08)

默认启动已改为**图形化学校养成试玩**，本轮 `add-graphical-school-playground` 完成5/5。原版头像、背景、五班编成与待命区、角色能力条、三门课程、成长卡片和MVP展示已接入同一个独立第四周会话。操作顺序为编班/选课→开始授课→确认记录→评选MVP；完成后可重开比较不同安排。底层沿用已有来源规则，不复制或改写成长公式。

试玩支持自动保存、手动保存/读取、重启恢复及损坏主文件的备份恢复；重开有确认，失败时保留当前进度。存档是重制自己的版本化操作序列，恢复时重新执行并核对最终状态，不是原版SAV。顶部「战斗预览」保留原有地图/精灵战斗及研究窗口，右上「返回学校试玩」恢复保存的学校安排。战斗预览尚未与本段学校共享出战和战后奖励。

运行 `~/bin/godot --path prototype` 即可进入；操作与存档位置见[学校试玩说明](docs/school_playground.md)。最终13张截图与验收日志见[本轮验收](analysis/school-playground-final-20261008/README.md)。全量Godot56套件371项通过，新界面输入80/73/26项、实际渲染83/81/28项，旧导航22项和旧MVP窗口73项输入/73项实际渲染兼容通过。6个展示文件重新生成一致、课程说明重点与源成长表一致；OpenSpec严格27项全部通过。来源规则未变，既有Python原版执行基线保留。本轮各阶段立即本地提交，未push。

**仍待完成**：本段日期始终是声明4月第4周；没有真实新局前四周经历、MVP台词或Chapter016/017正文播放，尚不能连续推进到下一周。后续优先接入剧情展示与一次真实周推进并扩展试玩存档，再把学校阵容、可操作战斗与返回接成共享状态。完整战术AI/技能/任务事件、其他教师和全年内容仍有大量缺口。

## 规则验证基线（2026-10-07，保留来源细节）

已建立素材解析工具和Godot战斗原型。返回数据变更完成13/13；既有学校返回、排序、成员移动、新局编班、课程安排/成长/确认及本轮 `add-school-course-result-handoff` 均完成3/3，尚未归档。独立第4周示例可安排教师101的来源课程12/11/10，结算成长、确认关系/职业/本周记录，再在“授课结果”页一次性记录MVP与待播放剧情入口。普通课程10选学生3，学生3待命则选学生4；重复点击和后续编班/改课不会重选或累计次数。原第0周与示例分别保留数据，显式重开才建立新示例。日期仍为声明4/4，章节正文、真实周推进与存档尚未执行。

最新Godot全部55套件367项通过；MVP结果页73项离屏输入/78项实际渲染、确认窗口66/71、成长81/86、课程77/83、编班94/99、跨会话导航22项和旧返回两路线79项输入检查全部通过。最终26张v4截图已逐一检查；修复确认页面板底框超出768的布局问题，补充完整面板/页脚边界检查。旧返回86项渲染沿用20261006基线。OpenSpec严格检查26项全部通过。Python来源4项（152.923秒）及兼容20项（25.962秒）分别通过，合计24项；新报告、期望和运行规则逐字节再生成一致。此前55项/279项全量保留各自基线。每个小阶段验证后立即本地提交，无push。

原版隔离执行在同一CPU由来源新局、声明4/4、课程10进入完整4C1AA0，执行真实成长、MVP主/子脚本及END、确认字段、MVP次数封顶、CH003装载和ADV请求6/结束后任务7；随后真实CH003日期分派到Chapter016入口。确认按钮或MVP按键等待时不会增加次数/请求剧情，平手次序、全零与更高值选择由独立反事实探针核对。角色属性/技能/等级/成长池在MVP后保持；运行时纯模块不读取期望快照。来源/API见[授课MVP与剧情交接](docs/school_course_result_handoff.md)，最新边界见[战斗返回审计](docs/battle_return_audit.md) §100–102；既有[确认](docs/school_course_confirmation.md)、[成长](docs/school_course_settlement.md)、[课程](docs/school_course_planning.md)与[编班](docs/new_game_school_grouping.md)结论保留。

最新[结果页验收](analysis/school-course-result-result-ui-v4-20261007/README.md)、[确认兼容](analysis/school-course-result-confirmation-ui-v4-20261007/README.md)、[成长兼容](analysis/school-course-result-settlement-ui-v4-20261007/README.md)、[课程兼容](analysis/school-course-result-course-ui-v4-20261007/README.md)和[编班兼容](analysis/school-course-result-grouping-ui-v4-20261007/README.md)含截图。日志见[Godot367项](analysis/godot-regression-course-result-20261007.txt)、[Python来源4项](analysis/python-regression-course-result-source-20261007.txt)和[兼容20项](analysis/python-regression-course-result-compat-20261007.txt)；此前[55项](analysis/python-regression-new-game-school-20261006.txt)和[279项](analysis/python-regression-20261005.txt)仍是历史基线。

来源链仍待执行本4/4结果的Chapter016→Chapter017真实END，再接后继任务7的完整周推进与CH001学校交接；当前推进重点见顶部。原版终场世界/资源演出、时钟/准备初态、前驱学生模板、鼠标命中/松开和完整新局前四周仍有声明输入或边界；本地Battle伤害/HP不能派生原版事件谓词或状态11记录。原型结果页呈现MVP字段，没有播放MVP台词或Chapter016正文。旧返回示例仍为零教师目录，新局/课程示例有来源教师101。此前默认入口为战斗原型，本轮保留为战斗预览；完整战术动态、并行事件调度、旧返回会话教师迁移、完整原版学校菜单和原版存档尚未完成。以下独立工具说明各自边界，较早补充保留为历史进度；当前能力以本节和审计最新章节为准。

入口文档：

- **`docs/REMAKE_BLUEPRINT.md`** — 重制蓝图总览（按模块组织，公式结论+分档案指针）
- `docs/formats.md` — 数据格式档案（脚本 VM/地图/容器/图像/音频）
- `docs/battle_mechanics.md` — 战斗公式/AI/攻击表字段图/ENGAGE TIME
- `docs/character_growth.md` — 成长/课程/转职/道具/加成链
- `docs/battle_scripts.md` + `ybc32_opcodes.md` — YBC32 字节码档案

## 目录

| 目录 | 用途 |
|---|---|
| `analysis/` | 脱壳镜像、全量反编译（`decomp_all/` 按地址命名）、脚本反汇编语料、JSON 表 |
| `docs/` | 逆向笔记 + 蓝图（见上） |
| `extracted/` | 素材解包输出（PNG/文本，`manifest.csv` 全清单） |
| `tools/` | 分析脚本（脱壳管线、YBC32 反汇编、容器枚举、纹理渲染） |
| `prototype/` | Godot 复刻原型、离屏战斗模拟器及测试 |

## 关键工具

| 工具 | 用途 |
|---|---|
| `tools/unpack_all.py` | 自调试壳脱壳（抓子进程 + 重建 PE） |
| `tools/ghidra_analyze.py` | PyGhidra 标注 + 全量反编译 |
| `tools/ybc32_disasm.py` | T*.BIN / .YBC 脚本反汇编（`-e cp932` 处理日文原版） |
| `tools/enum_container.py` | 偏移表容器枚举（432 容器/1,578 条目） |
| `tools/render_dximg.py` | DX 图像 (X1RGB555) → PNG |

原版游戏目录（`CROSS HERMIT/`、`超魔法大戰繁体中文版/`）不入库（.gitignore）。

## 运行环境

### 启动原版取证

```bash
python tools/launch_original.py --check  # 检查本地原版与关键资源
python tools/launch_original.py          # 使用安装快捷方式对应的中文启动入口
python tools/launch_original.py --direct-game  # 仅在明确诊断时直接启动游戏 EXE
```

启动器由自身位置解析原版路径，因此可以从其他目录调用。默认入口为 `CROSS HERMIT CHT.EXE`，与安装快捷方式一致，工作目录固定为其所在的游戏目录。不要把项目根目录当作原版的工作目录：原版使用当前目录解析资源。2026-10-02 排查中，不显式指定工作目录的直接启动出现 `DXAudio.CPP:568 / DMUS_E_LOADER_FAILEDOPEN / RegistWaveData()`；显式指定游戏目录后错误消失，用户确认可见标题菜单。用户随后检查两个入口并确认没有区别，显示问题已停止追查。启动成功不等于战斗/结算流程已完成，详见 `docs/battle_return_audit.md` §8–9。

### 原版退出函数的隔离核对

```bash
python -m venv --system-site-packages .venv-audit
.venv-audit/Scripts/python.exe -m pip install -r tools/requirements-audit.txt
.venv-audit/Scripts/python.exe tools/tactics_exit_emulation.py --out analysis/new-exit-report.json --godot-out analysis/new-exit-fixture.json
.venv-audit/Scripts/python.exe -m unittest discover -s tools/tests
```

该工具在隔离内存中执行经 SHA-256 核对的原版 x86 指令，不需要启动或操作游戏。输出必须使用新文件名；时间、动画及 VM 等外部输入明确模拟，不代表真实场景已经走通，也不授权角色或日历写入。Godot 模块 `prototype/sim/tactics_exit_handshake.gd` 只复现已核对的脚本完成后收尾部分，其七组逐帧期望值由上述原版指令执行导出。尚未接入学校持久事务。

进一步执行原版脚本与 VM 控制逻辑：

```bash
.venv-audit/Scripts/python.exe -m tools.scene5_script_emulation --out analysis/new-script-report.json --godot-out analysis/new-script-handoff.json
```

此工具从真实请求初始化、同步检查和脚本入口开始，执行原版 VM 的寄存器/条件跳转、定时等待、END 及收尾指令，不再模拟 VM 返回值。它模拟界面、世界命令与完成回调；成功案例不等于实机场景已走通。报告含两条退出案例和三个阻塞反例。原型测试以报告中实际执行到 END 的交接状态核对收尾模块；持久事务仍关闭。VM 分派使用 opcode−5，早期将 opcode 112 误映射到等待处理器的解释已纠正。

进一步执行工作完成、战术主循环与战果分派：

```bash
.venv-audit/Scripts/python.exe -m tools.scene5_task_emulation --out analysis/new-task-report.json --godot-out analysis/new-task-handoff.json
```

此工具保留明确声明的世界/任务初态，执行原版淡入淡出计时和等待清零、`451670 → 451A60 → 4539B0` 主循环、`439E30` 请求及 `49E2B0` 分派，再执行战果构造函数；不注入 `4CDF80` 完成回调。报告包含两条战果路径、四个阻塞反例和一个主菜单退出分支。原型 `TacticsResultTransition` 仅投影已核对的场景 5 收尾后请求，实际剧情条件、战果任务体、状态 10/12 及持久事务仍待闭合。

进一步核对战果退出控制至状态 10：

```bash
.venv-audit/Scripts/python.exe -m tools.battle_result_emulation --out analysis/new-result-control.json
```

执行原版战果初始化、界面控制、析构、请求 10 及准备任务构造；覆盖正常确认、两种跳过界面和两个等待阻塞分支。奖励/评分/成长准备计算仍以明确的未解析边界跳过，不能视为结算完成，也不授权持久事务。详见审计 §19。

进一步核对状态 10 场次门槛：

```bash
.venv-audit/Scripts/python.exe -m tools.battle_round_emulation --out analysis/new-round-gate.json --godot-out analysis/new-round-handoff.json
```

同一隔离实例继续执行原版场次比较、配置标量装载、临时名单与人数写入、场次递增及状态 12/16 请求；Godot `BattleRoundGate` 用来源样例逐字段核对这些变化。场次表是显式合成输入，配置资源与单位派生未执行，12/16 仅到构造入口边界；完整结算和学校返回仍待实现。详见审计 §20。

- Python 3.8+（PIL 用于图像渲染）
战果输入来源核对：

```bash
.venv-audit/Scripts/python.exe -m tools.battle_result_inputs_emulation --out analysis/new-result-inputs.json
```

执行原版 UnitCtrl 收尾，从同一任务读取结果选择参、计算两个条件键，并在身份匹配后复制多角色结算字段；单位和时限初态仍为合成输入，独立条件探针与完整任务回放分开记录。详见审计 §21。

任务 5 的原版战果准备：

```bash
.venv-audit/Scripts/python.exe -m tools.battle_preparation_emulation --out analysis/new-preparation.json
```

执行真实评分、奖励与七属性点包计算，使用原版角色模板和固定时钟种子；报告比较前后记录、道具标志、展示数据与成长池。仅核对指定任务/模式和合成参战初态，暂存点包不等于成长池已更新或学校返回完成。详见审计 §22。

Godot `TacticsScorePreparation` 已实现任务 5、模式 0、三单位的评分与点包准备子集，来源表由 `tools/battle_preparation_fixture.py` 直接从原映像导出，期望值来自独立原版执行报告。离屏测试逐字段核对普通、结果选择参 5 与封顶补偿案例，保持成长池和持久写入关闭。详见审计 §23。

- Python 3.8+（PIL 用于图像渲染）
- Ghidra 12.1.3 + JDK21（仅重新反编译时需要，产出已入库）

Godot `WeekSettlementReplay` 已逐字段对照原版完整周函数，包含参与者解锁、道具/技能整理和月末进位；隔离实例去重与未知输入保护通过。规则由 `tools/week_settlement_fixture.py` 从原映像导出，期望来自独立原版执行。未接入真实 `BattleReturn` 持久事务，详见审计 §26。

Godot `AllResultRoleReplay` 已按独立原版快照核对成长/技能候选、展示请求和确认后的角色字段，角色ID映射与两个应用阶段分别去重；模式1与特殊日期分支也有来源样例。新增技能随机/属性/职业边界及默认关系槽0取证，详见审计 §27–28。此模块仍是隔离角色档，学校与真实存档集成尚未完成。

Godot `ResultTransactionReplay` 已把角色应用和完整周结算接成同一隔离结果实例，整个输入预先验证、各阶段按实例去重，并用同一原版CPU实例的完整快照核对周入口及最终结果。学校剧情加载与结束后任务状态保留为明确请求，详见审计 §29–31。ADV参数7/18已纠正为剧情结束后的任务状态，脚本从同一代码起点执行；当前使用v2来源样例，历史报告字节保留。

Godot `WeekStartReplay` 已按原版状态7任务核对完整周推进、月末进位和淡出等待去重；普通状态12之后的周推进发生在此后继任务。CH001/结束后状态8仍是请求，前置章节完成在组合测试中明确为合成输入；详见审计 §32–33。

原版 `CH003` 日期分派与章节装载已在隔离VM执行：4/5→Chapter020、15/5→Chapter097，真实脚本代码执行到章节入口；章节正文及名单操作仍是明确边界。无章节日期的真实END可请求后继任务，不能代替目标章节完成。详见审计 §34。


2026-10-02补充：Chapter020真实角色加入已接入隔离 `RosterJoinReplay`，名单、装备、等级与职业解锁逐字段匹配原版输出，重复送达不再次登记。同一隔离CPU现已执行CH003→Chapter020→Chapter021真实END→请求7→完整四人新周结算→实际CH001装载/请求6，日期4/5→5/1；章节等待不推进周，新周淡出等待不重复结算。Godot当前25套件189项测试通过；Python206项全量及随后14项新增专项分别通过。CH001正文、职务室/学校任务和前置战斗条件与真实BattleReturn持久链仍待闭合，详见 `docs/battle_return_audit.md` §36–39。
