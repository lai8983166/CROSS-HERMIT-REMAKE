# 原终局确认后的角色与后续对白

`connect-terminal-followup-dialogue`，2026-10-27。接续固定父验收 `ac1937ef900d1ebb2bae5d70ca60f6ea7ae0949e8fc093af867fb6fcea27beab` 的 PC156/168、wait1。当前单元只完成下一组资源、原任务与新的确认等待。

## 原脚本及真实资源

T0004 段2在156执行30，完整四个literal为7/1/0/30。配置7对应层4，角色1姓名字节为 `b3cdaca5af53`，肖像为原SC001。原4CC190按层号写入30/31两个IMAGE槽，实际原side getter和4CDE10边界决定本次使用槽30；配置号不能直接作为层号，也不能沿用父槽32。姓名纹理记录为NODE4+60h，肖像按当前原注册容器取得。

后继176的43选择层4，184的17选择text2（原ANSI `a6d1ae76a14ba14ba148`），190的50等待全部就绪，194的51进入PC198/wait1。下一条43/config4不执行。

段11在168的43/config8选择层5，176的44只清文字计数和动画，不释放GPU纹理。180的17/text4（原ANSI `a14ba14ba14ba14b`）经原405160，在4051A9调用403730，先真正Describe/Release旧层5文字，再在相同record新建纹理。186的50、190的51进入PC194/wait1，下一43/config4不执行。旧姓名、槽32肖像和层7三行仍存活。

## 方法和证据边界

前驱时钟作为已捕获平台输入固定，当前完整PC156/168内存、57项CPU、队列和累计原摘要与父相等。新idle/press/release独立记录为新的声明回放周期，仍使用已验76/77流的256字节raw device；原4113D5–4116A4产生整A00键盘对象。原先三条bindings保留，不把本轮重放声称为新OS采集。

每帧只用原队列表头/arena复位、请求复位与完整454CF0四根；资源入口暂停后从原EIP/ESP连续恢复，不新增VM或handler根，不从主机改PC、wait、文字计数、角色或派生输入。唯一新增机器码范围是完整44体4C4EB0..4C4F23，原守卫函数的code object保持。设备、绘制门、几何、队列、冷CRT域和测量DC仍是明确方法输入，未完成原renderer启动或外层原生调度连接。

姓名及对白使用实际原14个字体参数、当前NativeGDI测量与DIB、原清底/阴影/前景三阶段、原两带转换和完整纹理读回。SC001核对全262168字节、512行原复制和全256×512纹理。ACP936、宋体选择与Big5原ANSI字节保持，不补画空白字或修复乱码。新LockRect全部初始字节直接取自当前原生wire，转换只改原rect覆盖范围；未初始化padding不强制归零。

旧GPU助手人为拒绝原生分配器再次返回已释放地址。本轮独立CS副本只去掉该项禁令，仍拒绝重复存活地址，保持原Owned表、ABI、十张同时存活/32次创建容量及析构。新来源和独立验证器以创建wire序号、record、逻辑/原生指针和实际存活区间区分世代；不能把同地址当成旧纹理仍活着，不能重试或伪造Create成功。唯一字节差异由主Agent另审，旧助手和全部父证据保持冻结。

每段保留全57CPU和原PC/写入局部摘要，每帧重读全部拥有区SHA、完整队列；字体、构造、替换、就绪、确认等关键边界保存完整内存及原栈。当前CRT/GDI/GPU全协议逐项归属，原HeapAlloc全部初始buffer和对齐padding由当前wire与原构造另验；仅按无碰撞JSON语义统一整数地址键，不把guest内存或任意原生hex归一化。

首轮独立基线在帧间连续性检查拒绝：完整owner快照包含MAIN+10B8的键盘对象，press/release原片段在两帧之间实际改变了该对象。两例均只有frame2/3的owner分别4/6字节变化，队列相等；诊断另存 `analysis/terminal-followup-frame-bridge-v1-20261027.json`。独立模型按整个A00键盘预测结果衔接完整owner，其余字节与全部状态/队列仍严格相等；逐segment完整内存和57CPU重放保持，不排除owner字段。失败日志保留。

来源前向冻结后另执行当前边界的实际原清理。胜利补清层4文字、槽30容器和姓名，再清父资源；超时父层5文字晚析构释放当前新text4，不补一遍再双释放。每个清理根保留实际完整内存/57CPU和原生缓冲，不生成旧终态CPU或累计SHA投影，也不计原任务退出。新实例从完整前驱流程重建当前CRT/GDI/GPU并复现全累计摘要，不能从旧hexdigest恢复SHA内部状态。

## 实测来源

| 分支 | 新增完整任务 | 累计完整任务 | 新增原指令 | 新增原写入 | 当前纹理峰值 | 实际原清理根 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 中立首帧胜利 | 112 | 402 | 6,132,185 | 3,455,628 | 8 | 12 |
| 战斗前超时 | 35 | 349 | 1,503,814 | 838,678 | 7 | 11 |

各例最终无pending任务。两例前向累计27,023,521条原指令、16,504,803次原写入；新段完整内存边界130/50个、文字更新257/70次，逐帧全部区域SHA、57CPU和完整队列另核对。当前全资源共8次Create及8次原Release；包括旧资源在内各48次原COM叶、56/51次整表面观察，完整GPU wire为105/100项（含close），CRT原操作205/153次（另含close），GDI叶135/162次。原清理另执行31,522/30,091条原指令及27,211/26,616次原写入，不计前向任务或退出。

主Agent另建真实GDI对象并独立转换核对：新姓名原字体高度20/宽0/字重700，测量63×20、完整纹理1064个非零字节；胜利text2原宽高0/字重400，测量100×20、607个非零字节；超时text4同字体参数测量80×20、转换全零。三个原LockRect初始表面本次均实测为零，验证仍保留任意当前初始字节，不把零写成前提。主审分别核对姓名5层、IMAGE构造12层及两句文字4层原EBP祖先至完整任务返回，并核对SC001全文件/512行/完整像素。最终拥有区374/322个、原区间458/145个，无pending任务；独立主审和像素证据见main-review-v1、main-raster-review-v1。

来源 `analysis/terminal-followup-source-v1-20261027.json.gz` 为693242756字节，SHA256 `c46d21d7064224e29de0f25a539dac92f23eecf407c26c4f20df14cac2268779`，实际PID46504正常退出0，完整监督记录另存。独立基线v3已对两例完成全原前向/新增段/实际清理核对；v1的输入桥接拒绝及v2的空组时序拒绝原日志保留。

最终独立验证从最新固定父来源的真实GetTickCount记录提取相同输入，不再为同一时钟额外解码更早祖先大报告。fresh runner保留公开run_case原code object，只替换此只读时钟提供者；机器、原指令、CPU、结果、清理和摘要没有替换。

原count0的4CB220直接跳过记录循环，AL=1/ret8且整个AB8对象保持、无draw，原栈仍逐指令重放；原1–10记录模型保持。此空组路径由主Agent另做原机器码反汇编核对。首轮96项专项仅一个队列副本篡改负例失败：完整入口protocol已绑定队列，独立Replay核对实际capture后还须绑定frame.queue_after与frame.after副本。补齐这两个相等检查，保持原完整内存/57CPU/队列核对；首轮失败原日志留存。

## 最终验收记录

96项专项v2以1036.125秒、实际PID25232正常退出0通过；加上62项层7、39项确认和355项基础历史回归，共552项测试通过。v1的96项中仅队列副本负例失败，其余95项通过，全部原日志和实际进程记录保留。

最终证明 `analysis/terminal-followup-proof-v1-20261027.json` 为16382字节，SHA256 `94f34f76e60c3eb3f10d9cfefda14c942c10dba4007b883981cf83fc117beb25`，实际PID64300正常退出0。两例各从完整前驱流程新建当前CRT/GDI/GPU资源，完整初末内存、57CPU、关键边界、逐帧全域/队列、全部累计原摘要以及12/11个实际原清理根均复现一致。完整原生协议逐项核对，没有旧清理CPU/SHA投影或从旧hexdigest构造累计SHA。最终实现5文件SHA同时绑定来源、专项进程、主审与证明。

封存清单以 `analysis/terminal-followup-acceptance-v1-20261027.json` 为准；父65项及验收本体、递归原资产/存档/检查点/历史报告保持。总规格仅按上述实测更新，R3/R4/R5/R6和2026-11-20目标保持。

## 复现

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.terminal_followup_emulation --out analysis/terminal-followup-source-NEW.json.gz
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.terminal_followup_verification --report analysis/terminal-followup-source-NEW.json.gz --out analysis/terminal-followup-proof-NEW.json
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_terminal_followup
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.terminal_followup_preservation --out analysis/terminal-followup-preservation-NEW.json
```

专项默认读取本轮v1来源，换来源时设置 `TERMINAL_FOLLOWUP_REPORT`。所有输出使用新名字，失败日志与诊断保留；大型来源、独立重放、专项和新实例证明分时执行。正常退出由后台监督记录真实PID、创建时间、命令和最终文件SHA。

## 交接

完整终局、下一个确认以后的命令、实际draw/Present、原外层同寿命、任务退出/奖励和学校交接继续待验。Godot未改，R3/R4/R5/R6未完成边界及2026-11-20目标保持；本轮无OS输入或解锁要求。最终实测、专项和封存清单见本轮验收记录。
