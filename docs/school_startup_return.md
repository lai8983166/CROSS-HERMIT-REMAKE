# 原版 gamma 调用与渲染启动函数完整返回

2026-10-19，独立、明确声明空缓存初态的原版启动链已完成最后的实际gamma接口调用，并执行原416CC0 ret4、413450成功值0及ret20，返回既有实验根调用的22000000停点。两个尺寸案例均使用同一原CPU和同一对实际拥有资源的助手，从原owner构造、设备/缓存/字体、manager与队列初始化一直运行到自然返回。原连续VM仍为40E2D0 / PC224 / wait1、manager owner0，没有接入本次独立对象。

370 来源：完整核对416CFA call [vtable+48h]、两次栈检查、416D14 ret4和413546 xor eax,eax、413558 ret14h。gamma接口返回void，EAX没有API状态含义；本轮仅记录调用后的实际寄存器位值，启动成功0来自后续原xor指令。接口语义参考[Microsoft的IDirect3DDevice8::SetGammaRamp说明](https://learn.microsoft.com/en-sg/previous-versions/windows/embedded/ms889716(v=msdn.10))，它也说明了窗口模式可能应用gamma及不支持时不返回错误的边界。

371 平台：新设备助手保持原create_device身份及全部旧操作不变，在两组字体状态完成后才允许一次gamma_prepare检查。它读取实际设备的vtable+72；该检查和审计映射在原416CFA之前单独记录，不执行原指令，也不改CPU、栈或其他内存。随后只接受实际device、flags1及完整1536字节原identity ramp。外来对象、早调用、错误flags/数据与重复调用均拒绝。

拥有进程中的25字节x86转发代码按原stdcall顺序传递三个参数，调用真实设备方法，原样返回观察到的EAX位值；转发代码逐字节核对并及时释放。它不写入游戏映像、IAT或原函数，也不提供虚构HRESULT。实际设备GetGammaRamp与桌面GetDeviceGammaRamp的调用前后完整缓冲分别记录为辅助检查；helper清理先恢复设备和桌面gamma，再按既有次序释放两组token、VB、纹理、引用、设备和隐藏窗口，DC取得/释放逐项平衡。

372 原gamma子函数：在同一CPU中执行原416CFA，通过实际拥有设备调用后回到416CFD，按真实stdcall清理12字节参数。继续两次原栈检查及原416D14 ret4，自然到413546，ESP恢复到字体启动调用者的TOP−88。该节点的EAX保留实际观察位值，本轮两案例均为0；验证器不将该值解释为接口成功，也不据此推断显示器是否应用了gamma。

373 完整原启动返回：原413546明确置EAX0，恢复EDI/ESI/EBX和0x48字节局部栈，执行原栈检查及ret20。最终ESP为TOP+24，EBP11223344、EBX55667788、ESI88776655、EDI44332211均恢复实验根调用的值，EFLAGS70；目标22000000的指令未执行。gamma阶段16条、启动后缀12条原指令及各返回位置/栈深/寄存器均独立核对，没有合成原游戏函数返回。

验证器使用新助手真实源码/可执行文件/编译器SHA与x86机器类型，逐一调用未修改的旧来源、ABI和全内存验证函数，再验证原manager/队列/gamma准备及新增节点。它不把新助手标记为旧build，也不重写旧trace。完整48KiB owner、原映像/分配计数/SEH0、晚期接口映射、五块原堆及保护区、32KiB层表/1MiB命令区及保护区、三个像素影子和退休DIB证据保持。两份小型边界证据以SHA引用同一完整轨迹和实际节点，均不能用于恢复已清理的句柄。

374 验收包括13项本批来源/平台/原返回/篡改/新鲜两案例重跑测试，加11项直接父链回归，共24项；30项严格规格检查。16,342个既有文件、十项存档规则和九份私有VM检查点保持；工作SHA与Git blob逐项验证。五阶段分别本地提交，未push；374/374是已列任务数，不代表全游戏逆向完成率。

证据：[来源](../analysis/school-startup-return-source-v1-20261019.json)、[实际设备平台](../analysis/school-startup-return-device-v1-20261019.json)、[完整连续轨迹](../analysis/school-startup-return-trajectory-v1-20261019.json)、[原gamma返回](../analysis/school-startup-return-gamma-v1-20261019.json)、[原启动返回](../analysis/school-startup-return-return-v1-20261019.json)、[验证](../analysis/school-startup-return-verification-20261019.log)、[回归](../analysis/school-startup-return-regression-20261019.log)、[严格规格](../analysis/school-startup-return-strict-20261019.log)、[保留检查](../analysis/school-startup-return-preservation-20261019.json)、[验收](../analysis/school-startup-return-acceptance-20261019.json)。

下一步的两个具体原调用点已核对机器码：412C70内的412D01与450570内的45067A均call413450。450570路径还先传递data目录值并调用4135D0、413630，在启动成功后调用413560；其传入条件也与本次明确声明的窗口化实验不同。这些上游函数仍未执行，需继续核对其实际调用条件、继承缓存生命周期和原外层调度，再建立与保留VM的真实衔接。

当前完整返回的是明确声明初态的独立413450调用；真实上游调用者正文、原VM/任务的正常返回、完整外层帧、GPU绘制/Present、可操作战场和后续AI/事件/结算仍待继续。Godot和原版存档未改；结束时设备/桌面gamma与调用前一致，所有拥有资源已释放。
