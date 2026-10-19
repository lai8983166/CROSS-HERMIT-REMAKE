# 原任务槽初始化与重复窗口检查（2026-10-20）

主对象构造后的原调用链已完成 `421660` 的 32 个任务槽初始化、实例参数保存、`Cross Hermit` 类名复制、真实 `FindWindowA` 查询及原布尔转换/返回。本批两组案例均实际查询到无重复窗口，随后执行原命令行保存、配置常量写入和六项参数压栈，停在未执行的 `450350` 入口。

见[完整连续轨迹](../analysis/school-main-window-trajectory-v1-20261020.json)、[验收](../analysis/school-main-window-acceptance-20261020.json)与[上一批主对象记录](school_main_context.md)。每组都在新鲜辅助进程中重跑原分配、完整构造和全局发布，再沿同一 CPU 继续；没有恢复已经失效的事件、临界区或窗口句柄。

## 已执行的原始顺序

| 阶段 | 实际执行 | 停点 |
| --- | --- | --- |
| 旧前缀重跑 | 原 `49DDC9→4288E0→428A40→44FBB0→49DE01` | 原 `49DE15` |
| 任务槽 | `49DE1E→421660`；逐槽两次 dword 清零，共 64 次；原实例参数写 `7A2728` | `49DE2C` |
| 类名与查询 | 原 `lstrcpyA` 写 256 字节类名区域；`4293E0` 真正调用 `FindWindowA`，转换为 0/1 并自然返回 | `49DE53` |
| 原分支 | 两组观测结果均为 0；原 `450290` 保存命令行，写 `+5C=69h/+60=67h` 并准备窗口参数 | `450350` 第一条指令前 |

窗口入口的原 this 是本次实际构造的主对象，参数按原栈顺序为 `[0, 0, 1024, 768, 90000000h, 1]`，自然返回地址为 `49DECB`。这些参数只是原程序的启动准备；本批没有改变桌面或现有游戏的分辨率。

原任务区域是对象 `+64..+163`，相邻的第二临界区从 `+164` 开始。验证逐项检查全部 32 个槽、两类原 store 的顺序和完整主对象，确认临界区及其他字段保持。父栈、保存寄存器和原 SEH 也保持。

## 系统调用和导入边界

新助手保留上一版全部 13 项构造 API 的实际行为，另外严格接收一次类名复制与一次原参数窗口查询；源码、编译器、x86 二进制及 Kernel32/SHLWAPI/USER32 文件指纹均单独记录。旧助手和旧报告不变，新助手使用自己的真实构建身份。

查询严格使用类名 `Cross Hermit` 和空窗口标题。返回值是系统实际观察的借用 HWND，未关闭、激活或操作任何已有窗口。API 的含义见 [Microsoft FindWindowA 文档](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-findwindowa)。若以后实际发现重复窗口，工具会执行原跳转并停在未执行的 `49E092` 退出处理入口；本批只对这个备选路径做源码与投影检查，不冒称它已经在原 CPU 上执行。

新 USER32 模块引用由助手显式持有，关闭时释放；它不等于原 WinMain 的实例参数。原构造所需两把临界区和一个事件也在各自进程中完整释放，覆盖空运行、部分运行与完整运行的清理测试。启动时的辅助 SHLWAPI 探测与模块加载均单列为助手行为。

`FindWindowA` 导入的审计 trap 映射只在任务阶段之后加入。加入前后逐字节核对完整对象/保护区、父栈、源映像和空页，CPU 全寄存器不变；随后原 IAT 指向的地址由调用钩子转交实际系统 API。没有写 IAT、改查询结果、改 EIP 或跳过原函数。

## 验证与保留

本批 17 项新增测试，加 18 项主对象直接父链测试，共 35 项通过；其中包含新鲜两组连续执行。覆盖原任务清零次序、相邻内存、实例参数、完整前缀、CPU/返回栈、REP 次数、导入映射、类名尾部、查询参数/借用所有权、布尔返回、观察分支、窗口参数及资源清理等拒绝案例。严格规格检查 30 项通过。

所有新原指令轨迹与独立源码路径完全比较；原写入次数和完整写入/API 输出重放均与独立对象/映像投影一致。完整后备区和两侧保护区、静态类名、整个源映像、栈、空页与所有导入映射均校验。原父链验证器复用实际前缀，不伪装新助手为旧构建。

[保留记录](../analysis/school-main-window-preservation-20261020.json)核对 16,422 个既有文件、10 份存档规则指纹及 9 份私有 VM 检查点。原 EXE、Godot、存档、旧代码、旧助手和历史报告均保留。OpenSpec 386–391 分阶段本地提交，不 push；列举任务数不是全游戏逆向完成百分比。

```bash
PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_school_main_window tools.tests.test_school_main_window_platform tools.tests.test_school_main_window_emulation tools.tests.test_school_main_context tools.tests.test_school_main_context_platform tools.tests.test_school_main_context_emulation -v
PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_main_window_verification analysis/school-main-window-trajectory-v1-20261020.json
openspec validate --all --strict --no-interactive
```

## 尚未执行的依赖

[下一个原函数的源码记录](../analysis/school-main-window-next-source-v1-20261020.json)已核对：`450350` 先调用 `SetRect`、`AdjustWindowRect`，构建 48 字节 WNDCLASSEXA，然后调用图标/光标/画刷、类注册和窗口创建 API。它使用原回调 `424980` 与图标资源 157。

当前实例值 `12340000h` 是继承的明确实验输入，命令行也是未解引用的声明标量；它们不是实际模块和字符串。接下来可先验证矩形和类结构准备；在实际图标读取、注册和窗口创建前，还需落实真实模块/资源身份与原回调桥接。不能把这个标量直接当真实模块句柄传给系统。

窗口创建、消息回调、COM、游戏工厂/音频/设备准备、旧字体缓存堆与完整外层调度仍待推进。原连续 VM 仍保持 `40E2D0 / PC224 / wait1 / manager owner0`，本批独立启动实验没有把它修复或继续，也没有完成绘制、Present、剧情或战斗。
