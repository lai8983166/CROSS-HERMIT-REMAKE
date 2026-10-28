## Context

父终局followup已封存于2026-10-27归档；当前HEAD a232efd6只迁移未推送大证据存储，父文件字节未变。父完整两例为PC198/194 wait1，8个创建世代，分别8/7个存活纹理。源资源、完整57CPU与累计摘要必须可独立核对。

## Goals / Non-Goals

目标是同一CRT/GDI/D3D8实例中完整新增两行组；不改变父时钟、机器码守卫或旧封存工具。停止边界分别PC230/226 wait1，后继43/30不执行。此单元不扩大到整段剧情、draw/Present、原生外层退出或奖励回写。

## Decisions

1. 新工具继承父来源但独立记录本阶段；入口仍为heads/arena/input/task完整任务，键盘只绑定采集raw256并执行原片段，严禁写PC/wait或派生状态。无新增guest代码范围。
2. 原43 config4选图层7，44只清count。胜利文字3/4替换旧record0并新增record1；超时文字5/6替换record0/1，原record2纹理虽超出count仍保留。每次原403730释放必须匹配4051AE caller、record、世代，不能按pointer跨世代合并。
3. 两个新DIB地址独立，真实GDI三阶段和LockRect原始初值/pitch/padding/全texel可重放；保留所有存活资源的readback与原析构，最多10创建世代且峰值不超现有helper容量。补充清理只证明测试所有权，不代表任务退出。
4. 独立验证从当前原生wire核对每个CRT/GDI/GPU调用和全部原x86、全内存/57CPU/队列/每帧摘要。冻结父forward只比较实际forward边界；后续真实清理不得投影成旧历史清理CPU或摘要。
5. 大型source/diagnostic保持本地ignore并复制到仓库外备份；Git只收小报告与path/bytes/SHA。验收分开检查受版本管理文件worktree/index/HEAD和本地证据文件字节，保留迁移后的存储事实。
6. 跨实例核对已发现全进程native地址投影会受驱动地址复用影响。两条本阶段新资源使用各自的overlay-replacement-0/1生命周期域，底层仍用原AddressSpace，原overlay域及父完整边界不改；验证器按创建世代和原record独立派生域，允许native地址跨域重用，拒绝同域重复和guest别名。不归一化任何原始内存、表面或堆字节。

## Risks / Trade-offs

- 原生地址复用与旧count外纹理 → 完整10世代台账及全部原Release，保留当前初始字节。
- 重复大追踪成本 → 来源运行与验证串行，先做小型静态和专项测试，主Agent保留必须独立验收，最多一个最小上下文实现子任务。
- 旧报告递归封存 → 冻结父76项和验收本体，递归旧资产/存档/检查点核对；旧acceptance的历史Git等式按原bundle解释，不改写。
