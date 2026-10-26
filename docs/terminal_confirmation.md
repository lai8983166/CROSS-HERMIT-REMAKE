# 原终局确认与下一句字体交接

2026-10-26，`connect-terminal-confirmation-handoff`。接续PC118/wait1，在同一当前GYBC、姓名、肖像、首句纹理及CRT/GDI寿命内，把原生采集raw键盘接到原确认查询，完整执行27和层7面板等待，经43及下一17自然停PC142的CreateFontA首指令前。

## 当前对象与采集来源

原4CCFE6从7A49FC取得当前MAIN，4CCFEC加10B8，4CCFF2调用4128F0。当前键盘为12A010B8，使用scan39h/mode0；历史保留案例的10010B8地址不适用于本对象。

两个新战斗实例分别绑定固定验收的76/77采集流。76使用`school-native-dialogue-held-76-v4-20261022.json.gz`样本0/1/10，77使用`school-native-dialogue-held-77-v2-20261022.json.gz`样本0/2/10；原验收、manifest与独立原生交接证明的SHA均由冻结工具核对。仅把样本中对象+12的256 raw device字节交给当前键盘；片段根栈、EBP/ESP/EFLAGS是明确方法输入。原4113D5–4116A4产生全部规范化、按下/松开和计数组，整A00字节用独立模型核对，不由主机赋派生键位。

这是先前系统输入的采集回放。本轮没有新的OS键盘/窗口操作，没有执行原DirectInput设备轮询或完整外层线程；无需解锁。当前键盘域沿用声明的MAIN内存并扩展原写守卫，原stack-only主机put算法保持。

## 原任务与面板

idle经原片段后，两次完整任务保持118/wait1。press经原片段后，完整454CF0只解除等待到118/wait0；release经原片段清按住位，下一完整任务才执行27。按下与27分属不同任务。

27的原编码是20000004/2fffffff/2fffffff；原type2 literal返回4/0fffffff/0fffffff。模板4的38字节来自624520+4×38，其类型0在4CC1C0直接跳4CC38E，配置层7而不加载姓名/肖像。原4CC600/4CC0F0/4CC7D0/4CC810全部执行，面板经4CA600/4CBDB0/407870复用当前资源组20/索引0；旧层5肖像同时查询组32/索引0，组号均为十进制。查询包、当前所有者和原入队记录保留；没有新文件、字体或纹理API。

原显示时长45使用严格递增/终止边界，27任务的首次更新为counter1/status3。后续到counter45仍status3，下一更新归counter0/status2，再下一完整任务才查询就绪并清VM等待。原判断将WORD计数零扩展后使用有符号jle；不替换成主机计数规则。实际46次后续完整任务到134/wait0，再由43选择层7到142/wait0。142的17选原text1，停其字体API入口，实际高度/宽度为0×0、字重400及原ANSI face；模板字号24/行距12在另两个成员，不代用字体API参数。原字体函数、文字处理器、VM及454CF0四层祖先、完整128KiB栈/57CPU/SEH保留；新字体第一条指令未执行。

各例新增52次任务进入，其中51次完整返回、最后一次部分任务；加上前驱累计260次完整任务和1次pending。另有三次明确键盘片段，不增加独立VM/27/面板根。前向任务只用原队列表头/arena复位、原输入复位和完整454CF0。

## 验证和资源寿命

每段记录全部57CPU、原指令/写入数量与累计摘要、平台栈参数及原查询观察。新增各帧重新读取所有拥有区域，保留每区域SHA、完整CPU和4096组队列表头/arena；键盘、确认、27返回、就绪和字体关键边界另保留全hex内存。独立Unicorn从初始全内存恢复，逐条原机器码重放，并在每帧重新读取全域比较；不使用源SHA字段自证。

末端实际整表面读回四张旧纹理，原始GPU协议新增四次只读观察。冻结前驱验证兼容视图剔除观察、恢复前驱原边界；补充析构的旧边界CPU由另一次原机器码执行推导，未改原始来源。原始142字体边界的实际补充析构另完整重放核对，包含原CPU、原指令/写入、记录和记账；不能把投影当作真实晚边界清理，也不把无法推导的SHA作旧累计证据。

字体边界冻结后，原首句纹理、肖像、姓名、GYBC、队列及CRT锁堆补充清理正常结束，当前GDI测量DC另关闭。不计当前悬挂任务自然返回或游戏退出；结束后的资源不能复用来继续此快照。

来源v1生成后，运行期采集入口再加严为当前分支、三次顺序及整份capture字典精确匹配，且在任何内存访问前拒绝伪造/第四次绑定。v1原采集本已匹配同一固定流；最终新资源重放验证加严后的实现，不把后加守卫说成v1生成时已运行。开发期smoke-v1至v5的验证器诊断原样保留，涉及复用字段、两资源组区别及全hex/逐域SHA核对；smoke-v6两分支原重放与前驱复核均通过。

## 复现与后续

| 分支 | 新增原指令 | 新增原写入 | 累计原指令 | 累计原写入 | 最终拥有区域 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 中立首帧胜利 | 1,990,204 | 1,163,952 | 7,636,225 | 5,027,203 | 295 |
| 战斗前超时 | 1,990,644 | 1,164,022 | 7,947,528 | 5,158,944 | 296 |

来源为`analysis/terminal-confirmation-source-v1-20261026.json.gz`，355374140字节，SHA256为`b2a22addd13640b2a89f766b4703d2ede260d0279e7c4384124a36455e38a9c3`。39项专项涵盖绑定/整A00模型、根与停止地址、逐帧全域/CPU/队列/原摘要、查询和平台输出、四原生读回及实际晚边界补充析构的篡改拒绝；355项相关历史回归另通过，共394项。

最终`analysis/terminal-confirmation-proof-v1-20261026.json`在两例分别重新建立当前CRT/GDI/GPU资源，全状态比较通过；`analysis/terminal-confirmation-main-review-v2-20261026.json`另核对原栈、方法输入与四个稳定实现SHA。`analysis/terminal-confirmation-preservation-v1-20261026.json`固定前驱52项及其验收本体，递归原资产/存档/检查点保全通过。验证子Agent中途模型容量失败，实际验证进程继续完成；主Agent观察实际Python退出码0，随后启动包装进程的退出码不可得，观察器原诊断及如实复核分别保存在process-run-v1和process-review-v2。它不计作游戏或原生助手失败。

归档前/后严格规格分别32/31项通过、0项失败；最终提交及全部证据的工作区/index/HEAD字节比较见`analysis/terminal-confirmation-acceptance-v1-20261026.json`。最终验收本体单独提交且不把自身列入其manifest，避免循环hash。

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.terminal_confirmation_emulation --out analysis/terminal-confirmation-source-NEW.json.gz
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.terminal_confirmation_verification --report analysis/terminal-confirmation-source-NEW.json.gz --out analysis/terminal-confirmation-proof-NEW.json
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_terminal_confirmation
```

继承的冷CRT六区335字节、当前设备/绘制门/几何、测量DC和有界队列仍是方法输入；精确重放继续使用采集的前缀时钟。原ANSI空白/乱码未修，实际draw/Present、下一字体/字形/纹理、完整终局、原加载/外层线程同寿命、任务退出/奖励及学校交接继续待验。Godot未改，R3/R4/R5/R6保持未完成，2026-11-20目标不变。
