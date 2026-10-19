# 原版两槽字体初始化完整返回

2026-10-19，独立、明确声明空缓存初态的启动实验已执行完整415F50，原返回值0，自然到达原413450调用者的4134E3，停在该指令执行前。原连续VM保持40E2D0 / PC224 / wait1、manager owner0，继承缓存缺失边界保持；Godot、原存档和旧检查点未改。

357 来源核对原第二轮三次GDI删除、4010D0 ret4、401810的8400字节VB与两套30调用状态块，以及415F50索引1→2、成功0、SEH恢复和ret。第二槽标志0跳过可选state7，与首槽一样执行两次完整状态序列；输出属于第二对象+60/+670/+674。

358 GDI助手使用独立第二轮计数、删除标志和对象字段。原DeleteObject(bitmap)、DeleteDC、DeleteObject(font)顺序保留，没有提前改选位图；辅助GdiFlush/GetObjectA确认位图已无法取得，单独记录GetObjectType而不靠它判断存活。中途停止则按真实当前选择恢复、补充释放。完整执行时两轮临时GDI对象都由原代码释放，助手的第二轮补充释放计数为0。

360 设备助手保留两张atlas、两个不同8400字节VB和四个不同实际token，第二轮状态只绑定第二张纹理。退出先结束任何中止的录制、删除两组token，再解除绑定、释放两个VB与两张atlas及此前缓存/引用/设备/工厂；两个VB/atlas最终Release均为0，四个DeleteStateBlock均成功。六项平台测试覆盖来源、真实资源与完整描述、删除寿命、外来/错序/重复/错纹理和中途录制/待删除位图的清理。

359 原清理：同一CPU从第二4017B6执行三次实际GDI删除、原栈检查/ret4和原调用者，停401810。4010D0返回0后，原4160EF把索引1载入EAX，因此401810入口EAX为1；它不是错误返回。验证器按第二槽的来源核对这一差异，不套用第一槽入口EAX0。

361 原VB：原401810创建独立第二VB，实际完整24字节描述为format100/type6/usage520/pool0/size8400/FVF0；指针写入第二对象+60，停40186E。第一个VB及其完整对象保持。

362 原状态：两次各30项原调用完成，两个新token写入第二对象+670/+674，且与第一组均不同；原401810返回0到416101。两个额外字体的VB创建共2次，状态调用共120次，四套块均真实录制。

363 完整返回：原九条回环前缀将索引1增为2，随后执行成功值0、FS0恢复0、寄存器/栈恢复、原栈检查和415F50 ret，精确到4134E3。ESP为原字体入口ESP+4，EBP/EBX/ESI/EDI恢复原调用者值；没有执行调用者的结果存储/判断、manager绑定或队列初始化。

本批每个尺寸案例都只构造一条完整连续轨迹，在同一CPU和两个助手寿命中记录cleanup/vertex/states/return四个节点；四份小型边界证据以SHA引用完整轨迹及其节点，不用过期句柄拼接独立重放。整条两案例轨迹另作一次新鲜重跑，边界仍分别测试和本地提交。

所有阶段核对完整1656字节第二对象、首对象、此前三块堆及五块堆的guard共60KiB、48KiB owner、原映像、原调用栈、接口映射、三个像素影子区域及旧DIB退休证据。第二DIB在原释放后，其影子也仅为快照。原游戏的完整字体析构链未执行，持久纹理/VB/token由拥有资源的助手在取证后清理，不冒充原析构或GPU绘制。

364 验收：19项本批来源/平台/四节点/连续重跑测试，加19项直接父链，共38项相关回归；30项严格规格检查。篡改覆盖原GDI寿命/ABI、第二槽入口EAX1、VB描述/不同身份、完整状态顺序/四个token、原返回/索引/SEH/父栈/寄存器、全对象/像素/退休证据与清理及剩余边界。16,291个既有文件、十项存档规则和九份私有VM检查点保持；工作SHA与Git blob逐项核对。八阶段分别本地提交、不push；364/364是已列任务数，不是全游戏完成率。

证据：[来源](../analysis/school-font-finish-source-v1-20261019.json)、[GDI平台](../analysis/school-font-finish-gdi-v1-20261019.json)、[设备平台](../analysis/school-font-finish-device-v1-20261019.json)、[完整连续轨迹](../analysis/school-font-finish-trajectory-v1-20261019.json)、[原清理边界](../analysis/school-font-finish-cleanup-v1-20261019.json)、[原VB边界](../analysis/school-font-finish-vertex-v1-20261019.json)、[原状态边界](../analysis/school-font-finish-states-v1-20261019.json)、[原完整返回边界](../analysis/school-font-finish-return-v1-20261019.json)、[回归](../analysis/school-font-finish-regression-20261019.log)、[严格规格](../analysis/school-font-finish-strict-20261019.log)、[保留检查](../analysis/school-font-finish-preservation-20261019.json)、[验收](../analysis/school-font-finish-acceptance-20261019.json)。

回归运行记录：首次38项运行中37项通过，旧父链上传重跑因连续六次实际地址映射碰撞被既有拥有边界规则拒绝，报1项错误；未修改父链代码、重试上限或碰撞规则。随后单独重跑同一测试，两个尺寸案例均通过，因此38项不同测试最终全部通过，共执行39项次。首次失败日志保留，单独重跑见[父链上传重跑](../analysis/school-font-finish-parent-upload-rerun-20261019.log)；本轮新完整连续轨迹及其新鲜重跑在首次运行中均已通过。

下一步沿原413450调用者继续，先处理4134E3成功判断和413500→40D970的manager/owner绑定、队列及后续启动。真实上游缓存/初始化与原连续VM衔接仍需独立证据，当前结果不等于已修复原VM或可操作战场。
