# 两条终局分支最后一组对白

connect-terminal-last-dialogue接续9846d8c1封存的PC294/312 wait1，父49项及其验收本体和全部递归原资产/存档/检查点保持。

| 分支 | 原指令组 | 目标边界 |
| --- | --- | --- |
| neutral_running | 294:43/config7，302:44，306:17/text9，312:50，316:51 | PC320 wait1 |
| timeout_before_combat | 312:43/config4，320:44，324/330/336:17/text10/11/12，342:50，346:51 | PC350 wait1 |

胜利配置7选图层4、重写record0；超时配置4选图层7，原count导出record0/1/2，三项均实际原替换。44只清count、保留旧指针，早期text7_3/世代49的record2一直存活；原405160调用403730先实际Describe/Release它，再创建新text12。峰值仍10/10，正式来源复用原10张/32创建助手及已有清理根。每帧仍沿heads/arena/input/task四根，76/77原采集raw256经原键盘代码更新全A00；原任务写PC/wait，无新增VM/handler根或主机派生字段写回。

初始按count误判第三槽为空，预期超时只有两次替换；v1在PC350两保持后由真实三次替换触发计数守卫，完整139,673,200字节诊断及精确代码输入均保留。此前11张实验helper和真实容量探针本身验证了11创建/12拒绝/11个显式释放，但不证明原VM需要扩容；它们作为独立失败实验保留，第二版采集回到未经修改的原10张助手，第三版沿用该助手。

旧GPU身份已接近GDI域；新创建使用48001000–49501000独立区间，每次创建单独投影域及7个身份。声明前验证全区间与全部实际before映射及旧退休/live身份无交叠，只改变后续分配起点，原AddressSpace分配代码、父ledger/guest地址/已验FU指针与表面alias保持。独立审计另验整段非交叠、每个实际wire身份/所有权及GDI/CRT边界，原HeapAlloc/LockRect/padding完整保留。

独立引擎保留来源完整PE初始映射、RX/RW及原快照分区，原指令/写回调不裁剪；核对父完整前向、新阶段全内存/57CPU/逐帧队列/全部摘要、当前全部CRT/GDI/GPU协议和原实际清理，两个新完整原生实例复现。流式JSON读写保留全部字段、值、像素与原始证据字节。

v2在固定父ML前缀被write SHA守卫拒绝：实际新字体重用了已删除字体的原生句柄整数，旧投影因此少分配一个guest身份。完整诊断和精确输入保留。v3按GDI创建寿命和角色绑定当前真实句柄；固定父小计划只规定opaque handle的guest身份，独立审计逐条与固定父原回执核对。API调用、native参数/返回、所有内存输出与像素保持实时原值；同一原生整数仅可在旧寿命删除后重用，新阶段创建始终取得新guest身份。SelectObject、所有删除、完整逐调用绑定/寿命和测量DC补充释放另验，父全内存/57CPU/原摘要仍须严格一致。

## 实测验收

| 分支 | 新增/累计完整任务 | 全映射区域 | 新增原指令/原写 | 存活纹理/创建世代 |
| --- | --- | ---: | --- | --- |
| neutral_running | 35/578 | 452 | 2064996/1106378 | 10/15 |
| timeout_before_combat | 59/605 | 502 | 3891503/1929252 | 10/18 |

两例前向累计52743893条原指令、29942022次原写，各57CPU，无pending。当前90/108次原COM、峰值10/10张live、15/18创建世代全部实际原释放，补充原清理根14/14。两个新完整原生实例复现全部累计摘要、全内存/57CPU和当前清理。专项89项及父守卫16项通过，父49项和验收本体、递归原资产/存档/检查点和旧helper保全另验。

neutral_running各新文字上传非零字节数：[437]；原ANSI/GDI结果原样保持，不称实际正确显示完成。

timeout_before_combat各新文字上传非零字节数：[799, 3928, 3016]；原ANSI/GDI结果原样保持，不称实际正确显示完成。

完整来源及诊断按analysis/terminal-last-dialogue-local-evidence-v1-20261029.json清单保存在本地和仓库外逐字节备份，Git只保存代码和必要小报告。


## 复现

```bash
.venv-audit/Scripts/python.exe -X utf8 -m tools.terminal_last_dialogue_emulation --capacity-out analysis/terminal-last-dialogue-capacity-NEW.json
.venv-audit/Scripts/python.exe -X utf8 -m tools.terminal_last_dialogue_emulation --out analysis/terminal-last-dialogue-source-NEW.json.gz
.venv-audit/Scripts/python.exe -X utf8 -m tools.terminal_last_dialogue_verification --report analysis/terminal-last-dialogue-source-NEW.json.gz --out analysis/terminal-last-dialogue-proof-NEW.json
TERMINAL_LAST_DIALOGUE_REPORT=analysis/terminal-last-dialogue-source-NEW.json.gz .venv-audit/Scripts/python.exe -X utf8 -m unittest tools.tests.test_terminal_last_dialogue_source tools.tests.test_terminal_last_dialogue
.venv-audit/Scripts/python.exe -X utf8 -m tools.terminal_last_dialogue_preservation --out analysis/terminal-last-dialogue-preservation-NEW.json
```

容量实验回归使用capacity-v1小回执，与实验11张helper精确源SHA绑定，未计入正式原VM纹理峰值。大来源/失败诊断留本地及仓库外逐字节备份，Git只保留代码、必要小报告和大小/SHA/位置。原ANSI/GDI的实际空白/乱码保留，不补画；后续清层/淡出/终止、实际draw/Present、完整终局、原外层同寿命、任务退出/奖励/学校及R3–R6继续待验，Godot和2026-11-20目标不变。
