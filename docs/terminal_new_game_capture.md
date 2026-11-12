# NEW_GAME 中间寿命有界采集（2026-11-12）

最新接续：新的只读RW机会锁已通过无窗口原生机制预检，v7原游戏接线已准备，但尚未
启动原游戏、没有补造NEW_GAME现场。正式仍2/8。具体链条、限定故障核验及下一窗口
门槛见[文件事件观察](terminal_oplock.md)；以下历史来源及失败结论保持原样。

本轮只完成离线采集准备；未启动游戏、截图或操作桌面。正式进度仍为 2/8。
旧 v5 原生来源及其采集、输入、验证代码保持原字节。新入口为
`devtools.terminal_host_menu_preflight_v6`，默认只打印计划，执行仍需要新的宿主机时段授权。

## 已定位的缺口

复用 `analysis/terminal-host-menu-state-native-v1-20261112.json.gz`，SHA256
`92fc2084af0e9208e53afb087c84d063a284e61a0e765cd4aeb7a324b9bf11e8`。
最后 MENU 样本在 283.578 秒，首次 ADV 在 284.515 秒，保存样本相隔约 0.937 秒。
旧观察器在每次完整快照都保留 worker，因此缺失不只是每秒保存条件造成的。
旧 `frozen` 先枚举全部线程，再逐个暂停、读取上下文及展开栈；已保存的 MENU 样本
每轮有 19 个线程，ADV 有 17 个。在读取其它线程时，尚未暂停的 MAIN 可以继续
构造或退役短寿命任务。这说明旧采集存在漏采窗口；并不能据此测得 NEW_GAME 寿命。

原字节中的合法路径仍是新游戏输入→event7→`49F570` 构造/注册→`49F4E0`
加载 `CH001.YBC`→event6→ADV。没有用静态路径或模拟对象补写旧原生记录。
旧严格验证器仍拒绝缺失 NEW_GAME 实例、TLS 和退出的来源。

## 新采集方式

`terminal_new_game_capture.py` 先打开并核对当前 MAIN 线程的进程/TID，保留该句柄。
每轮先暂停 MAIN，再读当前任务图；在 MAIN 仍暂停时复制当前原 worker 句柄并核对
PID/TID，随后暂停 worker，重读完整代次。仅接受 MENU、NEW_GAME、ADV 范围。
代次包含节点、vtable、TID、原线程句柄及 Event；地址或 Event 数值相同不合并线程。

取得完整原上下文、祖先栈、TLS/PTD、Event 类型及原始任务图后，先恢复 worker，
最后恢复 MAIN。复用冻结的原始快照字段及 TLS 认证代码，不删减所需原字节。
已退出的当前 worker 必须有保留句柄的零等待/exit0 查询，不能伪造上下文或 TLS。
退出时间在实际查询时记录。即使读取或预算失败，也逐一恢复已暂停线程并清理句柄；
关闭重试仅处理未成功关闭项。恢复异常会拒绝本次采证，不宣称恢复成功。

观察与输入保护串行执行；不创建并行 freezer，不暂停 MAIN 后单独放行 worker
等待其进入目标回调。NEW_GAME 的调用祖先尚未成立时，只恢复原线程后继续有界观察。
完整新增代次、状态变化和最终停止轮必须保留原始样本；其余重复轮保留有界审计记录。
这不是全进程原子快照、完整指令轨迹或连续等待/结果消费证明。

| 限制 | 上限 |
| --- | --- |
| 点击后观察 | 20 秒，与 v5 相同 |
| 菜单观察器总时段（含输入） | 40 秒 |
| 轮次 / 原始完整样本 | 2048 / 512 |
| 读取次数 / 读取字节 | 200000 / 16 MiB |
| 每轮暂停 / 累计暂停 | 250 ms / 5 秒 |
| 快速轮间休息 | 至少 10 ms，不承诺真实采样频率 |
| 完整宿主窗口 / 压缩报告 | 最多 10 分钟 / 6 MiB |

限额失败即收尾，不延长原窗口或自动重启。总预算保留原资产审计、清场和桌面恢复时间。
v6 继续使用原桌面检查：显示模式、任务栏、工作区、输入桌面、前台必须与原 baseline
一致，连续两次核对；异常保留原 sidecar，不覆盖失败记录。

## 独立验证和下一关口

`terminal_new_game_verification.py` 独立检查每一轮，包括未保存完整快照的轮次：
线程完整代次、首次保留来源、MAIN 先暂停最后恢复、每个活跃 worker 实际暂停、
退出例外的当前查询、读取/暂停/时序预算及完整句柄清理。随后执行 v5 的所有原始
输入边沿、原代码/资源、MENU 退出、NEW_GAME/TLS/exit0、后续 ADV/TLS 和桌面恢复检查。
没有以采集器的成功标记替代原验证，也没有放宽最终战斗退出验收。

离线预检复用了真实 MENU/ADV 原始字段，覆盖地址复用、读取/上下文/Event/暂停及
恢复故障、累计预算、未保存轮次篡改和关闭重试。模拟句柄只验证实现控制流，不算
新原生来源。下一步在新的已授权窗口只跑一次有界 v6 菜单测试，观察到 ADV 即收尾。
若仍漏掉 NEW_GAME 或预算失败，保留首个差异和实际轮询/暂停耗时，离线判断适用性；
不盲目重复、不回到截图、不直接进入战斗长跑。

本轮离线结果、实现身份和体积见
`analysis/terminal-new-game-capture-offline-v1-20261112.json`。实测是否捕获 NEW_GAME、
实际采样性能及该原生窗口桌面恢复尚待验证；连续等待、首次结果消费、资源/PTD 释放
及两例完整重放均未增加通过结论。

## v6 单次原生窗口结果（2026-11-12 13:12–13:18）

按用户新指令只运行一次宿主菜单测试。来源
`analysis/terminal-new-game-native-v1-20261112.json.gz`（88195 字节），SHA256
`9813d6dea1dd2e41db73eebddc80b7a5f9bedfb5fd2e8bb475806d25fe2a1c2e`。
采集和生命周期均无错误，205 轮观察保留 28 个完整样本；全部保留句柄已关闭，
Job 无强杀清空。新游戏输入的 press/held/release、两个按钮边沿保护及原倒计时
独立核对通过，只有一次输入尝试；按住 213.152 ms，最小倒计时 3521。

| 游戏寿命秒（原记录） | 原生现场 |
| --- | --- |
| 281.141–282.547 | 自动新游戏输入；无截图或图像回执 |
| 284.594 | 轮次 200，仍为 MENU，TID 19816 |
| 284.610 | 轮次 201 / 样本 24，任务图为空，MAIN 原事件 pending=1、id=7；原 MENU 查询 exit0 |
| 284.625 | 轮次 202 / 样本 25，任务图仍为空，MAIN 原事件 pending=1、id=6 |
| 284.641、284.657 | 轮次 203–204 / 样本 26–27，ADV TID 11008，真实上下文及 TLS/PTD 通过 |

本次终于保留了新游戏请求 7 到后继请求 6 的两个原始 MAIN 现场，但仍未采到
NEW_GAME 节点、线程、TLS 或退出。两端事件与原静态路径相容，并不证明某个具体
NEW_GAME worker 的寿命，不能替代要求的动态所有权。完整验证仍原样拒绝
`independent input and menu retirement to NEW_GAME required`；失败结果另存
`terminal-new-game-native-v1-verification-20261112.json`，已验证组件另存 `partial`，
明确 `strict_host_handoff_verification_passed=false`，正式仍 2/8。

点击后共 135 个轮次，记录的起点间隔为 15–16 ms，未记录到 NEW_GAME。
当前 Python 3.10 的 monotonic 使用 GetTickCount64，分辨率 15.625 ms；205 轮中
200 轮暂停时长被记为零，累计 0.079 秒只能称粗时钟记录，不能称精确暂停性能。
两个空图事件样本相差约 15 ms 也是量化时间，不能据此断言 NEW_GAME 的真实寿命
小于 15 ms。此证据支持停止用当前固定间隔轮询获取该短寿命实例；不把更密集采样
当作已经通过，不再照原配方重跑。后续先离线评估与原创建/退出边界关联的事件观察，
明确能否取得目标线程的 TLS 和正常退出，并在自有无 UI 短寿命探针中预检；记录时钟
须换用并认证 QPC 精度。事件计数本身也不能代替目标上下文或完整战斗退出证明。
现阶段没有已验证、可直接替换的确定性原生边界机制。ETW 生命周期账本或线程创建
通知本身不保证捕获初始化后的活体 TLS；不得承诺换成事件通知就能通过，也不复用
已经因保护父转发调试异常而失败的 debug relay 路线。

测试后最初两次检查发现任务栏尺寸和工作区短暂变化。没有修改桌面设置或重启
Explorer；13:17:43 的只读复查已经与原基线一致，13:18:04 完成两组连续复核。
3840×2160/60Hz 显示模式、任务栏、工作区、输入桌面及原前台全项一致，早于本次
13:22 固定截止。原失败 sidecar 不改写，新 recovery 保留同一 baseline 和后续时间序列，
独立验证通过。子进程状态 `0xC0000354` 仍不当作正常 WinMain 返回或资源/PTD 释放。

本次只保留一份有新定位价值的小型压缩失败来源、组件/恢复报告和校验清单；没有
新环境或备份，没有删除历史证据。完整清单与体积见
`analysis/terminal-new-game-native-v1-closeout-20261112.json`。

## 无 UI 同步事件正反对照（2026-11-12）

本轮未启动游戏、轮询、截图或输入。只用系统已有 C# 编译器在 F 盘构建 PE32/x86
GUI-subsystem helper，并在两个新建、无窗口的自有 Job 中执行 notified / silent 对照。
使用 Windows 调试事件作为同步停止点，不附加已有进程、不安装断点、不调用
SetThreadContext / WriteProcessMemory。只处理系统正常的初始 loader 断点，其它异常
按原策略传递；没有使用已禁用的原游戏保护父 debug relay。

| 对照 | 已认证的原生结果 | 实际能力范围 |
| --- | --- | --- |
| notified | PID32136 / worker38464，create48→live49→clear50→exit51；保留句柄最终 signaled、exit0 | 主动 OutputDebugString 通知时，实际 FS/TEB→TLS slot9→116B 数据、随后 slot0 均读到；读取前后完整返回的 WOW64 context 原字节一致 |
| silent | PID19704 / worker32300，create47→exit48；保留句柄 exit0 | 创建时 slot9 为0；worker记录执行段内整个进程没有任何调试事件，未捕获已初始化 TLS |

两例整个 case 分别约 92.6 / 38.8 ms；worker 自报 QPC 执行段分别 864.5 / 358.4 µs。
silent 中 ready→cleared 两个标记仅相隔1个10MHz QPC tick，不能将此称作完整 TLS
真实寿命恰为0.1µs。notified 的通知会让系统暂停进程，正例可观察区间被合作机制延长；
不作零扰动或与 silent 性能等价的声明。QPC 原计数与 perf_counter_ns 独立交叉核对，
本次两次顺序读时钟偏差为0.8–3.5µs。

这是 helper 自己分配的116字节 TLS 数据，不是原游戏 CRT PTD。没有循环值守、sleep
或 ready/ack 等待来保活 worker，但主动通知本身仍是新增合作条件。
[Windows 调试事件文档](https://learn.microsoft.com/en-us/windows/win32/debug/debugging-events)
说明事件会暂停被调试进程，创建通知发生在新线程用户代码执行前；
[ContinueDebugEvent 文档](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-continuedebugevent)
说明后续继续及系统事件句柄关闭规则。保留句柄来自实际创建事件的复制，正常退出
同时核对原事件和保留句柄查询；不使用已关闭的系统事件句柄作退出证明。

独立验证器为 `devtools.terminal_tls_event_verification`。固定4项采集依赖及实际 PE32
身份，验证所有保留线程/进程的事件归属、两套 QPC 时间轴、MAIN config、原始 TLS
数据、TLS清零、全部继续事件和桌面状态。24项离线篡改/桌面回归及独立复核通过；
原始采集实现和来源保持原字节。正常清理均无强杀、Job为空、所有自有句柄关闭；
桌面两次复核与原 baseline 一致，无桌面设置或输入操作。

**原游戏准入仍失败，正式仍2/8。** 原 NEW_GAME 的已核直接调用链没有认证到相同的
必经通知，保护父的调试所有权问题也未解决。创建/退出或 ETW 计数不能补成活体 TLS；
本轮不会把合作正例接成游戏采集，也不再扩大此候选的原生实验。下一步先判断原路径
是否存在 TLS 有效区间内、无新增通知/陷阱的真实可观察边界；没有证据前不启动游戏。

此外 v1 运行器只证明本次正常清理，异常路径尚不合格：Job 查询异常可能跳过后续
显式关闭，EXIT_PROCESS 的继续失败可能遗漏终止/drain，部分初始化在 try 范围外。
来源未触发这些分支，正常结果仍有效，但不能作为可复用的合格控制器。后续如确有
原游戏可迁移边界，必须另立版本修复及故障资格化；不得热改本次冻结实现。
采集 DEPS 未包含桌面模块和编译器的采集时身份；最终验证独立重算桌面结果，并只把
后续编译器哈希记录为事后诊断，不回填来源成完整构建/桌面模块时点证明。

唯一长期来源：`analysis/terminal-tls-event-controls-v1-20261112.json.gz`，压缩SHA256
`19d92d2f555e5882aad985678bfb43cb2aa092b692e7f31180502c2ba56f7ebf`；解压58597字节，
SHA256 `ee4f87da13a783eb59bfada8fb7196d3be3d2176949f87a5cad3e88be7ac405a`。
最终报告为 `terminal-tls-event-controls-verification-v2-20261112.json`；原始helper二进制
仅在 F 盘本地保留，位置/哈希、派生副本清理和本轮总体积见
`analysis/terminal-tls-event-controls-closeout-v1-20261112.json`。

## 原同步边界与观察入口的离线判定（2026-11-12）

本轮没有新原生执行。`terminal_new_game_boundary_contract.py` 固定原镜像、v6菜单
来源、旧CRT调试来源和relay失败复核的大小/SHA，核对50条关键原指令，并在有界
Unicorn内执行原 `49F507` 淡出尾段。它是隔离的原指令语义预检，输入栈/对象地址
明确为合成值；没有执行此前周结算、原线程创建或任何系统/COM调用，不是原生接续。

**第一个具体结论：90帧参数不保证NEW_GAME发生一次等待。** `4DB230→41E720`
检查音频对象 `+20/+22`，任一为零就清理淡出计数；`4DB270→41E7F0`在同类条件
直接返回1。原 `49F518/49F51A` 随即跳过 `49F521→422360`。三例预检结果：

| 声明输入 | 实际原指令结果 | 不能推导的结论 |
| --- | --- | --- |
| v6早期ready的632B音频字段投影 | 311条执行回调，ready=1，停在49F528，未调用等待 | ready时刻约2.063秒，距缺失交接282秒以上，不能认定当时NEW_GAME也走此分支 |
| 合成 `+20=1,+22=0` 分支输入 | 320条，第二个guard返回1，同样跳过等待 | 仅证明另一合法代码分支，不是新历史现场 |
| 合成活动音频及可读接口地址 | 406条，原代码设90计数；停在41DAED的COM调用之前 | 未调用真实音频设备、未取得ready返回，不能补写返回或声称已经走到等待 |

原字节还确定了几个容易混淆的同步点：

- 原CRT在 `56E141` 设置TLS、`56E15E` 写线程ID后，经原正常调用链进入worker
  及虚回调。其间 `56E169` 还有可选初始化钩子；固定镜像的`[76197C]`及退出钩子
  `[761980]`均指向`56CF50`的5字节空函数（`55 8B EC 5D C3`）。这不是当前原生
  指针认证，也未建立必经的“TLS就绪后等待观察器”步骤。
- MAIN原调度先创建挂起线程，再在 `421A44` 设置node事件、`421A5A`恢复线程，
  自己在 `421A8E`等待manager事件。MAIN的等待不等于worker仍在可观察的等待中。
- `439E30`在临界区内写MAIN的id/pending；这不是调试通知。普通无竞争锁和文件
  API调用也不保证停住线程等待观察器。
- worker的 `421FED` 完成信号早于 `_endthreadex`；`57554F`清TLS又早于
  `56E21B ExitThread`。等待原auto-reset事件会竞争原调度信号，且不能钉住TLS寿命，
  因此不能把复制事件句柄当成无副作用的采集订阅。

**第二个具体结论：已定位父调试循环，但没有取得合格的第三方同步入口。**
固定镜像 `.text1` 中 `8396E7` 调用WaitForDebugEvent，返回 `8396ED`；缓冲区在
`[EBP-A28]`，指针在`[EBP-A2C]`，原回复在`[EBP-A30]`；`83BE27/83BE48`继续
原事件。只读父栈仍需捕捉瞬间并处理缓冲覆盖，不能保证TLS活着。此处只认证静态
镜像，不将旧游戏`.text`认证扩大为当前父`.text1`原生身份。
[WaitForDebugEvent](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-waitfordebugevent)
与[ContinueDebugEvent](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-continuedebugevent)
属于原调试者的接收/续行协议；将其用作第三方订阅没有本轮可行证据。
[Windows调试事件](https://learn.microsoft.com/en-us/windows/win32/debug/debugging-events)
的创建通知发生在用户线程代码之前，不能当作初始化后的TLS停点。

复用八例旧CRT原始来源，每例确有两条 `0x40010006` 调试字符串异常；因此不能
笼统声称“游戏没有原生调试字符串”。但它们均在旧启动采证范围，不是NEW_GAME
TLS区间的必经事件。原记录是96B的NT状态：此异常为NT state6；NT state8是
single-step，不能混作Win32的OUTPUT_DEBUG_STRING_EVENT=8。旧来源依赖DR观察，
并明确强制结束，不能包装为本轮无陷阱、正常清理的来源。relay-v5的原回复及失败
结论保持不变，没有重新执行或替换回复。

关口判定：原指令语义预检通过，原游戏采集准入失败；本轮没有新增NEW_GAME真实
线程/TLS/exit证据，正式仍2/8。停止当前“创建/退出通知或父缓冲只读即可补齐TLS”
候选，不延长时间或增加轮询密度。下一候选必须具体证明TLS有效区间内的同步停点、
原调试所有权和恢复语义，再谈新的有界原生窗口；本轮结论不宣称所有其它观察机制
都不可能，也不缩减最终验收。

复现：`python -B -X utf8 -m devtools.terminal_new_game_boundary_contract --out analysis/<新名称>.json`。
每例限2048条回调/2秒，报告限128KiB，所有平台叶调用前停止；原报告不可覆盖。
结果与精确来源见 `analysis/terminal-new-game-boundary-v1-20261112.json`；独立复核、
只读桌面检查及本轮体积见 `analysis/terminal-new-game-boundary-closeout-v1-20261112.json`。
