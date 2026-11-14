# 当前所有者的释放与显示绑定

2026-11-14，本单元接续 e33cf5e8。正式任务仍为 **2/8**，不是完整战斗退出验收。

## 本轮实际推进

新增 D3D8 adapter0 的真实调用实现：原 factory 的 slot14 GetAdapterMonitor →
GetMonitorInfoW → 精确匹配 EnumDisplayDevicesW → 当前 DEVMODE220 与 gamma1536。
16204 字节固定结构包含完整显示身份；绑定、发布后、最终 device Release 后三阶段
均保留 MAIN/TLS、原始字节、真实 API 返回、PTD116/LastError 和 CPU57 恢复检查。
adapter 与父基线目标不一致时，在 CreateDevice 前拒绝，不猜 first display 等于 D3D0。
原窗口增加真实单调代次，释放回执与该 HWND/代次、当前基线 token 绑定。

`terminal_recovery_binding.py` 从原始请求和回执重建输入、图形引用、锁和状态块账本，
认证 Unacquire、Release、gamma、原窗口销毁、最终零账本与 Shutdown。两份纹理均从
原锁上传的 MEM_WRITE/GFX_LOCK_WRITE 和新的只读锁 MEM_READ 重建 131072 字节逻辑像素，
逐字比较；不只相信报告的 accepted 或摘要字段。

真实恢复观察者保留当前 helper 的进程及 query-only Job 句柄，核对精确构建白名单、
进程创建时刻、真实 TEB 的 PID/TID/self、当前 Job 成员。正常写恢复要求实际 exit0、
Job 空和完整释放认证；每次写前复核。父桌面基线与设备创建后输入线程的光标基线分开，
原输入线程先平衡其自己的计数，父桌面光标必须在最终两次真实读回完全一致。
旧 `NATIVE_ADMISSION=False` 未更改；新增恢复函数以本次证据局部准入。

故障收容另行分类：actual process death / Job 空不等于正常资源释放。新 native BEGIN
记录只在 MAIN 到达已校验危险叶调用边界时发出，保留原输入字节及 PTD/LastError。
父端“发了命令”不能充当该证据。无返回的调用只能贡献由其实际原输入严格推得的值；
未知 taskbar/clip/work-area 等差异拒绝。历史 post 值不作为永久恢复许可。

## 验证范围

- 一次完整原指令模型，64.718 秒、4,495,636 hooks、10,943 sites、904 API、20 回调、
  6313 组请求，原 4506E9 发布一次，三份 display / 两份 texture 和补充清理闭合。
- 原采集末尾的后置认证器因模型缺附加 token 字段报 `KeyError('token')`，该原文件不改。
  修正认证器从已有真实 MEM_READ 输出提取状态块 token，复用来源纯离线接续通过；
  未重跑原指令，且模型始终不提升为原生设备证据。
- 输入线序列共 21,654,756 字节。旧 16 MiB 总输入上限会在清理期间 request5771 失败；
  新构建仅扩大到明确的 32 MiB，单块32768、单行、命令数和 Reader/worker 逻辑未改。
- 最终 v6 x86 `/W4 /WX /MT` 严格编译通过。真实无窗口寿命 0.235 秒，错误寿命拒绝、
  活进程恢复拒绝、正常 exit0、Job 空、7 个父关闭及2个保留句柄关闭通过。
- 新监督器正常恢复模型、真实内核无限等待超时、绝对截止覆盖相对寿命三例通过。
  58 项局部回归与严格 OpenSpec 通过。实际 GPU、桌面写恢复和 GAME 均未执行。

外部监督器将命令和整个观察者裁到同一个绝对截止，并预留3秒收容；超时不是恢复成功。
正常路径与异常收容路径的原始回执、错误和最终桌面状态分别保存，不相互替代。

## 明确未通过的宿主准入关口

原 CreateWindowExA 的 style 为 `0x90000000`，D3D 绑定之前窗口已经可见。
若此段失败，当前 runner 只有两次“是否自行恢复”的观察，尚没有经过认证的前台恢复
路径。故 `terminal_game_bound_native.py` 的 `NATIVE_WINDOW_ADMISSION=False` 同时保护
`check_gate` 和 `run`；不存在可发布的 ready gate，伪造 JSON 的 ready=true 也不能启动。

下一单元先补这一个窗口前缀失败分支的实际变更与恢复来源，并强制完整 gate pin 集合，
做有界预检。通过后再提前告知新的宿主测试窗口，一次采真实 GPU 读回、GAME 发布及
正常资源清理；不从当前准备直接进入战斗。等待返回、首次结果消费和三握手仍未执行。
两例新寿命、独立完整重放、CPU/内存/ABI/累计轨迹、真实 PTD/资源释放及篡改拒绝不变。

## 证据入口

- `analysis/terminal-recovery-binding-preflight-v3-20261114.json`
- `analysis/terminal-recovery-binding-independent-review-v1-20261114.json`
- `analysis/terminal-recovery-binding-closeout-v1-20261114.json`
- `.venv-audit/terminal-game-bound-model-v1-20261114.json.gz`
- `.venv-audit/terminal-display-owner-build-v6-20261114/`
- `.venv-audit/terminal-recovery-binding-v3-20261114/`

旧父来源、原游戏资料/存档及既有未跟踪技能目录不改。构建草稿 v1/v2 的目录日期
20261115 是本轮命名笔误，实际创建于本轮2026-11-14；退役清单保留此说明。
