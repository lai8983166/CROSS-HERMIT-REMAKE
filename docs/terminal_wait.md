# 终局等待与退出接续（进行中）

当前正式功能验收仍停在 `422360` 的第一条指令之前。本轮增加了两个来源的认证诊断及新鲜资源注册前置机制，**未完成等待返回、结果消费或完整战斗退出**。有效 change 为 `connect-terminal-wait-and-battle-exit`，2/8任务完成；其余任务保留未完成，不归档。

## 当前来源的真实缺口

`terminal-wait-probe-v1-{neutral,timeout}-20261106.json` 分别绑定冻结v6来源、完整证明检查点和验证器身份。恢复仅用于诊断，不恢复旧原生助手、堆或句柄。两个来源均观察到：

- `TASK` 前0x30字节全零，包括虚表、flags、manager、node event、worker handle及ID；`MAIN+64`的0x120字节也全零。
- 原 `422360` 及 `422560` 执行85条指令、53次写，原代码把flags设为0x10000、delay设为0；场景结果1仍留在原栈上。
- 第一条OS调用是 `4223A8: call [592234]`（EnterCriticalSection），实际准备参数0x100。调用未执行，不向Windows传递不存在的临界区。
- 不能把 renderer `MAIN+1058` 当成 scheduler `MAIN+64`，不能补写虚表、线程/TLS字段或虚构等待成功。

每例从同一认证停点运行两次，完整57项CPU、所有内存字节/页面权限、指令与写轨迹、观察字段完全一致。它是重复诊断，不是独立原生证明。两例报告耗时约76.1秒和60.2秒（包含来源解码、认证和收尾；末条执行进度分别为69.5/52.8秒）；没有重跑战斗前缀。

## 等待以后的原代码

`terminal-wait-static-contract-v2-20261106.json` 固定原镜像SHA `588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005`，核对26项关键指令和两个原分派表。

1. `453CB5`检查原 `[EBP-8]`；非零调用`4967B0`，再在`453CCE`、`453CD8`各等待一次，`4539B0`才返回1。当前记录开关为0，不能声称已写ReplayData.rep。
2. 原祖先`451A60 → 451670`消费返回值后，还有十轮尾段等待、`465E60`清理、`4DB230/4DB270`完成门及事件选择。
3. 原worker正常退出、TLS/PTD释放、调度器卸链/析构和MAIN事件消费是后续独立条件。仅事件发布不等于奖励或学校完成。

现有终局前缀显式root是`4539B0`，返回到测试哨兵。它没有真实`451AB7/451711/421F88`祖先帧，不能在返回后补造这些栈帧来宣称连续执行。原等待不检查WaitForSingleObject失败值，因此自然ret也不足以证明握手。

## 已验证的注册前置机制

`terminal-wait-registration-v4-20261106.json.gz` 是独立基础节点实验，**没有加载当前终局TASK**。它复用已验冷CRT来源，由原`57B9D0/576F60`建立当前堆锁，再运行：

`421540 → 421660 → 422290 → 4216C0 → 4217C0 → 421850 → 421EA0 → 56E050`

实际到`56E0BE`的CreateThread CALL之前。六个参数为`(0,0,56E110,当前PTD,4,node+24)`；整个116字节PTD核对，包括worker`421F50`和当前node。共5137条原指令、1440次写、25次API叶调用，保留完整CPU/所有映射摘要、真实CRT及调度器wire、270项加载实现的前后身份。

原基础构造函数不初始化+20/+24，实验A5字节保持原样，未被解读为有效句柄。没有手工清零绕过。原PTD free、unlink、节点/manager析构、CRT锁/堆销毁执行成功；未创建worker对应的node事件由明确的补充owner关闭。两个助手均正常退出0，`forced_cleanup=false`，补充清理使用另一栈，原悬挂扫描栈保持原字节。

**剩余硬依赖**：CRT与事件目前属于两个不同helper进程。真实CreateThread不能拿另一个进程的PTD和事件直接运行；原逻辑地址也不能直接当原生指针。下一实现必须统一可执行映像、CRT堆/TLS、事件及worker的实际所有者，并从原`451170/451080`建立合法派生场景。这里不把原生边界改成游戏函数返回值桩。

## 接续准备的效率改进

两个来源分别有9923/9973个映射分区。最初逐次重做历史`mem_map`，实际在Unicorn映射建立处耗时；三次本轮诊断准备会话被主Agent中断，没有产生正式来源、原生助手或保留大转储。收尾guard发现其中两个会话留下了Python子进程，核实PID、父PID、启动时间和命令行后仅终止本轮这两个诊断进程树，并确认guard恢复idle；见`terminal-wait-owned-diagnostic-stop-v1-20261106.json`。会话中断不等于子进程退出，后续重试前必须核对进程并通过guard。

现实现先计算全历史map/protect/unmap后的逐页权限，检查每个来源分区、覆盖范围和不存在的页；相邻同权限分区合并映射（仅诊断内部表示）。`PartitionView`核对真实Unicorn全部字节覆盖和逐页权限，再按父原分区计算冻结摘要。所有原字节、地址、CPU、权限与父分区摘要保持；不会把孔洞或不同权限合并。冻结完整重放器未修改。16项恢复测试覆盖RAM、CPU、权限、遗漏分区、非法拓扑及合并等价性；注册测试逐个篡改六参数和116个PTD字节均拒绝。

复现（仓库根目录，新的输出名；不覆盖已有报告）：

```bash
.venv-audit/Scripts/python.exe -B -X utf8 -m devtools.terminal_wait_probe --case 0 --out analysis/terminal-wait-probe-new-neutral.json
.venv-audit/Scripts/python.exe -B -X utf8 -m devtools.terminal_wait_probe --case 1 --out analysis/terminal-wait-probe-new-timeout.json
.venv-audit/Scripts/python.exe -B -X utf8 -m devtools.terminal_wait_registration_probe --label terminal-wait-registration-new --out analysis/terminal-wait-registration-new.json.gz
.venv-audit/Scripts/python.exe -B -X utf8 -m unittest devtools.tests.test_terminal_wait_probe devtools.tests.test_terminal_wait_registration
```

## 保全与状态

历史工具、来源、存档、私有检查点及验收保持原字节；没有新增游戏功能验收，R3/R4/R5/R6不因此完成，Godot未改变。本轮只保留一份注册成功报告及其两个助手。被替代的本轮v1–v3及六个助手已按 `terminal-wait-registration-development-v1-20261106.json` 退役，不能再报告为可用。小型失败结论、回归和原大小/SHA保留；没有扩展历史删除授权。

## 连续采证的观察器预检（2026-11-09）

guest-v5 已从真实学校自然到战斗退却和后继菜单，详见 `terminal_school_handoff.md`。
该来源的离散栈观察没有补齐连续等待、结果消费及资源/PTD寿命。旧中立/超时来源也
不能借用该进程已经失效的句柄。两例新鲜完整重放必须等连续路径和验证器稳定后再启动。

新增 `terminal_exit_cleanup_contract.py` 核对固定原镜像、53处关键指令、18个范围、
PTD各释放点与真实析构虚表。局部原x86探针只验证PTD指针选择及调度卸链：前者明确
用合成free/TLS叶返回，后者执行原search/unlink及ABI检查、核对整个1KiB对象区。
这些探针不是当前堆真实释放或完整场景重放。原正常路径为
`421F8A → 422021 → 56E1E0 → 575450 → ExitThread`，不是返回仍在栈中的56E183。

资源取证必须进一步区分：

- `575450`处理PTD的6个非空嵌套指针及+50静态指针例外，最后释放PTD并清TLS；
  原代码不检查TlsSetValue失败，分配器还可能因hook拒绝或调试标志而延迟释放。
- MAIN在421B4C关闭节点事件，然后卸链、析构；该正常链没有关闭node+20线程句柄。
  需以动态对象身份确认并单列补充owner；关闭观察器DuplicateHandle副本不是关闭原句柄。
- manager事件跨后继菜单仍然有效，到整体manager析构才关闭。465E60在多层析构中重复
  调用，不能按进入次数重复计资源释放。

连续观察器先做短startup等待预检，没有重跑17分钟战斗前缀或两例小时级证明。
原保护父进程占有游戏debug对象，实验仅调试该父进程，以硬件断点观察其
NtDebugContinue；没有写游戏内存、通用寄存器或原debugger回复参数。
实测父线程DR0–3为0、DR7=155，并非四个空闲槽。开发实验只暂时复用一个槽，保留
另三个零地址执行断点；零页MEM_FREE不证明原断点无效，也不证明调试行为等价。
旧nested-v3也有此配置，但该旧实验失败，不能当作兼容性先例。

有界relay-v5实际仅命中422360入口。原父进程调用NtDebugContinue时，栈上回复为
80010001（NOT_HANDLED）；未修改它。随后观察父进程以4000001E退出，没有到下一
调用点4223A8，更没有观察到WaitForSingleObject返回。收尾WM_CLOSE窗口已失效，
Job对剩余成员执行应急清理，最终为空，四个可变私有文件恢复。
child退出码在应急清理后查询；不能据此判断它在TerminateJobObject前已经退出，
也不能用SuspendThread的ACCESS_DENIED单独推断线程状态。此例明确是失败，不能
以Job清空、进程结束或字段已恢复称正常资源寿命成功。

完整失败来源为 `analysis/terminal-wait-native-probe-relay-v5-20261109.json.gz`，
20,257字节，SHA-256 `6ee170b32160801bcb0bf28dc73044a235985c23421f92287d1e1c3ff99d7aaf`。
独立核对入口的当前FS/TEB/TLS/PTD、3段原代码、5个实际OS导出入口（按客体DLL与
实际加载基址应用PE重定位）及13条仅DR写入回执。相关failure-proof和独立review均
保持accepted=false；它们认证的是失败边界，不是连续等待成功。

`terminal_wait_observer_gate.py`已在宿主调度、guest probe和底层relay三个入口拒绝
重复启动这条已知不兼容路径，没有“换label重试”或关闭检查的CLI开关。
执行版本按增量ZIP封存；当前禁用代码不能重新签名旧来源。调试事件原句柄与显式
DuplicateHandle副本分开管理，最后一次续行返回、异常NOT_HANDLED、部分写入后的
恢复及预算超限pending事件均有局部回归。

下一路线先检查不注入#DB的客体ETW系统调用/调度事件能力及丢失计数。即使ETW可用，
它也不能单独替代完整用户态调用点、ABI、CPU/内存/累计轨迹或PTD实际释放证明。
正式进度仍2/8；连续证据未接通前，不启动两例长重放、不勾选后续任务。

### 客体ETW短预检与原来源接续

本轮只增加一次自有测试线程的ETW采集，没有启动游戏。测试线程分别取得等待成功0
和超时258，两个自有事件均关闭；NT Kernel Logger由本次StartTrace成功取得，StopTrace
返回0，三项丢失计数均为0。原ETL为3,735,552字节，SHA-256
`c3be0decc31aca6d12b27be955a7e7ad70df4ad4a960b13e5b04aa6000b13a0c`，保存在
`.venv-audit/native-worker/terminal-wait-etw-capability-v1-20261109/trace.etl`。
该测试线程不是原游戏worker，也不证明游戏结果消费或PTD清理。

首次tracerpt解码达到24 MiB派生XML上限而停止；其显示的时区偏移也与ETL原始
FILETIME不一致。保留原报告和实现，不通过提高上限、补时间容差或重采掩盖问题。
新入口`terminal_wait_etw_probe.py --decode-source ... --source-sha ... --etl ...
--etl-sha ... --out ...`只在核验的专用客体中读取已有ETL；不启动logger、测试线程或游戏。
以OpenTrace/ProcessTrace/TDH读取原始类型和FILETIME，检查实际64位结构布局、
源SHA、StopTrace原始统计字节、ETL时间范围、CPU数及线程PID/TID事件，关闭自有读取句柄。
源与解码输出分开，失败后也不重签原来源。

同一ETL已经完整读取77,137条记录、全部57个缓冲区，首事件时间严格等于ETL StartTime，
没有加校准偏移。第一次严格配对仍在目标线程两条连续SysCallEnter处拒绝，不能用
丢失计数为零推断逐调用配对完整。有限首差异及511条目标线程相关记录以约8 KiB
压缩现场保存；全系统事件不展开成持久化JSON/XML。原始ETL仍是可重新解码的来源。

`terminal-wait-etw-window-proof-v1-20261109.json`及独立review逐项核对了511条抽取的
原事件头、载荷、时间和CPU归属。两个原测试时间窗口内分别只有Enter、切出、切入、
Exit四条事件，实际NTSTATUS为0和258；同一服务地址跨CPU迁移的归属正确，窗口两端
观察到的Enter减Exit计数均为0。窗口外仍有7处重叠、全局241次Enter/240次Exit及
末尾计数1，未按猜测的嵌套栈消掉差异，原全局报告继续blocked。局部能力结论只适用
64位Python测试线程，未证明内核服务符号、游戏WOW64兼容或任何完整ABI/状态重放。

本轮248项相关回归普通及`-O`通过。客体冗余来源及可重建的派生XML共29,459,692字节
按SHA核对后退役，原ETL、必要小报告、原执行版本和一份必要恢复副本留在F盘；
删除客体文件不代表VMDK已经缩小。虚拟机已正常关闭，未向宿主机发送输入。
完整连续游戏采证仍需解决，不能把这次工具预检计作两例新鲜原生完整重放。

### 原游戏 WOW64 等待观察（2026-11-09 后续）

观察路径已从自有测试线程推进到原游戏 startup worker。全部运行位于 F 盘的
2 vCPU/4 GiB 后台 Windows 客体，重新核验当前启动身份、时钟及 D3D8/输入隔离；
没有宿主游戏窗口、宿主输入或用户操作。此处观察的是 startup 的原等待体，尚非
完整战斗三次握手，也没有把原等待体的单次观察计为任务 2.1 完成。

`devtools/terminal_original_wait_etw.py` 只读观察原管理器、节点、事件、线程、FS/TEB/
TLS/PTD、原栈和实际 WOW64 系统 DLL。ETW 开启 THREAD/CSWITCH/SYSTEMCALL，保留
原始 ETL、全部目标线程记录、原事件头/载荷及全流摘要；不持久化全系统展开 JSON。
由当前驱动枚举取得内核加载基址，并用实际客体 ntoskrnl.exe 的 PE 导出绑定系统调用
地址；没有读取内核指令内存，不能将磁盘导出核对表述为内核实时代码认证。

| 来源 | 原生运行时间 | 实际结果 |
| --- | ---: | --- |
| etw-v1 | 10.391 秒 | 主循环就绪不等于 startup worker 已注册；在开始 ETW 前拒绝，保留首个失败现场。 |
| etw-v2 | 7.797 秒 | 增加最多 5 秒的自然注册/原祖先等待，观察到一例原等待成功；离线 v1 解码通过有限来源检查。 |
| etw-v3 | 6.500 秒 | 采样前用同一个线程句柄核对 PID/TID，再挂起、读取及恢复；原等待可解码，但未采到 CRT 退出返回点，严格检查拒绝。 |

上述时间为原生进程观察范围，不是任务总墙钟时间；只做了三次短启动，未重新执行
约 17 分钟的完整战斗前缀。v2 使用旧冻结挂起助手，不能追认其具有 v3 的挂起前
所有者保护。v3 六份实际线程上下文均记录保护通过及原挂起计数 0，恢复只撤销本次
增加的计数；该保护也不能扩大为旧生命周期助手全部线程操作的证明。

v3 的原 `WaitForSingleObject` 栈参数为当前节点事件 `2032` 和 `FFFFFFFF`；
实际 ntdll `NtWaitForSingleObject` 的暂停点是导出入口 `+12` 的 `ret 0C`，其栈参数
为同一事件、Alertable=0、Timeout=NULL。107 条目标记录中，唯一完整覆盖暂停窗口
的调用为原 ETL 记录 1615 至 2165，包含 6 条调度切换，退出 NTSTATUS=0；暂停期间
完整落在记录 1948 至 2033 的切出/切入之间。暂停上下文 EAX=1 不是返回值，不能用它
替代后续 ETW SysCallExit。尚未核验全部用户态中间调用点/ABI，也没有完整 CPU/RAM 轨迹。

严格解码 v2 在读取 v3 ETL 前拒绝：34 条 shutdown 样本最终可见窗口关闭、三个原全局
指针清零，但无 `crt_exit` 回执或 `5714F2` 祖先；末条仍在 WinMain 原清理栈。
保护父进程退出 0、子进程 `C0000354` 不等于 WinMain/CRT 返回已证明。
原来源和拒绝报告保持原字节。新增显式 `--diagnostic-only` 只允许此类缺失采样的
有界等待诊断，默认严格模式不变；错误 CRT 字节、强制清理、异常状态、缺失原清理
祖先、错事件或 ETL 丢失仍拒绝。诊断报告状态明确为
`diagnostic_original_wait_observed_cleanup_unproven`，客体退出码 2，宿主命令也保持
非成功；`accepted/fullABI/fullstate/PTDcleanup/strict_source_cleanup_verified` 均为 false。

离线接续入口（使用新 label，既有来源及输出不可覆盖）：

```bash
.venv-audit/Scripts/python.exe -B -X utf8 -m devtools.isolated_vm_original_wait_decode \
  --source-label etw-v3-20261109 --label NEW_LABEL --diagnostic-only
```

入口会从保留的 F 盘来源恢复已退役的客体传输副本，传输前后核对 SHA；客体已有
异字节文件时拒绝覆盖。恢复分支已做局部回归，尚未另起客体做该分支的新实测；
实际 v3 解码执行版本仍保存在 decoder-implementation-v3 胶囊，不以当前入口重签它。

实际 v3 诊断读取同一份 1,114,112 字节 ETL，共 33,527 条事件，耗时 8.672 秒；
ProcessTrace/CloseTrace 返回 0。这些是读取结果，不是完整退出验收。v2 的必要成功
来源和 v3 的当前保护实现诊断来源分别保留；两者不是两例新鲜原生完整重放。
小来源、拒绝/诊断报告、执行版本和独立复核在 `analysis/terminal-original-wait-*`，
原 ETL 的本地位置、大小、SHA 及清理范围见本轮 closeout 清单。

本轮 294 项相关回归普通及 `-O` 通过，主 Agent 另从原事件字节重算 CPU 归属、单调用
配对和两层原栈参数；独立复核保持清理缺口。保全重新核验 832 个小文件 SHA 及 13 个
大文件大小，未把大文件大小检查说成重新完整哈希。

核对 SHA 后退役客体冗余传输文件 3,880,553 字节，必要原 ETL 保留在 F 盘宿主证据
目录。新复制的 11,597,168 字节内核文件与已有文件相同，但删除被自动审批策略阻止，
未继续尝试；该副本仍存在并计入本地体积，清理状态不标为全部完成。VM 已软关闭，
运行实例数为 0、无残留 VMEM；没有测量并声称宿主性能完全不受影响。

下一步仍是连续原用户态状态/等待返回与结果消费、实际资源/PTD 释放的证据机制。
ETW 只补充系统等待返回，不能替代完整状态和累计轨迹；该机制接通并通过一个代表
案例后，才调度第二例新鲜原生完整证明。正式任务保持 2/8，未归档、不降低验收。

### 同日连续等待窗口与前缀观察修正

新增独立短窗口入口、精确输入时间回执和流式离线验证。启动预检已在同一实际
原 worker 上配对十次不同的成功等待；38 份快照对应当前事件、原栈与 TLS，原 ETL
123,180 条记录完整读取、三类丢失计数均为零。严格 CRT 退出仍未证明；显式诊断
保持非成功退出码和正式完成字段 false，不用该预检勾选功能验收。

四次前缀分别在 908.891、653.703、374.687、1.375 秒停止，原因依次为保留句柄时机、
退役虚表过渡、暂停期间线程清单变化、工厂快照与激活时序。每次先定位并做局部
回归及短预检，再执行一个代表前缀；旧失败来源与执行版本没有被改写为成功。
新增观察层保留实际失败现场、分类边界和有界重试。完整输入与原资源身份验证不变。
新的聚焦预检已经实际取得工厂、就绪、激活的顺序及八帧同句柄线程保留证据。

执行入口、证据边界和接续命令见 [连续战斗等待窗口](terminal_battle_wait_window.md)。
正式连续结果消费、完整资源/PTD 清理及两例新鲜原生完整重放仍需实际证据；这些
观察器修正和启动能力检查不改变 2/8 的正式进度。

第六次前缀已在 F 盘虚拟机内自动完成退却确认、原战斗线程退出和后继菜单观察，
完整输入来源通过独立核验。准备移出输入观察后，触发耗时降至 8.859 毫秒，原
输入期限不变。保留同份 ETL 完整离线读取 186,675 条事件，有限诊断确认 69 次
真实等待返回；严格窗口仍拒绝四个跨调度区间快照。尾计数 0 和结果非零时的
`453CB5` 现场缺失，不能宣告连续结果消费或完整清理。Thread End 后九条记录
全保留，syscall 不猜测配对；PTD/原资源释放及两例完整验收仍未完成。
完整结果、原字节复核和接续边界见上述连续窗口文档；本轮 400 项回归普通/-O通过。

## 2026-11-09 等待证据接续补充

同一 battle-v6 完整输入来源现已找回 `453CB5` 非零结果和 `451758` 尾计数 0 的原生
现场。新 gap-audit-v2 核对原上下文、当前 TLS/PTD 与保存的栈字节；缺少这些补充
现场的精确区间和完整 Nt 参数，故不增加成功等待配对、不把端点组合当作连续消费。
旧四份跨调度帧没有原始 QPC，仍保持严格未证。

短双时钟观察已复现转换 UTC 与原始 QPC 判定不同的 17 帧，同时识别一份真正的
调度交叉。所有原事件保留，数据读取区间仍必须处于唯一真实 off-CPU 区间；没有
用校准偏移或容差修补旧来源。原上下文取得早于数据区间，完整状态/ABI/累计轨迹、
资源/PTD 清理及两例新鲜完整重放仍未完成，正式任务保持 2/8。新增端点、短观察器
及资源证据缺口的详细范围见 [等待窗口接续](terminal_battle_wait_window.md)。

随后新增同句柄持有期内显式 settling 的短来源，218 帧均通过原始 QPC 严格单区间
检查，支持 61 次不同等待，未发现真实跨界。该结论限于数据读取区间，先前上下文
取得与 settling 不在其中；不能升级为连续完整状态、生产长采集资格或资源清理。

## 真实返回采证的架构阻塞（2026-11-09）

本次没有接通第一关。优先检查真实 post-wait 现场，在 F 盘 2 核/4 GiB 客体内只执行
一次自有 WOW64 helper 的原生短预检；没有启动原游戏、重跑战斗前缀或操作宿主输入。
原生等待返回三次 0 和一次真实超时 258，注册/撤销回调均返回 0，句柄和私有缓冲正常
释放。但是返回观察记录为 **0**；四个调用者原始 post-return 帧不能冒充原游戏现场。
严格验证器因没有回调记录而拒绝，不以 helper exit 0 或单元测试通过当作能力通过。

当前系统原字节解释了这个失败：

- 与 battle-v6 原现场相同的 x86 ntdll SHA，其 `NtWaitForSingleObject` 加载
  `EAX=000D0004`，高位 selector 13 选择 `wow64cpu` 表项 RVA `36D0+13*8`。
  原路径 `1B46 → 1CE0 → syscall 1CF1` 之后直接返回 32 位代码，绕过
  `wow64!Wow64SystemServiceEx` 的 instrumentation callback 分派。
- 该版本 WOW64 回调字段实际为 `PEB32+490`，公开旧例的 `+488` 不适用。
  这只是原字节定位；没有向原游戏写入这个字段，也没有证明它的当前原生值。
- 当前客体内核的 `NtSetInformationProcess` class 40 分支在目标为 WOW64、调用者为
  native64 时，走 `6F5F21 → 6F5FDC` 返回 `C00000BB`。同为 WOW64 的调用者只写
  `PEB32+490`，不能改用它获得 native KPROCESS 回调。此项由本内核静态分支确认，
  没有再启动一次已知会失败的注册实验。

机器码、返回记录和系统模块 SHA 见
[短预检失败审计](../analysis/terminal-wait-return-callback-failure-v1-20261109.json)、
[内核拒绝分支增量](../analysis/terminal-wait-return-kernel-refusal-v2-20261109.json) 和
[主 Agent 独立复核](../analysis/terminal-wait-return-independent-review-v1-20261109.json)。
原报告没有记录 wow64cpu 加载基址；ECX 与静态返回位置的吻合只作一致性线索，不能
补成实际基址认证。第一次编译因客体 TEMP 目录不存在而失败，在创建明确目录后
才进行了唯一一次原生执行；冻结的失败回执没有改签。普通/-O 各 6 项回归在客体通过。

下一处硬依赖已经具体到**未修改的 wow64cpu 真实等待返回处，如何取得完整原状态**。
当前 callback helper 只用于复现这项不支持结论，不能安装到原游戏或充当生产资格。
不重复旧 #DB relay、这两种回调路径，不改原 syscall selector，不关闭 turbo 通道
来制造“相同原路径”的成功。候选机制必须先证明当前线程/原栈/完整状态与恢复能力，
再进入原游戏短预检；此后才有条件接 `453CB5 → 4967B0` 和另两次完整握手。
正式进度仍 2/8，三关均未通过；首次消费、三次游戏握手、资源/PTD 释放和两例新鲜
完整原生重放均未完成。

## 外部虚拟机监控器预检（2026-11-10）

第一关仍未通过。本轮不重试已证伪的父进程 #DB relay、WOW64 callback 或时间包络，
也没有启动原游戏。先检查当前 VMware 16.0.0 build 16894299 的外部监控能力。

| 本轮实际检查 | 结果与边界 |
| --- | --- |
| localhost GDB 接口与客体身份 | 由当前监听 PID/创建时间、同次启动日志中的专用 VMX 和可执行文件、运行清单共同认证；只允许本机连接。 |
| 原始状态读取 | XML 声明 536 字节，实际 `g` 仅 164 字节；x87 `p` 返回宽度也不同于 XML。没有补零或截断后当作完整状态。 |
| 同停点 CPU 元数据 | 有界读取 VMSS/VMSN 的 CPU group，每份读取 52,086 字节，CPU 原字节 22,357 字节，不读取 RAM。两颗 CPU 的 24 个核心寄存器与原 RSP 停点一致。支持原始 CR/DR、段缓存和 FXSAVE 解码；四个 FX 指针字段的格式仍未原生验证，64 位描述符 base 不截断成 Unicorn32 的值。 |
| 保存后恢复 | `suspend/resume` 后进入高 IRQL 时钟中断补齐循环。原栈 QPC 为 `fffffffffdc9587e`，CPU1 追赶异常巨大时间，CPU2 等待跨核 TLB 刷新。保留原字节和故障定位，不再次使用此恢复方式采游戏。 |
| 当前停点快照后直接续跑 | idle 快照的 CPU 字节可复用，直接续跑后客体通信正常。等待整个 lazy snapshot 在暂停期间完成会超时；不能把该超时回执改写成成功。由后续独立提取及清理回执记录实际结果。临时 4 GiB 快照已由 VMware 删除。 |
| 精确真实等待返回断点 | 自有 WOW64 fixture 在 `Z1/OK → c` 后触发两颗虚拟 CPU 的 `debugReg.c:287 NOT_IMPLEMENTED` panic。日志确认 Hyper-V/ULM 模式；没有得到等待返回停点、post-FXSAVE 或断点不改变 guest DR 的证据。 |
| 不附加观察器的同字节 fixture | 新鲜启动完成 `[0,0,0,258]`，三次 peer 响应、原 NtWait 字节不变、自有句柄/缓冲释放及 watchdog 撤销正常。仅证明 fixture 基线，不能冒充原游戏握手。 |

新增 [失败拒绝入口](../devtools/terminal_vm_wait_observer_gate.py) 固定认证真实失败，
拒绝把断点请求的 `OK` 当成资格通过。冻结的 `terminal_vm_monitor` v1–v4 和本地运行
脚本只用于复现与审计，不是生产采集入口；不得换标签重跑当前环境的隐藏断点。
也不把 `hideBreakpoints=FALSE` 的 INT3 写码路径作为替代。当前恢复为原先无调试监听
的虚拟机配置；本轮没有修改宿主 Hyper-V/VBS、启动宿主游戏或发送宿主输入。

证据见 [断点失败原始回执](../analysis/terminal-wait-vm-monitor-breakpoint-failure-v1-20261110.json)、
[恢复时钟故障](../analysis/terminal-wait-vm-resume-clock-spin-v1-20261110.json)、
[独立原生结果复核](../analysis/terminal-wait-vm-monitor-independent-review-v1-20261110.json)
和 [本轮收尾清单](../analysis/terminal-wait-vm-monitor-closeout-v1-20261110.json)。
普通及 `-O` 各 33 项检查在客体通过，均不能替代缺失的原游戏采集。

下一步必须先取得**当前隔离平台上可用、精确且不改写原代码的等待返回观察能力**，
通过当前线程/原栈、完整 57 项状态、全 CPU 一致暂停和正常继续/清理预检，再采原游戏。
恢复时钟异常与隐藏断点 panic 是不同故障，修复其中一个不代表另一个通过。
第一消费 `453CB5 → 4967B0`、三次完整握手、真实资源/PTD 释放及两例新鲜完整重放
仍未完成，正式保持 2/8，没有新增完成勾选。

协议范围参考 [GNU RSP](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Packets.html)；
VMware 快照/保存状态用途参考 [Broadcom 文档](https://knowledge.broadcom.com/external/article/323788/converting-a-snapshot-file-to-memory-dum.html)。
隐藏硬件断点与 INT3 的区别参考 [OpenCore 调试文档](https://github.com/acidanthera/OpenCorePkg/blob/master/Debug/README.md)。
同一 `debugReg.c:287` 在其它平台也有 [厂商社区记录](https://community.broadcom.com/vmware-cloud-foundation/communities/community-home/digestviewer/viewthread?CommunityKey=0c3a2021-5113-4ad1-af9e-018f5da40bc0&GroupId=7165&MessageKey=f6cffd4d-6518-4924-adb9-fa9876147e00)；
该记录不是当前 Windows 平台已修复的证明，本轮结论来自本机原始日志与协议回执。

## 内核等待尾部与替代后端预检（2026-11-10，KD）

本轮没有启动原游戏，第一关仍未通过。实际新增能力是：在原客体内核
`NtWaitForSingleObject+0x6a` 用官方 SDK KD 客户端停住一次普通系统等待，清除
断点后，同次启动的客体继续正常响应；另取得自有 WOW64 fixture 的当前 PID/TID、
native64 PEB/Ldr 链及实际 `wow64cpu.dll` 加载基址。两者不是同一目标等待现场。
目标 fixture 的合格停点为 **0**，没有三次受控返回、首次游戏结果消费或完整状态。

已复用原内核/PDB和DLL做静态核对：用户地址的硬件断点仍可能把异常交给原保护
DebugPort，不能用 KD 名称替代旧 #DB 路径；内核 PreviousMode=0 的分发边界不同。
固定内核 SHA 下，尾部 live RAX 才是返回值；原 handle 位于 `[RBP-48h]`，
Alertable 位于 `[RBP-40h]` 低字节。用户 timeout 会被复制到尾部 `[RSP+58h]`，
`[RSP+50h]` 已改成这个本地副本地址，不能拿它和原用户指针比较。
trap.R8/XMM 等槽位存在不代表本轮保存有效；陷阱帧也不含完整 x87 状态。
实际用户 RIP 必须与独立认证的 wow64cpu 基址加 `1CF3h` 核对，不能由 RIP 反推
基址再循环认证。详见 kernel-boundary、kernel-pdb-context 和独立复核报告。

本轮失败保持原样：

- 手写 DbgEng 客户端经历接口标识、遗漏 `STDMETHODV`、live-kernel 超时契约的修正；
  v6条件中的 `&&` 被 MASM 拒绝，只取得其它线程的停点。v7 在事件处理时发生宿主
  客户端 AV，根因未定位，不能称已修复；它的异常清理也不能保证脱离成功。
- 官方 KD 的单次普通内核尾部预检通过；CLI v1/v2 在后台准备调用超时，尚未启动 KD。
  没有分阶段回执，不能把这些超时归因于某个 PEB 读取或模块枚举函数。
- v3 改为客体监督进程和 VMware Tools 小文件交接，取得真实模块来源；最初的
  fileExists 缺失返回被编排当错误。v3b接续同一fixture，装好复合条件断点后 go
  文件复制超时，0个目标 BEGIN/END/COMPLETE。不得换标签重复同一配方。
- 恢复期间另观察到初次 `g` 后仍有待处理的 `DbgBreakPointWithStatus`；官方 CLI
  显式再续跑一次后，同boot响应恢复。该现象解释恢复停住的现场，不足以把此前
  所有超时归为同一根因。`EndSession`、`GO`请求或客户端退出不代替客体恢复证据。

QEMU 候选也在迁移前拒绝：所查 GDB 路径把多个 x87 状态字段返回为零；HMP/
VMState 未补齐完整字段，FXSAVE helper 同样不能补造。当前发布二进制与所查上游
源的精确构建闭合还未建立。没有启动 QEMU VM、创建磁盘覆盖层或迁移原游戏。

所有 `isolated_kd_engine*`、`terminal_kd_wait_*` 和本轮监督器均是冻结的开发/失败
复现代码，**不是生产采集入口**。接续先解决原调用身份过滤、调试中断续跑和
控制交接的有界可靠性，再证明完整用户postreturn状态；不使用内核RAX、浮点文本
或文件SHA充当完整原CPU/映射内存/ABI证据。此后才可采原游戏并接
`453CB5 → 4967B0`。三关及原任务2.1–4.2继续未完成，正式保持2/8。

本轮原始小回执及执行脚本见 `analysis/terminal-wait-kd-support-v1-20261110.zip`，
独立复核见 `analysis/terminal-wait-kd-independent-review-v1-20261110.json`，
环境恢复、保全和全部新增体积见 `analysis/terminal-wait-kd-closeout-v1-20261110.json`。
QEMU下载包及提取运行时的删除被工具策略拦截，暂留F盘且不进入Git；获取URL、
字节数/SHA和未退役状态保存在收尾清单，未把这些文件报告为已清理。

SDK契约参考微软 [WaitForEvent](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/dbgeng/nf-dbgeng-idebugcontrol-waitforevent)
及 [结束KD会话](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/ending-a-debugging-session-in-kd)；
live kernel要求INFINITE等待，外部中断请求和实际恢复必须分别检查。

## 限定线程的等待尾部复核（2026-11-10，thread v1–v4）

本轮原游戏启动数和合格目标等待停点均为 **0**，第一关仍未通过，原任务保持
2/8。没有取得 `453CB5 → 4967B0` 或三次游戏握手的新连续证据。

已将普通系统停点缩到当前 fixture 的 EPROCESS/ETHREAD，独立读取实际 wow64cpu
加载基址，再设置内核尾部硬件断点。v2 日志出现一次 `Breakpoint 0 hit`，但没有
停点时的 PID/TID/handle/返回状态核验，不能认证为目标等待；客体最终回执是
准备门超时，没有目标 returns。v1 的启动命令虽然超时，监督进程实际已启动，
不能按“没有启动”再次发起。v3 因准备脚本把 source SHA 写入错误键而被夹具
原有身份检查拒绝；v4 修正清单后仍在获取准备回执时遇到控制通道超时，没有
附加 KD。其监督器超时后放行清理，首个返回为 258，并非三次成功握手。

已修正一个明确的客户端缺陷：发出 `g` 后，旧日志末尾的 `kd>` 不能继续授权
查询或清除断点。`terminal_kd_session_v3.py` 区分连接中、运行、暂停、查询和
未知状态，仅接受当前游标之后的新提示符；查询标记允许紧跟提示符同一行。
12 项离线回归通过。v3/v4 在附加前已失败，因此**新状态机尚未通过原生验证**。
旧 v2 未记录逐次输出可见时间和 gate future 结果，无法证明那一次停点是迟到
还是日志迟显，不能把所有超时都归因于同一个解析错误。

完整状态的另一处阻塞已从原字节确认：本内核的 KD context 指针位于
KPRCB+8980h，但 kernel-CS 的 `KeContextFromKframes` 路径跳过 FXSAVE；浮点
有效标志不能证明槽位保存过原 x87。DS/ES/FS/GS 有常量赋值，控制状态里的
LDTR 被写零，DR4/DR5 没有独立原值槽位。WOW64 返回块也没有补全这些原值。
见 `analysis/terminal-wait-kd-raw-context-contract-v1-20261110.json` 的 57 项来源
逐项清单。普通 KD CONTEXT 不能被提升为完整用户返回现场；在补齐缺失字段的
真实来源前，停止沿这条不完整状态路径采原游戏，不能通过填零或拼接旧现场通过。

另外，本机 pywinrm 的 `operation_timeout_sec` 只限制单次请求；
`Protocol.get_command_output` 会对接收超时无限重试。这不是整个任务的期限。
后续调度必须先给控制交接加独立总期限并核实远程命令是否结束；仅调整 20/30 秒
参数或在外围写一个轮询 deadline，不能证明有界。未热修改旧管理器或第三方包。

晚到的客体批量回执确认四例均已结束，均报告自有句柄/缓冲释放；这不是原游戏
资源/PTD 释放证据。控制恢复曾需要专用 VM 强制关机，已单独记录；随后恢复原
客体 BCD、移除本轮七项串口设置，冷启动核对后正常关机。没有宿主输入、宿主
BCD 修改或 VM 快照。收尾、独立复核及小型复现包见
`analysis/terminal-wait-kd-thread-closeout-v1-20261110.json`、
`analysis/terminal-wait-kd-thread-review-v1-20261110.json` 和
`analysis/terminal-wait-kd-thread-support-v1-20261110.zip`。

## 只读控制期限修复（2026-11-10）

新的 `isolated_vm_bounded_query_v3` 已在专用 Windows VM 中完成短预检，解决新入口
被 WinRM 接收重试拖成无限等待的问题。实测 2 秒期限终止本次宿主查询进程树，随后
同 boot 状态查询正常，客体正常关机；没有启动 KD、fixture 或原游戏。超时明确保留
客体命令结束状态未知，不能把宿主 Job 结束报告成远端取消。旧入口没有热修改。

v1 因独立解释器缺少原环境的系统依赖导入而失败；v2 修正依赖路径及请求大小/迟到
响应判定后通过客体短测；v3 再补齐初始化及清理异常记账，最终短测通过。失败版本
只供复现，后续查询使用 v3 的 `query` 和 `completed`。三次短测均没有新增游戏返回
证据，第一关和任务 2/8 不变，完整57项/首次消费/三次握手/资源PTD仍未完成。

普通 KD CONTEXT 的完整状态缺口仍在；不因控制期限通过再次重复该配方。WHP 原始
寄存器结构仅是新监控后端的静态候选，不可附着当前 VMware 分区，也没有证明无
客体改写的精确停点、全CPU同一停机代次或浮点字段有效性。先验证这些能力，再考虑
操作系统/游戏迁移；不得用候选字段声明把完整状态标真。

## WHP 自有 CPU 的自然返回预检（2026-11-10）

候选后端已从静态字段检查推进到实际硬件执行：两个自有 32 位保护模式 VP 分别
自然执行 CALL/RET，在页内返回地址 `307B`、首次整数结果消费之前停下，恢复后
各消费一次。三个边界均等待两个 WHvRun 调用结束并 join 后才读取状态，不宣称
两个 VP 在同一墙钟瞬间停住。仅改变 GPA 执行权限；首次运行后不设置寄存器、
不写指令或 DR、不注入客体事件。这是自有微客体，不是 Windows 或原游戏。

每例配置两个 VP，保留 4 GiB 地址范围但实际只提交/映射 64 KiB。现有 Windows VM
保持关闭，无磁盘、图形、网络或输入迁移。v1/v2 原生过程分别约 0.125/0.110 秒，
外层独立 Job 监督分别约 0.313/0.266 秒；均实际删除 VP、解除映射、删除分区及释放
地址范围，监督结束后 Job 活跃进程为 0。这些清理不是原游戏资源/PTD 清理。

原始 FP/XMM 读取与客体执行的 FXSAVE32、WHP XSAVE 逐字段一致；TOP=4、物理
FTW=B0 的空洞顺序重建全标签 30FF。v1 普通路径的 FOP/FDP 实测为 0，不填造。
v2 在原合成程序中留下未屏蔽零除，取得 FOP=04B3、FIP=2059、两 VP 各自的
FDP=8008/9008，三方一致，证明接口能够返回非零值；不能倒推其它时刻。v2 每个
边界另复读原始 XSAVE，字节一致。CPUID 声明的 FCS/FDS 弃用语义、XSTATE_BV 的
init-state 语义分别处理，不能把缺失状态解释成零。尚未验证 64 位或 WOW64 兼容
模式、隐藏描述符高位和 Windows 当前所有权。

**执行权限退出将保存的 RF 置为 1，完整 flags 透明性仍失败。** 这也可能影响下一
条指令的执行断点；DR 数值不变不足以证明调试行为不变。该效应符合
[Intel SDM §28.3.3](https://cdrdv2-public.intel.com/789573/252046-sdm-change-document.pdf)
的 EPT 退出规则。禁止统一清 RF 或用推测的旧值通过完整状态检查。下一步必须先
证明原 RF 的可追溯来源及调试/恢复行为等价，或验证不会丢失该原值的停机机制；
再核实 Windows/WOW64 适配，之后才可迁移系统和采 `453CB5 → 4967B0`。

离线验证固定报告 SHA 和每份内存/XSAVE 原字节，拒绝改 PC、提前消费、清 RF、
伪造浮点指针、未 join 及提升 fullstate。独立复核另从原字节复算。全部通过只认证
上述有限能力；`accepted/fullstate/fullABI=false`，三次游戏握手、真实等待消费及
资源/PTD 仍未完成，正式任务保持 **2/8**。无需为这轮预检启动游戏长前缀。

证据入口：`analysis/terminal-wait-whp-proof-v1-20261110.json`、
`analysis/terminal-wait-whp-proof-v2-20261110.json`、
`analysis/terminal-wait-whp-review-v1-20261110.json`；原始小型恢复包及清单见
`analysis/terminal-wait-whp-support-v1-20261110.zip` 和
`analysis/terminal-wait-whp-closeout-v1-20261110.json`。压缩包是同盘恢复副本，
不是独立容灾备份；不复制全部父历史，也不修改旧失败来源。

## RF 与真实客体断点的对照（2026-11-10）

这轮实际检验了上一节的恢复风险，**没有找到可用于原游戏的通用 RF 还原方案**。
两 VP 启用原合成程序的 DR0=307B、DR7=401，使用客体真实 IDT 和 #DB 处理器；
宿主不拦截/注入 #DB、不替换代码或 DR。只在明确标记的错误修复负例中，宿主将
已停止 VP 的 RF 清除，原值和唯一位差全部保留，不能把负例入口作为生产采集器。

| 原执行路径 | 不加返回页拦截的基线 | 返回页拦截后保留 RF | 返回页拦截后错误清 RF |
| --- | --- | --- | --- |
| CALL / near RET | 每 VP 处理 1 次 #DB、消费 1 次 | 1 次 #DB、消费 1 次 | **2 次 #DB**、消费仍 1 次 |
| 自有 IRETD 恢复 RF=1 | 0 次 #DB、消费 1 次 | 0 次 #DB、消费 1 次 | **新增 1 次 #DB**、消费仍 1 次 |

这里的基线仍包含共同的 callee-entry EPT，只对照返回页是否拦截，不称全程无观察器。
保留 RF 的两组最终完整 64 KiB 内存、64 个原始寄存器和 960 B XSAVE 与各自基线
逐字节相等。错误清位的 RET 组最终寄存器和 XSAVE **仍然相同**，内存却在两 VP
的异常计数各多 1；因此不能只用最终寄存器相等、消费一次或进程退出认证恢复等价。

新现场还证明：RET 在执行断点处先进入 #DB，处理器中的 IRETD 把 RF=1 带回
307B，然后才触发返回页 EPT。拦截时消费计数为 0、异常计数已经为 1，DR6.B0
和原异常栈核对一致。返回地址和恢复的 ESP 并不能证明直接前驱仍是 near RET。
参考 [Intel SDM Vol.3B §20.3.1.1](https://cdrdv2.intel.com/v1/dl/getContent/671427)
及 [Vol.3C §30.3.3](https://cdrdv2.intel.com/v1/dl/getContent/671506)；官方规则和
本机实际退出次序分别核验，不将这组实测扩大成所有事件递送/页面错误的顺序定理。

初版基线已执行至 HLT 后 5001，但断言错误要求 5000；原失败回执保留，复用其
完整原字节离线验证，未重跑/重签基线。第二版在原 #DB 已执行后拒绝“异常计数应
为 0”的假设，没有清 RF。第三版纠正观察模型，五个不同对照各执行一次；共七次
有界微客体调用，无 Windows 或原游戏启动。每次监督约 0.25 秒，所有 VP/分区/
内存和 Job 均清理。没有同停点 XSAVE 二次读取原件，不沿用上一轮的复读声明。

下一条件是取得**真实前驱及事件递送路径**或不丢失 RF 的观察出口；在此之前拒绝
“看到返回地址便清 RF”和“保留 RF 的两组对照通过便通用认证”两种推论。完整57项、
Windows/WOW64、真实等待消费、三次握手及资源/PTD 仍未通过，任务保持 **2/8**。
这轮没有为测试原游戏再次运行长前缀，也没有降低完整状态或事件/资源验收要求。

证据：`analysis/terminal-wait-whp-rf-proof-v1-20261110.json`、
`analysis/terminal-wait-whp-rf-review-v1-20261110.json`、
`analysis/terminal-wait-whp-rf-closeout-v1-20261110.json`。原始报告/内存/XSAVE 按内容
去重保存在 `analysis/terminal-wait-whp-rf-support-v1-20261110.zip`；manifest 记录
原路径、大小、SHA 和恢复位置，验证器直接读取压缩包，不依赖展开缓存。清理清单
只针对本轮已核对入包的展开副本，不删除历史原始资料或旧证据。

### 前驱记录接口预检（2026-11-10）

当前 SDK 26100 的 WHV_REGISTER_NAME 没有直接的 DebugCtl/LBR/LER/PT 项；TLFS
HV_REGISTER_NAME 属于另一接口，禁止把其编号直接传入 WHP getter。公开的
ProcessorPerfmonFeatures 能力查询 code=1009 已只读执行：当前 DLL 返回
HRESULT=80370300、written=0，未获得有效 8 字节能力结构。因此 PMU/LBR 支持状态
保持 unknown，不能解释为硬件不支持，也不能把 XSAVE 能力当作 LBR 能力。

此次没有创建分区、启动 Windows/游戏、修改配置或发送输入。真实前驱及事件历史
仍未取得，RF 恢复、等待消费及正式任务2/8不变。下一步需先查明当前运行时对该
公开能力入口的支持条件，并建立合法的记录读取路径；能力位即使可用，也不等于
已取得目标前驱或完整事件递送来源。原查询实现及回执见
terminal_whp_predecessor_capability.py 和 terminal-wait-whp-predecessor-capability-v1-20261110.json。

### 当前运行时支持边界（2026-11-10）

实测宿主 Windows 10 家庭中文版 build19045，WHP DLL FileVersion19041.6093。
独立原字节分析确认 WHvGetCapability 对1009在分派阶段直接返回80370300：
WrittenSize先置0，没有进入硬件能力读取，也不写返回缓冲。因此当前障碍是这份
宿主 DLL 未实现该 selector，不能靠换 SDK、重复查询或仅升级客体系统解决；不据此
推断物理CPU没有LBR。原字节范围/分支及哈希见 runtime-review 报告。

接口分开处理：WHP 的 perfmon property 是功能暴露开关，不是前驱记录读取器；
TLFS编号不能混入WHP。微软另公开了受管 Hyper-V VM 的
[Set-VMProcessor -Perfmon](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/performance-monitoring-hardware)
配置路径，但本机 Hyper-V 模块和该命令均不可用。该路径还要求受支持硬件/VM配置，
开启后仍需客体记录读取及精确停止、事件过滤/丢失验证，不能冒称现有VMware客体
或WHP分区已具备前驱读取资格。QEMU作者的
[兼容性补丁](https://patchew.org/QEMU/20260324151323.74473-1-mohamed@unpredictable.fr/20260324151323.74473-2-mohamed@unpredictable.fr/)
将20348系列作为这项WHP查询的实现起点；这是上游实现说明，不是任意后续系统
及硬件组合的通过保证。

本轮有界预检止于接口/运行时条件，不创建分区、不启动游戏、不更换系统DLL、
启用宿主功能或重启。当前配置下，WHP-LBR路线尚不具备采集入口。后续必须先取得
兼容运行时和合法读取机制，或验证不依赖该接口的观察后端；不能把问题继续归为
等待/消费代码错误而重复长跑。真实前驱、事件递送、RF恢复和第一关仍未完成，2/8不变。

### 不修改宿主的 TCG 前驱/事件有限预检（2026-11-10）

复用 F 盘已保留 QEMU，使用纯软件 TCG、one-insn-per-tb、exec/int/nochain 日志，
运行无磁盘、无网络、无显示窗口的自有 multiboot ELF32。配置2 vCPU/4 GiB，但
目标路径仅由BSP/VP0执行，不能称双CPU握手。该路径不调用旧GDB/HMP浮点读取，
旧完整状态缺口保持不变，不以模拟执行冒充原游戏硬件原生验收。

v1在15秒边界退出，stderr明确缺少multiboot_dma.bin，未进入目标代码；原失败
和ELF原样保存。只从已有已验安装包增加提取该固件，并修正静态发现的JMP偏移，
v2约1.578秒监督完成，客体输出SHDR1E。v3增加原异常栈/DR6字节输出，约1.688秒
监督完成；没有增加时限重跑同一失败。两成功例均自然通过isa-debug-exit结束，
私有宿主Job清空，没有Windows启动、原游戏、宿主输入或系统配置改变。

v3原ELF及逐条TB入口联合证明有限路径：CALL100300→RET100384→#DB at100305→
原IDT处理器100400→IRETD100433→首次消费100305。原异常帧字节是
EIP=100305、CS=8、EFLAGS=6，DR6=FFFF0FF1；事件日志核对DR0=100305、DR7=401。
处理器在自己的异常栈上设置RF，再执行IRETD；R输出和该入口只出现一次，输出1
是异常处理计数，不是另一个消费计数器。日志按VP核对，不能把相邻地址或Trace
入口单独解释为指令退休。原栈、事件记录、后续执行及原指令必须共同保留。

这是一个可运行的**有限前驱/事件观察后端**，不是完整原游戏采集器。TCG执行语义
与硬件原生等价、发布二进制与精确构建源码闭合、完整57项/浮点字段、Windows/
WOW64和原生资源寿命仍未证明。没有据此修复WHP的RF，也没有启动战斗长前缀。
下一步先补全这一后端的状态来源与精确构建身份，并验证真实Windows边界；只有
通过原验收标准才接等待消费。任务继续2/8。原始小包、有限proof及独立review见
analysis/terminal-wait-tcg-predecessor-*；原字节未覆写，未复制旧QEMU环境。
# 2026-11-10 TCG 精确源码与 x87 实际导出预检

本轮只执行 F 盘 headless、无磁盘/网络的自有 ELF32 客体，2 VP/4 GiB，目标路径仅
VP0；Windows 与原游戏未启动。预检外层约 1.5 秒、Job 清空，没有宿主输入。
发布者 Git 浅层源码现已取得并按 Git 对象校验：提交
`e470268ff446ec56728215a987ed166d5ed8fb64`，树
`f7f8eccd4e165c6c448946419cfbdb48f9e3db28`。它与运行时版本字符串对应，但发布
构建脚本未锁定编译器/MSYS2 依赖，缺少该次构建日志及干净树证明；未做字节一致重建，
不能把源码提交可读报告为精确二进制构建来源全部闭合。

新实际反例先把 FXSAVE 区域填 A5，再执行 FNINIT、FLD 1、FADD 2、FXSAVE、FNSTENV。
ST0 得到 3.0；FNSTENV 给出 FIP=10016F、FDP=100904、CS=8、DS=10h，但 FOP=0，
并非该 FADD 的 005。FXSAVE 的 FOP 保留 A5A5，FIP/FDP/CS/DS 全零；实测
CPUID.7.0:EBX=0，不可用 zero-fcs-fds/fdp-excptn-only 特性解释。完整原始 544B 与
逐 TB 轨迹保留，独立复核按实际 ELF 指令定位，未用预期值填充采样。

精确源码进一步显示恢复路径缺口：FLDENV/FXRSTOR 未恢复指针/操作码，GDB 浮点
读写旋转不对称，完整 tag 的表示也需审查。因此完整57项及 Windows/WOW64 准入
**拒绝**；只增加 getter 或推算/补零不合格。下一实施门是 F 盘可追溯的独立构建，
修正并复核 x87 更新/保存/恢复及状态接口，先通过有界非零状态与恢复对照，再接原
等待和消费者。未勾选任何新验收项，仍 2/8。

证据：`analysis/terminal-wait-tcg-source-identity-v1-20261110.json`、
`analysis/terminal-wait-tcg-fp-proof-v1-20261110.json`、
`analysis/terminal-wait-tcg-state-review-v2-20261110.json`。小原件另有一份同盘 ZIP，
不是独立容灾备份；精确源码 pack 留 F 盘，不进 Git。首轮45秒超时的26,206,207B
不完整 pack 已记 SHA 并删除，旧运行时/旧历史证据不变。832份小文件新鲜 SHA、13份
大文件仅大小保全通过，普通/-O各4项检查与严格 OpenSpec 通过，不替代功能验收。

### F 盘可追溯 TCG 修正版与保存/恢复预检（2026-11-10）

以同一固定提交构建项目修正版，依赖子模块固定到实际提交，保存编译器组件、动态库、
配置、源差异和运行二进制 SHA。沿用已经位于 F:\WSL_Linux 的 Ubuntu，所有新源码、
构建缓存、临时文件及证据位于 F 盘；没有安装宿主包、修改系统设置或操作宿主输入。
构建限制为 nice 10、两个编译任务；自有客体继续 headless、2 VP/4 GiB、无磁盘/网络。
这是可追溯的本地构建，不是发布者二进制的字节一致重建。

已修复非零 x87 FOP/FIP/FDP/选择子维护、环境与 FX 保存恢复、64 位指针格式及
GDB ST 写入的 TOP 索引。32 位、真实长模式高指针和 FNSTENV/FLDENV 短预检通过。
修正此前完整 tag 的推断：现代 x87 保存内部空/非空，非空分类由 FP80 内容派生；
不凭旧报告增加无硬件依据的 shadow tag。保留旧记录，具体修订见 patch contract。

硬件反例发现未屏蔽 0/0 的寄存器除法错误提交了结果并弹栈。针对 D8/DC/DE 寄存器
FDIV/FDIVR[/P] 修复预计算异常的提交顺序；六组硬件对照覆盖屏蔽/未屏蔽 #I/#Z 和
正常正反除法，比对状态、TOP、tag 与全部非空 FP80，全部通过。此结论不扩展为
所有 x87 算术、内存源转换或 #O/#U/#P 后计算异常已经等价。

新增停止态 typed QMP 来源，检查每个 VP 实际 stopped，并输出全宽 GPR、段缓存、
CR/DR、x87/FP80、MXCSR/XMM。DR4/5明确遵循别名/#UD规则，不伪造独立槽。GDT/IDT
的容器字段不冒称额外架构寄存器。此来源仍标记 fullstate_accepted=false。

同进程设备流恢复补齐 FCS/FDS、零值 FOP/FIP/FDP 和 TCG 条件旗/DF 缓存。首次实际
加载触发 yank 注册/注销不对称断言；定位后增加与原清理配对的注册，保留首个失败。
修正版三组保存 A→客体指令扰动 B→加载 A→自然重执行 B→退出均约 1 秒通过：
32 位非零、32 位零值反向、64 位高指针。两 VP 全部已导出字段相等；64 位 FIP 为
0x10010039f、FDP 为 0x100100904，XMM15 从零恢复到原非零内容。包含页表的自有
20 KiB 区域在四个停点 SHA 一致；没有把这个范围称为全 4 GiB 内存证明。

设备流显式使用 send-configuration=off/suppress-vmdesc=on，仅限本次同构建、同
机器/CPU/拓扑的无盘微客体。它**不含 RAM**，加载失败也不保证原子回滚；其它可选
CPU 子节、完整机器状态与原生资源寿命未获认证。短预检不是 Windows/WOW64 或
游戏验收，不据此启动战斗长前缀。真实等待返回、首次结果消费、三次握手、资源/PTD
释放与两例全新原生完整重放均未完成；正式进度仍 2/8。

精确构建链见 analysis/terminal-wait-tcg-build-manifest-v1..v4-20261110.json；
补丁、实际原件、独立复核、保全与容量汇总见本轮 tcg-build closeout/capsule。

### 架构 57 项、RF/IRQ 与含 RAM 恢复（2026-11-11）

复用上述固定来源实现版本化架构 57 项适配及 Unicorn 读回。FP0..7 保持物理槽顺序，
完整 tag 由原 FP80/空位派生，DR4/5 按 CR4.DE=0 的真实 DR6/7 别名读取；DE=1 拒绝。
旧 Unicorn raw API 的 DR4/5 是可独立写入的填充槽，原接口和旧验收保持原字节，
新合同不冒称与其直接兼容。实际 oracle 又证实 UC_MODE32 的 FIP/FDP 可以完整保存
64 位；v2 更正 v1 的过严宽度限制，保留旧报告，未将高位合成宽度例冒充新现场。
普通 32 位来源的完整57项读回、真实指令别名和拒绝回归通过，隐藏段缓存另保留。

新增只读全 RAMBlock SHA 与事件观察，沿用 F 盘源码/依赖并逐次认证构建。完整
QMP 文件迁移保存配置、CPU、设备及 RAM，源客体自然结束后才启动新的恢复客体，
始终最多一台2 VP/4 GiB无盘无网络后台客体，没有宿主交互输入或系统配置修改。
迁移流约9.8MiB，实际 RAM 块合计4,312,342,528B，包括完整4GiB pc.ram；当前v8两例
原流及压缩恢复副本可恢复全部原字节，摘要不替代原流。停止VP+RCU并非任意DMA/IOthread冻结证明，
本轮范围限于这个无外部I/O的自有客体。

首次加载发现 INMIGRATE→DEBUG 不在状态转换表，最小补丁允许恢复原调试停止状态，
没有先执行客体再补现场。复用原流继续定位：同步异常已失效时仍存在旧 payload，
另有真实 HARD IRQ 差异。新TCG子节完整保存 error_code/is_int/next_eip/old_exception，
不清零或过滤；后续两端明确使用同一 icount 与虚拟 RTC。真实IRQ仍逐字段比较。
源/恢复流同时固定同一二进制身份，跨版本旧流诊断单独标记，不计同构建通过例。

RF静态复核发现 GDB 与客体执行断点同址时，旧处理器可能把 RF=1 的观察停点转换为
额外 #DB。修补仅限制非watchpoint分支，保留原RF及RF0行为。1.25秒短检实际经历
原 #DB→处理器→IRETD→RF=1 同址停点→消费，原异常帧RF和计数1均保留，无额外#DB。

完整迁移三组有界证据现已取得：普通CALL前、IRETD后的RF=1返回点、真实PIT/PIC
待递送IRQ。每组两个停止边界A/B的架构57项、两VP原始导出状态、全部已导出事件
字段和8个RAM块哈希一致，A/B的RAM确实由客体指令改变；自然输出和退出均一致。
pending例在A实见IF=0及HARD2，恢复后原STI/NOP使IRQ20递送一次，再完成#DB/IRETD。
完整案例约69–73秒，主要是四次全RAM哈希，未启动完整游戏采集或小时级前缀。

第一组原report的 continued_trajectory=false 原样保留：校验曾把已声明B之后的
异步 isa-debug-exit 监督尾段也算入。独立复核确认A→B前74条入口及异常路径完全
一致；target在B后额外记录100327的TB入口，不能推定HLT已退休。新的固定端点证明
引用原SHA，显式保留exit_suffix_equal=false，不宣称退出监督尾段完整指令等价。
另外两组用修正后的端点验证；TB入口仍须联合原事件/栈/输出，不单独当指令退休。

Windows/WOW64 准入仍拒绝。真实兼容模式短客体经原远返回进入 CS32/LMA，仍保留
R8=123456789ABCDEF0、4GiB FS基址、高位FIP/FDP和XMM15；当前普通32位适配正确拒绝，
没有丢弃高位套用旧引擎。首个该fixture切片长度错误造成GDT移位，已按原字节定位
修正并保留小失败；不是Windows失败。下一步需要兼容模式的完整64位上下文包络、
无损57项视图及独立读回/续跑合同，再启动Windows/WOW64的真实边界预检。同步异常
待分派、活跃AP调度、一般设备/磁盘状态与游戏资源寿命也不由这些微客体自动认证。
原等待返回、453CB5首次消费、三握手、PTD释放和两例原游戏完整验收仍未完成，2/8不变。

本轮证据索引：analysis/terminal-wait-tcg-checkpoint-closeout-v1-20261111.json；
canonical57 v1/v2合同、event-observer合同及checkpoint独立复核均保留各自身份。
收尾清理了本轮被替代v5/v7全迁移流及中间二进制，原大小/SHA与替代原因见retirement；
这些已退役全流不再报告为可用，小失败/轨迹/状态记录仍保留。当前RF压缩主来源、
pending IRQ原流主来源及一份同盘恢复副本仍可用，不称独立容灾备份。
`devtools.terminal_tcg_checkpoint_materialize`可在全新F盘目录认证展开当前来源，不启动VM，
不覆盖原目录；RF实际展开后端点复验已通过，临时副本已清理。旧历史证据保持原字节。

### 兼容模式无损上下文与真实高位消费（2026-11-11）

`terminal_tcg_compat_context`新增独立版本包络，不把兼容模式强行装入旧Unicorn32格式。
完整原raw64记录保持可逆，57名视图显式派生；低32位GPR视图之外保留高32位、R8–15、
XMM8–15、全64位控制/调试寄存器和段缓存基址。FIP/FDP不随当前CS32而截断。
CR4.DE=1时DR4/5标记不可读，不造零值。来源摘要由调用方外部固定，包络本身不冒充
采集签名或整机状态。普通及`-O`各10项拒绝/无损回归通过。

自有客体真实远返回进入CS32/LMA，再执行原远跳转进入CS64消费：R8写入输出，FS寻址
读取4GiB以上虚拟地址，XMM15存储，RDMSR读取FS.base，FXSAVE64保存高位FIP/FDP。
高地址页实际映射另一物理页，低页放不同哨兵，截断基址不能碰巧读到同值。首个fixture
因低地址3MiB尚未映射而#PF，修正其自身页表后3.62秒短检通过；旧失败保持原字节。

首个完整异步迁移案例CPU/RAM和消费虽一致，A点IRQ仍不一致，正确判失败。独立解码
证明IRQ=2已在保存流内，问题是采样后返回事件循环再保存的间隙。新同命令接口先观察、
同步保存、再观察，最终完整恢复案例保持before=after=targetA、sourceB=targetB，
两VP、全部已导出事件及8块共4,312,342,528B RAM一致；消费输出552B、自然退出33一致。
固定A→B的74条执行入口记录一致；入口记录联合原指令/输出使用，不单独宣称指令退休。
v11b和启用VMDK的最终v12分别88.71/89.84秒完成，最终源码/编译依赖/二进制身份可追溯。

同步保存内部仍可能临时释放BQL，不是通用原子快照。接口拒绝附着磁盘、网络客户端
和用户IOThread；查询未涵盖所有内部IOThread，因此仍只认证固定无外部I/O微客体。
Windows磁盘不可走此接口；没有以预检成功代替Windows/WOW64、真实等待或资源寿命验收。
原453CB5首次消费、三次握手、PTD释放与两例全新原生完整重放仍未完成，正式2/8。

证据入口：`analysis/terminal-wait-tcg-compat-current-v1-20261111.json`及兼容模式
closeout/capsule/stream清单；独立复核保留原v11b结论及最终v12增量。当前完整流压缩保留，
另有一份同盘恢复副本；中间构建/被替代全流的退役记录明确列出原SHA与现可用性。

Windows仅完成60秒有界启动观察：首次因精简运行时未含VMDK而在打开原盘前拒绝，
启用固定源码的原VMDK驱动后，使用新qcow2覆盖层启动同一Windows磁盘。20秒看到
Windows标志，60秒仍为加载指示，未观察到桌面或WOW64应用；不报告为系统准入通过。
客体2VP/4GiB、无网络、无显示窗口、无输入；覆盖层承接写入，原VMDK大小/mtime保持，
未额外计算整块原盘SHA，不能将此检查说成逐字节校验。全部本轮QEMU均已退出。
当前构建无slirp，后续需先完成有界启动定位和客体内自动控制通道，再验证WOW64真实
模式切换/等待边界。不得改宿主网络或回退到宿主交互桌面；不得直接把无盘同步保存
接口用于Windows磁盘快照。当前两个截图及覆盖层保留在F盘，尚未重跑游戏前缀。

### Windows 启动定位与隔离控制通道（2026-11-11 接续）

复用精确v12运行时与上一轮只读覆盖层。分阶段CPU/RAM架构读取、磁盘计数和画面
显示Windows从64位内核启动推进到设备准备、计算机设置和锁屏，不是始终停在同一
位置。保留原盘和父覆盖层，写入仅进入本轮新子层；2VP/4GiB，无宿主显示或输入。

既有Linux环境已含libslirp0；仅在F盘提取同版本开发包头文件，不安装宿主软件。
启用slirp触发整个目标重编，180秒预算停止且没有产生v13运行时，不重复长构建。
后续仍用已验v12执行客体，复用已有Windows QEMU的machine none网络转发进程。
转发端只绑定回环地址，restrict=on，无TAP/桥接及宿主网络配置修改；实际QMP确认
running、CPU列表为空、base/plugged memory均为0，不把该进程当另一台Windows客体。

首个转发配置带-S，源码复核发现非running时发送路径仅排队；旧失败保留，发现后
立即停止下一次尚未认证的探针。移除-S后0.766秒真实ARP请求/应答及Job清理通过。
客体抓包随后证明DHCP及10.0.2.15地址使用，5985端口先RST、后SYN/ACK和双向数据；
因此网络与WinRM服务启动阶段已分开定位。raw PCAP仅在F盘保留，Git摘要不含认证载荷。

WinRM保持NTLM与强制消息加密，使用独立QEMU UUID/Manufacturer/计算机名约束，不
冒用原VMware DHCP/UUID身份。宿主查询复用已验Windows Job监督，明确区分请求完成
与超时未知。第一次5秒operation超时，增大至20秒/55秒宿主总期限仍未成功，不能
将失败仅归因为预算过短；后续记录open_shell/run_command/get_command_output等
阶段，并保持同一客体有界运行以定位，避免每次失败就重新启动Windows。

这些启动/网络结果不替代完整状态恢复或游戏原生验收。Windows磁盘仍禁止使用仅
认证无盘微客体的同步检查点接口；真实等待返回、453CB5消费、三握手、资源/PTD
和两例完整重放均须按原合同验证，三关及正式2/8不因网络可达而改变。

最终同一客体内的阶段记录证实open_shell约7.4秒、run_command约0.4秒成功，停点是
get_command_output。55秒监督到期仅终止客户端Job，未宣称远端取消。新接续工具校验
原phase文件SHA及owned shell/command GUID，仅继续Receive，绝不重投；约1.438秒
取得客体身份、2CPU/4GiB和WinRM运行状态，随后cleanup_command/close_shell完成。
同寿命WOW64命令也通过原GUID续收：SysWOW64 PowerShell中IntPtr.Size=4、Is64BitProcess
为false、Is64BitOperatingSystem为true，退出后PID不存在；约8.453秒续收并清理完成。
原超时报告不改成成功，新的成功报告明确引用原命令和续收；普通/-O各5项拒绝回归通过。

最后一轮455.27秒内由Agent主动结束，未到600秒监督上限；所有VM/sidecar及宿主查询
Job均清空，无用户输入。这里只证明实际32位进程可运行/退出，不证明该进程的完整
CPU上下文恢复、原游戏ABI/等待返回或原生资源清理。Windows时钟/boot字段按客体原值
记录，不将其UTC显示直接当宿主时间对齐证据。下一步使用已通控制通道准备无UI的
当前所有者等待探针，补TCG真实停止点和完整Windows/WOW64状态合同，再接原游戏消费链。

本轮最终磁盘用safe rebase合并到上轮只读基线，qemu-img compare验证虚拟内容等价；
比较前后本轮源层和上轮基线SHA不变。之后才退役本轮源层，旧qcow2容器字节不再可用，
当前逻辑磁盘内容由`tcg-windows-current-v1/disk.qcow2`及固定父链保留，不冒称容器字节
相同；原worker.vmdk只做size/mtime检查，未重新全盘哈希。原盘、上轮基线、旧验收均未改。
证据入口为`analysis/terminal-wait-tcg-windows-control-proof-v1-20261111.json`、对应
evidence/capsule/retirement和三份独立复核；raw认证网络片段仅留F盘，Git只含头部摘要。
# 2026-11-11 无 UI 等待探针控制通道预检

来源为 `analysis/terminal-wait-tcg-native-control-closeout-v1-20261111.json`，
小现场在同前缀的 `terminal-wait-tcg-native-control-v1-20261111.zip`。
沿用已认证 v12 TCG 和 current-v1 磁盘，新增一次 2 CPU / 4 GiB 客体，
838.128 秒内结束。无宿主输入，没有执行 go 或观察器，目标等待停点为 0。

真实进展：WinRM 标准输入上传的探针四文件已通过 SHA 校验；发送超时后，
原 command 的续查取得 prepared=true，命令和 shell 关闭。长 EncodedCommand
版本在 run_command 失败，保留为失败来源，不再复用此上传方式。
启动命令两次 55 秒接收期限后最终出现 JSONDecodeError；随后只读查询在
open_shell 阶段超时。旧库可能在客户端退出前消费但未保存输出，现有证据
不能判定具体丢失位置，更不能把空输出当作探针失败或成功。

后续入口为 `terminal_tcg_wait_control_v5`：使用标准输入传输，并调用
`terminal_winrm_output_v2` 在 Receive 前持久化 pending，逐片保存输出；
存在未完成 Receive 时拒绝续收为完整证据，转读客体持久结果。已运行版本
保留原字节。修正版只有离线正反例和独立复核，未通过真实 WinRM 恢复验证。

复核还发现：探针在 go 前启动两条忙循环，同时启动 300 秒 watchdog；
该时序与慢控制通道存在预算竞争。双 CPU 诊断都在 64 位内核态，单快照
不能证明忙循环是此次失联根因。下一轮先复用失败 overlay 读取客体持久
ready/result，调整新版本的计数器放行时序，再做有界预检；不得重复本配方。
未执行的观察器草案仍缺最终消费帧/FX/完整 ABI 核对，不能作为验收器使用。

原任务维持 2/8；完整目标状态、等待返回、首次消费、三握手、资源/PTD、
Windows 状态恢复和两例新鲜游戏重放均未新增验收。VM/侧车已退出；这不能
代替探针自身资源清理证据。保留一份 83.06 MiB 失败 overlay，待恢复独特
现场并解决原因后退役；屏幕原字节 gzip 保留，没有备份。832 SHA / 13 size
保全通过，原 current-v1 SHA 不变。早期接收器离线测试曾使用默认临时目录
并自动清除，最终测试已改为显式 F 盘；新 VM/镜像/日志/持久证据均在 F 盘。

## 2026-11-11 客体现场恢复与自有等待消费链

证据入口：`analysis/terminal-wait-tcg-gated-closeout-v1-20261111.json`，独立复核
`terminal-wait-tcg-gated-review-v1-20261111.json`，原字节小包
`terminal-wait-tcg-gated-source-v1-20261111.zip`。这是 self-owned 能力预检，正式仍 2/8。

只读解析既有 VMDK/QCOW2/NTFS 链，1.125 秒恢复旧 ready/result，确认旧探针成功
就绪、未收到 go、240 秒 gate 到期，signals=0、清理字段成功。四份上传输入与原
SHA 一致，磁盘原字节未改。未为恢复旧现场启动 Windows，不复用旧事件句柄。

本轮只启动一次 2 CPU / 4 GiB 无显示客体，871.418 秒内结束，内部先后两个自有
新进程。v2 将 counter/peer 原工作推迟到 go 后，但完整私有内存读取遇未驻留页，
观察未完整；恢复后首个 2 秒等待超时，清理成功。v3 在构造阶段预触碰全部 16 KiB
私有页，前三轮相对超时显式为 30 秒、末轮零，214 B 指令模板未改。这个调度余量
不是游戏参数，也不把延长时间当作原游戏等待的等价性证明。

WinRM 普通 PowerShell/WMI 就绪查询仍曾达到 55 秒；同一已认证启动身份下的固定
路径 cmd type 只读查询实测 7.016 / 2.703 秒，结果查询 2.469 秒。durable receiver
实际保存片段，未知 Receive 不续接为完整输出。go 的回执在调试暂停期间 ReadTimeout，
没有重发；客体 go_received、原目标指令和返回轨迹独立确认已经放行。不能把宿主
Job 结束当作远端取消，过期查询随本次 VM 寿命结束，不声称其逐命令取消已验证。

v3 观察 38.845 秒，12 个 CALL/真实 NtWait RET12/post 停点，剔除 3 次非目标命中。
保存双 CPU raw64、兼容视图、TEB PID/TID 原字节、CR3/FS、栈参数、私有内存、代码、
超时原字节；首次 RET 附有 RAM 摘要及 pending events，没有保存全 RAM 或执行恢复。
实际返回 [0,0,0,258]、signals=3。四轮 RET→post 仅精确 EIP/ESP 改变；九槽保存帧、
FP TOP 映射和 XMM0..7 FXSAVE 与 post 原状态匹配。独立审查不调用 consumer 重算
核心记录得到相同结论。helper 清理全部成功，外部查询确认进程退出；宿主/客体
QEMU 和侧车进程均清空，无宿主输入，没有启动原游戏。

严格验证器仍为 false，仅四个 call→ret.raw64 检查失败：CR2 前三轮变化；R9
四轮最终等于真实返回 stub PC 0x775b3bfc；XMM0..5 全被清零。保留实际值和拒绝
报告，不依据 ABI 常识增加豁免。本例 RF 始终为 0，不能声明非零 RF 已等价恢复。
下一步固定 NtWait call edx 所向 0x775d6710 的实际 WOW64 映射字节与模块身份，
追踪 R9/XMM 写入及分支，另查 CR2 页故障/调度来源，然后再评估完整状态合同。
还未独立观察 FXRSTOR 后完整调用者恢复，未进行 Windows 状态恢复、独立完整重放、
两例新鲜游戏寿命或原游戏资源/PTD 清理。自有消费链成功不勾选 2.1–4.2。

普通/-O 各 25 项离线测试、832 SHA/13 size 保全通过；严格规格和 Git 审计见收尾。
新增本地证据约 87.8 MiB，无备份；唯一新 overlay 约 86.4 MiB。完整观察 JSON 和
截图已无损压缩，Git 小包保留原字节及原相对路径，旧验证器复用前从包恢复输入并
核对 SHA。压缩替换清单位于本轮目录 retirement.json，未删除任何历史来源。
