# CR2 事件来源审计与下一轮最小采集合同

状态：设计/静态核对，accepted=false；不修改既有验收、冻结运行时源码或客体，不启动 VM 或构建。范围为 self-owned WOW64 wait fixture，非原游戏验收。

## 固定来源与观察

源码根 .venv-audit/native-worker/tcg-build-v1/source，HEAD e470268ff446ec56728215a987ed166d5ed8fb64。本次逐文件 SHA-256 核对 v12 manifest 的全部 14 项 modified_source，均一致；下列 excp_helper、misc_helper、svm_helper、seg_helper、tcg/excp_helper、cpu.c、helper.c 与固定 HEAD 原字节相等。v12 二进制 manifest SHA 为 f4c6aa60808051ae7395a549cbe4302cc1d2945ffa425c76f173b0a801448cef（本报告未重新散列二进制）。

probe-v3/observation.json.gz 的 CPU 0 CR2：

| 轮次 | call | ret/post |
|---|---|---|
| 0 | 0000000072e60920 | 0000000001117008 |
| 1 | ffffdc8fd2d35000 | 0000000075b2c1ff |
| 2 | ffffdc8fd2d36880 | 00000276982e5978 |
| 3 | ffffdc8fd2d37880 | ffffdc8fd2d37880 |

所有列出的停止点 CPU 0 CR3 为 000000003d473000；CPU 1 的 CR2 也多次变化。停止点相同 CR3 不证明中间未切换地址空间/线程，也不证明第 2 轮的 64 位地址来自当前 WOW64 用户线程。第四轮端点相等不证明中间无写入。consume.json 的 fixture_observation_passed 与 accepted 均 false，保持原结论。

## CR2 写入路径（相对源码根，当前行号）

- target/i386/tcg/system/excp_helper.c:651：x86_cpu_tlb_fill 的地址翻译失败路径写入 err.cr2，再在 653 行 raise_exception_err_ra。probe=true 在 635–639 行返回，stage2 在 641–643 行另走 VMEXIT；intercept_exceptions 分支 645–650 行只写 VMCB exit_info_2，不写 CR2。不能将所有失败都称作 CR2 写入；非 canonical #GP 在 595–596 行明确保留旧 CR2。
- target/i386/tcg/system/misc_helper.c:78–131：helper_write_crN 的 default 在 128 行写 env->cr[reg]；reg=2 为 MOV CR2。tcg/emit.c.inc:368 生成该 helper 调用。这不是 #PF，不会自动产生 -d int 条目。
- target/i386/tcg/system/svm_helper.c:333–334：VMRUN 从 VMCB 恢复 CR2。201、801 行是向物理内存保存 CR2，不是向 env 写入；VMEXIT host reload 段未见恢复 CR2。应记录 VMRUN 或在合同中明确拒绝发生嵌套虚拟化。
- target/i386/gdbstub.c:377–382：GDB 寄存器写通道可写 CR2。现有观察声明 host_guest_state_writes 不能代替下一轮的协议审计；须拒绝 P/G 等状态写操作。
- target/i386/machine.c:1855：VMSTATE_UINTTL(env.cr[2], X86CPU) 在迁移/快照装载恢复 CR2。 machine.c:295–305 cpu_pre_save 在 pending #PF 且非 guest-mode 时也会将 exception_payload 写入 CR2，不能只禁止 load 而允许窗口内 save。
- target/i386/cpu.c:9388：reset 的 memset 覆盖 CR2（cpu.h:2014 的 cr 在 end_reset_fields:2217 前）；helper.c:612–628 INIT 调用 reset，随后 start_init_save:2026 之后的恢复范围不包含 CR2。窗口内 reset/INIT/hotplug 一律拒绝。
- 其它编译模式路径：tcg/user/excp_helper.c:39 用户模式故障；emulate/x86_mmu.c:333 emulation #PF；KVM kvm.c:849,4662,4705；HVF hvf.c:480、x86hvf.c:204；MSHV mshv-cpu.c:609,693；NVMM nvmm-all.c:289；WHPX whpx-all.c:932。它们不应在固定 system TCG 路径运行，需由已认证构建配置/启动参数排除，不能笼统当作已观测事件。
- tcg/system/smm_helper.c 的保存/恢复涉及 CR0/3/4，无 CR2 写入；SMM 内普通 #PF/MOV 仍归上述路径。

以上是对当前 x86 源码的直接赋值、动态索引、迁移字段和整体 reset 检查，不把一次文本搜索宣称为未来版本的通用完整性证明。

## 现成日志的证据边界

tcg/seg_helper.c:1201–1225 的 do_interrupt_all 在 protected mode 打印全局 static int count、vector、error code、is_int、CPL、CS:EIP、linear PC、SS:SP；vector 0x0e 时附 CR2，并调用 log_cpu_state。cpu-dump.c:455–459 的状态行含 CR0/2/3/4。tcg/excp_helper.c:54 check_exception 只有 old/new vector。

这些是中断交付/异常升级日志，不是每次 CR2 赋值日志：没有旧 CR2、赋值原因、可靠的每 CPU 单调序号/窗口绑定、故障访问类型/mmu_idx、对应 call/ret stop 编号。header 没有 cpu_index，不能把全局 count 当成双 vCPU 事件身份或无丢失证明；输出还可受日志启停、过滤、截断及线程交错影响。MOV CR2、VMRUN、GDB、迁移/重置没有相应完整记录。当前 target/i386 与 accel/tcg 的 trace-events 未提供覆盖上述写点的 CR2 事件。

因此下一轮只开 -d int 能帮助定位候选 #PF，不能闭合状态合同。匹配最后一个 #PF 的 CR2，或缺少 #PF 时允许 arbitrary CR2，是不合格的验证器放宽。

## 下一步：有界诊断与可验收事件链分开

1. 先固定本报告、原 observation/consume 摘要及主 Agent 的 WOW64 字节路径。仍不运行。若仅需调查候选，可在下一次独立命名 fixture 采集中按停止窗口打开 -d int；声明其只提供线索。不要为了拿 -d int 日志重跑长全前缀。
2. 要证明差异，必须新增独立版本的 QEMU 事件能力（本报告没有实施或授权构建）。在每个实际 CR2 写点记录 old/new（含同值写）、reason、CPU index、每 CPU 连续序号、window id、原始 CR3、CS/CPL、正确恢复后的 fault/instruction PC。#PF 加 vector/error_code、linear fault address、access_type、mmu_idx、stage2/intercept 结果；MOV 加已认证指令位置和源值。GETPC 是宿主返回地址，不能直接冒充 guest PC；翻译故障需按既有 raise_exception 的恢复语义取得精确客体位置。
3. 最小窗口为 call-0 前所有 vCPU 停止至 ret-0 后所有 vCPU 停止；先做单轮代表案例而非四轮/两例长采集。原两核配置保留；记录两个 CPU 的起末 CR2 和计数器，包含期间其它进程的 CR2 写入，不能只按 fixture CR3 过滤。call/ret 原完整状态及所有权仍保留。
4. 建议固定 65,536 条记录、16 MiB 未压缩事件上限、60 秒活动窗口（超时只停止并失败）；预分配有界缓冲，达到任一预算即置不可清除 overflow/truncated 标志并停止成功路径。没有环形覆盖，没有采样。保留一份压缩事件流、小报告及 SHA/大小。可按首次实测再调整下一版本预算，不能当场静默扩大。
5. ARM/END 必须在所有 vCPU 已停止且缓冲 flush 后，以同一只读端点原子绑定 stop state、window id、每 CPU start/end counter、记录数/字节数及摘要。QMP/GDB transcript 限定只读观测与现有运行控制；禁止迁移 save/load、reset、INIT、hotplug、外部 register/memory write、调试器注入。日志 I/O/flush 失败、关闭事件或未知 writer 必须拒绝。只依靠文字声明“没有发生”不够，需相应执行入口拒绝或完整控制记录。

## Fail-closed 消费规则与必要回归

- 固定 QEMU/源码/配置/输入/fixture 身份；完全验证原有停点、真实返回、owner 与清理，不更改旧 receipt 或旧 consume。
- 每 CPU 从 call.CR2 顺序应用事件，逐条 old 必须等于累计值，PF 的 new 必须等于 fault address，MOV 的 new 必须等于可核对源值，最终累计值必须等于 ret.CR2。零事件要求端点精确相等；同值写仍计数。
- 事件序号与 start/end counter 严格连续且数量一致；顺序、CPU/window id、摘要、边界确认全匹配。缺失事件、删尾、重复、重排、CPU 混淆、伪造原因、off-by-one 边界、超预算、unknown writer 均失败。仅 old/new 链自洽不能证明日志完整，必须依赖经过审计的写点覆盖与计数器。
- 每个允许原因需要独立事件语义验证；不能把记录到了写入等同于原调用语义已正确。迁移、reset、外部写、VMRUN 等本轮不支持原因一律拒绝。#PF 与 MOV 需单独正反例，此外测试无事件相等、同值写、端点不匹配以及所有截断/丢失/串 CPU 篡改。
- 原 call-ret 的其它 raw64 差异照常严格验证。CR2 的成功只证明该窗口 CR2 事件链，不等于 WOW64 全路径、完整重放、原游戏或最终验收通过。

本次仅新增本小报告，不新增工具、测试、缓存或运行证据；没有修改冻结文件。主 Agent 仍需独立审查本合同，并由本审查者复核其 WOW64 路径结果。

## 对并行 WOW64 静态路径的独立复核

本审查者用独立 objdump 读取 tcg-wow64-path-v1/System32-wow64cpu.dll，确认 preferred ImageBase=0x6b100000；RVA 0x3738 qword 为 0x6b101b46；0x1b46 的路径在 0x1b51 call 0x1ce0；0x1b82 原字节 45 8b 4d 3c 为 mov r9d,[r13+0x3c]，0x1b8e 为 ljmp [r14]；0x1cf1 syscall，0x1cf3 ret。该返回段无 XMM 清零。

两处分支仍需活体证据：0x1b6c 的 jb 0x1b91 可进入 iretq 慢返回；0x1cef 的 jne 0x1cf4 可选择 int 0x2e 而非 syscall。磁盘字节不证明运行时映射、分支或 r13 上下文内存；暂不放行 R9/XMM 差异是正确的。extractor 当时仅将 current/wait 两层 SHA 与旧回执比对，compat 只前后相同，worker.vmdk 未记录认证；已向主 Agent 提出补全整链身份或缩小结论，后续修正由主 Agent 汇总。

事件 PC 实现补充：tcg/excp_helper.c:92–115 的 raise_interrupt2 最后才 cpu_loop_exit_restore(cs, retaddr)。写点的 env->eip 不保证精确 fault PC；不应仅为日志提前恢复状态而改变异常处理语义。应选无副作用解码、经验证的恢复后完成事件挂点，或明确只做无精确 PC 的诊断而不宣称事件原因认证。

## ntoskrnl 六条 PXOR 的独立只读复核

已重新散列提取的 System32-ntoskrnl.exe：11,597,168 字节，SHA-256 5669b9b8bfcf20f08b7d1d65dc2deccbf836279c0e3f66722d72ad33ee7f672a，与 kernel-extraction.json 一致；PE preferred ImageBase=0x140000000。独立 objdump 确认两段各 24 字节的连续指令，原字节均为：

    66 0f ef c0 66 0f ef c9 66 0f ef d2
    66 0f ef db 66 0f ef e4 66 0f ef ed

分别为 pxor xmm0,xmm0 至 pxor xmm5,xmm5，每条 4 字节：

| 范围（RVA，末端不含） | 前一完整指令 | 后一完整指令 | fallthrough sysretq |
|---|---|---|---|
| 0x41a2b6–0x41a2ce | 0x41a2af mov r9,[rbp+0xd8] | 0x41a2ce mov r11,[rbp+0xf8] | 0x41a302 |
| 0x428e72–0x428e8a | 0x428e70 xor edx,edx | 0x428e8a mov rcx,[rbp+0xe8] | 0x428ec3 |

前向边界分别从 0x41a2a1、0x428e5e 的完整指令开始连续解码可达上述序列。第一段后 0x41a2de、第二段后 0x428e9f 均存在 jne 0xa8adc0，故不能称为无条件直达 sysretq；另有 CET/影子栈分支，最后分别在 0x41a2ff、0x428ec0 swapgs，再 sysretq。两条返回路径均在后续 xor r9d,r9d，WOW64 返回段再从上下文载入 R9 的候选链与静态字节兼容。

结论仅为已提取磁盘映像中存在这两段指令。kernel-extraction.json 的 clear_six_xmm_hits 当前为空数组，不能据该字段宣称自动扫描命中；本附录给出的是独立反汇编复核。需要认证实际内核映射、逐条停点与输入/输出状态、线程/CPU 所有权、分支及返回链，才可认定本次调用执行了其中一段。CR2 不完整事件归因仍拒绝，静态 PXOR 与 SYSRET 字节不放行其它状态差异。

## v4 实际指令证据与 effects 消费器独立审查

输入 wow64-trace.json SHA-256 d4f8f62282905e921ab11c81fa9c8f99edd01ffb85bc49955a73e006d0572015；effects.json 引用该摘要。六条 PXOR 的实际 CPU0 停止线程均为 01，原指令每条 4 字节，EIP 从 fffff8030c628e72 连续至 fffff8030c628e8a；逐条仅 EIP 与对应 XMM 低/高 64 位变化，相邻步骤状态完全连续。

load-r9d 原字节 458b4d3c，CPU0 EIP 774b1b82→774b1b86，R9 0→77533bfc，匹配 return-branch 保存的 fc3b5377；另仅 hflags 40c0bb→40c0b3，清除 bit3/mask0x8。v12 cpu.h:161/191 定义 HF_INHIBIT_IRQ，translate.c:3586–3594 使该前态的下一指令在 TB 结束；3623–3631 调用 gen_eob，1990–1992 经 683–690 精确清除 mask0x8。两文件 SHA 仍匹配 v12。该语义可以解释这个已观测前态下的已知 MOV，不证明实际执行过邻接 MOV SS，也不允许泛化屏蔽 hflags。CPU1 每步均有状态变化，结论仅限 CPU0。

首次审查 terminal_tcg_wow64_effects.py 的纯内存负例（未改来源或工具）：基线 true；R9 错误 opcode、额外 hflags 位变化、单独 CR2 变化均正确 false。但以下三个畸形来源仍 true，已通知主 Agent 修正后再审：

- 将 R9 before/after 与 return-branch 的 states[0].cpu 同时改为 1：r9.owner_bytes 未断言 CPU0。
- 插入重复 pxor-0 label 的伪步骤：字典构建静默覆盖重复项。
- 所有 point/step 状态删除 cr0_cr2_cr3_cr4：未核验完整 schema，剩余字段比较仍通过。

因此原输入局部效果和精确 bit3 派生规则成立，但该版消费器的“完整状态/篡改拒绝”尚不能通过独立审查。accepted、cr2_explained、consumer_connected_in_this_trace 持续 false 的边界正确。后续修订不得覆盖旧 trace 的失败或把局部效果等同于全 VM、消费者连接、原游戏验收。

### effects v2 再审

独立重算 terminal_tcg_wow64_effects_v2.verify，真实输入局部效果为 true，与 effects-v2.json 除 inputs 外全部字段一致；旧三项反例（R9 CPU1、重复步骤 label、删除 CR 数组）全部拒绝。精确 shadow 清理仍通过原 v1 语义函数，CPU0 范围与 accepted/cr2/consumer=false 保持。

额外类型负例发现两个小缺口：所有 target_bits 改为浮点 64.0、vp_stopped[0].stopped 改为整数 1，仍因 Python 值相等而通过。已反馈主 Agent；这不改变实际来源的局部语义结论，但在修正或缩小声明前不能称全部元数据类型严格验证。此再审只执行纯内存校验，无新运行、来源修改或工具改动。

### effects v3 最终局部审查

已审查 v3 的 exact-int target_bits、exact-int vp.cpu 与 stopped is True 前置检查；其后仍调用 v2 完整字段/数组形状/CPU 次序/标签唯一性和 v1 精确指令效果规则。旧 v1/v2 保留，无追改原失败证据。

独立从保留 ZIP 读取原 trace，SHA-256 仍为 d4f8f62282905e921ab11c81fa9c8f99edd01ffb85bc49955a73e006d0572015。独立运行 devtools.tests.test_terminal_tcg_wow64_effects，普通 Python 与 -O 各 2 个测试方法、12 类篡改全部通过；另加纯内存 vp.cpu=False 负例确认拒绝。未创建测试缓存、未改其它文件。

结论：本轮发现的 CPU 标签、缺失字段、重复标签与数值/布尔元数据别名问题均已修复，v3 的当前来源 CPU0 局部 PXOR/R9+shadow 效果审查通过。其验证的是已导出 raw64 schema 与局部精确转换，不是所有内部 QEMU 状态、全 VM 时间线或日志来源不可伪造证明；来源 SHA/保全仍依赖外层证据链。accepted、CR2 归因、消费者连接均 false，整体验收不扩大。
