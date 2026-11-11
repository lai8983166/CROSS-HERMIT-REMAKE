# CR2 微客体与消费者独立复核

2026-11-11。仅只读现有来源、运行纯内存消费器及objdump；未启动VM，未修改已执行代码或来源。accepted=false，windows_admitted=false，full_state_verified=false。

## 原字节与端点等价

四份guest.elf均8192 bytes，SHA-256 f5a6d27403da8866522992a5ca62f1d8e9ff7be2b14479ce4ee1e39872786463。来源目录均在 .venv-audit/native-worker 下。分别直接比较baseline-v1与ledger-v1、normal-baseline-v1与normal-ledger-v1的start/end/fault_handler整个双CPU导出JSON、fault_frame、fault_count、exit_code、expected，全部精确相等；不是掩码比较，也没有排除CR2/EIP/hflags等字段。

normal命令实际为tcg,thread=single，没有one-insn-per-tb选项；因此本次等价检查没有仅依赖逐指令TB。单指令组为tcg,thread=single,one-insn-per-tb=on。两组均2CPU/4G、无磁盘、无Windows。CPU1始末CR2为0且0条事件。

报告SHA-256：

| 目录 | report.json SHA-256 |
|---|---|
| tcg-cr2-baseline-v1 | 2be5dcaf076fa3e86bf84f0dfed460951f9945a1f18257d1ef79808ed621f564 |
| tcg-cr2-ledger-v1 | 70f98fdcf861ffa105da7a36b56eafba4d82e25ffb2450ae3c685aef18eb9961 |
| tcg-cr2-normal-baseline-v1 | f2d7c749ae4fecb03a6d2f6a62383fee07824774174e5a7f480c23272fa38ef4 |
| tcg-cr2-normal-ledger-v1 | ceed0066ba9c33e90d1ad0a8e5c15e837205f2595364a8b708b43c88148f3a95 |

## 事件原因及精确PC

独立objdump对保留ELF原字节反汇编，未调用microguest.image生成替代字节：

| PC | 原字节 | 实际指令 |
|---|---|---|
| 0x100300 | b878563412 | mov eax,0x12345678 |
| 0x100305 | 0f22d0 | mov cr2,eax |
| 0x100308 | 0f22d0 | mov cr2,eax |
| 0x10030b | a100004000 | mov eax,[0x400000] |

两组事件均为CPU0 seq1/2/3、window1，PC与上表对应。第一MOV old=0/new=0x12345678；第二MOV old=new=0x12345678仍有独立事件；PF old=0x12345678/new=fault_address=0x400000。三事件CR3=0x105000、CS=8、CPL=0。PF vector14、error0、access_type0、mmu_idx5，非stage2、非intercept。

独立读取实际fault_frame=000000000b0310000800000086000100：error=0，保存EIP=0x10030b，CS=8。这支持PF记录的是故障指令PC而非helper宿主GETPC或handler入口。原微客体handler地址0x100400，实际fault_handler停点及帧与v12相等。两组均一次PF、自然退出码33、输出C。结论仅覆盖这两条MOV和一个32位监督态读PF，不外推到所有异常升级、执行/写PF、SMM、双CPU同时写或Windows路径。

## 实际拒绝来源

memory-reject-v1：GDB内存写回复OK，但END为gdb-memory-write poison，后续ARM回复CR2 active or poisoned，进程已退出；这是窗口拒绝，并不声称写动作未发生。report SHA-256 da50443e51a047d77bb3f2eb5954b23bd9184256f0c5ee64867520b934c65562。

reset-reject-v2：实际reset后END为reset-init poison，后续ARM拒绝，进程已退出。report SHA-256 3973ade66a064d74c86a5594de23987a642fa409a2ec1d2accf1932eba16cecf。

reset-reject-v1保持失败：ConnectionResetError、无END/重ARM证据、rejection_passed=false。其-no-reboot配置引起退出不能算poison通过。report SHA-256 44e331e06388f50bc3c5a8397a57fa8d4ab9610aa949e1de4575021802960130。

本审查不把这两种拒绝扩展为全部unsupported writer、overflow或60秒timeout实际运行验证。

## 冻结消费者审查

devtools/terminal_cr2_ledger_verify.py SHA-256 060c498aa3ac6455dd53e03391db0d0610c1602bde8281c74feed84bdd690992。本次只导入执行，不编辑。对两份真实ledger独立重跑均cr2_chain_verified=true、event_count=3，accepted/full_state_verified/windows_admitted保持false。

以normal来源为基线，纯内存篡改并在需要时重算JSON字节数/摘要：删尾、重排、重复事件、混CPU、序号偏移、old错误、vmrun伪原因、删去同值写、poison=true、elapsed_ns恰60秒、CPU=False、JSON重复键，共12类全部拒绝。实际拒绝发生在counter/sequence/chain/metadata/deadline/duplicate-key校验，不依赖未更新摘要侥幸失败。

消费者本身仅检查PC/CR3/CS合法编码和事件链；把首个MOV PC改为0x109999并重算摘要后仍cr2_chain_verified=true。因此它不是独立的opcode/操作数或故障PC验证器。当前命名和accepted=false符合该范围；不能把cr2_chain_verified泛称完整原因认证。上述微客体PC结论来自本节之外的原字节与实际异常帧交叉核对。后续Windows事件必须保留经过身份认证的来源/后端以及所需原因语义检查，不能用链自洽替代全部原调用验证。

## 结论和新增证据

normal与single微客体局部等价、三条实际事件及memory/reset-v2拒绝复核通过，旧reset-v1失败不追改。此子任务仅新增本报告，无原始采集、缓存、备份或VM变更；不扩大原游戏/Windows/完整逆向验收。

## overflow-v2 与缓冲QMP追加审查

同日仅只读检查，Windows v5正在运行，未改动任何运行代码/来源。独立运行 devtools.tests.test_terminal_cr2_ledger，普通Python及-O各2个测试方法、20类反例全部通过（各0.042秒）；PYTHONDONTWRITEBYTECODE=1及-B，未写缓存。

terminal_cr2_qmp.py（1202 bytes，SHA-256 e61080b949d47630e899ddeccb338a0a47e4244831ebf5afe5ab45252e81235f）使用64KiB缓冲、readline(LIMIT+1)，非换行帧/EOF或超过64MiB拒绝；写请求后显式flush，最多忽略128个未匹配ID帧。socket timeout=10秒不是端到端硬期限；本容量测试另有独立15秒进程组watchdog。该库不能单凭socket timeout推广为所有调用的总期限保证。

overflow-v2 report.json：39,155 bytes，SHA-256 a586bf3046dae61010050637be64bcf142e064a318a0a3846bb081247507f2af。end.json.gz：174,605 bytes，SHA-256 07cde4225ab7a24e7532bb2a40fa6104813294aadb3c32f43b6c1c2048dd4595。独立解压后19,395,015 bytes，SHA-256 6c3f93a44c677f44c9bf1a6d3a7f07180e94d0f35e0bd9406d5d14c5a4fe17c7，与report.full_ledger完全一致；除events_json外的整个END与report.ledger相等。

events_json为16,777,085 bytes，SHA-256 8149f20bed546df7e616cd949f0b7f3b05c1e04613809d50e2a2512504ab8504；独立解析50,114条。CPU0 seq1..50114完整连续，CPU1零条；每条window=1、reason=mov、new/source=0x12345678，old由0到该值后保持相等。起末counter分别[0,0]及[50114,0]。下一相同格式记录会使数组达到16,777,420 bytes，超过16,777,216预算，因此先触发字节上限而不是65,536条上限。

实际END overflow=true、poisoned=true、reason=overflow，query-status=paused/running=false；重ARM回复CR2 active or poisoned，进程已退出。采集器在cont后只轮询query-status，未发stop，支持后端主动请求停止结论。elapsed_ns=55,522,700，整轮1.220804704秒，无15秒超时。容量上限和永久poison局部验证通过。overflow-v1仍是15.301秒失败，不将其取大帧超时追改为通过。此追加未测试60秒定时器或独立记录数上限触发。

### 新发现：v3正常多指令TB的首条MOV PC不准确

不能因容量拒绝通过而忽略事件语义缺陷。独立objdump检查overflow-v2原ELF：0x100300为b878563412（mov eax,0x12345678），0x100305为b901000100（mov ecx,65537），真正MOV CR2是0x10030a的0f22d0，后续0x10030d dec ecx、0x10030e jne 0x10030a。

实际seq1记录pc=0x100300，错误地指向TB早先指令；seq2..50114才均为0x10030a。这里的第一条PC错误可由保留ELF与事件直接复现，不依赖推测。此前简单normal微例的三条PC确实相等，但不足以外推普遍正确。

候选原因：write_crN仍声明TCG_CALL_NO_RWG，而新日志读取env EIP；仅在翻译侧gen_update_eip_cur不保证helper前全局EIP存储已物化。该判断是待验证定位方向，不冒称已修复。需在当前运行结束后另开版本，核查helper全局读写flag合同或显式传入准确guestPC，重做此多指令TB微例及原端点等价。运行中的v3/Windows源码与二进制保持原字节，不热修改。

因此v3账本的容量/连续链检查可用于诊断，但MOV原因PC通用认证目前不通过；当前Windows运行结果不得凭该后端宣称精确MOV PC完整认证。已即时通知主Agent，accepted继续false。此新增发现不追改先前窄微例实际观察，只收紧其外推结论。

### helper声明与优化路径的静态证据

冻结源码相对 .venv-audit/native-worker/tcg-build-v1/source：target/i386/helper.h:100准确声明为 DEF_HELPER_FLAGS_3(write_crN, TCG_CALL_NO_RWG, void, env, int, tl)。include/tcg/tcg.h:216–229明确NO_READ_GLOBALS涵盖直接读取及经异常读取，且蕴含NO_WRITE_GLOBALS；NO_RWG就是NO_READ_GLOBALS别名。target/i386/tcg/translate.c:3444将cpu_eip注册为offsetof(CPUX86State,eip)的TCG global。

tcg/tcg.c:3946–3951的liveness分支在NO_READ_GLOBALS存在时不执行la_global_sync；4365–4368的后续检查对NO_READ_GLOBALS标记为Nothing to do；5925–5936的helper调用寄存器分配分支同样在NO_READ_GLOBALS时不sync/save globals，只有NO_WRITE_GLOBALS分支调用sync_globals。后端v3在write_crN中调用terminal_cr2_write，进一步直接读取env->eip，因此新行为违反原helper声明。

这给出了可直接核查的优化合同冲突，较“可能lazy EIP”更具体。仍未采集该TB的生成宿主机器码，不声称已凭反汇编证明某一次store实际移动的位置；也未修改flags或验证修复。若后续选择调整flags，必须在新版本重新检查全部helper实际全局读写和异常路径，不能只凭这段说明机械放宽声明后宣布完成。

## v4修复后的独立复核与限定退役

Windows v6已运行期间仅只读来源及纯内存验证，未修改运行文件、未构建、未启动VM。

独立读取overflow-v3（实际binary为v4）完整end.json.gz，50,114条事件的PC全部为0x10030a，包含此前错误的seq1；每条CPU0序号连续，事件数/字节数/事件SHA与完整JSON摘要均一致。字节数仍16,777,085；实际paused、overflow永久poison及rearm拒绝均成立，整轮1.322027882秒。旧overflow-v2的首条错误PC保留，不改写旧失败来源。

report.json SHA-256 fef0c93f09e3f08bfc216134b92cca598a2a8ad17583870a5d6302257bef8128；end.json.gz 174,600 bytes，SHA-256 1dcf1a8fd4c127cf42534cd31ed26dc65c728aceb8d7acd3ebbb764bec0fc612。

normal-ledger-v2整轮0.481689994秒：与v12 normal-baseline-v1的完整双CPU start/end/fault_handler、fault_frame、fault_count及exit_code精确相等；三事件PC仍0x100305、0x100308、0x10030b，同值写和PF序列不变。独立重跑冻结consumer得到cr2_chain_verified=true/event_count3，accepted/full_state_verified/windows_admitted仍false。report.json 113,139 bytes，SHA-256 989b0b4f42c967445c8d3070743ddbbb2b6e2760c600b809c019108d338961b4。

结论：v4修复通过本次首MOV多指令TB反例及正常微例等价复核。它补齐已发现局部PC缺陷，不把这些微例扩大为Windows全路径、全部PF访问类型或原游戏验收。

按本轮明确授权，仅退役tcg-cr2-build-v1/objects及tcg-cr2-build-v2/objects中的.o/.d派生文件，共30个、2,505,585 bytes。每个文件删除前解析绝对路径并验证仍在对应objects目录，先记录SHA/size，再逐文件核对并删除；没有递归删除目录。日志、overlay源码、失败重建记录、v3/v4及任何历史来源全部保留。具体已删除路径/原SHA/size/替代来源见analysis/terminal-wait-tcg-cr2-build-retirement-v1-20261111.json；不能再把其文件报告为可获取。

清理后v1/v2/v3/v4本地构建目录分别1,048,208 / 1,041,662 / 32,860,411 / 30,892,927 bytes，合计65,843,208 bytes，包含保留失败诊断/源码/成功产物，没有另建备份。该数字仅构建子任务范围，不含主Agent微例或Windows来源。旧报告中清理前数字为历史时点，本追加说明当前存留状态。

## v8回执恢复与有界只读轮询审查

v8后台boot/编排运行期间，只读terminal_cr2_receipt_poll.py、wait_run_v4、wait_read_v4及依赖代码；运行纯模拟测试，未连接客体、未修改运行代码、未重投任何命令。v6/v7的未知Receive及首次文件缺失不能证明远端命令取消。已独立读取tcg-cr2-control-logs-v2/recent-events.json：客体06:27:15.852有WinRM事件91 shell start；06:27:46.774/819有三条PowerShell事件600 ProviderStarted，说明进入了部分提供程序初始化；所保留日志未见该次事件400 EngineAvailable。不能说完全没有PowerShell启动记录，也不能把未确认引擎就绪提升为远端取消或执行未发生。

恢复方向正确：prepare和launch各只调用一次request；返回未确认时只调固定prepare-receipt.json/launch-receipt.json的type读取，未调用prepare.ps1/launch.ps1重投。request的宿主55秒监管和read worker的35秒监管分开；父fast包装另有45秒上限。读取使用本轮固定目录及固定JSON文件名；prepare恢复要求本轮已记录owned shell/command ID，内容再核对prepared、UUID和目录。后续读要求本轮boot-auth，ready再匹配已确认launch PID。遇到已退出VM报告/vm-stop拒绝。匹配失败或未知读取结果不继续变更；主流程finally仅请求关闭本轮VM，不声称客体fixture已取消。

poll使用completed判据并在查询返回后再次检查期限，晚到成功明确拒绝，非缺失的错误身份/未知读取立即拒绝。因此它不会借超时后读到的“成功”放宽原55秒操作回执。轮询是新只读命令，不是再次Receive未知变更命令，也没有再次Send原PowerShell输入。go只执行一次；失去go回执没有重发路径。

独立测试：devtools.tests.test_terminal_cr2_receipt_poll普通Python与-O各3个测试通过。覆盖缺失后获得持久回执、晚到成功拒绝、错误身份/未知读取拒绝。只出现既有isolated_windows_vm.py:168的SyntaxWarning（无效转义），没有执行WinRM或产生缓存。

### 发现的期限与可观测性限制（只报告，未热改）

1. poll固定最多12次，并不是持续等满150/90/120秒。独立纯模拟每次立即返回file_present=false、seconds=150，实际12次/24秒就抛错；其后wait_run_v4会关闭本轮VM。因此这些值只能称接受时间预算上限，不能声称保证等待完整150/90/120秒。对慢启动命令仍有过早结束的可能；已有3个测试未覆盖这个边界。
2. poll没有将剩余预算传给query。独立纯模拟seconds=10、单次query耗时35秒，函数在35秒才拒绝。真实单次读取由35秒_supervise加清理/45秒fast包装限制；poll总预算本身不是硬执行截止点。当前900秒VM监督是另一个外层界限，不能把它和poll接受预算混为一谈。
3. read_v4将type的任何非零退出都映射为file_present=false，包括可能的权限/路径/命令错误；这是保守未确认而非成功，但不能据该字段断言文件确实不存在。读取异常/部分JSON则立即失败，不会获得完整poll等待窗口。该路径从未知状态失败退出是安全收窄，但实际慢启动恢复能力仍须按运行结果报告。
4. 本轮read_v4的type没有先检查客体文件大小。它依赖固定自有小JSON语义、35秒宿主监管及外层证据预算；不能单凭_supervise最终stdout限制宣称流式WinRM接收缓存或逐段receive文件存在同等硬字节上限。未看到本轮实际超量证据，这项是范围说明。

结论：未发现恢复分支重投准备/启动，亦未发现代码把未知远端状态直接认作取消。当前已有测试通过，但时间预算语义须以上述限制描述；不能仅凭该版本源码宣称已解决全部慢启动/回执恢复问题。当前v8继续原冻结代码运行，任何调整应待其结束后另开版本。

本节审查的源码身份：receipt_poll.py SHA-256 d94bfd0be55c8a23067ccd43436e5c6fe40c480155f521c835126ce1fdbc85b0；wait_run_v4.py 3cc7029d345fa9709c00fc1783a548d505980d073b343f3e1cf9a891ca939ea8；wait_read_v4.py d80b95357afcc4d3085b239bbffb40cb8f5c78956228ef70b221eefdbb895223。12次为独立尝试上限，150/90/120秒为接受预算，以上限制并非要求当前冻结运行热改或立即创建新版本。
