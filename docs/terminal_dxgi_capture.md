# 独立呈现帧捕获（2026-11-12）

当前change为connect-terminal-wait-and-battle-exit，仍2/8。DXGI资格只检查独立
截图通路，不升级为原游戏兼容、连续等待/消费或正式资源清理验收。

## 实现与范围

`terminal_dxgi_frame_v2.cpp` 使用已有MSVC 14.44/SDK 10.0.22621构建，所有新文件
位于F盘 `.venv-audit/host-frame-v2`。没有安装依赖、更改显示设置或调用PrintWindow。
按当前窗口所属显示器创建D3D11/DXGI duplication；整屏纹理只留在GPU，仅将
自有窗口区域复制到CPU staging。核对当前PID/前台、可见性、遮挡和屏幕坐标，
跨屏/旋转输出拒绝。受保护内容、鼠标更新帧、陈旧时间戳、设备错误均不算成功。

自有256×192窗口显示两幅确定的颜色网格。先创建取帧通道，再呈现图案；
AcquireNextFrame等待总预算5秒，Python助手总预算至多25秒，桌面窗口最多60秒。
C++检查像素后，Python独立读取文件并逐像素核验两幅图及QPC顺序、文件摘要。
成功必须同时通过原desktop恢复门的两次连续状态核对；异常也执行该检查。
辅助窗口结束后恢复原前台目标（核对原PID），不重启Explorer、不修改自动隐藏。

文档依据：
[Desktop Duplication](https://learn.microsoft.com/en-us/windows-hardware/drivers/display/desktop-duplication-api)、
[帧元数据](https://learn.microsoft.com/windows/win32/api/dxgi1_2/ns-dxgi1_2-dxgi_outdupl_frame_info)。
本接口涉及目标显示器帧，执行前须明确该范围并取得当前桌面时段授权；仅保存自有区域。

## v1实机结果与修正

用户授权的首轮于北京时间03:21运行，不启动游戏。获取到的新时间戳帧中，
自有窗口区域仍是弹窗出现前的背景，49152像素中43261像素不匹配。
这证明“帧时间较新”不足以证明目标窗口图案已呈现；没有视为资格通过。
已停止并检查两个任务栏、显示模式、工作区、输入桌面及前台恢复，desktop记录
restored=true、两次checks均为空。辅助进程结束，没有启动游戏或点击菜单。

失败图意外含先前背景，因此已删除；其大小、SHA及原因记录在
`analysis/terminal-dxgi-qualification-v1-20261112/retired-image.json`。
保留首个像素差异数量、QPC和清理记录，不把已删除图像报告为可读来源。
v1源码和二进制身份保留，未热修改失败实现。

v2在原5秒预算内，丢弃尚不匹配当前图案的过渡帧，只在逐像素一致时保存；
记录丢弃数量和首次差异，超时仍拒绝。不在失败后延长期限或重启设备反复探路。
这是一处具体就绪条件修正，目前编译和离线检查通过，仍待新授权的实机预检。

## 菜单接入准备

`terminal_dxgi_game_capture.py` 认证最近45分钟内的成功资格文件、构建、原始助手
回执、两幅图像及desktop清理报告。原游戏截图需当前Job、精确exe、PID/HWND/MAIN
属性和前台一致，读取真实呈现帧，仅持久化裁剪后的PNG。纯色帧记录RGB极值；
不会因存在图像就声称游戏渲染或菜单正确，仍需Agent检查。

`terminal_host_menu_preflight_v3.py` 使用上述接入，不修改冻结v1，也不解禁拒绝
PrintWindow的v2。默认仅打印计划；真实执行需成功资格、当前明确授权及至多10分钟
到期时间。资源核对后不足410秒则不启动。路径仍是原startup自然退役、菜单独存和
selector原栈、截图复核、一次原新游戏选择、ADV后继观察；最后强制desktop恢复门。
截图、调用轨迹、线程退出、正式资源/PTD清理分别验证，不以预检或exit 0替代验收。

以上为准备阶段状态；11月12日后续实机结果如下。

## 11月12日资格与两次菜单窗口

v2两幅自有图案均通过C++及Python独立逐像素核对（零差异），QPC顺序、
精确构建身份与两次桌面恢复检查通过。第一幅丢弃一帧未就绪内容，第二幅无丢弃。
来源：`analysis/terminal-dxgi-qualification-v2-20261112/qualification.json`。

首次菜单窗口实际截图为“Please Wait …”，捕获成功，但45.3秒图像复核晚于
v3的30秒限期；未进入菜单。v4只修正早期复核预算至最多90秒，同时保留350秒
后续预算及原十分钟总时限，拒绝晚到回执，未修改已运行的v3。

第二次窗口中，启动截图为“Now Loading …”，早期复核通过；原启动线程在
273.593秒exit 0且菜单独存。取得清晰Cross Hermit主菜单，但菜单截图复核回执
晚到153.498秒，采集已结束。原菜单worker约341.640秒退役，后继vtable为
0x5CAA48（启动任务），没有点击、剧情后继或战斗推进。不能把该后继当作ADV。
`terminal_menu_handoff_verification`拒绝：
`no observed startup/menu resource-owner overlap with successor`。
进度仍2/8，独立帧捕获资格不等于菜单交接或完整图形/逆向验收。

两个游戏窗口退出后任务栏由40缩为32逻辑像素，原desktop记录保留失败。
按用户恢复授权重启当前会话Explorer，并恢复已核验原前台；新recovery记录
均再次与各自原始baseline连续核对两次，通过分辨率、工作区、任务栏和前台检查。
第二轮原Job为空、无强杀，最终无游戏/捕获助手残留；子进程状态不作为WinMain
正常返回或PTD清理证明。证据及体积见本轮closeout-v2。

下一窗口前先离线解决菜单复核调度：菜单有效期内必须及时消费当前图像复核，
超时立即拒绝；不得将本次晚到回执用于下一原生寿命，不得移除当前状态和输入门。
不得单纯加长游戏等待或再次启动相同配方。需要新的桌面窗口时另行提前告知。
