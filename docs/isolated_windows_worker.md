# 独立Windows原生测试环境

用户授权专用Windows虚拟机，以2个虚拟CPU、4 GiB内存进行兼容性和输入隔离预检；宿主机必须继续可供用户正常使用。所有新环境数据位于宿主F盘 `F:/project/chaomofa/.venv-audit/native-worker`。客体自己的逻辑C盘包含在F盘的VMDK文件中。原来临时位于宿主C盘的下载目录已迁移并移除，没有在C盘创建虚拟磁盘。

本环境是 `connect-terminal-wait-and-battle-exit` 的测试前置，不修改其8项任务的完成标准。目前正式完成数仍为2/8，原游戏兼容、等待返回、结果消费和完整战斗退出不能由环境配置成功推定。

## 配置和数据预算

- 使用本机已有VMware Workstation 16及其 `vmrun`，专用VM仅通过 `start ... nogui` 启动；不打开或点击宿主上的VMware控制台。
- 微软官方Windows Server 2022 Standard Evaluation桌面体验映像，180天评估期；它与宿主Windows 10版本不同，预检须记录实际系统及运行库。原程序和系统接口均保留原生执行，不用Wine或重写输入字段替代。
- 2 vCPU、4096 MiB内存、40 GiB按需增长的独立虚拟磁盘；不挂载宿主物理磁盘，不接入其它现有虚拟机。默认关闭USB、共享文件夹、剪贴板同步和拖放。
- 环境预计初始20–30 GiB，包括约4.70 GiB安装ISO、Windows系统、144,656,384 B既有VMware Tools介质的F盘副本及必要测试部署。40 GiB是虚拟磁盘上限，不是预先占满；介质另计。
- 这是用户明确授权的运行环境存储例外，不是把大型CPU/内存快照追加成逆向证据。Git只提交脚本、必要小报告及大小/SHA/位置；ISO、VMDK、凭据和客体副本不进Git。环境只保留当前一份，无克隆或快照备份。
- 私有安装口令随机生成，仅存F盘受限ACL目录及客体安装介质；不打印命令行凭据、不写入公开报告。`vmrun`超时/启动失败使用净化错误，不回显含密码argv。

## 自动流程

`devtools/isolated_vm_download.py` 从微软原官方下载链接解析得到的HTTPS地址继续下载，核对每段HTTP Content-Range和总字节数，记录完整SHA。下载SHA是取得原字节的身份，不冒称微软独立发布的校验值。已完成分段可续用；分段缩小的迁移记录保存旧实现与进度摘要。

`devtools/isolated_windows_vm.py prepare` 在写任何分区配置前重新核对完整镜像SHA，读取ISO中 `install.wim` 的实际XML元数据，选择唯一Standard Evaluation的 `INSTALLATIONTYPE=Server` 桌面映像。自动安装答案文件位于专用虚拟软盘，只清理新虚拟磁盘0；启动前校验完整附件白名单和独立40 GiB稀疏磁盘描述符。安装后自动安装VMware Tools并重启客体，无需用户操作。

`devtools/isolated_guest_preflight.cs` 在任何窗口/输入操作前核对专用客体名称、VMware硬件、2 CPU/4 GiB和当前交互控制台会话。它只对客体自己的测试窗口发送带随机标记的鼠标/F24事件，检查目标及消息，再测试32位Direct3D 8 HAL的窗口与全屏Clear/Present、COM释放和窗口销毁；不以参考软件渲染器代替HAL失败。

`devtools/isolated_vm_preflight.py` 通过VMware Tools复制和运行该程序。宿主只读监听器始终调用下一hook，不注入、不拦截、不记录用户具体按键。核对挑战事件在客体完整收到、在宿主观察窗口未出现，且主客机器UUID不同，所有执行源码/二进制身份在本轮保持不变。这个有界结论不宣称永久零输入泄漏或所有负载下性能零影响。

`devtools/native_input_isolation.py` 在新游戏采集器启动前检查当前机器及完整预检原字节；物理宿主、其它虚拟机或缺少有效资格的环境直接拒绝，发生在资产长校验及游戏启动前。新鼠标生产入口同样受限。资格原JSON随新采集的input_isolation记录保存，宿主独立验证器重算SHA和全部预检判据，不信任单独的passed标记。

## 前置来源

- [微软官方Windows Server 2022下载](https://www.microsoft.com/en-us/evalcenter/download-windows-server-2022)
- [Windows无人值守安装](https://learn.microsoft.com/windows-hardware/manufacture/desktop/automate-windows-setup?view=windows-11)
- [VMware后台运行及客体交互会话说明](https://community.broadcom.com/vmware-cloud-foundation/communities/community-home/digestviewer/viewthread?CommunityKey=fb707ac3-9412-4fad-b7af-018f5da56d9f&GroupId=7171&MessageKey=e063d032-fab3-48b7-865a-6c72f623cf1f)

实际安装、设备预检、原游戏短观察和清理结果须另以新报告记录；不能用本说明代替执行证据。

## 本机兼容配置与恢复（2026-11-08）

已自动安装 Standard Evaluation Desktop Experience（20348.587），实际客体名为
`CHAOMOFA-WORKER`，UUID 为 `E6D84D56-0960-FA47-1543-6C62C21D5DC7`。
宿主 Windows 10 Home 的 Hyper-V/WHP 保持原状，没有重启或修改宿主安全策略。

初始客体在 OOBE 前出现 0x7E/C0000094。只读提取的原内核与微软公开符号将候选
除零位置指向 `MiComputeRunTimeZeroComparisons+0x103`；没有完整转储和现场基址，
不能将候选地址说成完全证明的根因。专用 VM 的
`monitor_control.virtual_rdtsc = "FALSE"` 避开了重复蓝屏。重建时可在该 VM 停止后执行
`python -m devtools.isolated_vm_compat_profile`；它备份原 VMX，不修改宿主 Hyper-V。
这是明确记录的本机兼容配置，不能推广为所有 VMware 的默认设置。
[VMware 时间说明](https://www.vmware.com/docs/vmware_timekeeping)指出这一模式有时钟局限，
因此本环境不使用挂起恢复、快照迁移作为有效测试接续。

客体完成安装和一次冷启动后，分别运行有界时钟检查：两 CPU 各持续0.5秒采集
RDTSC/QPC，并做256次跨 CPU 切换，未观察到零值或倒退，亲和性和分配内存清理通过。
该检查不证明长时间或所有负载的时钟等价性。冷启动后的原生交互必须重新获取资格；
`native_input_isolation.py` 将原资格的 UUID、精确 boot UTC、CPU/内存与当前机器对照。

若刚冷启动时 Tools 服务存在而认证 RPC 尚未就绪，新的 boot watcher 只在启动阶段
通过该 VM 的 DHCP MAC/UUID、加密 NTLM WinRM 执行至多一次客体 Tools 服务重启。
它不改宿主 TrustedHosts，不在游戏运行期间重启服务。安装诊断120秒截止时曾中断
Tools 初装；后续自动修复和冷启动均另有报告，不能把该诊断说成自然安装成功。

客体 Server Manager 自启动和关机原因弹窗会影响客体前台，因此由
`isolated_guest_desktop.ps1` 做客体专属配置；系统崩溃日志保留。
`isolated_guest_audio.cs` 将当次默认客体输出端点静音并核实，未改变宿主声音。

原游戏原字节在 Server 的 DEP OptOut 默认策略下于初始化前以 `0xC00001A5` 退出。
宿主原策略为 OptIn。兼容诊断仅针对私有完整 EXE 路径注册 DEP OFF，
系统策略、SEHOP、原 EXE 字节不变；使用 `GetProcessDEPPolicy` 记录本轮实际进程值，
不把注册成功或查询失败返回的零值算作生效证明。
`isolated_guest_dep.ps1 -Action restore` 可移除该单项覆盖，恢复结果仍须核对。
[微软应用级缓解配置说明](https://learn.microsoft.com/en-us/defender-endpoint/enable-exploit-protection)。

新增 `isolated_guest_focus.py` 只在已核资格的客体会话中激活当前 Job 的原窗口；
直接激活被拒绝时，可短暂附加同一客体控制台前台线程的输入队列，必须核对参与
PID/TID/会话，并在 finally 中解除。它不发送键鼠、不附加宿主线程、不改冻结父脚本。
资格查询在启动前完成，避免同步 CIM 查询遮住原程序短暂 factory 阶段。

## 部署与重用

客体 Python 3.10.11、审计依赖和原游戏资产均装在 `C:\ChaomofaWorker`，它们的全部
物理数据包含在 F 盘 VMDK 中。传输包有大小/SHA 清单；解压拒绝路径逃逸及大小写
重名。原资产与私有运行目录为独立复制，私有四个可变文件单独恢复；每次原生测试
仍重新核对8105个不可变文件（1,541,607,697字节）与固定父清单，不能用部署成功替代。

编译入口为 `python -m devtools.isolated_guest_build preflight`（或 `clock`、`audio`），
使用现有系统 CSC 只读编译 x86 winexe，输出和 TEMP/TMP 均为 F 盘。
随后使用 `python -m devtools.isolated_vm_preflight --label <new-label>` 取得当前启动资格。
资格仅用于本轮实际观察；完整游戏兼容、结果消费和完整战斗退出始终分开报告。

`python -m devtools.isolated_vm_run compat --label <new-label>` 在复制本轮支持源码前
拒绝任何已有客体游戏/Python采集，随后通过 Tools 在客体交互会话运行短测。
`school` 子命令使用同一机制运行1800秒上限的原流程接续；宿主只通过命令和小回执
观察，不打开控制台。脚本即使得到客体失败退出码也拉取报告及小日志，不自动重试。
运行中的源码保持原字节；复用既有部署不会重复下载系统或复制完整父证据。

本轮 v10 原始输入/图形报告通过独立复核；v5 原游戏短测观察到原 factory、WinMain
就绪及30秒 startup 循环，counter 371→2105，当前客体前台归属成立，实际父子 DEP
flags=0/permanent=true，四个私有可变文件恢复，Job非强制清空。
本次游戏激活为 already-foreground，未实际执行 Attach 分支；该分支的客体测试窗口
实测记录来自前面的 v8 预检，不能拿单元测试替代当前游戏里的实测。
清理父退出0、子退出0xC0000354与旧 menu v6 来源相同；不认作 WinMain 正常返回、
完整PTD释放或战斗退出。宿主标签输入未泄漏的结论限于预检观察窗口，不声称
任何负载下零性能影响；2 vCPU/4 GiB 是客体配置，VMware 宿主进程还有额外开销。

本轮收尾已正常关闭VM，未留下游戏进程；下一次启动必须重新做当前boot资格预检。
当前 `C:\ChaomofaWorker\isolation-qualified.json` 是旧boot的运行资料，不能直接复用。
取得新资格后，自动化调用 Tools 将本次 `preflight-<label>.json` 复制为该固定客体路径，
再启动采集。三个预检源码及客体采集源码须与本轮声明的身份一致。

清理只删除本轮已验证部署的主客传输ZIP及客体重复报告，逐项保留原大小/SHA与
替代位置。资产、原存档、旧验收及检查点未删。主来源与一份恢复副本都在F盘，
不称为独立容灾备份；删除客体文件不会立即缩小VMDK物理文件。
本轮原始结果与容量清单见 `analysis/isolated-windows-worker-v1-20261108.json`。
