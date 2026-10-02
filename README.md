# 超魔法大战 (Cross Hermit) 研究工作区

2002 年 EnterBrain 出品的 SRPG+养成游戏，2004 年光谱资讯繁体中文版。
本工作区用于**私下研究**：黑盒规则逆向 + 素材格式分析 + 复刻原型（Godot）。

## 当前状态 (2026-10-02)

已建立素材解析工具和 Godot 离屏战斗原型。当前推进 `trace-battle-result-school-transition`，计划任务完成 10/13；原版隔离执行已核对场景 5 脚本收尾、战果输入、评分/奖励/点包准备及状态 10 场次门槛。现在已在同一实例运行状态 12 构造与总战果任务，核对成长应用、确认后职业/周记录/关系写入，以及模式 1 的条件性成长应用；普通路径月周不变。原版完整周函数及参与者解锁、道具/技能整理也已在隔离实例执行，月末进位另有直接函数探针。Godot 已复现评分/点包子集和完整周函数投影，周投影覆盖实例去重及状态12/场次/分支门槛。场景世界/单位/分组初态和 MVP/学校脚本仍有明确模拟；真实条件入口、角色/周历持久事务和学校任务回放仍未完成。最新证据及限制见 `docs/battle_return_audit.md` §26。

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

Godot `ResultTransactionReplay` 已把角色应用和完整周结算接成同一隔离结果实例，整个输入预先验证、各阶段按实例去重，并用同一原版CPU实例的完整快照核对周入口及最终结果。学校脚本/状态保留为明确请求，详见审计 §29–30。
