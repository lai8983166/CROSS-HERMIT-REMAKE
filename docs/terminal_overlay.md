# 原终局覆盖层资源与首次正常工作等待

2026-10-26，connect-terminal-overlay-resources。接续3307b3fe；每例重新创建战斗对象并实际生成终局请求，不装载战后快照或修改旧检查点。

## 连续执行结果

中性首帧胜利和第三帧战斗前超时两例，均在原世界/事件生成选择1/4后完成两次原输入复位、454CF0任务、453F10阶段及世界/事件。第三任务自然执行167、PC0→8，再沿4D29E0→4D2CA0→407870取得当前组20/索引0，执行覆盖层原入队和临时包析构，VM与完整任务自然返回。

后继两次完整任务执行指令8与117：指令8的关系1为相等，变量0由167写1，与立即数1相等，因此PC8直接跳44，跳过166和11。117从PC44前进52并设置原WORK等待；同一完整任务的497AA0已更新一次，原浮点转整数步长648，淡入值648、剩余59、活动1/状态1、VM+92E0=1。本单元在此完整任务返回后冻结，未宣称等待已解除。

每例共5次完整454CF0自然返回、3次覆盖层查询和入队，无新增独立VM或117处理器根。暂停后时钟分别保持35999/1与0/3；PC、等待、分支与计数均由原指令产生。运行期主机put仅用于明确根参数栈，专项真实资源运行拒绝其它put写入。

## 当前资源与所有权

原加载路径将 data/adv/bin/Gybc_00.bin 注册到20（14h）。安装原文件524312字节，SHA256为558b9530e36bb9970af3f0ea92df8031893132a4c85a94d9d879ecb192b256af。容器头、唯一偏移12、12字节DX2头及512×512个16位像素独立解析。

原42AE20/42AC50实际只读打开、分配、ReadFile及CloseHandle；原416790→4167E0→41F090/41F0E0分配向量，原构造器、IMAGE/DX加载和512次原逐行复制均执行。原403BD0和当前COM叶创建512×512、格式25、单层managed纹理，原LockRect/UnlockRect上传后整表面GPU读回。全部524288像素字节与原文件偏移24后内容一致，无历史COM回执或旧句柄复用。

原40D970绑定当前绘制所有者/设备；40DB10建立4096组表头，40DBF0建立65536字节有界arena；后继帧明确调用原40DB90/40DC80复位。图层51头指向唯一92字节命令，尾链0；四角坐标、UV、颜色FF808080、IMAGE指针和全部保留字节独立预测，余下表头和arena未用尾部逐字节核对。查询后的完整128字节原包也独立核对。

这是明确资源初始化方法：从已验冷.data投影六区335字节CRT域，当前客体原57B9D0/576F60建立新堆/四锁；独立原根完成文件、纹理和队列初始化，未称完整原场景加载器或渲染器启动连续执行。owner设备字段、绘制门1和256×256尺寸为首根前方法输入，设备/尺寸来自当前实际隐藏D3D8助手。4096表头及64KiB容量也是声明输入，不称原默认1MiB完整初始化；没有关闭绘制门跳过依赖。

64位宿主、32位客体、x86 CRT助手和x86 D3D8助手分别记录。当前文件句柄、堆、锁、接口和表面地址仅在平台叶作类型/角色投影；CRITICAL_SECTION的DebugInfo、OwningThread、LockSemaphore身份明确投影，原计数/状态保持实际值。OS校验、读取或释放前同步整个实际堆缓冲。这是同一逻辑实例的原指令与当前资源连接，不是原版进程同寿命外层调度。

## 清理和验证

前向冻结后另声明原41F4E0(20)补充根，完成descriptor/Release、IMAGE/向量析构、原链摘除/释放及清表。两队列缓冲由原428AD0补充释放，再原576FA0/57BA60销毁四锁/堆；两个原计数恢复各自保留基线，无全局清零。两助手正常退出并确认资源全释放。补充清理不计终局任务退出；清理后对象不能作为存活检查点复用。

来源为 analysis/terminal-overlay-source-v13-20261026.json.gz；两例累计2000408条前向原指令、1361392次原写入。每例72次当前CRT Windows叶、9次实际空字符串/null IME叶、6次当前COM叶（含补充descriptor/Release）。证明为 analysis/terminal-overlay-proof-v3-20261026.json：独立像素/记录/包/队列/分支/等待规则，以及新实例重新建立当前资源后的全216映射、57项CPU、原摘要、任务/原栈和加载后全内存重放一致。

冻结前驱36项及固定验收，递归原资源/存档/检查点保全；专项、相关历史回归和严格规格另存验收产物。开发失败和模型诊断保留，不计成功验收。

复现命令（每次使用新的输出路径）：

    PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.terminal_overlay_emulation --out analysis/terminal-overlay-source-NEW.json.gz
    PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.terminal_overlay_verification --report analysis/terminal-overlay-source-NEW.json.gz --out analysis/terminal-overlay-proof-NEW.json
    PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_terminal_overlay

当前隐藏设备可创建并上传/读回，无键鼠输入或解锁。实际draw/Present未执行，入队不能代替真实终局显示。下一步在新有效寿命重跑本前缀，继续剩余59帧WORK等待及后续VM；完整表现、其它终局资源/文字/精灵/声音/确认、原外层线程/调度、任务退出、奖励和学校交接仍待验。R3/R4/R5/R6整体未完成，2026-11-20目标保持。
