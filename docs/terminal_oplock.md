# 保留原调试所有权的 NEW_GAME 文件事件观察

2026-11-12：**RW oplock 已在无窗口原生案例取得活体 TLS 和正常返回/退出；原游戏尚未运行，正式仍 2/8。** 本轮没有重试轮询、截图、保护父调试 relay 或主动 OutputDebugString 通知。

## 实际取得的链条

观察器对 F 盘私有文件持有只读、异步 RW oplock（READ1+WRITE4=5）。原 worker 按游戏
已核参数调用 CreateFileA：GENERIC_READ、share READ、OPEN_EXISTING、flags1。文件系统
发出需要 ACK 的 RW→R break，并阻住这次打开；观察器读取实际 worker，再关闭自己的文件
句柄隐式 ACK。原 worker 继续读完64字节、清自己的 TLS、释放自己的分配并退出。
原父进程始终接收和继续 child 调试事件；观察器没有附加调试器、断点、注入或写目标状态。

| 项目 | v2 原生现场及独立核验范围 |
|---|---|
| 原文件调用 | 保存的 WOW64 EIP 位于 NtCreateFile+12 的 RET 2c；原参数、栈内 OBJECT_ATTRIBUTES/UNICODE_STRING 与目标文件名匹配 |
| TLS | 实际 FS→TEB→slot9→116字节全部匹配；这是helper自有数据，**不是游戏 CRT PTD** |
| 时序 | 原open7.2888ms；break→释放6.9467ms；暂停读取0.4471ms |
| 调试所有权 | 原父事件账本、进程父关系、现有debug port、同一线程创建/退出与保留句柄exit0闭合 |
| 恢复 | 原读取内容相同，父/子自然结束，Job为空、句柄关闭；两次桌面检查与原基线一致 |

v1正常结束，但采集器预期transition CALL内部栈；实际是WOW64保存的返回状态，因此
缺少原文件名内存。独立验证保持拒绝。v2只补齐已定位布局的原参数读取，不改v1原字节。

三个有界故障也已真实执行并独立核验：没有opener时取消并关闭、看门狗关闭、实际break后
在暂停前注入观察器异常并清空Job。第三例是**强制清场**，不算自然退出；这些案例不证明
所有OS API故障、暂停期间故障或原游戏异常路径已覆盖。

限制保持：机会锁延长真实I/O，不宣称零时序扰动。没有完整机器57项状态、逐指令恢复或
游戏资源/PTD释放证明。helper清TLS/free来自自身报告和后继原退出，不是独立清零停点。
v2记录当前系统调用32字节，未认证完整ntdll模块文件，不提升为通用系统后端。

接口依据：[FSCTL_REQUEST_OPLOCK](https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ni-winioctl-fsctl_request_oplock)、
[Create对oplock的作用](https://learn.microsoft.com/en-us/windows-hardware/drivers/ifs/irp-mj-create2)、
[关闭句柄隐式确认](https://learn.microsoft.com/en-us/windows-hardware/drivers/ifs/acknowledging-oplock-breaks)。
事件不携带PID/TID，必须另证实际文件名、原调用及线程。系统不提供锁超时；实现采用15秒
看门狗与异常清场。取消不等于异步完成，失败缓冲保持至专用观察进程终止。

## 原游戏接线与下一窗口

`terminal_host_menu_preflight_v7.py` 默认只打印计划。执行前重新认证两份固定SHA原来源、
冻结实现/二进制及故障记录，并要求新的360–600秒宿主窗口授权，不沿用历史时段。

1. 复用私有目录，完成原资源核验、自然启动退役及原菜单状态/输入保护。
2. 一次新游戏输入前，对该副本 `DATA/ADV/DAT/CH001.YBC` 申请只读RW锁。
3. 最多6秒等一次事件。实际NEW_GAME→CH001→CreateFileA/NT调用、线程/TLS和原父/
   debug port均匹配才保留；错来源、看门狗或超时均拒绝，不重试输入。
4. MAIN先暂停的既有采集只执行一次事件现场，即时放行，再等保留线程句柄最多4秒取得
   exit0，最后观察ADV。不用后续轮询补造NEW_GAME；ADV持续场景观察沿用原合同。
5. 沿用桌面收尾，复核分辨率、任务栏、工作区、输入桌面与前台；未恢复不得报告成功。

`terminal_new_game_oplock_verification.py` 将事件证据接入既有完整菜单、TLS、退出、ADV
及桌面验证。短暂停预算和原生elapsed采用QPC。v7尚无原游戏成功来源；接线和helper通过
不增加任务勾选，不代替等待返回、首次消费、三握手及两例全新完整重放。

## 固定来源

- `analysis/terminal-oplock-controls-v2-20261112.json.gz`：成功原报告压缩；解压SHA
  `ed36127a535be8f9f51f5b7b727a520f054d8537edd4d4af0867985154e251e4`。
- `analysis/terminal-oplock-controls-v1-20261112.json.gz`：缺原filename的首次现场，保持拒绝。
- `analysis/terminal-oplock-faults-v1-20261112.json.gz`：三故障原报告；解压SHA
  `f0404cb75858477e71f512fd3c10bb144d42fbaf10855a8e4cdf846d9b03ce1f`。
- `analysis/terminal-oplock-controls-verification-v2-20261112.json`：成功及三故障独立复核；
  旧v1 proof只涵盖正常例，原字节不变。
- `.venv-audit/oplock-preflight-v{1,2}-20261112/`、`.venv-audit/oplock-faults-v1-20261112/`：
  原小报告/sidecar和实际二进制。与Git压缩报告同盘，是恢复用副本，不是独立容灾备份。

保全、哈希、容量和清理结论见 `analysis/terminal-oplock-closeout-v1-20261112.json`。
