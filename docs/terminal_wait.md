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
