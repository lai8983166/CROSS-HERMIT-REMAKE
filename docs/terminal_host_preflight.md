# 宿主机截图与原菜单交接预检

2026-11-12，connect-terminal-wait-and-battle-exit，正式仍 2/8。
本轮只完成离线准备；没有启动游戏、截图、改变前台或发送输入。

## 已知事实与不再重试的路径

- `docs/battle_return_audit.md` 第15/16节已记录普通资源管理器也出现
  FrameArrived/window capture 超时；重选、激活、重置 Node 连接没有恢复。
  因此不能只归因于 D3D8，更不能宣称已查明底层截图服务根因。
- 11月12日宿主机短测已认证原启动逻辑推进，但仅观察45秒；旧已认证来源中
  原动画约273秒、计数16205后才自然退役。短测没到菜单不是交接路径被证伪。
- 原菜单必须成为唯一任务，MAIN空闲，原selector栈和鼠标生产者一致；由原
  左键释放边沿选择新游戏、发布event7，再由原排程进入ADV。禁止叠加旧三根。
- 受保护子进程C0000354与WinMain/worker正常返回分开；自有Job为空不证明PTD释放。

## 新候选与止损

`devtools/terminal_host_capture.py` 是默认禁用的 PrintWindow/PW_CLIENTONLY 候选。
微软说明 [PrintWindow会同步阻塞并由目标窗口处理绘制](https://learn.microsoft.com/windows/win32/api/winuser/nf-winuser-printwindow)，
因此在独立隐藏子进程中只调用一次，5秒超时结束该助手并等待退出。
父端/子端核对精确私有exe、PID、HWND、MAIN属性和前台，父端另核对当前Job。
不读取整个桌面，不改分辨率、注册表、兼容设置或游戏内存，不向游戏注入代码。
位图上限2048×1536；空白/未改写/截断像素拒绝，PNG还须由Agent查看后确认。
非空图不等于游戏渲染正确，PrintWindow仍可能不兼容；当前没有真实图像成功证据。

`devtools/terminal_host_menu_preflight.py` 默认只打印计划。实际执行需要本次明确
宿主桌面时限和新增截图后备授权，不能沿用上一窗口。原鼠标后备授权保持原范围。
总预算最多600秒，包含完整资源核对；核对后不足380秒即不启动游戏。
自有Job定时器在总期限前15秒终止超时的本次进程，记录失败；常规路径发送原WM_CLOSE。
捕获/判断/点击任何一处失败不自动重试、不运行第二例、不调度战斗长前缀。

顺序：完整资源核对 → 原游戏启动 → 启动图像一次捕获及Agent复核（最多30秒）
→ 原startup自然退役 → 菜单图像一次捕获及Agent复核 → 原条件二次检查
→ 一次已授权的新游戏点击 → ADV现场 → 自有进程清理。
两次捕获对应不同阶段，不是失败重试。最早截图失败就清理，不等273秒动画。
所有新输出放F盘analysis；没有新增环境或运行副本。

Agent复核图片后才写对应 `.startup-review.json` / `.review.json`：
`{"sha256":"对应PNG摘要","image_visually_confirmed":true}`。
此回执记录Agent确已查看图像，不替代用户对截图后备和桌面时段的授权。
菜单点击仍由旧原字节/所有权/原光标位置保护；图像回执不直接指定坐标。

只读计划：

```text
.venv-audit/Scripts/python.exe -B -X utf8 -m devtools.terminal_host_menu_preflight
```

获本次授权后才由Agent填入带时区的真实到期时间、新输出名，并加
`--execute --allow-native-capture --desktop-until <ISO8601> --out <fresh-path>`。
本次预检只到菜单→ADV，不推进剧情至战斗。输出successor_observed也只是观察结果，
还须独立核验菜单原返回与worker退出；没有任何正式验收字段因预检成功变为true。

## 离线检查

普通模式64项通过：新增host_preflight、已有menu_input和menu_handoff_verification。
其中旧来源重放保留原调用/输入边沿/TLS等验证；新测试只检查拒绝合同和合成像素，
没有用合成图像冒充实机截图。冻结实现不修改，正式2/8与三关口保持不变。
当前尚待批准并执行真实宿主预检，截图问题未宣告修复。
