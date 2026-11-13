# 同一原生所有者的平台叶协议（未获原生准入）

`devtools/terminal_native_owner.cpp` 是 x86、Windows subsystem、无窗口的候选平台叶
所有者。当前只完成静态编译；编译不构成原生预检、首次协作让出或游戏准入。
它不加载原程序，不安装原程序代码，不执行游戏 callback，不填写游戏结果。
外部原指令执行器负责原 `56E110 → 421F50 → callback` 及全部游戏逻辑。

本次原生调用如获准，只能由总调度器在一份有硬期限的 Windows Job 内启动一次，
最长 30 秒，失败停止。该程序自身的 `INFINITE` 等待是真实原生等待；它没有超时后
合成成功的后备路径。外层总期限与失败清理不可省略。

## 线程与入口投影

- lane `0` 是程序的真实启动线程，作为 MAIN 服务线程。lane `1` 是唯一游戏 worker
  对应的真实 `CreateThread(..., CREATE_SUSPENDED, ...)` 线程。
- 另有一个仅解析 stdin、入队的基础设施 reader 线程。它不执行请求的平台叶。
- `CreateThread` 由 MAIN 调用；native entry 明确为 `WorkerDispatcher`，并非 `56E110`。
  guest entry 仅允许 `0x56E110`。guest/native 入口映射和参数映射必须由执行器记录、
  审核；不能称为原生 CPU 直接执行原 `56E110`。
- 两个 lane 队列彼此独立。因此 WORKER 在真实 `WaitForSingleObject(INFINITE)`
  中时，reader 仍接收 MAIN 的 `SetEvent`，MAIN 仍可实际调用它。
- 每项成功进入 dispatch 的请求均在该 lane 固定 TID 执行。回复附真实 TID、TEB。
  `TlsGetValue` 在该真实线程调用并返回 OS 值，同时与所有者跟踪值比较。
- 队列、输出和跟踪代码可能改变 Win32 LastError；每次叶调用前恢复该 lane 上次叶
  捕获的 LastError，调用后立即捕获。`GetLastError` 因而观察平台叶的线程局部状态。
  内存桥接命令不改变该值；协议拒绝返回明确的错误，不伪装成执行过平台叶。

## 编码

stdin/stdout 必须都是管道。ASCII，每行一个消息，数字全部为无符号十进制 u32。
请求 ID 从非零开始且严格递增；响应可能跨 lane 乱序，必须按 ID 关联。

```text
id lane OP arg0 arg1 ...
R id lane native_tid last_error ok result teb=N [key=value ...]
E READY version=1 pid=N main_tid=N main_teb=N reader_tid=N pointer_bits=32
E WORKER_START worker_tid=N teb=N guest_entry=N guest_param=N native_entry=N
```

`ok=1` 表示白名单中的调用确实执行；API 自身失败仍保留实际 `result` 与 LastError，
例如 `TlsAlloc` 的 `4294967295`，不能只看 `ok`。
`ok=0` 表示所有者拒绝执行，附 `reason=SYMBOL`；调用方必须立即判失败。
void API 的 `result=0`、`void=1` 不声称有 Win32 返回值。
所有输出共用互斥串行写入，不混行。协议/基础设施错误直接导致非零进程退出，
不补造正常资源清理报告。除每个调用的回复外，无逐帧或全状态转储。

## 白名单与参数

下表省略每行前面的 `id lane`；指针、句柄均指当前所有者的真实 u32 值。
执行器必须维护显式 guest/native 映射，不得直接传其它进程的地址或句柄。

| OP 与参数 | 结果及限制 |
| --- | --- |
| `GetCurrentThreadId` / `GetCurrentProcessId` / `GetLastError` / `GetTickCount` | 实际 OS 值 |
| `SetLastError error` | void；在对应真实线程设置平台LastError，供原57543B恢复先前值 |
| `Sleep ms` | 真实 Sleep，`ms ≤ 100` |
| `HeapCreate flags initial maximum` | 实际 heap；flags 只能 0，大小各 ≤ 4 MiB |
| `HeapAlloc heap flags size` | 实际地址；flags 仅 0 或 HEAP_ZERO_MEMORY=8 |
| `HeapFree heap flags pointer` | BOOL；flags=0；必须是该 heap 的完整块起点，无在用锁或另一lane的TLS引用 |
| `HeapValidate heap flags pointer` | BOOL；flags=0；pointer=0 或该 heap 的已跟踪块起点 |
| `HeapDestroy heap` | BOOL；必须先释放全部已跟踪块 |
| `MEM_ALLOC size` | 真实 RW VirtualAlloc；无可执行内存权限；保留lane原leaf LastError，实际基础设施错误另记native_last_error |
| `MEM_FREE base` | 真实 VirtualFree；仅完整已跟踪虚拟块且无在用锁/TLS；保留lane原leaf LastError，实际基础设施错误另记native_last_error |
| `MEM_READ address size` | `result=size hex=...`；仅自身已跟踪有效范围 |
| `MEM_WRITE address hex` | `result=字节数`；仅自身范围；hex 非空、偶数长度 |
| `InitializeCriticalSection address` | void，附实际24字节`hex`；4 字节对齐、至少 sizeof(CRITICAL_SECTION)=24 的自身范围 |
| `EnterCriticalSection address` / `LeaveCriticalSection address` | void，附实际24字节`hex`；真实临界区；离开必须由当前持有线程执行 |
| `DeleteCriticalSection address` | void；无持有者、无等候调用才允许 |
| `CreateEventA sa manual initial name` | 真实 event；sa/name=0；manual/initial 各为 0 或 1 |
| `ResetEvent event` / `SetEvent event` | 实际 BOOL；仅自身 event |
| `WaitForSingleObject handle ms` | 实际 wait status；ms≤1000 或 INFINITE=4294967295；仅自身 event/thread |
| `CloseHandle handle` | 实际 BOOL；不能关闭正在等待的句柄；worker 须先观察到真正终止 |
| `CreateThread sa stack guestEntry nativePtd flags guestTidPtr` | 仅 MAIN、仅一次；sa=0、flags=4、guestEntry=5693712、stack≤1MiB；nativePtd 在自身分配的116字节范围，+0x48为0x421F50、+0x4C非零 |
| `ResumeThread workerHandle` | 实际 suspend count；仅 MAIN、一次 resume |
| `GetExitCodeThread workerHandle` | `result=BOOL exit_code=N`；输出参数直接编码入回复 |
| `ExitThread code` | 仅 WORKER；发出退出请求回执后，由该真实 WORKER 执行不返回的 ExitThread |
| `TlsAlloc` | 实际 TLS index |
| `TlsSetValue index value` | 实际 BOOL；value=0 或自身分配内地址 |
| `TlsGetValue index` | 实际指针，附 `tracked_value=N`；不一致即失败退出 |
| `TlsFree index` | 实际 BOOL；两个 lane 均须先清零本 slot |
| `IsBadReadPtr address size` / `IsBadWritePtr address size` | 实际 BOOL；仅自身已跟踪范围，不对外部或无效地址做探测 |
| `GetVersionExA buffer` | 实际 BOOL；自身148字节范围且首字段为148；遵循Windows实际兼容语义 |
| `GetCurrentDirectoryA size buffer` | 实际 OS返回及写入；仅自身范围；只读取本进程工作目录，不改变它 |
| `STATUS` | 仅 MAIN；返回资源计数和 worker 生命周期观察字段 |
| `Shutdown` | 仅 MAIN、必须最后一行；仅全部显式清理完成后返回1并正常结束 |

`CreateThread` 回复额外包含：`worker_tid`、`guest_entry`、`guest_param`、`native_entry`、
`guest_tid_ptr`、`ptd_entry`、`ptd_node`、`ptd_hex`。PTD字段和116字节hex在调用CreateThread前
从实际nativePtd读取，执行器必须已同步原当前PTD字节。其中 `guest_param` 是传给 OS dispatcher 的真实 native PTD 地址；
`guest_tid_ptr` 只记录原 guest 输出字段位置，本程序不写入该位置，执行器必须把真实
`worker_tid` 投影回原输出字段。执行器应另外记录原 guest PTD 与此 native PTD 的映射。

`ExitThread` 回执 `exit_requested=1 termination_observed=0` **不是终止证明**。
回执发送后它先销毁本次通信临时对象，再实际调用 ExitThread。MAIN 必须随后实际
`WaitForSingleObject(workerHandle, ...) == WAIT_OBJECT_0`，再读取实际退出码，最后
关闭句柄。只有这些结果、PTD/TLS/锁/事件/heap 全部显式清理及整体正常退出共同成立，
才可报告本桥接层的资源清理完成；仍不是原游戏完整验收。

## 边界与限额

最多 8 heap、128 分配块、64 临界区、64 API句柄、16 TLS slot；同时分配 ≤4 MiB，
单块 ≤1 MiB，单次传输 ≤32 KiB，两方向各最多16 MiB，最多100000请求，单lane待处理
队列≤256。MEM_READ/WRITE 不允许覆盖活跃临界区字节；锁叶回复的实际24字节hex用于
执行器单向镜像，不允许写回真实锁，也不声称是与另一原生线程活动同步的原子快照。
释放有另一lane TLS 引用的块、删在用
临界区、线程持锁或TLS未清零时退出、资源未清完时 Shutdown，均被明确拒绝。

原 `57553E` 先经 `56F3B0` 释放本线程PTD，`57554F` 才执行 TlsSetValue(index,0)。
因此 HeapFree 允许当前lane释放自身TLS仍指向的块，并回报
`tls_reference_pending_clear=1`；跟踪值保留至原代码实际清零，不提前清除或替换顺序。
其它lane仍引用该块时一律拒绝；ExitThread/Shutdown仍不允许残留TLS值。

没有任意函数调用、任意内存、文件写入、进程注入、GUI、截图、全局输入、GDI/D3D、
场景资源或结果 callback 接口。未知 OP 一律拒绝。程序内的 SetErrorMode 仅用于
自身进程避免错误对话框，不改变宿主全局配置。

编译可使用 VS 2022 Community、VC 14.44.35207、Hostx64/x86：
`/O2 /W4 /WX /MT /EHsc /std:c++17 /link /SUBSYSTEM:WINDOWS /ENTRY:wmainCRTStartup`。
编译目录、TEMP/TMP、obj/exe/log 必须全部在 F 盘。静态 x86/PE subsystem/导入核对
不能替代唯一一次有界原生预检，不能据编译成功启动原游戏。
