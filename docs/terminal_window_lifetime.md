# 原窗口关闭与桌面恢复的有界准入

2026-11-14，已执行一次获授权的宿主窗口测试，原生寿命2.625秒，整个调用约9.25秒。
原窗口实际创建并经原WM_CLOSE完成DestroyWindow、PostQuitMessage、RemoveProp和
WM_NCDESTROY，共29次同步回调。两次最终桌面读回均与基线一致，没有执行恢复写操作；
分辨率、任务栏、工作区及前台恢复检查通过。无截图、全局输入或战斗。

本次组件仍失败：观察器把GetProp返回NULL后的LastError=2误判为属性未移除，因而
在WINDOW_CLOSE完成判定处拒绝，尚未执行类注销、模块卸载及MAIN/PTD/CRT正常清理。
助手由Job终止（exit94），Job空、8个父CloseHandle均成功；这只证明失败后的收容，
不能算正常资源释放。正式任务仍2/8，GAME发布、场景等待和首次结果消费未完成。

## 真实失败与窄修正

本次唯一原生来源保存在F盘
`.venv-audit/terminal-window-destruction-build-v1-20261114/native-window-case-v1.json.gz`，
81,230字节，SHA-256 `b0ca313f94e737821eac86dae289a5b4cedc80afdc015079c81977fbd1cb5175`。
同名`.desktop.json`保留桌面基线和恢复读回；不复制完整来源进Git，Git保存复现代码、
小报告及位置/校验清单。旧二进制、源码、失败报告和已用一次标记均保持原字节。

原424958处RemoveProp真实返回当前MAIN `1348472864`；辅助GetProp返回0、error2。
[GetPropA约定](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getpropa)
按返回NULL判断未找到属性，并未保证此时LastError为0；
[RemovePropA返回](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-removepropa)
移除项原先关联的数据。v3仅修正这处台账：非零当前owner、移除返回值等于owner、
辅助读回为0；保留全部真实错误码。窗口/线程/回调所有权、原调用点、实际销毁、
quit及后续正常清理的条件均不放宽，也不写游戏结果字段。

修正版x86严格编译通过，6条C++编译期断言覆盖本次真实值、空owner、移除失败、
错误owner和残留属性；生成源码除这一个判定和纯函数/断言外与旧版逐字一致。
新v2入口复用原execute、20秒Owner、run_native和桌面恢复实现，以新构建身份和新
单次标记准入。完整符号路径复用固定父关口，不将旧失败改成成功，也未再次启动窗口。

[本次独立复核](../analysis/terminal-window-native-case-review-v1-20261114.json)；
[修正版离线准入](../analysis/terminal-window-lifetime-gate-v2-20261114.json)。

下一步是在新的明确60秒桌面授权内，仅测试修正版一次，确认正常类/module/MAIN/PTD/
TLS/heap清理与自然exit0，再推进GAME合法发布。现有一次授权已经使用，不自动重跑。

当前路径由同一 MAIN 所有者取得真实资源模块，作为原 WinMain 的入口参数，再经原
MAIN 构造、窗口准备、类注册、CreateWindowExA 和同步回调，到原 HWND 发布停点4504E1。
随后测试程序仅对当前所有者窗口发 WM_CLOSE，原424980/450D30在450F6E调用实际
DestroyWindow；WM_DESTROY内原450F84调用PostQuitMessage，原424958删除CPP_CLASS。
WM_NCDESTROY及IsWindow失效观察共同证明窗口销毁，不能把WM_CLOSE返回0当成成功。

原关闭代码不会清零MAIN+4或7A0BB4。此处保留原状态，不写假零；原44FE60析构的窗口
基类清理不再读取这个失效HWND。类注销、资源模块卸载、补充原MAIN析构/free、PTD释放
与TLS清零、锁/TLS/堆销毁的目标是在同一原生寿命中完成，本次拒绝前尚未执行这些步骤。
补充清理根使用独立栈，暂停的
WinMain栈保持不变，因此这不是WinMain自然返回，清理后该暂停状态也不能再原生续跑。

## 此前已完成的离线验证（不替代本次原生失败）

- 完整符号路径17766条原指令、147次平台调用、20次回调，全部回调恢复57项CPU；
  模型资源账本归零。创建消息形状参考固定旧来源，所有当前身份和销毁返回值明确为
  模型输入；没有把这些值当成新鲜原生结果。
- 两份旧创建状态上的独立销毁模型各执行623条原指令、8个原API和3条声明消息。
  旧原生关闭记录缺少完整逐回调轨迹，不能用它伪装完整销毁重放。
- 10项不完整销毁/错误线程、TEB、消息、父请求、深度、lane拒绝，以及真实watchdog
  参数收紧到20秒的无Win32回归通过。
- 新旧桌面回归共18项通过，覆盖既往任务栏塌缩、Job未空、用户新输入、前台寿命变化、
  查询超时、部分恢复及异常路径。它们使用脚本化后端，没有读写真实桌面。
- x86 `/W4 /WX` 构建与当前完整代码/构建身份准入通过；独立审查记录见下方。

[完整离线关口](../analysis/terminal-window-lifetime-gate-v1-20261114.json)；
[销毁模型](../analysis/terminal-window-destruction-model-v1-20261114.json.gz)；
[验证记录](../analysis/terminal-window-lifetime-validation-v1-20261114.json)；
[独立复核](../analysis/terminal-window-lifetime-review-v1-20261114.json)。

## 一次真实测试的具体范围

默认命令只输出计划。必须有新的明确宿主授权和剩余55–60秒的期限，才允许进入运行
入口；准备完成后若剩余不足45秒，拒绝创建进程。原生硬watchdog20秒，失败Job清理
最多3秒，桌面读取/恢复每次独立隐藏子进程最多5秒，两次最终读回间隔0.5秒；正常
恢复最坏预算43.5秒，保留余量，不扩大授权时段。每个build目录只允许一次原生尝试。

原CreateWindow样式含WS_VISIBLE：即使停在ShowWindow之前，也会显示约1024×768的
原窗口并可能取得前台。不是隐藏窗口测试。此关口不执行原游戏EXE进程、GAME初始化、
D3D/音频/gamma/DirectInput、截图或全局鼠标键盘操作，不进入战斗。

测试前记录显示模式、任务栏、工作区、前台窗口/进程寿命及输入桌面。测试Job确认清空
后，且没有新用户输入、原shell和桌面身份仍一致，才按基线恢复变化的模式、任务栏
几何、工作区或前台；不重启Explorer、不写注册表、不改任务栏自动隐藏策略、不强制
附加输入线程。两次稳定读回都通过才标记监控范围内恢复成功。检测到用户继续操作时
拒绝覆盖其新状态，测试不得算通过。

gamma、光标形状、像素等不在本窗口组件的恢复证明范围内；后续GAME/D3D平台必须
另补相应清理与恢复证据，不能沿用本关口宣称全部桌面状态已验。实际销毁还可能产生
模型之外的消息；不支持的原API必须拒绝，保留首个现场，不重复启动同配方。

只有这一次真实组件测试通过，才能向GAME合法发布继续推进。两例全新原生完整重放、
连续三次握手、等待返回/结果消费和独立完整验收标准保持不变。
