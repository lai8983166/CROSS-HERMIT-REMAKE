# 原主对象分配、构造与全局发布（2026-10-19）

原 `49DDC9` 调用链已执行 `4288E0` 计数器重置、`428A40` 的 4368 字节申请、完整 `44FBB0` 构造及 `49DE01` 的全局指针发布，停在未执行的 `49DE15`。两组独立案例使用 A5/CC 保护字节，各自沿同一 CPU、同一辅助进程寿命连续运行。完整证据见[轨迹](../analysis/school-main-context-trajectory-v2-20261019.json)和[验收](../analysis/school-main-context-acceptance-20261019.json)。

这是明确声明的 WinMain 中段栈实验。早于 `49DDC9` 的 CRT、调试输出和 WinMain 入口没有执行；父帧、保存寄存器、局部变量、实例和命令行参数是实验输入。分配使用有界 debug CRT 适配器返回自有空间，原计数器更新及原构造函数均由原指令完成。尚未接回原连续 VM。

## 已执行并核对的内容

| 阶段 | 实际执行 | 停点 |
| --- | --- | --- |
| 分配 | 原计数重置，原分配封装及非空分支；CD 初始化 4368 字节，8192 字节后备区与两侧保护区 | `44FBB0` 第一条指令前 |
| 构造 | 26 次原函数调用，含 7 个直接子构造、完整输入重置、目录与路径函数 | 自然返回 `49DDEC`，调用者尚未执行 |
| 发布 | 原保存构造结果、`49DE01` 写 `7A4A00`、原非空判断 | `49DE15` 第一条指令前 |

每个构造过程实际调用两次 `InitializeCriticalSection`、一次 `CreateEventA`、一次 `GetCurrentDirectoryA`、一次 `PathAddBackslashA`、七次 `lstrcpyA` 和一次 `lstrcatA`，共 13 次。辅助进程使用原游戏目录作为明确声明的工作目录，创建匿名、自动重置、初始未触发的事件。只在内存中拼接 `SaveData\`，没有创建目录或写存档。

`InitializeCriticalSection` 的返回类型是 void，记录的 EAX 只是自有 19 字节转发器观察到的寄存器位值。两把临界区始终留在辅助进程原分配地址；VM 中的 24 字节副本仅作不透明取证快照，不作为可运行或可迁移的临界区。关闭时删除两把临界区并关闭事件句柄，部分运行也有清理测试。参见 [Microsoft 的 API 说明](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-initializecriticalsection)。

辅助进程启动时在独立空缓冲区调用一次路径 API，以加载并检查 SHLWAPI；此辅助探测与原游戏调用分开记录。取证显式处理 WOW64 文件重定向：记录系统报告的 System32 路径及审核器实际读取的 SysWOW64 文件路径，核对 x86 文件与 SHA，不拿 x64 同名文件冒充实际模块。

## 零长度目录 memset

原 `429744` 的参数实际是 `memset(7A2000, 20Dh, 0)`：写入长度为零。因此静态目录缓冲区尾部的旧字节保留；真实目录查询只覆盖当前路径和终止零，后续原路径 API 追加反斜杠。验证逐字节检查剩余尾部。七个主对象路径区中，`AF0` 与 `DFC` 原本没有整区清零，其路径末尾后的 CD 字节同样保持。

首次执行的有限函数范围漏掉了 `memset` 零长度分支最后的完整返回指令，运行在 `56CF13` 被拒绝；已保留 v1 源码证据及失败日志，v2 将范围补至 `56CF18`。首次验证器也曾把未执行的构造入口要求为已执行入口，验证失败日志保留；修正后自然调用边界、完整原始轨迹和新鲜运行均通过。旧报告和失败日志没有覆盖。

## 验证与保留

本批新增 18 项测试，加 4 项直接来源父链测试，共 22 项通过；包括新鲜两案例完整重跑，以及错误接收者、零长度改写、API 参数/尾部/返回指针、void 状态伪造、缺失写入/返回、REP 次数、寄存器、SEH、全局发布和资源清理的拒绝测试。严格规格检查 30 项通过。

完整后备区、保护字节、原映像、静态目录、导入映射、空页和父栈均核对；源控制流、调用参数、自然返回、原写入次数及完整写入/API 输出重放同时与独立对象投影比较。`80A398` 缓存头保持旧值。实验中的 `7A4A00` 由原指令写入新对象，不改写既有轨迹、原 EXE 或原连续 VM。报告含历史句柄和不透明系统字节，不能用于恢复已关闭的资源寿命。

[保留记录](../analysis/school-main-context-preservation-20261019.json)核对 16,390 个既有文件、10 份存档规则指纹和 9 份私有检查点；Godot、原存档、旧助手和旧证据保持原样。

```bash
PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_school_main_context tools.tests.test_school_main_context_platform tools.tests.test_school_main_context_emulation tools.tests.test_school_upstream_factory -v
PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_main_context_verification analysis/school-main-context-trajectory-v2-20261019.json
openspec validate --all --strict --no-interactive
```

## 接下来的实际依赖

[后继原指令证据](../analysis/school-main-context-next-source-v1-20261019.json)只做源码核对，尚未执行：`49DE1E→421660` 初始化 32 个任务槽；保存 HINSTANCE，复制 `Cross Hermit` 类名；`4293E0` 通过真正的 `FindWindowA` 查询重复窗口；随后 `450290` 保存命令行，进入窗口创建等后续步骤。需要在新鲜主对象和系统资源寿命内顺序继续，不能复用已关闭的事件或临界区。

之后仍需原窗口/COM/游戏工厂 `450570→4500B0`、音频及设备准备，核对游戏路径不同的启动模式，并处理捕获的旧字体缓存堆和完整工厂返回/外层调度。原连续 VM 仍停 `40E2D0 / PC224 / wait1 / manager owner0`。绘制、Present、VM/输入/世界循环和战斗后续工作没有因这次独立实验而完成。

OpenSpec 380–385 是本轮阶段任务；累计列举任务完成数不是全游戏逆向百分比。全部仅本地提交，不 push。
