# 采集键盘与保留任务的离线连接

本单元 `connect-retained-keyboard-replay` 已完成3/3任务，归档至 `openspec/changes/archive/2026-10-22-connect-retained-keyboard-replay`。六组合运行及独立机器码复核通过，192项集成回归通过。将2026-10-22已验的两个原版键盘采集流接到三个已恢复的逻辑案例，全部在客体中完成，不需要Windows保持解锁，不启动窗口或提交新系统输入。

冻结完整任务报告的67帧原指令先被完整独立重放，恢复矩形祖先的逻辑内存、原初始化覆盖与CPU，到PC248/opcode50文字就绪等待。随后继续原425DE0请求消化、原队列复位和完整454CF0；没有新增独立4CE8F0根。

宿主仅把固定采集样本的原始256字节写到客体声明的GetDeviceState输出区，再执行原4113D5–4116A4，派生前次、当前、按下、松开和连发缓冲。整个A00h对象与独立公式核对；PC、wait和派生按键位没有宿主赋值。原生采集对象的指针没有搬进旧场景。

新平台服务只在原调用方、原IAT目标和相同空输入前提成立时回放已记录的ImmGetOpenStatus(0)与lstrlenA(空字符串)返回。它们是记录回放，不是这次新执行的OS查询；原游戏函数全部运行原机器码。旧图形助手已退出，其原生句柄不复用，本次不声称新GPU或资源寿命。

验收范围为自然文本就绪、无输入确认对照、实际采集按下解除确认、实际采集松开及下一条opcode30处理函数4C61C0的自然入口。入口第一条指令保持未执行，完整外层线程/调度、世界与后继资源仍待后续连接；不能称完整R3完成。

复现需全新输出：

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_keyboard --out analysis/fresh-retained-keyboard.json.gz
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_keyboard_verification analysis/fresh-retained-keyboard.json.gz --out analysis/fresh-retained-keyboard-proof.json
```


## 六组合运行与独立复核

initial、student9_waiting、fifth_class各接入76/77两个独立原版的采集流，共六组合。每组合先自然执行20次完整任务，从PC248的文字等待进入PC252/opcode51确认等待；再执行两次无输入对照，PC252/wait1保持。采集按下经原键盘规范化后，下一次完整任务将wait改为0，PC仍252；采集松开后，下一任务按原分派到4C61C0入口，opcode30/PC252，参数为0、原脚本指针+704、1，原返回地址4CEDA7。

每组合23次完整任务加一次下一任务前缀，三个原键盘处理区，共99段新源执行、677813条原指令。两个采集流有不同现场来源，但设备波形同为单空格按下/松开，不代表新增两种输入规则。回放按逻辑更新消费采集样本，不声称重现现场120ms墙钟时序。

新平台调用仅包含已声明的空IMM与空字符串查询。首次独立复核发现JSON数组与原CPU元组表示的比较差异，随后发现与冻结重放器的无参根元数据接口差异；已明确规范化/适配，原运行报告不改写，两份失败日志保留。最终独立证明 `analysis/school-retained-keyboard-proof-v3-20261022.json` 已通过，23项本单元正例/篡改/来源测试已通过，完成快照为 `analysis/school-retained-keyboard-targeted-tests-v1-20261022.json`；相邻回归与本单元合计192项测试均通过，原始日志为 `analysis/school-retained-keyboard-validation-v3-20261022.log`。


六组合的独立复核逐段验证所有新原指令/完整写入摘要、原调用参数及自然栈，最终118个完整内存映射与全部架构寄存器一致。每个逻辑案例的270段父前缀、1950759条原指令先由冻结重放器核对，再分别从同一不可变恢复状态建立两个独立客体分支；缓存只避免重复验证同一父状态，新分支的所有新指令均各自执行与复核。


## 集成验收和剩余边界

192项测试覆盖本单元、原生输入、场景、bootstrap、调度寿命、启动、保留渲染与完整任务。严格规格及归档后完整保全结果见 `analysis/school-retained-keyboard-acceptance-v1-20261022.json`；上一单元86份冻结输入产物和更早全链历史/存档/资源保持不变。本单元源指令/写入数量只说明此次实际执行量，不构成全游戏完成率。

当前已把原生采集数据接到保留任务的确认路径。下一实际边界是4C61C0肖像/图层指令体，以及保留状态与原49E540/4217C0外层线程、事件和世界更新的同一有效寿命连接；需继续核对资源所有权和实质交互转换。完整R3、R4–R6和Godot实现仍按总规格分别验收，2026-11-20目标不变。
