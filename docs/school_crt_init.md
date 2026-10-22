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
- 26项原生截面/来源破坏校验通过，覆盖父事件、完整代码/数据、所有节点/保护字节、普通寄存器写入、残留进程/桌面、伪造正常退出和保留恢复声明。
- 参考接口：[Microsoft DEBUG_EVENT](https://learn.microsoft.com/en-us/windows/win32/api/minwinbase/ns-minwinbase-debug_event)、[Microsoft WOW64 CONTEXT](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-context-r2)、[Microsoft CreateDesktopW](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createdesktopw)；原生调试状态结构参照[System Informer PHNT ntdbg.h](https://github.com/winsiderss/phnt/blob/master/ntdbg.h)，ABI与实际内存事件交叉核对。

## 已验的原初始化与函数生命周期

两个新建的无窗口x86 API助手在hello时均没有堆或锁。客体以原镜像代码及上述实测CRT入口的整个.data开始，声明独立的平坦CPU/栈/FS/路径输入，不移植原生寄存器、不单独清零调试链、计数或锁字节。原57B9D0执行实际HeapCreate(0,4096,0)，再经原57B7A0实际GetVersionExA选择heap_mode=1；原576F60依次初始化四份静态锁。平台边界只翻译新建堆的逻辑token，不把旧进程token传入Windows。

随后七个已验原函数根完成262168/88字节的并存分配、原头部/FD/CD/DD和链摘除、SC004完整原ReadFile/CloseHandle及原释放。最后原576FA0删除四份锁，原57BA60实际HeapDestroy。助手要求原代码先释放全部对象才能正常关闭，driver不补做正式样本的CRT销毁。

每例11个独立原根、268259条原指令、263867次原写入和58次实际OS叶调用；两例全部机器码/写入摘要、每根后的完整客体镜像内存/CPU、真实接口全缓冲、所有权和正常助手退出独立重放一致。释放后的镜像块保留末次源程序字节供审计，不冒充已释放原生堆的物理空闲链；删除后的锁也不再作为有效对象访问。这是独立函数初始化验证，未逐指令执行整个143次原生CRT请求，也未重放所有C++初始化器。

正式夹具：`analysis/school-crt-init-fixture-v2-20261022.json.gz`；独立复核：`school-crt-init-fixture-proof-v1-20261022.json`。首版driver克隆通用函数时遗漏Python默认参数，原堆初始化后报TypeError；其日志/源码原样保留，该失败不计正式资源清理。修正后两套正式样本均由原代码创建与销毁全部CRT资源。

不会将新进程的142个CRT块冒充旧快照丢失的节点；旧快照的request=105与这些新进程不同。新增59项（26项原生来源、33项初始化/所有权）及历史348项回归全部通过，共407项；完整旧证据链、存档、私有检查点与资源保全通过。下一步仍需为保留任务建立有来源的有效CRT环境，并接回原肖像读取、构造/上传及handler。R3/R6和Godot完成状态不因本独立夹具成功而变更。
