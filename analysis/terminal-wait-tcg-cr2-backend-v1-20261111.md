# 有界 CR2 事件后端（开发实现）

accepted=false；本文件只记录新后端及局部构建，不是 Windows、原游戏或完整逆向验收。执行目录均在 F 盘；没有启动 VM、Windows、原游戏或 UI。主 Agent 独立调度微客体与验收。

## 实现

新增 devtools/terminal_tcg_cr2_backend_v1.c 与版本化构建脚本。冻结 v12 源码及二进制保持原字节；修改仅写到独立 sparse overlay，通过旧 compile_commands 的原参数定点编译到新对象，再替换 link 输入。原 build 对象亦不覆盖。原源文件、overlay、新对象、全部原链接文件、编译器/动态库及配置 SHA 均写入新 manifest。

x-query-tcg-state 的 cpu-index=-2 ARM，-3 END；正常非负查询保持原行为。两者必须 system TCG、恰好 CPU0/1 且所有 CPU stopped。ARM 拒绝 active/poisoned，END 拒绝 inactive。ARM/END 嵌入原 tcg-state-v1 双 CPU 完整导出状态及 CR2/counter。窗口号、每 CPU counter 单调；poison 不允许重置。END 导出 ASCII events_json 及原字节 SHA-256，bytes 是该字符串 UTF-8 长度。

预分配16 MiB事件缓冲，65536条，60秒 realtime clock窗口（单调时钟）。定时器到期请求停止并poison；每次写入和END再次核查。无环形覆盖/采样，超限保留已捕获前缀并永久poison。无文件I/O的内存端点；外层QMP失败/截断需消费器拒绝。

MOV CR2（含同值写）在原赋值前记录old/new。仅 CR2 翻译路径增加 gen_update_eip_cur(s)，使helper读到该指令的准确客体EIP；这改变内部lazy EIP更新时间，必须由原v12与新runtime微客体完整导出状态等价检查，而不能仅据编译通过宣称无影响。记录CR3、CS、CPL、linear PC、源值。

PF在原赋值前置pending，原 raise_exception_err_ra 及 cpu_loop_exit_restore 中的恢复顺序不变；在原cpu_restore_state完成后、原cpu_loop_exit之前完成记录。保留原vector/error/access/mmu；exception_index非14、pending重叠/未完成/值不匹配一律poison。GETPC不作为客体PC；无提前恢复或新异常注入。

不支持writer通过reset/INIT、VMRUN、GDB寄存器写/内存写、CPU迁移pre_save/post_load、load入口钩子置poison。操作可能仍执行，但窗口永远不能成功；它们不是获准事件原因。GDB硬件断点Z/z仍可用。非TCG路径由端点和启动身份排除。该实现不是通用恶意控制端隔离器，QMP/GDB原始协议记录和外层允许列表仍必须认证；内存写/设备控制/热拔插等控制的语义不能只由文字声明保证。

## 构建经过与证据

首次构建在compile_commands逐条Path.resolve处慢遍历，尚未执行对象编译；停止自有Python进程。该次脚本曾原地修正且空日志被重开，未及时封存原字节；已依据明确逆变换写出 tcg-cr2-build-v1/build-attempt-1-reconstructed.py，这是重建副本，不声称原始封存。其后已执行版本全部独立文件/目录保存。

第二次（v1修订）在发现cpu-exec-common同时有user/system两个编译条目时拒绝。v2仅选system，对象编译无诊断；链接发现旧build唯一缺失 libsystem.a.p/net_slirp.c.o 而失败。v3从固定commit核对原net/slirp.c并在新目录重建该对象，无新源码语义变动。上述失败不涉及客体执行或Windows来源。

## 验收边界

构建成功和 --version 只证明产物可启动。微客体需独立认证两次同值MOV、PF精确PC/错误码、双CPU链和v12完整导出状态等价；还需真实admin-write poison、超限/超时及消费器篡改拒绝。此前不准入Windows。具体执行与结果由主Agent独立报告。

## 构建结果与容量（子任务范围）

v3 binary 29,805,128 bytes，SHA-256 ab2da916537ac0aaa0055ab8acacec1a84c5abf49ba9c23f3a6f4a25f73b4ae7。manifest 322,187 bytes；编译/链接日志为空（无诊断），--version正常返回 QEMU 11.1.0。构建后重新核对 v12 全部14项modified_source及旧binary，均与manifest原摘要一致。

新增本地构建目录v1/v2/v3分别1,954,483 / 2,640,972 / 32,860,411 bytes，合计37,455,866 bytes（含所有失败来源、对象、重建脚本；无备份副本）。尚未删除失败派生对象，待主Agent微客体验收后可按明确清单清理；不得将仍在的文件称为已退役。该数字不含主Agent另行生成的微客体/Windows证据，整轮容量由主Agent汇总。版本化构建脚本均已运行，勿重跑覆盖既有目录；后续修正另开版本。
