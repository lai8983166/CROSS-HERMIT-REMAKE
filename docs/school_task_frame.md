# 原输入请求与完整任务帧（R3单元）

当前change：`connect-original-task-frame`。R3总目标仍未完成。本单元将R2直接VM根替换为完整任务更新，并使用实际系统IMM查询，不代表线程外层/物理键鼠/完整世界交互已经完成。

## 断言来源校正

R2在425F12→424F80停住时，ECX中的FFFFFFFF来自对**输入+630h请求标志字节FF的有符号扩展**。源425ED0在登记下一次IME请求前要求该标志为0；它不是输入设备索引。历史R2报告和旧交接中的“输入索引−1/未初始化”解释不准确，原始报告字节保留，本文件与当前总规格明确校正。

原49E540在49E5A4先调用425DE0(MAIN+180h)，然后进行队列清空和任务调度。425DE0读取+630h，负请求走425E60(0)→425C70→56CD4A→原IAT5920EC的IMM32.ImmGetOpenStatus；当前捕获上下文INPUT+8为0。真实API返回关闭后，原425E3F自行把请求标志清为0。完整454CF0随后通过457830调用425ED0(0)，登记下一帧请求FF；这一对请求/消化需要每帧交替，不能跳过重置后声称需要清全局或跳过断言。

本机真实IMM32路径/SHA、宿主64位/客体32位、实际BOOL和last-error均记录。当前上下文为0、没有传递非零跨进程句柄；平台边界拒绝未拥有非零上下文，且不会查询或更改用户正在使用的输入法上下文。原输入对象为1080180h，与R2渲染管理器所在1000000h根的内嵌输入成员区不能混为一处。

## 实施与复核

复用R2完整原初始化、逻辑恢复和有效设备寿命。每帧声明425DE0输入请求重置、原队列重置和完整454CF0任务根，所有原函数执行原机器码；没有手写+630h、PC、wait或代用调试返回。原多线程4217C0调度和49E540仍另计，不能把独立驱动根写成已执行原外层。

来源与实际API检查：

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_school_task_frame
```

后续在三个保留场景中核对完整任务、VM、文字生成与实际绘制，自然返回和源写入须独立重放；本单元验收前R3保持进行中。

## 已接通的完整任务

首例initial已完成67次完整454CF0更新，每次由原425DE0消化FF请求至0，原任务再写FF；任务phase2、自然EAX0返回和原454EC1均核对。每次任务实际执行457830→425ED0/425A10，进入4CE8F0并执行4563D0等辅助门控，再自然返回。原425A50在捕获设备为空时走输入缓冲清理分支，没有把这些操作称为物理键鼠采样。

67帧使面板从PC224推进至文字激活232、第一行238、第二行244、等待248。274段执行中271个新根明确声明，**0个独立4CE8F0根**。独立CPU复核逐段重放2004237条原指令，完整写入、自然CPU/栈返回、实际IMM输出、原图形参数及纹理像素一致。原完整任务增量没有用原VM返回值或调试响应代替。

两张文字纹理、两次真实DrawIndexedPrimitiveUP、矩形与Present正常执行，真实帧缓冲SHA仍为`8bc242da1c4b3b2bd1db8d22cdc2f91cf11691a40f952e42353f3f197eb54613`。源文字透明/白色混合像素以及原初始化、资源释放、两个原生助手退出码0均通过R2独立模型。复核代码通过私有Python函数globals副本复用冻结R2驱动/验证器，替换的是审计驱动类和实际新API的回放类，未修改共享模块、历史文件或任何原游戏函数。

复现（使用新的证据路径）：

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_task_frame --case initial --out analysis/new-task-report.json.gz --image analysis/new-task-frame.png
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_task_frame_verification analysis/new-task-report.json.gz --out analysis/new-task-proof.json
```

## 下一实际边界

本单元完整任务来源成立，但原49E540与4217C0未执行；4217C0→421850含原事件/线程等待和启动分支，需建立同一有效寿命的OS同步对象、线程/任务回调协议后接入。完整任务当前也没有访问46B470世界更新根，不能凭执行辅助4563D0就称世界帧推进。下一R3单元应连接原调度/实际输入/世界入口并跨越实质性交互转换；静态精灵GPU纹理与ACP936/Big5兼容问题仍保留。
