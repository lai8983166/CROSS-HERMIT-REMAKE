# 真实创建消息与原版 WM_NCCREATE（2026-10-20）

原 `4504CF CreateWindowExA` 已携带此前准备的全部 12 个参数进入真实 Windows 接口。系统首条实际消息为 **`WM_NCCREATE=129`**，原 `424980` 回调、`424730` 对象绑定、主虚函数 `450D30`、输入分派 `4272E0` 和默认分派 `424A90` 均已执行，最终把真实 `DefWindowProcA` 的结果 **1** 返回 Windows。

下一条实际消息是 **`WM_NCCALCSIZE=131`**。实验停在它的原回调第一条 `424980` 指令前，没有回应这条消息。此时 `CreateWindowExA` 仍在等待回调，尚未返回或执行原 `4504DC` HWND 全局发布。取证后明确结束自有助手进程，记录待返回的接口和未回应消息；没有把该结束方式称作原版正常销毁或资源平衡清理。

见[完整原始轨迹](../analysis/school-window-callback-trajectory-v1-20261020.json)、[独立验证](../analysis/school-window-callback-verification-v1-20261020.log)、[原生阶段证据](../analysis/school-window-callback-native-v1-20261020.json)及[本批验收](../analysis/school-window-callback-acceptance-20261020.json)。409–412 四阶段分别本地提交，未 push。

## 原创建调用与嵌套回调

每例都从实际资源模块进入初始 WinMain 中段参数，完整重跑既有主对象构造、发布、任务槽、重复窗口检查、矩形、资源和类注册。原 `4504CF` 自己压入 `4504D5` 返回地址；模拟器在接口目标处停出 `emu_start` 后再等待真实 Windows，避免在同一个 Unicorn 实例中重入执行。

Windows 回调到自有 stdcall 传输地址时，助手发送实际 HWND、消息、WPARAM、LPARAM 和 CREATESTRUCT 字节，允许审计端在它等待期间请求真实系统接口。编号、请求、响应、原回调结果和未回应下一条消息全部保存在按发生顺序记录的通信证据中。系统接口没有被固定结果或 Python 游戏逻辑代替。

回调使用另一个带保护区的模拟栈及明确声明的 stdcall 寄存器初值。这是用于验证原回调 ABI 的模拟调用帧，不是宿主原生寄存器捕获。完成回调后，先验证原返回/保存寄存器，再恢复暂停的原创建调用者上下文；原创建栈和返回地址始终保持。

## 原回调实际做了什么

两组案例均执行下列真实接口序列：

| 原接口 | 实际结果及来源处理 |
| --- | --- |
| `GetPropA(hwnd,"CPP_CLASS")` | 新窗口尚无该属性，返回 0 |
| `GetWindowLongA(hwnd,4)` | 返回 0；实际 LastError=1413 保留，原代码按返回值选择分支 |
| `SetPropA(hwnd,"CPP_CLASS",20000000h)` | 返回 1；额外只读回查确认实际属性为原 owner 值 |
| `GetWindowLongA(hwnd,-4)` | 返回自有宿主回调地址，明确反向映射为原 `424980` 供原比较使用 |
| `DefWindowProcA(hwnd,129,0,真实LPARAM)` | 返回 1，由原函数逐层自然返回 |

原指令把实际 HWND 存到主对象 `+4`，对话框标志 `+0C` 保持 0。原 `424805` 比较自然匹配回调身份，未走替换窗口过程分支，`+8` 旧过程仍为 0。原虚表首项 `5986A0→450D30` 仍来自已执行的构造，没有替换虚函数或跳过游戏消息处理正文。

## CREATESTRUCT 与地址转换

助手保留 Windows 提供的完整 48 字节 CREATESTRUCTA。第一个 dword 是原 owner `20000000h`，后续模块、位置、尺寸、样式等字段与本组实际创建参数核对。原回调仅在其 stdcall 参数中把真实 LPARAM 对应到带保护区的 `25001000h` 影子，原指令随后读取影子的第一个字段取得 `this`。

默认系统处理时反向使用该消息的真实 LPARAM。真实调用前后 48 字节完整保留并核对，本次没有变化。属性中的 owner 只是实际存储的原模拟地址，助手不会把它作为宿主对象解引用。窗口过程查询也同时保留实际宿主返回值和明确的反向转换结果，原程序的比较指令保持原样。

微软文档说明创建接口会发送创建阶段消息，并通过 CREATESTRUCT 的 `lpCreateParams` 传递创建参数；参见 [CreateWindowExA](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createwindowexa)、[CREATESTRUCTA](https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-createstructa) 和 [GetWindowLongA](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowlonga)。

## 独立核对与保全

验证器使用独立 Unicorn 实例，不导入生成器的类或钩子方法。它从已验证的原启动状态构造映像、owner、原创建栈及声明的回调帧，重新执行原机器码；只有已核对 ABI/真实宿主身份/原属性数据的系统响应被重放。逐项比较全部指令、读取、写入、返回、寄存器、完整 owner/栈/影子/映像和保护区。

每例完成 **416 条原指令、110 次读取、208 次写入、5 次真实接口调用**。整段没有读取 `7A49FC` 所指旧游戏对象，捕获全局也未改写。9 项本批与 13 项直接类注册父链测试共 **22 项**通过，严格规格 **30 项**通过。16,541 个既有文件、10 项存档规则和 9 份私有 VM 检查点保持。

助手进程在下一条消息入口被明确终止并等待退出。报告保留当时仍注册的类、绑定属性及尚未正常清理的自有资源；没有伪造 `RemoveProp`、`UnregisterClass`、临界区删除或事件关闭记录。报告中的所有句柄随进程结束失效，也没有可恢复的真实待执行创建调用。

## 下一步

先继续真实消息 131 的原属性查找/虚函数/默认处理，并记录实际 RECT 或 NCCALCSIZE_PARAMS 的输入输出；随后处理真正到达的 WM_CREATE 和绘制消息。来源表已确认消息 1、5 的原分支返回 0，绘制消息 15 才调用 BeginPaint/GetClientRect/EndPaint。详见[下一步来源](../analysis/school-window-callback-next-source-v1-20261020.json)。

另已定位 `49DF73` 把 `&7A49FC` 作为窗口创建之后的工厂输出参数传入 `49DF85`。捕获映像中这个全局仍指向未捕获的旧堆；其新启动初值和完整初始化来源尚未解决。后续实际消息 28、512、1124 的原路径会检查它，需要先追清来源再执行相关对象读取。

原连续 VM 仍停 **`40E2D0 / PC224 / wait1 / manager owner0`**。本批接通的是独立启动实验中的真实早期回调，原连续 VM 衔接、完整窗口/工厂/音频/COM、输入与外层调度、实际游戏绘制和战斗完整流程仍待继续。Godot 和原存档保持；412 个已列任务完成不代表全游戏逆向完成率。
