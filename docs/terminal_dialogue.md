# 原终局首句对白与确认等待

2026-10-26，`connect-terminal-first-dialogue`。接续当前GYBC、姓名和肖像资源的PC96/wait0，在同一资源寿命内接通首句原文字栅格、第四张当前纹理、完整任务和确认等待。本单元停于PC118/wait1，后继27尚未执行。

## 原执行与资源来源

每例从新战斗对象、原初始化及真实T0004重新执行前缀，中性胜利选择1/脚本段2、三帧超时选择4/段11。没有从已经清理的肖像边界恢复句柄或内存快照。两个代码段的PC96/104/110/114分别是43/17/50/51：43以`20000008`选择配置8、图层5；下一完整任务才执行17、读取原文字表索引0。首句原字节分别为`a14ba14ba14ba14b`与`a6d1ae76a14ba14b`，保留原ANSI路径和本机ACP936语义，未修复Big5乱码。

原4CABD0从文字对象取得高度/宽度，本夹具两者均为0；4CACF0实际`push 190h`，对白字体字重400，姓名字体的700不适用于此处。原4CAD03经原IAT请求14参数CreateFontA，返回地址4CAD09。原face字节`826c827220835383568362834e`仍经原ANSI接口传给Windows，实际字体与测量取本次回执，不称完成原renderer字体初始化。原格式化、414440和405160栅格体、403BD0及405A80转换、原字体/位图/绘字DC删除均执行。使用前缀仍存活的同一实际测量DC；新DIB在客体地址3E100000，保留姓名3E000000区域的历史字节。

第四张纹理由原请求经同一当前D3D8设备实际创建、描述、锁定及上传，全表面读回逐字节核对；GYBC、姓名、肖像也再次全表面读回。没有使用旧GPU回执。GDI句子另外独立重画清底、阴影和前景三个阶段，再用独立转换公式核对整张格式25/A1R5G5B5纹理，包括填充像素。

两例测量均80×20，padding2、DIB84×24，原名义84×24进位到实际128×32/8192字节纹理，一次转换。胜利首句三阶段DIB全零，当前纹理也全零；超时首句三阶段非零字节分别0/554/950，转换后纹理607非零字节。两次TextOutA均实际成功，阴影080808/前景FFFFFF。保留这一真实ANSI/字体结果，不把空白或乱码纹理称为可见正确对白，也不换编码、字体或像素补画。

本次实际选中字体均为宋体。Windows实际CP936转换把胜利原字节映射成四个U+E4D1，超时映射成U+03C1/U+754D/U+E4D1/U+E4D1；在本次字体下私用区标点绘字为空白。此原因由另建离屏资源与实际字符转换复核，区别于原Big5文字含义。

## 完整任务与验证

前向只声明40DB90队列表头复位、40DC80 arena复位、425DE0原输入复位和454CF0完整任务四种根。17任务在真实字体和原403BD0入口暂停观察后沿原CPU/栈继续，自然返回PC110。后续完整任务执行50、原文字淡入/间隔更新及就绪判定，到PC114/wait0；再由51进入PC118/wait1，两次无输入完整任务均保持。主机没有写PC、wait、输入派生值、纹理记录或计数，也没有新增独立VM/文字handler根。

两例各31次新增完整任务、126前向原区间：第0次43，第1次17，第2–27次文字等待/就绪，第28次进入确认，第29/30次保持。累计各209完整任务；每例93新增平台叶为27 GDI、4 COM和62任务查询，608条原查询观察。

| 来源分支 | 新增原指令 | 新增原写入 | 前向累计原指令 | 前向累计原写入 | 最终映射 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 中性胜利/段2 | 1,020,681 | 613,250 | 5,646,021 | 3,863,251 | 295 |
| 三帧超时/段11 | 1,028,990 | 614,384 | 5,956,884 | 3,994,922 | 296 |

独立Unicorn执行器从PC96全部拥有内存和57项CPU恢复，逐条执行新增原机器码，核对每段原PC/写入摘要、全部平台栈参数、原命令/转换/就绪查询观察、每帧全部映射/CPU/4096组队列表头与arena，以及字体、栅格、任务返回、就绪、确认和末端边界。兼容视图仅供冻结前驱验证器读取，原始GPU顺序和全部CRT回执另完整保留。最终还由新当前资源实例重建两分支，核对全状态和累计摘要。

前向冻结后明确补充原403730对白纹理析构，再执行原肖像、姓名、GYBC、队列及CRT锁堆清理。补充析构的原指令/写入、57项CPU、完整记录和记账另核对，不计原任务退出。助手正常协议退出，不能以驱动兜底释放冒充原析构。

开发失败v1保留了把43与17误放同一任务的自然返回；v2保留了过早替换DIB映射引发的重复映射拒绝。正式执行延后到姓名/肖像前缀结束后才切换平台DIB地址，未改原代码或清门继续。

## 固定证据

- 来源：`analysis/terminal-dialogue-source-v3-20261026.json.gz`，304406265字节，SHA256 `b09a5860494c1c3c6f1ab0f90babfaf9d7bfbb2367015e2c475b2ee193ecb116`。
- 独立证明：`analysis/terminal-dialogue-proof-v2-20261026.json`，两例另建当前资源全状态重放均通过；明确记录原字体0×0/字重400、实际宋体/ACP936、空白/乱码及未确认可见对白。
- 主Agent复核：`analysis/terminal-dialogue-review-v4-20261026.json`，另核原根/完整任务和全部CPU边界、原字重指令、四纹理释放及主机写入口；实现SHA与证明完全一致。
- 专项`analysis/terminal-dialogue-tests-v2-20261026.log`47项、历史回归`analysis/terminal-dialogue-tests-regression-v2-20261026.log`308项通过，共355项。原资料保全`analysis/terminal-dialogue-preservation-v2-20261026.json`固定前驱46项及其验收，并递归复核原资产/存档/检查点和历史证据。
- 验证器开发失败v1–v3和proof启动失败v1保留，分别发现姓名非空前提、原入队metadata副作用及导出引用范围；正式v4逐阶段核对和最终proof v2通过，不计失败作验收。
- 严格规格归档前32/32、归档后31/31通过；全部3项任务完成，归档于`openspec/changes/archive/2026-10-26-connect-terminal-first-dialogue/`。最终清单为`analysis/terminal-dialogue-acceptance-v1-20261026.json`，工作区、Git索引与HEAD原始字节逐项比较后封存。

## 复现与后续

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.terminal_dialogue_emulation --out analysis/terminal-dialogue-source-NEW.json.gz
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.terminal_dialogue_verification --report analysis/terminal-dialogue-source-NEW.json.gz --out analysis/terminal-dialogue-proof-NEW.json
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_terminal_dialogue
```

无需交互桌面、屏幕解锁或系统输入。继承的冷CRT六区335字节、当前设备/绘制门/几何、测量DC和有界队列仍是明确方法输入；精确前缀时钟重放沿用采集的平台输入，不称原生时钟连续性。没有完成完整原加载器、renderer启动或原外层线程同寿命连接。实际draw/Present、确认解除、后继27及完整终局、任务退出、奖励/学校交接仍待验。Godot未改，R3/R4/R5/R6保持未完成，目标日期仍为2026-11-20。
