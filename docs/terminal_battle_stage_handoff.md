# 原终局战斗阶段交接

connect-terminal-battle-stage-handoff接续9338d05d封存的两条已选终局任务完成握手（VM PC404/434 inactive/wait0，TASK阶段6/status3，byte[TASK+171]/[TASK+172]均为1，原454CF0同帧自然返回1），在同一当前CRT/GDI/GPU所有者寿命内按原0x4539B0顺序执行五根任务帧40DB90/40DC80/425DE0/454CF0/453F10。原453F10阶段5消费已置位的byte[TASK+171]（454293/45429A，非零触发），清word[TASK+108CC2]并置阶段15（4542A1/4542AD）；阶段15置word[7A4184]=0（45444B）；阶段16每帧415040(MAIN,4)累加，首次达到或超过0xFF（45448D，本输入为0x100）按原dword[TASK+174]分派原4998B0五臂并写[5FF720]（4544DC..454562）；阶段17逐帧原499910至完成（454636）；阶段18置word[7A417C]=0x4FF（454653）；阶段19按214帧×128个原矩形（45470B/454748经410310）及415040(MAIN,6)计时，并在该帧由原0x454793以返回地址0x454798自然调用473860、返回1（454798）；阶段20自然返回1（4547A1）后冻结。未调用独立454CF0或473860根，未跳到阶段20冒充自然退出。0xC臂在原代码中需word[7F4488]==0x2D且结果类型为4/5（4545A8/4545D4/4545E6）；两例实际word[7F4488]=4，守卫对该臂直接拒绝，不预设立场。

确认输入按来源接通而非主机写入：只在原499910动画状态字节ctr[30998+1]实际为2时写入录制流中的原始256字节设备样本到KEYBOARD+12，执行原0x4113D5至0x411CE2生成整A00键盘输出并独立预测MAIN动作字，随后写入录制释放样本；不写PC/wait/阶段/完成标志。文本端点按原帧结构整序核对：349帧中每帧的原input段查询自有空IME、原task段对声明有界字符串调用lstrlenA，共349+349条收据且帧索引连续0至348；三份录制采集段（帧98/99/100）自身不调用文本端点。

## 实测验收

| 分支 | 帧/段 | 结果类型/配置/模式 | 累计完整任务 | 全映射 | 累计原指令/原写 | 本阶段原指令/原写 | 前向存活纹理 |
| --- | --- | --- | ---: | ---: | --- | --- | ---: |
| neutral_running | 349/1748 | 1/2/0 | 762 | 454 | 41677156/24352234 | 10315102/6162429 | 8 |
| timeout_before_combat | 349/1748 | 4/5/2 | 789 | 504 | 42480544/24626831 | 10315157/6162456 | 8 |

两例各349帧、五根×349=1745段加三份采集段共1748段，698条输入端点收据、27392次原矩形、70个原函数进入/自然返回事件；累计入口增量仅result audio play的0x40D390各1次。逐帧全映射/57CPU/队列及原摘要、最终全内存与当前15/18世代、90/108原COM、全部CRT/GDI/GPU字节和所有权核对；完整父全前向与累计摘要不变，两个新完整原生实例复现全部累计摘要。61项专项（45项来源报告/静态守卫及16项原字节静态）与每例复用的父source/protocol/native/prefix守卫通过；父80项清单、验收本体、递归原资产/存档/私有检查点及旧助手原字节保全。

失败与修正记录如实保留：proof v1整体固定父内存（992 s）、v2完整前缀task_APIs（990 s）、v3阶段边界leaf计数（728 s）、v4输入端点集合守卫（1421 s）均真实失败并封存；v5正常完成（7148.44 s），但其运行后三份来源报告测试的测试侧断言经独立复核发现缺陷（过严集合守卫、在无运行进程的测试中比较运行期write_PCs、篡改字节落在比较窗口之外），修正后为保持实现哈希与提交代码一致而不直接采用；v6在fresh_case新建实时D3D8设备时因另一独占全屏程序占用显示，CreateDevice返回0x88760868（D3DERR_DEVICELOST），于2761.08 s真实失败并封存；环境恢复且三设备隔离探针通过后，v7以修正后的同一验证代码（exit 0、normal exit、6867.5 s、开始/结束实现哈希一致）正常完成，正式成功来源采用v7；v5/v6记录不删除。

## 复现

```bash
.venv-audit/Scripts/python.exe -X utf8 -m tools.terminal_battle_stage_handoff_emulation --out analysis/terminal-battle-stage-handoff-source-NEW.json.gz
.venv-audit/Scripts/python.exe -X utf8 -m tools.terminal_battle_stage_handoff_verification --report analysis/terminal-battle-stage-handoff-source-NEW.json.gz --out analysis/terminal-battle-stage-handoff-proof-NEW.json
TERMINAL_BATTLE_STAGE_HANDOFF_REPORT=analysis/terminal-battle-stage-handoff-source-NEW.json.gz .venv-audit/Scripts/python.exe -X utf8 -m unittest tools.tests.test_terminal_battle_stage_handoff_source tools.tests.test_terminal_battle_stage_handoff
.venv-audit/Scripts/python.exe -X utf8 -m tools.terminal_battle_stage_handoff_preservation --out analysis/terminal-battle-stage-handoff-preservation-NEW.json
```

新运行只用新文件名，既有来源/失败记录原字节保留。正式来源实际导入输入及验证代码分别以监督开始/结束哈希绑定；完整原始数据仅本地及仓库外逐字节备份，Git仅收代码、小报告、大小/SHA/位置清单。

仅两条已选终局的阶段5至20交接与0x454793自然473860；后继46B470/432100战斗退出、实际显示、原外层同寿命、奖励/学校、全部候选终局及Godot、R3–R6仍未完成，2026-11-20目标保持。不push；无需OS输入或解锁。
