# 原终局肖像资源与角色任务就绪

2026-10-26，connect-terminal-portrait-resources，基线354f0c9a。沿两新战斗实例、原世界终局选择、完整终局任务及当前GYBC/姓名资源前缀，在清理之前接续原4CDE10；不加载战后快照，不复用已结束助手的句柄。

## 连续原执行

胜利角色2读取data\\adv\\bin\\sc002.bin，超时角色1读取sc001.bin，均为262168字节单项DX2容器，256×512、格式25、131072个A1R5G5B5像素。原目录查询、只读打开、大小、原分配、完整ReadFile、CloseHandle、调试数组构造/注册、512行原56D4D0复制、原文件缓冲摘链/检查/DD填充/实际释放及IMAGE返回连续执行；未代用游戏/CRT函数结果。

同一当前GPU设备同时持有512×512的GYBC、64×32或128×32的姓名、256×512的肖像三张纹理。肖像全部262144字节上传和整表面读回与原文件24字节头后的像素一致；另查询GYBC与姓名整表面确认原像素保留。原槽32只由原注册和加载标志写入，两个未初始化IMAGE填充字节保留CD。

原姓名前缀中悬挂的角色30、VM和454CF0任务自然返回，PC76推进到96。随后仅按原队列表头复位、arena游标复位、425DE0输入复位、454CF0完整任务的次序推进：延迟参数30实际31次更新、淡入参数45实际46次更新，背景参数60实际62次更新；最后另一次VM就绪查询才解除等待。首次更新在原悬挂任务完成内发生，其后77次完整任务达到就绪。各例累计178次完整任务，无悬挂任务，下一条43尚未执行。没有独立VM、角色handler或动画更新补充根，也没有主机写PC/wait/层模式。

构造时原纹理入口保留十二层原栈，依次为DX、entry、container、container wrapper、extended register、register、image、resource、layer、handler、VM、task；IMAGE的ret8自然回到原资源帧。完整128KiB栈及57项CPU在各阶段核对，任务返回后SEH恢复0。后继普通任务仍冻结世界时钟，未恢复原生外层线程或执行奖励/任务退出。

## 平台及所有权

新增独立本轮助手，冻结旧工具。CRT平台只允许原GYBC和sc001/sc002三个固定相对路径、原只读参数及精确文件大小；有界同时分配上限由4增至6，实际峰值5，容纳两个队列、GYBC数组、肖像文件和肖像数组。新GPU助手仅增加256×512格式25请求。当前32位CRT堆/四锁与GPU、64位GDI宿主及32位客体地址继续按类型区分。

文件由实际ReadFile直接读入CRT助手当前原生堆缓冲，再完整投影到逻辑客体；原调试头/用户区/保护区和88字节数组分别sync/实际整块读回。客体中的原CRT/构造指令和原生OS叶分开报告，不冒称完整原版CRT/C++启动。六区335字节冷CRT域、owner设备/门/几何/测量DC/有界队列仍是继承的明确方法输入，原完整加载器和renderer启动未补齐。

前向冻结后明确补充原槽32容器析构：真实descriptor/Release、原容器/数组清理、清表及两计数恢复仅有前驱资源时的值，再由前驱原姓名/GYBC/队列/锁堆清理收束。测量DC仍为宿主补充释放；字体/bitmap/栅格DC早已自然删除。原生助手正常协议退出，无残留纹理由助手兜底释放。补充析构不计原任务退出，清理后的客体资源不可复用。

## 复核与边界

原始来源报告为analysis/terminal-portrait-source-v6-20261026.json.gz。独立验证完整文件/容器/每行像素、原调试分配/链/保护与DD填充、原API完整ABI及当前原生请求/响应；从已验肖像入口的全部内存和57项CPU开始另起Unicorn，逐原机器码重放构造、IMAGE和每次完整任务，核对各截面全内存、CPU、逐条PC/写入摘要、每帧VM/owner/输入/队列。独立动画规则检查严格延迟/淡入/背景和等待解除顺序。

每例新增2259524条原指令/1506959次原写；两例前向累计9553234条原指令/6630539次写，最终291/292个完整映射和57项CPU。每例新增22次原CRT OS叶、4次当前肖像COM叶、154次实际空串/null IME查询；累计各355次任务查询。两个整块原生分配读回为另记的观察操作，均有独立原生请求/响应。

正式证明analysis/terminal-portrait-proof-v1-20261026.json记录两例当前资源新实例全状态重放通过。36项专项与272项历史回归共308项通过；固定前驱48项及其验收，并递归复核更早原资源、存档、检查点和证据。严格规格归档前32项通过，归档后及Git原始字节一致性另见固定验收清单。

另在两个新实例实际重新创建当前资源，比较全部初始/最终映射、原栈/CPU和累计原摘要。前缀精确GetTickCount重放仍采用采集输入，非新原生时钟连续性。旧验证协议视图只投影去掉新增操作并重编号；真实完整原生序列和新增操作分别核对，原始报告不改。

开发失败v1–v5及诊断原样保留，依次补齐原动画设置4CC3E0、计时设置4C9610、精灵入队4CBDF3、等待查询4CD060和姓名入队末段40911F的允许代码区间。首轮专项把EAX篡改为其合法原值0而未触发拒绝，修正为不同的1234h；原执行结果未改。失败不作为通过验收，未关闭绘制门或替代返回。专项篡改拒绝、相关回归、当前资源全状态重放、递归原资料保全、严格规格及工作区/index/HEAD字节一致性另记固定验收。

复现使用新输出路径：

    PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.terminal_portrait_emulation --out analysis/terminal-portrait-source-NEW.json.gz
    PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.terminal_portrait_verification --report analysis/terminal-portrait-source-NEW.json.gz --out analysis/terminal-portrait-proof-NEW.json
    PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_terminal_portrait

本轮无OS输入或解锁要求。姓名ANSI在ACP936下的Big5乱码未修复。实际draw/Present、后继对白与完整终局、原外层原生调度/加载同寿命、任务退出、奖励及学校交接仍未完成；R3/R4/R5/R6保持进行中，目标2026-11-20不变。
