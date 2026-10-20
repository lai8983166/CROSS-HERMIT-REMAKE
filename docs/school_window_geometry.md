# 原窗口几何与窗口类前半段（2026-10-20）

独立启动链已经从原 `450350` 入口继续，执行原函数序言、真实 x86 `SetRect`、原客户端矩形复制、真实 `AdjustWindowRect`，再执行窗口类前半段的七项原字段写入和图标参数压栈。两组新鲜案例都停在 `450416` 的 `LoadIconA` 调用指令前。

见[完整连续轨迹](../analysis/school-window-geometry-trajectory-v1-20261020.json)、[验收](../analysis/school-window-geometry-acceptance-20261020.json)和[前一批任务/窗口检查](school_main_window.md)。每组均从原主对象分配、构造和全局发布开始，重跑真实无重复窗口检查，随后在同一 CPU、同一助手寿命内继续。没有移植旧句柄、修改旧检查点或伪造窗口不存在。

## 三个原边界

| 阶段 | 原执行内容 | 未执行的下一条指令 |
| --- | --- | --- |
| 客户矩形 | 原 `450350` 序言、`SetRect(owner+8BC,0,0,1024,768)` 及原栈检查 | `45039C` |
| 窗口矩形 | 四个原 dword 把客户端矩形复制到 `EBP-14`；实际 `AdjustWindowRect(local,90000000h,0)` 及原栈检查 | `4503D5` |
| 窗口类准备 | 原七项类字段写入，压入实例标量与图标号 157 | `450416` 的导入调用指令 |

系统实际返回的客户端和窗口矩形均为 `[0,0,1024,768]`；这个样式没有产生额外边框尺寸。对象中的客户端矩形与栈中的局部窗口矩形分别验证，不能因结果相同而省略原复制或实际 API 调用。`SetRect` 是矩形赋值，`AdjustWindowRect` 是窗口尺寸计算；参见 [SetRect](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setrect) 和 [AdjustWindowRect](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-adjustwindowrect)。本批没有创建窗口、改变桌面分辨率或操作现有窗口。

原窗口函数的自然父返回地址仍是 `49DECB`，六个参数仍是 `[0,0,1024,768,90000000h,1]`。原 prologue、全部 REP 填充、API 压栈、stdcall 清栈、原 `56CE80` 检查与完整寄存器均核对。

## 保留原部分初始化结构

48 字节 WNDCLASSEXA 位于原 `EBP-44`。到 `450416` 为止，原指令只设置：

| 字段 | 原值 |
| --- | --- |
| cbSize | 48 |
| style | 0 |
| lpfnWndProc | `424980` |
| cbClsExtra / cbWndExtra | 0 / 0 |
| hInstance | 继承的声明标量 `12340000h` |
| lpszClassName | 原静态类名地址 `7A2628` |

其余 hIcon、hCursor、hbrBackground、lpszMenuName、hIconSm 五项仍为 `CCCCCCCCh`。验证保留这些原字节，没有提前清零或补造有效句柄。这是窗口类的部分准备，尚未到注册条件。

最后停点是导入**调用指令**，不是 API 已进入的栈：当前栈只有 `[12340000h,157]` 两个已压入参数，尚无这次调用的返回地址。取证使用 `stack_args` 和 `call_instruction_executed:false`，不把实例参数误标为返回地址。

## 图标与回调来源

只读资源核对表明，当前反汇编映像和原 `CROSS HERMIT.EXE` 中的图标资源逐字节一致：组号 157、语言 1041，指向图像 5，大小 2216 字节，32×32、8 位。模块完整 SHA、资源 RVA/大小/SHA 及组目录字节都纳入源码契约；本批没有加载模块或读取图标为系统句柄。

[后继源码记录](../analysis/school-window-geometry-next-source-v1-20261020.json)还核对了原 `424980` 回调：先调用 `GetPropA`；创建消息 1/129 可从创建结构首字段取得 this，经 `424730` 绑定，再进入对象虚函数。这里只做反汇编来源检查，没有执行回调，也没有用替代回调假装原逻辑已运行。

## 验证、资源寿命和保留

新不可覆盖助手增加两项有界系统调用，只在真实窗口查询为不存在后接收原参数。两块 RECT 使用完整 16 字节输入/输出和两侧保护字节；请求拒绝测试覆盖提前调用、错误尺寸、错误样式、错误菜单、错误副本及重复调用。部分/完整寿命都核对两把临界区、事件与自有 USER32 引用的释放，另外分别记录两项真实几何调用次数。

新导入映射只添加原 SetRect/AdjustWindowRect 目标的审计 trap；加入前后完整 CPU、对象/保护区、源映像、父栈和空页不变。原 IAT 不改。完整原轨迹、所有原写入次数、写入/API 输出重放与独立结构投影一致；整个对象后备区、所有栈字节、空页和导入映射都验证。

本批 17 项新增测试，加直接父链 17 项，共 34 项通过，包括新鲜两组完整重跑；严格规格检查 30 项通过。[保留记录](../analysis/school-window-geometry-preservation-20261020.json)核对 16,450 个既有文件、10 份存档规则及 9 份私有 VM。原 EXE、旧助手、旧代码、旧报告、Godot 和原存档不变。OpenSpec 392–397 分六阶段本地提交，未 push；累计列举任务数不是全游戏逆向百分比。

```bash
PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_school_window_geometry tools.tests.test_school_window_geometry_platform tools.tests.test_school_window_geometry_emulation tools.tests.test_school_main_window tools.tests.test_school_main_window_platform tools.tests.test_school_main_window_emulation -v
PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_window_geometry_verification analysis/school-window-geometry-trajectory-v1-20261020.json
openspec validate --all --strict --no-interactive
```

## 接下来

先建立包含这些相同资源字节的真实自有模块身份，再以真实模块句柄作为明确的新实验输入从头重跑原链。当前 `12340000h` 只是既有声明标量，不能传给实际模块 API，也不能在停点手工修补成新句柄。随后才可继续两次原图标读取、光标/画刷和完整类结构。

类注册和窗口创建还需要承接真正的原消息回调/创建结构/窗口属性/虚调用，之后是消息循环、COM、游戏工厂/音频/设备及旧缓存与调度器衔接。原连续 VM 仍保持 `40E2D0 / PC224 / wait1 / manager owner0`；本批并未推进它，也未完成 GPU 绘制、Present、剧情或战斗。
