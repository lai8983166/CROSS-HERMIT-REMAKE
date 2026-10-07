# 超魔法大战 (Cross Hermit) 研究工作区

2002 年 EnterBrain 出品的 SRPG+养成游戏，2004 年光谱资讯繁体中文版。
本工作区用于**私下研究**：黑盒规则逆向 + 素材格式分析 + 复刻原型（Godot）。

## 当前状态 (2026-10-07)

已建立素材解析工具和 Godot 战斗原型。返回数据变更 `trace-battle-result-school-transition` 完成13/13；返回界面、待命排序、教师/班级、学生移动、教师移动/工作表、课程解锁、新局学校初始化、编班、课程安排及本轮 `add-school-course-settlement` 均完成3/3，尚未归档。主窗口可演示战果确认、学校详情、待命排序和独立来源新局编班。第4周课程示例可安排教师101的来源课程12/11/10，点击一次结算更新学生属性、等级、新技能及成长加成；重复点击或重新安排不再增长，显式重开才建立新示例。原第0周新局与示例分别保留数据。示例日期是声明输入，结算后仍为4/4，尚不执行结果确认后处理、周推进或存档。

最新Godot全部51套件353项通过；成长结算窗口81项离屏输入/86项实际渲染、课程窗口77项离屏/83项渲染、编班94项离屏/99项渲染、跨会话导航22项和旧返回两路线79项输入检查全部通过，16张本轮截图已检查归档。旧返回页面未改布局，86项渲染沿用20261006基线。项目级OpenSpec严格检查24项全部通过。Python来源结算4项（181.844秒）及课程安排/解锁/运行规则15项（23.395秒）分别通过，合计19项；相关原版报告、期望和运行规则逐字节再生成一致。既有55项和279项全量沿用各自基线。每个小阶段验证后立即提交，无push。

原版隔离执行已在同一CPU核对场景5条件选择→战术收尾→战果→剧情入学→唯一完整周→职务室→学校任务构造与已捕获初始化字段；实际本地Battle终局已接入显式返回回放。来源新局初始化/准备后的成员移动和课程安排已核对；本轮八个授课案例实际执行4A6A10→4BD870→4C00C0/4C0400/4D3600及技能、随机数、属性/等级函数。4D3600的第二缩放因子实际固定50%，修正见 [授课成长结算](docs/school_course_settlement.md)。操作/API另见 [班级课程安排](docs/school_course_planning.md)、[新局编班](docs/new_game_school_grouping.md) 和 [返回流程演示](docs/campaign_return_ui.md)，最新边界见 [战斗返回审计](docs/battle_return_audit.md) §94–96。最新 [结算窗口验收](analysis/school-course-settlement-ui-20261007/README.md)、[课程兼容验收](analysis/school-course-settlement-course-compat-20261007/README.md) 和 [编班兼容验收](analysis/school-course-settlement-grouping-compat-20261007/README.md) 含截图；本轮Python日志见 [来源4项](analysis/python-regression-course-settlement-source-20261007.txt) 和 [兼容15项](analysis/python-regression-course-settlement-compat-20261007.txt)，既有基线见 [55项](analysis/python-regression-new-game-school-20261006.txt) 和 [279项](analysis/python-regression-20261005.txt)。

原版终场世界、资源/演出、时钟/准备初态等仍有声明输入；本地Battle伤害与HP不派生原版事件谓词或状态11结果记录。49E930、来源成员移动、课程安排和授课成长已隔离执行，但前驱学生模板加载、鼠标命中/松开及呈现仍有声明边界，完整新局剧情/原版学校菜单未执行；只移植所定义学校字段和成员资料。Chapter012117仍仅是加入前缀；旧返回演示保持零教师目录，新局/课程示例有来源教师101。下一步核对授课结果确认后的关系/职业进度处理，再接真正周推进的来源链。默认入口保留战斗原型；完整战术动态、并行事件调度、返回会话教师迁移、完整授课结果确认、完整原版学校菜单及原版存档仍未完成。以下独立取证工具说明各自边界，较早补充记录保留为历史进度；当前能力以本节和审计最新章节为准。

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
