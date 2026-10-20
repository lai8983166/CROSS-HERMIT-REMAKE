# 真实资源模块、原图标调用与完整窗口类（2026-10-20）

本批建立了真实自有资源模块，并把 Windows 返回的 HMODULE 作为原启动链的新声明输入，从第一条 `49DDC9` 指令之前开始重跑。原 `49DE26` 自然发布该句柄，随后原两次 `LoadIconA(module,157)`、系统光标和库存画刷调用全部执行，原指令将实际返回值写入完整 48 字节 WNDCLASSEXA，停在未执行的 `45047D RegisterClassExA` 调用指令前。

见[完整原始轨迹](../analysis/school-window-module-trajectory-v3-20261020.json)、[真实实例输入证据](../analysis/school-window-module-instance-v1-20261020.json)和[本批验收](../analysis/school-window-module-acceptance-20261020.json)。两组案例中的真实模块地址不同；每组都在同一 CPU 和同一助手寿命内，完整重跑主对象分配/构造/发布、任务槽、实际重复窗口查询、矩形与部分窗口类，再继续本批资源调用。

## 资源模块实际建立了什么

新 DLL 为确定性构造的 3072 字节 x86 PE，仅有一个只读资源节：

- 入口地址为 0，无可执行节、导入、导出、TLS 或原游戏代码。
- 保留原 RT_ICON 5 与 RT_GROUP_ICON 157，语言 1041，所有资源字节与原 EXE/当前反汇编映像一致。
- Windows 通过真正的 LoadLibrary 加载它；助手在返回 hello 前通过实际 FindResourceEx/LoadResource/LockResource 读取并核对完整资源字节。
- 真实句柄在声明初始 WinMain 栈帧时写入 `TOP+4`，发生在任何原指令执行之前。没有在 `450416` 停点修补 CPU、实例全局或参数。

这是自有的资源承载模块，不是原游戏代码模块或完整原 WinMain 入口。资源 DLL 的构造源、完整 PE SHA、加载后资源字节和原始来源均有证据。该工作方式参见 [Microsoft 资源 DLL 说明](https://learn.microsoft.com/en-us/cpp/build/creating-a-resource-only-dll?view=msvc-170)。

## 原调用与实际字段

| 原调用 | 原参数 | 写入字段 |
| --- | --- | --- |
| `450416→LoadIconA` | 真实模块，157 | hIcon |
| `450433→LoadIconA` | 同一真实模块，157 | hIconSm |
| `45044C→LoadCursorA` | 0，32512 | hCursor |
| `450460→GetStockObject` | 4 | hbrBackground |
| 原 `450470` store | 0 | lpszMenuName |

两组记录中的两次图标加载各自返回相同的共享图标句柄，没有把它们冒称为两个独立图标。实际系统光标和库存画刷也按借用资源处理，不调用 DestroyIcon、DestroyCursor 或 DeleteObject。关闭时只释放自有资源模块/GDI32/USER32 引用、两把临界区及事件。空运行、部分图标加载和完整流程均有清理测试。参见 [LoadIconA](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-loadicona)、[LoadCursorA](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-loadcursora) 和 [GetStockObject](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getstockobject)。

完整类结构包含原 cbSize=48、style=0、原回调 `424980`、两项 extra=0、真实 HINSTANCE、实际图标/光标/画刷、menu=0、原类名地址和实际小图标。前一批保留的五项 CC 字段已由对应原指令逐项填充。最终栈上只有原类结构指针，注册调用还没执行，也没有这次调用的返回地址。

## 旧验证器的复用边界

旧轨迹和旧验证器使用声明标量 `12340000h`，本批原始证据使用真正的动态 HMODULE。为保持旧文件不变，新验证器构造一个**只供校验的深拷贝**，在 31 个明确列出的位置归一化这个输入及其原指令派生值：调用者参数位、原实例发布、对应寄存器/全局、类 hInstance、图标压栈，以及这些字段派生的导入接入哈希。

创建这个副本之前，逐项要求原始值等于实际模块句柄，独立检查完整真实映像、初始栈、原发布 store、字段位置和接入前后状态。其他字节或字段一律不转换。然后由原完整前缀验证器检验副本，接着新验证器继续校验原始资源调用、写入重放和完整类结构。

每项转换都有位置、原值/哈希、校验值/哈希和用途记录。副本的 SHA 与完整原始前缀 SHA 分开保存。负例测试确认这套转换不能隐藏错误的原回调、CPU、资源、映像或晚于启动的参数修补；验证前后的原始报告 SHA 也相同。工具没有修改运行中的模拟器、原始快照或旧验收报告。

## 验证与保留

17 项新增测试加 17 项几何直接父链测试，共 34 项通过，包含新鲜真实模块实例的两组重跑。30 项严格规格通过。完整对象及保护区、所有栈字节、源映像、空页和导入映射核对；原四项资源 ABI、返回值、栈检查、所有原写入次数及完整窗口类重放均与原源码一致。

首次两次证据采集因新包装器缺少原快照字段的符号而拒绝，v1/v2 失败日志保留；补齐后新建 v3 完整轨迹并通过独立验证，没有覆盖历史日志。[保留记录](../analysis/school-window-module-preservation-20261020.json)核对 16,478 个既有文件、10 份存档规则和 9 份私有 VM。旧源码、旧助手、原 EXE、历史报告、Godot 与原存档均保持。所有阶段仅本地提交，未 push。

```bash
PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_school_window_module tools.tests.test_school_window_module_platform tools.tests.test_school_window_module_emulation tools.tests.test_school_window_geometry tools.tests.test_school_window_geometry_platform tools.tests.test_school_window_geometry_emulation -v
PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_window_module_verification analysis/school-window-module-trajectory-v3-20261020.json
openspec validate --all --strict --no-interactive
```

## 下一段

[后继来源记录](../analysis/school-window-module-next-source-v1-20261020.json)已核对原类注册调用、CreateWindowEx 的 this 参数，以及 `424980→GetPropA→424730→450D30` 的创建消息/对象虚调用链。下一步落实自有原回调桥，验证真实类注册、查询和注销，再承接真实创建消息与原回调栈。当前原 `424980` 是客体代码地址，不能直接当辅助进程的可执行回调使用。

原窗口类注册、窗口创建、回调、消息循环、COM、游戏工厂/音频/设备和旧缓存/调度器整合仍未完成。原连续 VM 仍保持 `40E2D0 / PC224 / wait1 / manager owner0`；本批没有推进它，没有创建窗口或改变桌面，也没有完成 GPU 绘制、剧情或战斗。OpenSpec 398–403 的阶段完成数不代表全游戏逆向百分比。
