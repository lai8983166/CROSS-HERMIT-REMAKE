# 超魔法大战 (Cross Hermit) 研究工作区

2002 年 EnterBrain 出品的 SRPG+养成游戏，2004 年光谱资讯繁体中文版。
本工作区用于**私下研究**：黑盒规则逆向 + 素材格式分析 + 复刻原型（Godot）。

## 当前状态 (2026-10-14)

默认启动为**图形化学校养成试玩**。已接通编班/选课→授课成长→确认记录→评选MVP→第四周两段原版剧情→4月第5周→第五周原版剧情→职务室与巡逻班对白→第五周编班→必修冒险出发准备。Chapter018有126页、Chapter205有32页62条原文，累计267页386条剧情原文。初始4/4仍是独立声明样例，尚无完整前四周经历。

试玩自动保存安排、成长、MVP、阅读进度、周结果和第五周编班。存档version4，兼容version1/2/3；第五周调动保留第四周属性、等级、关系和MVP。存档重放命令并核对最终状态，不是原版SAV。顶部旧「战斗预览」仍为独立MAP01测试阵容，不共享学校战后奖励。

现有「必修冒险 · 出发准备 → 队伍操作试验」保留，新增并列的「战斗操作试验」：当前参战学生用原版精灵出现在MAP05的来源编队位置，携带实际成长后的HP/MP，加入11个来源活动场景对象（含7个初始敌人）。左键选人/查看对象、右键移动/攻击；学生自动接近到来源射程内，敌人按来源移动率0保持原位并在附近还击。八向施法/攻击/收势、HP条、伤害反馈、死亡淡出已接入。中键拖图、滚轮/按钮缩放、暂停/停止、查看队伍/敌人、显示全图和阻挡层；空格暂停、S停止、Esc返回学校。待命编班影响出场名单，教师仅为领队；关闭丢弃试验位置与HP，重开重新部署。

地形通行、编队、当前攻击/防御字段、场景初始对象与图像来自独立来源解析，战斗试验加载118张原版帧，不读取原生审计案例。修正学生调色板mode2表值+1的绑定，当前variant为3/4/2；原版实际参战单位七份44字节攻击快照与独立来源相等，24组声明标量探针核对伤害公式。后续原版世界前缀已完成模式函数、首次嵌套开场控制器、计时/地图更新、开场视野及完整显示/分类列表、空命令队列/输入/光标和暂停单位循环，后续十个空闲特效槽及空命令转送，首次暂停46B470世界更新函数已实际返回，第二次自然开场更新已开启行动，首个学生初始化及首轮主/附动画已实际验证到482A30入口；单位后续效果和完整原游戏帧仍待闭合。**寻路、曼哈顿范围、敌人选择/攻击时点、本地HP应用和死亡淡出仍是明确的重制调度；24个待触发模板、原版完整world/AI/效果链、通关与奖励尚未接通，正式按钮仍禁用，必修限制保持。**

既有「查看本关地图 → 开场演出」继续显示原版伊里安/瑟希莉絲立绘、框、姓名和十段开场文字，支持淡入和键盘翻页；前三句已有原版执行核对，其余为静态来源投影，尚不是完整原VM/world loop。学校状态和存档不因地图、开场、移动或战斗试验而改变。

夜间续篇全量Godot65套件426项、Python来源14项、战斗145项离屏/157项真实窗口、旧移动136/147项、旧开场262项/地图92项/出发页155项/导航26项离屏兼容与严格规格30项均通过。23张最终窗口截图覆盖1024×768/1280×800/800×600，已检查；908个历史/规则保全文件及十项存档规则指纹不变。150–157八个小阶段分别本地提交，未push；157项完成只表示已规划阶段，不是全游戏完成率。

后续158–160阶段继续原版世界模式与自然控制器调用：三种实际编班、21组独立模式探针、完整区域/50项寄存器/64KiB栈恢复核对通过；新/父来源及证据14项、严格规格30项通过。原版开场控制器仅首次更新到状态4，请求仍为1、完成仍为0，未打开AI/事件或完成开场。Godot运行时与存档规则未改动；先前426项及窗口验收保留为基线。见[世界模式进展](docs/school_world_mode.md)及[本轮验收](analysis/school-world-mode-acceptance-20261014.json)。

161–163阶段继续原版计时与地图子链：三种实际编班、24组计时和27组鼠标探针通过。开场仍暂停计时，但原版地图会交换/清空6144字节临时平面，计算格子/像素位置并更新小地图矩形全局；原版memset指令体真实执行。新/父来源与证据21项、严格规格30项通过，Godot运行时和存档规则保持原字节。见[地图/计时进展](docs/school_world_map.md)及[本轮验收](analysis/school-world-map-acceptance-20261014.json)。

164–166阶段执行原版开场视野与完整250槽列表循环。实际占用38/37/37槽，可显示状态14/13/13个，24个延后工作副本状态0进入辅助表，尚未激活；当前镜头候选4/3/3个。原版同高交换、小数定点排序、视口边界与完整缓冲验证通过；三份已验证私有CPU检查点可供后续直接续接命令队列。新/父来源与证据29项、严格规格30项通过，1286个历史/运行时文件及十项存档规则保全。见[视野与单位列表](docs/school_world_lists.md)及[本轮验收](analysis/school-world-lists-acceptance-20261014.json)。

167–169阶段从上轮固定SHA私有CPU/全内存恢复原版，完成空队列、无新命令输入、选择规范化、光标重置、250槽检查及38/37/37个占用单位更新。开场action0绕过行动/动画/AI，14/13/13个状态1单位仍更新格子，视野合并4/3/3次；当前位置未变，未执行占用增减或移动。12组声明选择探针恢复CPU/栈/全工作区；后续私有检查点停在490FC0，完整world tick、非空队列和开启行动仍待取证。本轮来源/原报告/父回归37项、严格规格30项通过；1306个历史/运行时文件及十项存档规则保全。Godot代码/图像未改，旧窗口检查保留为此前基线。见[暂停命令与单位更新](docs/school_world_command.md)及[本轮验收](analysis/school-world-command-acceptance-20261014.json)。

170–172阶段沿490FC0检查点，完成原版后续光标/菜单/悬停、十个空闲特效槽、五个未激活次级槽及空命令转送，原46B662真实返回EAX0，根栈和EBP核对。外层返回仍是已声明的审计驱动，不称为原游戏完整任务帧；活动动画PC/子链、行动/AI与开场VM完成尚未执行。9组声明计数器探针（90次原40A100）核对16位回绕并恢复完整CPU/栈/输入。本轮来源/证据/父回归45项、严格规格30项通过，1324个历史/运行时文件及十项存档规则保全，Godot图形与代码未改。见[首次暂停世界更新末尾](docs/school_world_tail.md)及[本轮验收](analysis/school-world-tail-acceptance-20261014.json)。

173–175阶段重放并核对完整首次世界末尾后，明确发起下一次46B470，原499DA0自然消费开场请求、打开行动门控、进入状态5并设置180等待；之后原地图/视野/列表/空队列/输入与首个学生状态前导逐段执行。19段完整拥有字节、来源prologue推导的栈和119MB以上其他映射内存验证通过，停在475D60第一条指令前；学生正文、活动动画及180次启用行动更新未执行，不称为VM开场完成。三份新私有检查点可直接续接首个学生处理器。来源/证据/父回归53项、严格规格30项通过，1342个历史/运行时文件及十项存档规则保全，Godot画面与运行代码未改。见[第二次世界更新与学生入口](docs/school_world_second.md)及[本轮验收](analysis/school-world-second-acceptance-20261014.json)。

2026-10-15的176–180阶段继续首个学生：原方向2/姿态18绑定D1A程序89；原共享池扫描/初始化两个88字节持久附属节点，按头插连接EFCT程序63/103，立即等待5/29、层12/7。原学生处理器返回0，随后实际更新主动画、两个链接及五个空辅助，等待29/4/28、主未完成/空辅助完成、工作计数1；三种编班完整250工作槽/2048节点池和119MB其他内存相等，停在482A30第一条指令前。6份私有CPU/内存检查点（初始化/动画各3）均在report/file SHA和完整状态验证后才反序列化。来源/原报告/父回归70项、严格规格30项通过，1360个历史/运行时文件及十项存档规则保全。学生后续效果/单位返回、其他单位和180启用更新/VM仍待闭合，Godot画面/运行代码未改。见[学生初始化与原版动画](docs/school_student_action.md)及[本轮验收](analysis/school-student-action-acceptance-20261015.json)。

见[本轮战斗验收](analysis/school-night-combat-acceptance-20261014.json)、[战斗操作与边界](docs/school_combat_trial.md)、[来源攻击核对](docs/school_attack_inputs.md)、[旧移动验收](analysis/school-field-acceptance-20261014.json)和[图形开场](docs/school_graphical_opening.md)。源码运行已验证，独立导出包、语音/音效及完整原版战场摄像机仍待验证或实现。

**接下来**：沿已确认世界入口继续t0005开场后原版world/行动调度与491EF0效果应用，核对初始敌人与场景事件/波次的真实触发，再完成通关结果→奖励成长→返回学校→解除必修限制的闭环。原版后继演出、完整战术AI/技能、其他角色及全年内容仍有未闭合部分；后续逆向按功能需要展开，REA按需使用。

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
