# 原 DeleteDC 的实际状态与清理判断修正

## 最新：正常清理组件已通过

2026-11-13后续单元只执行一次新鲜原生寿命，使用已核验旧二进制的NTFS硬链接及新的
运行目录/次数标记；没有重编译，没有复制父内存或重用旧句柄。修正版实际运行4.656秒，
175031条原指令、114次原API、457条native请求，组件及独立复核通过。

本次原DeleteDC之后，GAME内存由原HeapFree释放；后续DC_INFO再次确认type0/font0、
GDI数回到基线0。然后原MAIN析构/free、原575450释放PTD并TlsSetValue(0)、实际TLS读回0、
静态锁销毁、TlsFree及HeapDestroy全部完成。独立重建的heap/内存/事件/锁/TLS/DC账本为0，
实际helper自然exit0、Job为空、无超时/强制终止；7个父侧CloseHandle真实BOOL全部1。
原CRT debug-free对本PTD的116B DD填充按原调用现场识别，未把它误判成TLS失效或跳过检查。

独立审阅核对302项文件身份、5315个原指令站点、250份CPU57及81次完整PTD读回，并拒绝
7项指令/DC/TLS/free/退出篡改。它是独立记录及资源审阅，不是重新执行完整指令序列；
完整独立重放标准仍保留。这里的清理来自明确声明的补充原函数根，WinMain与GAME工厂
栈仍处于各自停点，不声称WinMain自然返回、GAME已发布或战斗退出。

**当前构造与正常清理组件通过；正式仍2/8。** GAME合法发布、场景worker、等待返回、
结果消费和两例完整验收未通过。本轮没有游戏窗口、截图、输入、显示模式或gamma修改。

来源：`analysis/terminal-scene-dc-preflight-v2-20261113.json.gz`；独立审阅：
`analysis/terminal-scene-dc-independent-review-v2-20261113.json`；收尾：
`analysis/terminal-scene-dc-closeout-v2-20261113.json`。

GAME后续准备已固定可复用实现和真实缺口，见
`analysis/terminal-game-owner-readiness-v1-20261113.json`。旧原窗口同步回调和gamma恢复
实现可以复用合同，但属于不同原生助手，必须合入当前同一MAIN线程/所有者。
当前dispatch持有stateMutex，普通drive只等待API返回：直接接CreateWindow会有嵌套
回调阻塞风险，须先完成同线程回调递送、CPU57及父栈恢复，再接COM/图形/输入生命周期。
现有桌面核对没有统一gamma/光标/输入设备恢复，所以尚不准入桌面测试，不提前占用用户桌面。

## 前次预检与修正记录（保留）

2026-11-13，本轮只执行一次有界无窗口原生预检，实际3.625秒；原MAIN发布、原GAME
完整构造、原GAME析构与HeapFree完成。没有游戏窗口、屏幕像素读取、输入或显示模式操作。
**已取得本次 DeleteDC 后的真实对象状态；组件验收仍拒绝，正式仍2/8。**

## 本次实际证据

同一原生MAIN线程、同一DC、原413417调用DeleteDC，新增观察保留其返回值和LastError：

| 时点 | GetObjectType | GetCurrentObject(OBJ_FONT) | 当前进程GDI对象数 |
| --- | --- | --- | --- |
| GetDC之前 | 未查询 | 未查询 | 0 |
| GetDC之后、原DeleteDC之前 | 3（OBJ_DC） | 非零实际字体句柄 | 1 |
| 原DeleteDC返回1之后 | 0 | 0 | 0 |

GdiFlush返回1，GDI计数查询无错误，原DeleteDC的LastError仍0。原调用成功、对象查询
由有效变为无效、当前进程GDI数回到原基线，三者共同支持**这个当前实例已销毁DC**。
本轮没有重复ReleaseDC，不把旧来源的ReleaseDC=0补写成成功，也不修改原游戏的DeleteDC。
该结论限定于本次实际执行；不是建议把所有GetDC改为DeleteDC，跨平台仍以实际状态验证。

观察含义见微软[GetObjectType](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getobjecttype)、
[GetCurrentObject](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getcurrentobject)、
[GetGuiResources](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getguiresources)。
元数据查询不读取像素；GDI计数只查询当前helper进程，不查询用户其它程序。

## 本轮错误、修复与未通过的范围

C++使用SDK的OBJ_DC，数值为3；Python采集器及离线模拟却误用1，启动前复核也漏掉了
这个ABI常量。真实回执已经满足C++退休条件，Python仍拒绝，随后按一次30秒止损合同
结束测试。这是采集器错误，不能归因于原游戏资源失效。

旧采集器、原生可执行文件、失败报告全部保持原字节。新
`devtools/terminal_scene_dc_probe_v2.py` 固定旧实现SHA，从本次Windows SDK的wingdi.h
核对OBJ_DC=3，仅修正两处比较；不改返回值、结果字段、执行路径或一次性标记。
已用冻结真实回执重验，9项伪成功/活对象/错误计数变体全部拒绝；独立AST复核确认只有
两处常量变化。修正后的符号模型完整走通175028条原指令、114次API及原MAIN/PTD清理，
但模拟平台返回不是新增Windows执行证据。

失败发生于计划的第二次DC_INFO之前，MAIN析构、PTD/TLS/heap正常清理与Shutdown均
未执行。实际helper经Job终止exit94，Job为空，未超时；8个父侧CloseHandle的真实BOOL
均为1，其中包含强制分支保留的Job成员句柄。正常退出路径预期7个，不能把失败分支
8个改成7个；也不能将强制退出当作原资源寿命完成。

独立审阅核对原字节、57项执行器状态形状、ABI、61次PTD真实读回、343条同线程回执，
并拒绝3项证据篡改。它不是重新计算累计摘要的完整独立重放。原指令仍由Unicorn执行，
真实Windows叶在同一x86 helper线程执行；没有声称物理CPU直接执行整个游戏。

## GAME合法发布的准入

复用既有启动/工厂证据，重新核对33条决定性原指令，确认：

1. WinMain49DF85调用450570，45067A前硬编码全屏mode0，不能用隐藏HWND将原链变成窗口化。
2. 原413560输入初始化会移动系统光标，并用前台DirectInput协作级别；原450350本身也会显示窗口。
3. 413450还必经设备gamma调用。即使独立412C70窗口化工厂成功，也不能声称对桌面无影响。
4. 412C70没有原450570的音频、DirectShow、输入初始化，不得把它的独立输出当作完整合法GAME发布。

当前继续沿用户选择的宿主路线；没有新增虚拟机要求。下一关口顺序是：

- 在新的明确有界单元，用修正采集器完成第二次DC_INFO及MAIN/PTD/TLS/heap正常清理；
  本轮once标记保持，禁止删除或换输出名重复运行。新构建目录须生成与v2身份匹配的离线门。
- 复用旧已核构造合同，准备同一真实所有者中的窗口、COM/音频、D3D8及DirectInput接口，
  保留原全屏参数及消息/事件父调用链，不修改原GAME发布条件。
- 在分辨率、gamma、任务栏、工作区、前台/光标及输入设备恢复准备可审查后，提前告知并
  取得有界宿主桌面时段，再运行原450570发布。当前尚未达到这个准入条件，没有启动它。
- GAME合法发布后继续原49E2B0事件16→451080→49E540→4217C0/worker；不得从453CB5新起根。
  首次等待返回、结果消费、三次握手及两例新鲜原生完整重放仍按原标准验收。

## 来源与存储

- 实际来源：`analysis/terminal-scene-dc-preflight-v1-20261113.json.gz`。
- 独立复核：`analysis/terminal-scene-dc-independent-review-v1-20261113.json`。
- 修正判断：`analysis/terminal-scene-dc-correction-v1-20261113.json`。
- GAME决定点：`analysis/terminal-game-publication-route-v1-20261113.json`。
- 构建/体积/退役清单：`analysis/terminal-scene-dc-closeout-v1-20261113.json`。

所有新增构建、临时文件、日志及证据均在F盘，仅保留一份本次实际来源，没有备份副本。
旧失败和其它历史资产不清理；本轮可再生编译对象按独立退役清单删除。
