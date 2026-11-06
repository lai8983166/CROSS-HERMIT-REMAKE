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
