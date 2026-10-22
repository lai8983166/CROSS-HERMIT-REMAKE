# 原 CRT 分配、肖像文件读取与保留状态缺口

有限 change：`verify-crt-allocation-file-lifecycle`。本轮不需要解锁桌面，不启动游戏窗口，不发送输入，也不创建 GPU 对象。

## 保留分支：已定位，尚未接通

以 `school-retained-portrait-file-acceptance-v1-20261022.json` 为前序证据，重放 initial、student9_waiting、fifth_class × capture76/77 的完整原内存/CPU。连续执行原 428A40 → 56E810 → 56E860 → 577040 共73条指令、49次写，停在 EnterCriticalSection 的第一条指令之前；未替换原函数、未响应原生 API、未重写 IAT 或调试堆状态。

旧快照中 lock9 指向80A4B0，原 OS 堆 token 为04D60000，调试链首/尾为04D605B8/04D68FA0，两个32字节节点均不在已保存映射中。debug_flag=1、heap_mode=1，仍启用调试链。只提供新堆/锁无法恢复这些历史节点及其所有权，因此这六个保留分支仍不能宣称完成分配或图片载入。

原分配函数 `_malloc_dbg` 56E920 调用原 hook578120、raw allocator577FD0。32字节头依次保存 prev、next、源文件、行号、请求长度、类型、序号和4字节 FD guard；用户区初填 CD，尾 guard 为 FD。正常 Windows 堆路径的底层请求向16字节对齐。释放经428AD0 → 56F830/56F3B0/56F420 → 5787E0，执行指针检查、HeapValidate、保护区检查、链表摘除、DD填充和 HeapFree；游戏计数器79FC74同步加减。

## 独立函数夹具的边界

独立测试以原代码/数据为基础，**明确声明空调试链、清零统计、request=1 是测试输入**，另绑定自有 Win32 堆和临界区。这些输入不写入保留快照，不作为启动初始化来源，也不证明原进程链路已经恢复。debug_flag及heap_mode保持1；旧 CRT 小块堆模式2/3尚未测试。

独立夹具使用无窗口 x86 helper，仅封送实际 Win32 堆、锁、只读文件 API。所有 CRT、原 hook、memset、原文件包装器和释放函数执行原机器码。旧 token 仅作为 guest 逻辑标识，不传给 Windows；每次原生指针消费者前同步完整源程序缓冲区，并检查自有对象、边界和调用顺序。锁 API 的 void 返回在 guest 中归一为0，不作为功能结果。

## 已验函数生命周期

七次明确的独立原根依次为4288E0重置游戏分配计数、428A40(262168)、428A40(88)、428AD0(首块)、428AD0(次块)、42AE20(SC004路径)、428AD0(文件缓冲区)。这不是保留任务的连续调用栈。

每步原指令数分别为33、65954、436、66251、734、68036、66254，总计267698；原写入263780次。47次原调用的实际 OS 叶接口全部核对，另有明确标记的完整缓冲同步/读回与实验资源建立/销毁。两个块同时存活时验证双向链，先释放首块再验证剩余块 prev=0。完整262168字节 SC004 文件由原 ReadFile 调用读入，原 CloseHandle 关闭，不再依赖探针代关；所有用户字节与安装文件逐字节相同，SHA256 为 `a4443ca63b9889503e35170da0c8b976a799c25ec3f0bd1b0f80dc97c38a6164`。

原头部保存源文件594E28、行号141、类型1、请求序号1/2/3。三个底层对齐分配分别为262208、128、262208字节；每次用户区CD、前后FD和释放前整个请求块DD均检查。最终 first/last/current/game_bytes 均为0，累计 total=524424、high=262256、next_request=4，由原代码自然得到。原生堆3次分配/3次释放、文件1次读/关闭，源锁均衡，助手正常退出并销毁自有堆/临界区，无强制清理。

独立验证器重新执行原机器码，逐项检查自然返回栈、IAT/原指令字节、完整指令与写入摘要、全部 native 请求/回执、原生所有权及七个返回点的全内存/CPU。模型另核对全部debug header、链变更、统计与文件字节。初始化声明与保留基线严格分开；验收中 `retained_heap_restored=false`、`retained_integration=false`、`R3_complete=false`。

## 可复核证据与检查

- 六分支原前缀：`analysis/school-retained-crt-boundary-v1-20261022.json.gz`；独立复核：`school-retained-crt-boundary-proof-v1-20261022.json`。
- 完整独立函数夹具：`analysis/school-retained-crt-fixture-v1-20261022.json.gz`；独立复核：`school-retained-crt-fixture-proof-v2-20261022.json`。首版验证器的通用重放适配缺少key字段，失败日志原样保留为 `school-retained-crt-fixture-verify-v1-20261022.log`，修正适配后通过；未改原实验报告或原机器码。
- 新增13项保留来源/状态拒绝检查与40项夹具/原生所有权检查通过；完整历史回归结果见本单元最终验收。
- 运行环境：项目 `.venv-audit/Scripts/python.exe`，`PYTHONPATH=.`、`PYTHONUTF8=1`。先运行 `python -m tools.school_retained_crt --verify <boundary-report> --out <fresh-proof>`，再运行 `python -m tools.school_retained_crt_fixture_verification <fixture-report> --out <fresh-proof>`。输出路径必须不存在，保留原始失败证据。

研究 R3/R6 与 Godot 完成状态不因独立夹具成功而变更。下一步仍需从可证明的原初始化/有效寿命恢复CRT依赖，再接回原肖像加载/构造/上传及handler；不得将本夹具的清零输入移植到保留分支。六条短编码、ACP936/Big5乱码和原外层世界的同寿命连接仍是其他已知缺口。
