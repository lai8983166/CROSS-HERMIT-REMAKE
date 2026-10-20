# 原版尺寸、位置、显示与 WINDOWPOS（2026-10-20）

同一原启动 CPU 已从此前真实 `[129,131,1]` 继续完成 **WM_SIZE=5、WM_MOVE=3、WM_SHOWWINDOW=24、WM_WINDOWPOSCHANGING=70**。系统随后再次发送70；首条 WINDOWPOS 标志为 `0x43`，第二条为 `0x03`，本批停在第二条回调入口，未执行第一条指令或提供返回值。

原 `CreateWindowExA` 尚未返回，`4504DC` 的 HWND 全局发布尚未执行。取证后已结束并等待自有助手进程退出，报告不能恢复这个已结束的原生调用。原连续 VM 仍停 **40E2D0 / PC224 / wait1 / manager owner0**；Godot 和原存档保持。

见[完整原始轨迹](../analysis/school-window-events-trajectory-v1-20261020.json)、[标量证据](../analysis/school-window-events-scalars-v1-20261020.json)、[位置结构证据](../analysis/school-window-events-position-v1-20261020.json)及[验收](../analysis/school-window-events-acceptance-20261020.json)。418–422 五阶段分别本地提交，未 push。

## 实际消息与原路径

| 实际消息 | 实际输入 | 原版结果与路径 | 指令 / 读取 / 写入 / 真实接口 |
| --- | --- | --- | --- |
| WM_SIZE 5 | wParam=0；打包尺寸1024×768 | 消息表到450EDD，再经451030自然返回0；仅GetPropA | 230 / 52 / 126 / 1 |
| WM_MOVE 3 | 打包坐标16,16 | 原虚函数及424A90转真实DefWindowProcA，返回0 | 299 / 74 / 161 / 2 |
| WM_SHOWWINDOW 24 | wParam=1；reason=0 | 原默认处理路径，原样传递wParam=1，返回0 | 295 / 71 / 161 / 2 |
| 首条WM_WINDOWPOSCHANGING 70 | 真实指针及WINDOWPOS28，flags=43h | 原默认处理路径，真实输入/输出结构字节一致，返回0 | 299 / 73 / 160 / 2 |

每条消息的真实 GetPropA 均返回已经绑定的主对象 `20000000h`；原代码跳过重复绑定。尺寸的宽高为无符号16位，位置坐标为有符号16位，显示消息使用布尔WPARAM和标量reason。标量LPARAM没有被当成指针；十进制24是显示消息，十进制18是退出消息，不能混用。

首条位置结构是32位布局 `<II4iI>`，完整28字节，包含实际 HWND、实际插入位置 HWND、x/y/cx/cy及flags。当前坐标和尺寸字段均为0，但flags包含NOMOVE/NOSIZE，不能据此宣称窗口被移动到0或缩成0。`hwndInsertAfter` 是Windows提供的借用句柄，只作为实测数据记录，本批不拥有、修改或销毁它。

`0x43 = SHOWWINDOW | NOMOVE | NOSIZE`；下一条的 `0x03` 少了SHOWWINDOW位。本批保留两条的全部实际字节及真实指针，没有把它们合并成同一条消息。接口定义见微软的 [WINDOWPOS](https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-windowpos) 和 [WM_WINDOWPOSCHANGING](https://learn.microsoft.com/en-us/windows/win32/winmsg/wm-windowposchanging)。

原回调对这些消息只转交LPARAM，不解引用 WINDOWPOS，故原真实地址作为不透明数值进入声明的stdcall帧；真实默认函数仍使用Windows的原地址。新助手仅增加70/71结构的原始字节采集，原指令执行器、游戏消息函数、虚函数和IAT保持。

## 独立验证及保全

两组填充A5/CC的完整轨迹均完成 `[129,131,1,5,3,24,70]`，每组累计 **2068条原指令、505次读取、1102次写入、15次真实接口**。独立验证器不复用生成器类或执行钩子，在新的Unicorn实例内重放完整原回调，检查完整指令/读写/返回/寄存器、真实参数/默认前后字节、owner保护区、回调栈、影子保护区、源映像及恢复后的原调用者CPU与完整栈。

验证直接检查原始完整七消息证据，不把新记录伪装成旧格式。启动前缀沿用已公开的31处实例派生值校验副本，原始动态值与执行CPU未改。WM_SHOWWINDOW的wParam=1和零LPARAM单独验证，没有沿用旧回调一律wParam=0或LPARAM必须是指针的假设。

12项本批及11项直接创建父链共 **23项测试**，严格规格 **30项**通过。负例覆盖错误标量/转交值、缺失读取、错误写入、调用者恢复、重复绑定、结构长度/所属HWND/flags/输出、后续消息被错误回应、旧全局或清理声明被篡改。16,592个既有文件、10项存档规则和9份私有VM检查点保持。

声明的回调寄存器是客体ABI输入，不是宿主CPU抓取。实验从声明的49DDC9启动帧执行，尚未覆盖完整WinMain入口。原资源DLL及系统接口确实由Windows加载/调用；原主对象确实构造和绑定，但尚未接入旧连续VM。

最终消息没有回应，助手退出不等同原程序正常清理。尚未执行原属性移除、窗口销毁、类注销、事件关闭或临界区删除；所有仍存活的自有资源随该进程寿命结束。报告明确不声称正常清理或可恢复的原生创建调用。

## 接续边界

下一步在新助手寿命内重跑已验证前缀，接第二条70/flags03的真实输入/输出，然后依实际消息继续。见[下一步来源](../analysis/school-window-events-next-source-v1-20261020.json)。后续顺序不能从消息名称推定，创建返回及HWND发布必须等待原调用自然返回。

激活28等原路径仍会检查捕获的 `7A49FC→04D70068`；该旧堆对象缺失，不能将全局清零绕过。应追清真实新启动初值/初始化来源，再接相关对象读取。完整绘制、正常销毁/属性与类清理、主工厂/音频/COM、渲染初始化和连续VM接入，以及外层调度、AI/事件/通关奖励仍待完成。422个已列任务完成不代表全游戏逆向完成率。
