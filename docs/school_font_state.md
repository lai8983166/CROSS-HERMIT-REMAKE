# 原版首个额外字体清理与设备状态

2026-10-19，继续明确声明空缓存初态的独立初始化链。原连续VM保持40E2D0/PC224/wait1、owner0，旧缓存缺失边界保持。

332来源：4017B6依序DeleteObject(bitmap)、DeleteDC、DeleteObject(font)，4010D0原ret4返回，415F50原调用者进入401810。后者创建8400字节/usage520/FVF0/pool0顶点缓冲，执行两次完全相同的30调用状态块录制：Begin、纹理绑定、14个render state、13个texture-stage state、End；标志1跳过可选state7分支。实际VB指针写+60，两个token写+670/+674，完整函数返回416101。四项来源测试核对所有原虚表偏移/推参、两套完整调用序列和1656字节对象投影。

333实际GDI平台：保留原版三次调用顺序，不预先改选位图。此机器上的DeleteObject和DeleteDC均返回1；仅凭GetObjectType仍返回7不足以证明对象存活，辅助GdiFlush/GetObjectA检查已无法取得位图对象。全部三次原调用之后，额外字体/位图/DC均由原序列释放，助手只清理此前共享缓存等资源。辅助flush/对象查询明确不是原代码请求。

调查历史保持：v1/v2把类型值当存活检查导致错误拒绝；v3用GetObjectA正确验证完整原清理，但中止后的补充清理仍假设旧选择句柄不变；v4补充检查时机仍不够。v5在已有DeleteObject请求时核对实际恢复后的当前位图，而非比较已删除对象的旧句柄，完整及中途停止两条清理均通过。旧源码/构建/失败日志和报告独立保留。三项平台测试覆盖构建来源、真实三次调用/对象寿命、越序/外来对象及待删除位图的补充清理。

见[来源](../analysis/school-font-state-source-v1-20261019.json)、[实际GDI平台v5](../analysis/school-font-state-gdi-v5-20261019.json)。
