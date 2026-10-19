# 两条原版上游工厂的分配、构造与下一调用

2026-10-19，已从原412C70、450570工厂入口分别执行实际分配和完整owner构造，不再只从独立413450入口开始。四个案例（两条路径各640×480/A5、1024×768/CC）各沿同一CPU和拥有资源的助手寿命，记录allocation、constructor、admission三个节点。窗口支路到达原413450第一条指令前；游戏支路到达原4500B0第一条指令前。工厂的输出参数仍为原声明的DEADBEEF，没有发布成功owner，也没有接入保留VM。

375 来源确认两工厂均调用428A40(BA20h)，再调用412E30。窗口支路随后传入window/1/1/width/height进入413450；450570在其0/1启动参数之前，还先调用4500B0、4135D0和413630，启动成功后还有413560。继续查看原代码可见，4135D0进入DirectMusic音频初始化，413630进入两组COM设备初始化；这些正文本轮均未执行，不假定它们成功。

376 原分配：原工厂设置真实父栈SEH，执行428A40的调试CRT包装，只在56E810接受一次明确声明的47,648字节分配响应，初始CD、block type1、源文件地址和行号141均核对。原包装器自行增加分配计数，然后原调用到达412E30。窗口支路子函数入口ESP为TOP−116，游戏支路为TOP−120，未把此前独立构造结果塞入新工厂。

377 完整原构造：在各自父栈中执行412E30的全部42次原函数调用，包括两元素数组、完整清零与继承计时器分支；实际GetDC、QueryPerformanceCounter和QueryPerformanceFrequency响应由未修改的x86助手提供。原构造自然返回412CC2或4505C7，EAX为该次分配owner，恢复父EBP及保存寄存器。每例61,547条原指令观察的控制流连续性、全部函数嵌套/栈ABI及原返回均核对。此时外层工厂SEH仍为TOP−16，没有错误地要求它恢复为0。

378 下一调用：窗口支路继续原非空判断和五参数准备，原412D01 call413450，停在子函数入口；游戏支路执行原4505FB读取7A4A00，传入原data字面量后，经450601 call4500B0，停在其入口，尚未解引用缺失主对象。窗口值和游戏工厂this只是本次明确声明的标量输入；本轮没有创建窗口、调用D3D、初始化音频/COM或播放音频。助手退出只释放本轮实际取得的屏幕DC，旧设备/字体助手均未改变。

重要边界已用完整原映像核对：这两段真实工厂前缀都没有清空缓存头80A398，仍为04D61D08；主对象全局7A4A00仍为04D60B38。两块地址既未映射到本次实验，也不在SHA钉住的保留VM检查点中。因此，原工厂前缀本身不能消除此前的缓存缺失，更不能替代游戏主对象或跳过其初始化。原连续VM仍为40E2D0 / PC224 / wait1、manager owner0。

完整核对48KiB owner视图、实际BA20h分配外的1504字节及前后4KiB保护区、三页输出参数区域及保护字节、原映像/计数/继承指针、SEH/栈保护区和所有外部接口页。独立源码遍历推导allocation/admission的精确指令路径；构造复用未修改的通用原指令/栈帧校验，另核对42调用序列、完整独立字节投影和实际平台协议。初始CD浮点字段、未初始化填充等均按原字节处理。

首轮v1的原执行和内存通过核对，但构造返回后停在父函数中，此时栈顶是保存的EDI；初版将其标注为return_va。该字段已修正为stack_top_dword并生成v2，v1保留为被拒绝的边界记录，测试确保不能通过现行验收。没有覆盖旧报告或删除历史内容。

379 验收：11项本批来源/三节点/篡改/四案例新鲜重跑测试，加10项直接相关的既有owner来源、平台和构造回归，共21项；30项严格规格检查。16,367个既有文件、十项存档规则和九份私有VM检查点保持。五阶段分别本地提交，工作SHA与Git blob逐项核对，未push。379/379只是已列任务数；两工厂均尚未返回成功。

证据：[来源](../analysis/school-upstream-factory-source-v1-20261019.json)、[完整连续轨迹v2](../analysis/school-upstream-factory-trajectory-v2-20261019.json)、[原分配](../analysis/school-upstream-factory-allocation-v1-20261019.json)、[父栈内原构造](../analysis/school-upstream-factory-constructor-v1-20261019.json)、[不同下一调用](../analysis/school-upstream-factory-admission-v1-20261019.json)、[v1拒绝原因](../analysis/school-upstream-factory-v1-refusal-20261019.json)、[回归](../analysis/school-upstream-factory-regression-20261019.log)、[严格规格](../analysis/school-upstream-factory-strict-20261019.log)、[保留检查](../analysis/school-upstream-factory-preservation-20261019.json)、[验收](../analysis/school-upstream-factory-acceptance-20261019.json)。

下一项具体前置条件也已定位并核对原字节：WinMain路径49DD70在49DDCE请求1110h字节，经49DDD3调用428A40、49DDE7调用44FBB0，最后49DE01才把构造结果发布到7A4A00。见[下一前置条件来源](../analysis/school-upstream-factory-next-source-v1-20261019.json)。下一步应继续这段主对象的原分配/构造与目录状态，随后处理音频/COM和实际渲染启动条件。该段本轮只做来源核对，没有执行或修补全局指针。缓存生命周期、完整工厂成功交接、外层调度与保留VM衔接仍待推进；Godot、原版存档及保留VM未改。
