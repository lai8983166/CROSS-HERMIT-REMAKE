# 同一原生所有者接续：基类 worker 寿命已接通

2026-11-13，本轮离线准备从08:08:40 UTC开始，约31分钟后完成，少于60分钟预算。
随后只执行一次无UI原生预检，原生所有者实际寿命1.391秒，外层30秒期限未触发。
没有启动游戏、虚拟机、截图、桌面输入或显示设置操作，没有重试。

## 实际取得的连接

固定原镜像的8558条指令驱动71次原API。原执行器仍执行原指令；它把平台叶路由到
同一新鲜x86进程29136内的MAIN线程28080及真实CreateThread创建的worker8012。
reader线程18192只负责管道，不代替MAIN/worker执行平台叶。

1. 原5752D0建立MAIN的TLS/PTD和静态锁，原421540/421660/422290/4216C0构造、注册对象。
2. 原56E050实际请求CREATE_SUSPENDED；PTD116字节由原calloc和原写入产生。
   原ResumeThread恢复当前worker，56E110在该线程的OS TLS中安装其当前PTD，随后进入
   421F50及**由原基类构造器发布的422330回调**。没有替换虚表或手选回调。
3. 原worker置完成标志，Reset节点事件、Set管理器事件。MAIN原INFINITE等待返回0，
   沿原调度器读取退出码并完成节点移除与事件关闭。
4. 原575450保留“先释放PTD、再清TLS”的顺序。真实worker ExitThread(0)后，额外的
   所有者Wait/GetExitCodeThread确认真正终止，关闭原代码未关闭的worker句柄。
   MAIN的PTD/TLS、全部锁、事件和heap也沿声明的原清理函数释放。

最终原生清单中的heap、分配、锁、API句柄和TLS slot全为0；助手exit0，Job为空，
未强制终止。进程退出不替代上述各项资源回执。

## 证据边界

这是**同一所有者的原基类worker寿命预检**。原代码在Unicorn中执行，native入口为
WorkerDispatcher；完整57项是guest执行器状态。原入口、PTD、指针、线程分别有显式
投影，不声称物理CPU直接运行原56E110，也没有导入宿主特权状态或隐藏段缓存。
每线程API边界记录完整guest CPU、全映射内存摘要、累计指令/写摘要及原生回执。
PTD在其存活期间于相应lane同步并逐字读回；TLS在真实对应线程调用后读回。

MAIN等待请求早于worker的原SetEvent，SetEvent回执后收到wait返回。由于没有采集
进入Wait的额外通知或内核等待状态，不能据此断言MAIN此前已阻塞进入内核；本轮证明
的是实际等待调用、同owner完成事件及原返回路径。额外TLS读回会影响LastError，
因此恢复原叶LastError；基础设施内存操作也不污染原叶值。

父Python关闭两个初始子管道端时没有保存CloseHandle的BOOL，不把它称作逐句柄关闭
证明；外层Python已exit0。原生资源零、helper exit0和Job为空有单独回执。正式收集器
准入前仍需补强这一父端诊断，不能改写本轮冻结实现或回填缺失记录。

**场景首次协作让出、422360等待返回、453CB5结果消费、三次握手和独立完整重放均未完成。**
原基类422330为空回调，不能替代451670。现有场景前缀在第一次让出前需要真实GAME时钟、
文字队列及派生场景构造。没有填零GAME、跳过构造、修改结果或复用历史原生句柄。
正式任务仍2/8，三关及两例全新原生寿命、ABI、资源清理、独立重放标准不变。

## 接下来只推进原场景依赖

复用本轮所有者/线程路由结论，先离线闭合412E30及451170等原构造的必要平台叶、
GAME发布和真实父调用链，再评估首个原422360让出/唤醒。不能从453CB5新建根，不能
把基类回调成功计为首关通过。新采集需要新的明确范围和预算；本轮一次原生额度已用完。
不回到截图、VEH完整原机搬运或TCG环境扩建。

## 来源与复现

- [原生来源](../analysis/terminal-native-owner-preflight-v1-20261113.json.gz)
- [独立复核](../analysis/terminal-native-owner-independent-review-v1-20261113.json)
- [构建、预算与存储清单](../analysis/terminal-native-owner-closeout-v1-20261113.json)
- [平台叶协议](terminal_native_owner_protocol.md)
- 实现：`devtools/terminal_native_owner.cpp`、`devtools/terminal_native_owner_probe.py`。

本地可执行文件及精确构建清单保存在F盘
`.venv-audit/terminal-native-owner-build-v1-20261113/`。原生单次标记
`native-attempt.once`保留，禁止以换输出名重跑本次实例。`--prepare`只核对来源、构建
和初态；模拟平台返回的离线路径检查不是实际Windows证据。完整编译命令、编译器位置、
身份、实际来源大小/SHA及保留位置见收尾清单。没有复制旧全量历史或大型内存快照。
