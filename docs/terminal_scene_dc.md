# 原 DeleteDC 的实际状态与清理判断修正

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
