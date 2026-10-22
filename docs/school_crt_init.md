# 原版 CRT 冷启动来源与初始化

有限 change：`capture-original-crt-initialization`。本轮始终使用独立、不可见且未切换的桌面，不要求解锁，不发送输入；原版安装文件、存档和私有检查点只读。

## 原生截面

两轮、每轮四个独立的原版进程树，分别在5713C0（CRT入口）、57B9EA（HeapCreate实际返回后、写全局前）、576F60（原锁初始化入口）和49DD70（WinMain入口）的首指令前停止。各截面来自新的进程，不能拼成同一进程的逐指令轨迹。

每份均保留整个191000h字节原.text及20D000h字节.data、716字节WOW64上下文、256字节原栈窗口、完整调试分配链和真实导入入口。八份.text与固定原镜像逐字节一致；两份CRT入口.data逐字节相同。观察到 debug_flag=1、request=1、break_request=FFFFFFFF、hook=578120、四份静态锁表指针，以及全零的调试链、统计、堆token/mode和未初始化锁字节。由此补上此前独立夹具“空链输入”的原版来源；这是实际post-unpack状态，不能以保护层尚未展开时的零内存代替。

WinMain入口每份有142个存活的type2 CRT块，request为1–143（缺失已释放的3），next_request=144，累计32670、当前18376、高水位30494字节，heap_mode=1。独立解析全部原头部、文件/行号、双向链、完整用户区与FD保护字节，并核对原统计。此时尚未执行游戏主函数，原游戏对象/资源未构造。

## 为什么需要观察保护父进程

从创建时调试父进程或过早接入子进程，保护加载未展开游戏代码；较晚直接附加子进程则返回87。实际对照中，正常父进程创建子进程并通过NtDebugContinue管理其调试事件，保护过程会清除子进程调试寄存器。

正式采样先正常启动父进程，待自有子进程发布后仅附加父进程。用父进程硬件断点观察NtWaitForDebugEvent的自然返回与NtDebugContinue入口，在CRT原字节已出现、子进程硬件槽为空时设置一个目标执行断点。命中后在保护父进程处理该事件前读取原子进程完整状态，立即回收该探针。没有改写原代码、游戏派生状态、普通寄存器或保护父进程的调试回执。WOW64返回的EFLAGS保留位1有0/1归一差异，原始请求/前后上下文保留，其他所有普通/FPU/段寄存器及有效标志位逐字节不变。

探针用TerminateJobObject回收所有自有进程并关闭私有桌面，**明确不是原游戏正常清理**，不作为R3同寿命集成验收。失败采样与当时源码按版本原样保留，不计已验冷启动截面；早期失败报告中“WinMain未执行”字段未经证实，正式验收不采纳这些失败报告的状态声明。

## 证据与验证

- 正式来源：`analysis/school-crt-init-probe-v2-20261022.json.gz`；独立验证：`school-crt-init-probe-proof-v1-20261022.json`。v1成功试跑另存，v2补齐全部采样依赖来源摘要。
- 23项原生截面/来源破坏校验通过，覆盖父事件、完整代码/数据、所有节点/保护字节、普通寄存器写入、残留进程/桌面、伪造正常退出和保留恢复声明。
- 参考接口：[Microsoft DEBUG_EVENT](https://learn.microsoft.com/en-us/windows/win32/api/minwinbase/ns-minwinbase-debug_event)、[Microsoft WOW64 CONTEXT](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-context-r2)、[Microsoft CreateDesktopW](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createdesktopw)；原生调试状态结构参照[System Informer PHNT ntdbg.h](https://github.com/winsiderss/phnt/blob/master/ntdbg.h)，ABI与实际内存事件交叉核对。

下一步使用已验原.data作为新的独立函数夹具输入，执行原堆/锁初始化、分配/文件/释放和原CRT资源销毁。不会将新进程的142个CRT块冒充旧快照丢失的节点；旧快照的request=105与这些新进程不同，仍需保留执行本身的初始化/有效寿命连接。
