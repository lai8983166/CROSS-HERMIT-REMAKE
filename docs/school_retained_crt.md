# 原 CRT 分配、肖像文件读取与保留状态缺口

当前有限 change：`verify-crt-allocation-file-lifecycle`。本轮不需要解锁桌面，不启动游戏窗口，不发送输入，也不创建 GPU 对象。

## 保留分支：已定位，尚未接通

以 `school-retained-portrait-file-acceptance-v1-20261022.json` 为前序证据，重放 initial、student9_waiting、fifth_class × capture76/77 的完整原内存/CPU。连续执行原 428A40 → 56E810 → 56E860 → 577040 共73条指令、49次写，停在 EnterCriticalSection 的第一条指令之前；未替换原函数、未响应原生 API、未重写 IAT 或调试堆状态。

旧快照中 lock9 指向80A4B0，原 OS 堆 token 为04D60000，调试链首/尾为04D605B8/04D68FA0，两个32字节节点均不在已保存映射中。debug_flag=1、heap_mode=1，仍启用调试链。只提供新堆/锁无法恢复这些历史节点及其所有权，因此这六个保留分支仍不能宣称完成分配或图片载入。

原分配函数 `_malloc_dbg` 56E920 调用原 hook578120、raw allocator577FD0。32字节头依次保存 prev、next、源文件、行号、请求长度、类型、序号和4字节 FD guard；用户区初填 CD，尾 guard 为 FD。正常 Windows 堆路径的底层请求向16字节对齐。释放经428AD0 → 56F830/56F3B0/56F420 → 5787E0，执行指针检查、HeapValidate、保护区检查、链表摘除、DD填充和 HeapFree；游戏计数器79FC74同步加减。

## 独立函数夹具的边界

独立测试以原代码/数据为基础，**明确声明空调试链、清零统计、request=1 是测试输入**，另绑定自有 Win32 堆和临界区。这些输入不写入保留快照，不作为启动初始化来源，也不证明原进程链路已经恢复。debug_flag及heap_mode保持1；旧 CRT 小块堆模式2/3尚未测试。

独立夹具使用无窗口 x86 helper，仅封送实际 Win32 堆、锁、只读文件 API。所有 CRT、原 hook、memset、原文件包装器和释放函数执行原机器码。旧 token 仅作为 guest 逻辑标识，不传给 Windows；每次原生指针消费者前同步完整源程序缓冲区，并检查自有对象、边界和调用顺序。锁 API 的 void 返回在 guest 中归一为0，不作为功能结果。

证据、独立重放、回归与最终验收结果在本 change 完成时补齐。研究 R3/R6 与 Godot 完成状态不因独立夹具成功而变更。
