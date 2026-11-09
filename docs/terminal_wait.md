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
