# Windows v8 首次等待 CR2 连续账本独立复核

2026-11-11；accepted=false。只读tcg-wait-native-v8保留JSON并直接编写独立序号/值链检查，未调用terminal_cr2_ledger_verify.verify，未启动VM、未修改任何运行来源。范围为自有WOW64 wait fixture第一次CALL→RET窗口，不是原游戏或完整逆向验收。

## 来源身份

以下路径相对 .venv-audit/native-worker/tcg-wait-native-v8；摘要针对本次读取的未压缩原JSON字节。后续gzip只能作为无损存储替换，仍须核对解压后的这些身份。

| 文件 | bytes | SHA-256 |
|---|---:|---|
| observation.json | 347342 | ce6808131362295bf9fd9c97e3f0aee1198f21e5e2358904bab50e3467e42269 |
| result-exit-response.json | 36364 | 161f49de1bc057f4ebe343d621c971eb58722833b928bdab644801c2b79ef19b |
| orchestration.json | 219 | cb86fa550e5d79da062cb01311257521e43b20da2e3783b6847f9324de5d6b5a |
| report.json | 2662 | 9197198079e789e624869c65de3a9acffd8960ca5404a3a6b549607256ef64d9 |

## 不依赖消费器的事件链重算

直接解析events_json，并独立验证原字节长度、SHA、记录数、窗口号、每CPU序号、逐条old与累积值、PF的new=fault_address/vector14、source=0、stage2/intercepted=false。按记录顺序累积，两CPU独立维护值和计数，最后与END对应CPU值/计数精确比较。未按fixture CR3过滤，也未丢弃其它地址空间事件。

ARM窗口1，事件空数组、count0；END无poison/overflow，start对象与ARM完全相等。ARM的两个嵌入完整state分别与call-0.states精确相等，END的两个state与ret-0.states精确相等。每CPU计数从0开始，结果如下：

| CPU | CALL CR2 | 事件数 / END counter | RET CR2 |
|---|---|---:|---|
| 0 | 00000000733a0920 | 56 | 0000000000c07008 |
| 1 | 00007ffff782c2b8 | 5 | fffff8033ccf4000 |

共61条，全为PF；连续序号CPU0=1..56、CPU1=1..5，无断点/重复。events_json 20,005 bytes，独立SHA-256=719699e24e8b655b8ba1f804e01fdebfc168de8bd42a04d42b1deaccf6c0ae52，匹配END。实际账本窗口elapsed_ns=2,018,408,000（约2.018秒），没有超过65,536条/16MiB/60秒预算；37.563166207秒是整个observer时长，不能写成账本活动窗口时长。

事件覆盖5个CR3：0x10db9b000、0x120d99000、0x1284fd000、0x12d1ef000、0x2aaf1000。CPL0共8条、CPL3共53条；访问read32/write19/execute10。这支持记录未只限于一个WOW64地址空间，但本复核没有逐条解码Windows故障指令或验证所有页表故障原因；不能把链及认证后端记录替代完整原因语义证明。

QMP顺序明确ARM在CALL完整重复状态查询后，END在RET完整重复状态查询后；x-query-tcg-checkpoint位于END之后，不在账本活动窗口内。三个停点的repeat_equal均true。观察器声明host_guest_state_writes=0、errors=[]，本复核未将该声明单独视为对所有外部控制接口的证明。

## CALL、RET和post差异范围

三次CPU0 TEB client ID原字节均a4050000e00a0000，解码pid=1444、tid=2784，与ready及持久launch PID匹配。CPU0 CALL EIP=0x0434006f，RET EIP=0x77c23bfc，post EIP=0x04340071。

CPU0 RET→post整个已导出state逐字段比较，仅EIP及gpr[4]/RSP变化：RSP=0xefedc4→0xefedd4，增加16；RET栈顶原字节71003404为返回地址0x04340071。nt_wait原字节在偏移12为c20c00（ret 0xc），与弹出返回地址4字节加12字节参数完全相符。此段所有其它导出字段精确相等，包含CR2、R9、XMM、hflags。与此同时CPU1的GPR、EIP、EFLAGS发生变化，故“仅EIP/RSP变化”只限CPU0，不能写作全VM无其它状态变化。

CPU0 CALL→RET实际差异为：GPR索引0/1/2/4/9、EIP、CR2以及XMM0..5；其它导出字段精确相等。具体R9=0x77c23c9c→0x77c23bfc，XMM0..5从初始化模式变为全0。CR2已由本窗口连续事件链闭合；R9及XMM清零不能仅凭此前不同boot/不同来源的WOW64静态路径或逐条轨迹自动放行。本来源没有相同身份的六条PXOR/R9载入逐指令链，完整raw64调用转换仍未被本报告证明。RAX/RCX/RDX/RSP/EIP的调用/返回语义也不因本次CR2成功就免除原有严格验证。

ready代码、三停点code_hex及helper code_after完全相等；ready.nt_wait_before、三停点nt_wait及helper nt_wait_before/after完全相等。这里是本轮原字节一致性，没有跨boot地址映射推断。

## 持久回执、go与退出清理

prepare-response和launch-response原请求均55秒超时，remote_completion=unknown、host job active=0。随后boot-auth与launch-auth通过新只读命令取得持久回执：prepared=true/本轮目录/正确UUID，launched=true/pid1444/正确UUID。它们证明对应持久结果存在，不证明原未知Receive的shell/command已关闭。新只读回执的command_and_shell_closed=true只属于新读取命令。

go-response同样35秒超时、remote_completion=unknown；orchestration.go_receipt_confirmed=false保持正确。之后真实CALL/RET/post轨迹以及最终helper go_received=true证明fixture实际收到go，但不追改原go WinRM响应为“已确认”，也不推断未知Receive原shell已清理。

result-exit-response独立完整：remote_completion=observed、errors=[]、host_job_active_after=0、host_exit_code=0、response.ok=true、该结果读取command_and_shell_closed=true。helper error=null、cleanup_errors=[]、peer_error=null、counter_errors=[null,null]，workers_stopped/peer_completed/main_affinity_restored/handles_closed/buffers_released/watchdog_disarmed/fixture_completed全true，counter_native_entered及counter_affinity_restored均[true,true]；returns=[0,0,0,258]，signals=3。helper.ready与observer.ready完全相等。

result.ps1在读取result.json后查询ready.pid是否仍存在，将process_exited=true加入结果；这与报告中的fixture完成字段及VM最后process_exited=true一致。清理字段来自自有helper的报告，并非本审查重新枚举了全部客体句柄。后续三轮helper返回不等于它们也被本次三停点/61条事件窗口完整观测。

VM report errors=[]、正常quit回复、process_exited=true，总时长424.768229369秒；编排415.25秒、errors=[]。这些不证明旧未知WinRM shell在退出前曾逐一正常关闭，不能混同宿主Job清空、helper资源清理及VM寿命结束三种不同范围。

## 独立结论

该第一次等待的双CPU CR2事件连续性、摘要、完整停点绑定及CPU0真实ret 0xc返回局部证据复核通过。原有R9/XMM等完整状态转换仍需同来源原因链/严格消费；本次不放宽ABI、累计摘要、原生所有权、完整重放或原游戏验收。accepted和original_game均维持false。仅新增本小报告，无VM、原始采集、备份或来源改动。
