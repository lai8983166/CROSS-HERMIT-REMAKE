# GAME 发布前的平台接续（2026-11-14）

本轮完成原 WinMain 到音频、两组影片对象初始化的平台适配，并在有界模型中连续走到
`413450` 图形初始化入口之前。原生助手严格编译通过，**没有运行**。GAME 尚未发布，
等待返回、首次结果消费、三次握手均未执行；正式任务仍为 **2/8**。

## 已实现的具体调用链

新增 `devtools/terminal_game_native.py/.inc`，复用已执行并固定的窗口 v3 所有者；
原 Reader、worker 调度及旧文件保持原字节。新增接口只在同一 MAIN/TID/TEB、显式
GAME_GATE 内执行：CoInitialize/CoUninitialize、InitCommonControlsEx、三种固定
CoCreateInstance、五种原 Graph QueryInterface，以及音频初始化/音量/搜索目录、
影片通知和对应 Stop/CloseDown/Release。GUID、参数个数、调用槽和返回位由原字节核对。
它不是通用 COM 调用器，也没有启动游戏的入口。

`terminal_game_platform.py` 在当前原执行器中适配这些接口。真正的本机返回值与输出
缓冲须原样读回；客体 COM 代理仅投影当前活体接口，保留同指针别名和引用计数。
平台调用释放 dispatch 锁，允许同 MAIN 的同步原窗口回调，回调父请求、线程、TEB、
深度和 CPU57 恢复均继续检查；当前只验证了模型包络，未资格化实际 COM 重入。

有界模型的三个初始根是原 heap、TLS 初始化和 `49DD70` WinMain。随后沿原指令执行：

```text
49DD70 → MAIN/原窗口450350 → ShowWindow/UpdateWindow/窗口矩形
       → CoInitialize → InitCommonControlsEx → 450570
       → 412E30完整构造 → 4500B0路径准备
       → 4135D0/40C340音频 → 413630/两次41D5D0影片
       → 停在413450首条指令之前（7A49FC仍为0）
```

没有改成另一个 `412C70` 工厂，没有修改全屏参数或直接补写 GAME/结果字段。
`4297A0` 实际使用 PathAddBackslashA；不能据此误加 SetCurrentDirectoryA。
真实资产工作目录与 DirectInput 所需实例身份仍须单独核实。

清理用独立 WORK_STACK 调用六个**明确声明的补充原函数根**，先原 GAME 析构/free，
随后窗口、COM apartment、MAIN、PTD/TLS/锁/堆清理。原析构在模型中释放15份 COM 引用，
两组影片先 Stop/通知归零，音频先 Stop/CloseDown，再 Release；全部模型资源账本归零。
这不是 WinMain 自然返回。清理后已废弃的原生状态不能恢复使用。执行器断言挂起的64KiB
WinMain 栈未改并保存摘要；报告未保存全栈原字节，不能替代独立完整重放。

## 本次预检与证据范围

最终 v5 模型7.625秒，记录222146次指令钩子、7018处原字节、216项 API、20次模型回调、
828组请求/响应；回调 CPU57 恢复、COM 别名正例及6项身份/引用/回调拒绝通过。
所有 Windows/COM 返回值、设备、句柄、TID/TEB/PTD 均是**显式模型输入**，不是本机观测。
旧窗口成功来源只复用身份和合同，未把其已释放句柄带入新所有者。

新助手为 x86 Windows subsystem，`/W4 /WX /MT` 严格编译成功；新导入仅限 COM、
common controls 和有界字符串转换。没有窗口、截图、全局输入或桌面状态读写。
独立复核核对原字节、ABI、模型记录和资源顺序；主 Agent 独立复核子 Agent 编写的原生
实现，子 Agent 复核主 Agent 编写的执行器。该复核不是完整指令重放或新鲜原生寿命。

来源及校验见 `analysis/terminal-game-platform-preflight-v1-20261114.json`，
独立复核见 `analysis/terminal-game-platform-independent-review-v1-20261114.json`，
保留/退役与容量见 `analysis/terminal-game-platform-closeout-v1-20261114.json`。
模型和构建产物只保留于 F 盘 `.venv-audit`，不追加到普通 Git 对象。

## 尚未满足的 GAME 实测准入

1. 将既有 D3D8、字体/纹理缓存、状态块和队列平台合同接入当前 MAIN/CPU57 所有者，
   继续原 `413450`，保留原全屏模式与真实错误返回。旧工具不能作为新寿命的资源来源。
2. 接入原 `413560 → 410E90 → 411090` 的 DirectInput 和实际光标调用。原 cooperative
   flags=6 依赖前台；不能改成后台模式或隐藏窗口后宣称等价。窗口和实例身份须合法。
3. 完成下面的 gamma/输入/显示恢复，并验证失败分支。现有窗口恢复仅覆盖显示模式、
   任务栏、工作区、前台和 Job；它没有验证 gamma、光标或 DirectInput。
4. 先做有界离线原链和清理预检；只有上述准备通过，才提前告知并取得新的有界宿主授权，
   在预留清理时间内验证实际 COM/D3D/输入寿命。当前没有可启动的 GAME 测试方案。

## 恢复顺序与拒绝条件

已有 `tools/school_startup_return_device.cs` 的 Cleanup 在设备 Release 前调用
RestoreGamma，随后释放资源、设备和窗口；其既有窗口模式证据保留原结论。新全屏路径
还必须在设备释放及显示模式恢复**之后**读回 gamma，不能直接沿用旧成功结论。
Windows 文档指出显示事件可重置 gamma，且 SetDeviceGammaRamp 的成功返回可能不代表
实际应用，因此验收必须比较实际读回的原1536字节。[Microsoft gamma 说明](https://learn.microsoft.com/en-us/windows/desktop/api/wingdi/nf-wingdi-setdevicegammaramp)

后续实现应按以下顺序保留真实回执，任何缺项均拒绝实测成功：

1. 在创建设备前固定受影响显示器/适配器身份、模式、gamma，以及光标位置/形状/可见性/
   限制区域和输入状态基线；记录当前进程、窗口寿命与用户输入代次。
2. 在原所有者中停止音频/影片、清除影片通知，按实际依赖解除输入 Acquire 并 Release。
   DirectInput 使用的窗口必须保留到输入对象完成清理；不能先销毁再把调用成功当释放。
   [Microsoft cooperative level 合同](https://learn.microsoft.com/ja-jp/previous-versions/windows/desktop/ee417921(v=vs.85))
3. 清理字体/缓存、纹理、VB、状态块及全部持有引用；设备存活时恢复设备 gamma，随后
   释放设备/工厂，并完成窗口、类、模块、COM 和 MAIN/PTD/TLS/堆清理。
4. Job 为空后检查显示模式，必要时只恢复本轮改变且身份仍匹配的状态；**最后**比较并
   有条件恢复桌面 gamma，再次实际读回。禁止用线性 ramp 代替原基线。
5. 在无更新用户输入、显示器/壳层/原前台寿命仍匹配时，恢复本轮改变的光标/限制状态、
   任务栏、工作区和前台；有新用户状态则拒绝覆盖，明确报告未恢复项。禁止屏蔽输入或
   强制重启 Explorer。按既有方案取得两次稳定读回及实际释放回执。

这部分是已核对依赖后的**待实现恢复合同**，不是本轮恢复测试通过。无桌面操作的本轮
不需要执行恢复写入。模型/编译通过均不解除上述阻止条件，不降低完整状态、ABI、资源
寿命、两例全新原生、独立完整重放、篡改拒绝和独立复核标准。

## 下一单元和止损

先离线复用现有图形合同，完成当前所有者的 D3D8/字体与恢复实现；60分钟到点报告具体
停点，不扩建 VM、截图或原机上下文搬运。每个有界模型沿第一次明确失败定位，修正后
才继续；当前模型单例上限25秒、压缩证据4MiB。本轮不因为模型通过而另开一次桌面测试。
合法 GAME 发布并完成真实设备清理预检后，才继续原 worker、等待返回与首次结果消费。
