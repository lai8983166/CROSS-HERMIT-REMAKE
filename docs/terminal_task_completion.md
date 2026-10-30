# 原终局任务完成握手

connect-terminal-task-completion接续f73a06cd的已停VM，PC404/434 inactive/wait0，TASK阶段4/status2。当前CRT/GDI/GPU所有者继续有效，通过原40DB90/40DC80/425DE0/454CF0四根帧执行资源释放及完成标志。

原454EE0循环10至88并跳过20，78次41F4E0按各组真实pointer/count析构54h记录，再原删除数组/清slot。组20继续保留；存活纹理由实际原执行决定。阶段5由原TASK+4C分支产生171/172、status3并自然返回，不执行后继453F10消费者。

来源和独立重放分别记录全内存/57CPU/队列及所有原调用入口/自然返回。Replay初始化/清理机器算法保持；原完整execute AST只适配两个观察payload、增加资源表写观察及本阶段零输入的分段合同，四处之外必须完全一致；Replay另强制2帧0绑定，无原指令/写事件裁剪。补充清理根从固定父方案及当前完整最终内存独立推导，仅跳过已被前向原循环清零的容器，保留原跳过依据，不投影父cleanup CPU/SHA。

## 实测验收

| 分支 | 新增/累计完整任务 | 映射区域 | 新增原指令/原写 | 阶段/status/返回值 | 前向存活纹理 |
| --- | --- | ---: | --- | --- | ---: |
| neutral_running | 2/762 | 452 | 27126/21534 | 6/3/1 | 8 |
| timeout_before_combat | 2/789 | 502 | 27126/21534 | 6/3/1 | 8 |

两例各完成78次原资源组调用，组20未调用且整slot保持；阶段5自然产生171/172=1并返回1。全部全映射/57CPU/队列及当前15/18世代、90/108原COM、CRT/GDI/GPU完整协议和每个实际释放核对。实际补充原清理12/12根，只跳过前向已清空容器，完整原始依据保留。

57项专项、18项父守卫通过，两个新完整原生实例复现全部累计摘要/全内存/CPU/实际清理；父69项及验收本体和递归原资产/存档/检查点保全。大原始证据依analysis/terminal-task-completion-local-evidence-v1-20261030.json仅存本地及仓库外逐字节副本，Git只收小报告和代码；v1/v2调试终止、v3监督迟加载检查失败及文档命令误启动均明确不计成功来源。


## 复现

```bash
.venv-audit/Scripts/python.exe -X utf8 -m tools.terminal_task_completion_emulation --out analysis/terminal-task-completion-source-NEW.json.gz
.venv-audit/Scripts/python.exe -X utf8 -m tools.terminal_task_completion_verification --report analysis/terminal-task-completion-source-NEW.json.gz --out analysis/terminal-task-completion-proof-NEW.json
TERMINAL_TASK_COMPLETION_REPORT=analysis/terminal-task-completion-source-NEW.json.gz .venv-audit/Scripts/python.exe -X utf8 -m unittest tools.tests.test_terminal_task_completion_source tools.tests.test_terminal_task_completion
.venv-audit/Scripts/python.exe -X utf8 -m tools.terminal_task_completion_preservation --out analysis/terminal-task-completion-preservation-NEW.json
```

新运行只用新文件名，既有来源/失败记录原字节保留。正式来源实际导入输入及验证代码分别以监督开始/结束哈希绑定；完整原始数据仅本地及仓库外逐字节备份，Git仅收代码、小报告、大小/SHA/位置清单。

仅两条已选终局任务握手，后继战斗退出/实际显示/原外层同寿命/奖励学校及Godot、R3–R6未完成，2026-11-20目标保持。不push；无需OS输入或解锁。
