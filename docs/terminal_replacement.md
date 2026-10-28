# 终局图层7两行替换

本单元为connect-terminal-replacement-dialogue，接续封存的PC198/194 wait1。原资源、存档、私有检查点、旧验收及其字节不改；大型来源保存于本地analysis路径，存储方式见local-evidence.md。

## 原脚本边界

| 分支 | 原命令序列 | 新边界 | 后继未执行 |
| --- | --- | --- | --- |
| neutral_running | 198:43 config4；206:44；210:17 text3；216:17 text4；222:50；226:51 | PC230 wait1 | 43 config7 |
| timeout_before_combat | 194:43 config4；202:44；206:17 text5；212:17 text6；218:50；222:51 | PC226 wait1 | 30，完整四参数7/2/0/30 |

config4的真实模板首字段为7，选中图层7。44只清OBJECT+16h的文字计数，不释放纹理或清空旧record。405160构造目标record时在4051A9调用403730，原Describe/Release后再写入新纹理。

胜利旧组只有一行，替换record0再追加record1；超时旧组有三行，替换record0/1后，count外record2的旧第三张纹理仍然存活。世代按创建wire与record记录，不能按地址复用合并，也不能把count外资源当作已释放。

## 执行与验证

只绑定76/77已采集流的新idle/press/release周期raw256，完整原键盘片段生成A00；heads/arena/input/task四根完整执行，不单独调用VM或文字handler，不写PC/wait或派生状态。新组就绪后进入51，再无输入保持两次完整任务。没有新OS输入，无需解锁屏幕。

两个新DIB地址为3EA00000/3EB00000。原字体参数、ACP936、ANSI字节、真实GDI清底/阴影/前景三阶段及全texel分别独立核对；LockRect原始字节、pitch和未触及padding保留。仅本次来源新增观察记录，原机器码允许范围及代码/IAT、写入守卫与父工具保持一致。

独立验证从真实当前wire核对全CRT/GDI/GPU及原x86、完整映射内存、57CPU、原栈、每帧全域SHA、队列和原指令/写入摘要。固定父只比较forward；本次实际补充清理独立记录，不制造旧清理CPU或累计SHA。补充原清理不代表任务退出。

v1的跨实例比较曾发现末端映射表不同。后续唯一诊断实例与v1全部相等，因此没有取得失败实例的具体差异；诊断同时实测了旧text7_1与新text0复用同一原生LockRect地址。原AddressSpace以全进程native地址为key，驱动是否重发旧地址会影响guest分配序号；这是静态推断与声明反例确认的宿主投影依赖。v2仅把本次两资源路由到overlay-replacement-0/1，仍使用原AddressSpace算法，父overlay域不改。每域固定6个接口身份及1个表面身份；验证器从真实wire和原record独立重建分配顺序与范围，拒绝跨域别名。实际原生指针、原始LockRect/堆/表面字节均保留，不作字节归一化。诊断与边界说明见terminal-replacement-mapping-review-v1-20261028.json，失败记录及v1来源原样保留。

v2的CLI只把新来源的gzip压缩级别改为6，JSON原字节格式与读取方式不变，旧terminal.save及封存文件不改。父回归选择20项静态/守卫检查；完整父前向仍由当前两例原x86集成核对覆盖，不再另跑一套未修改的旧动态语料。

## 实测验收

| 分支 | 新增完整任务 | 累计完整任务 | 全映射区域 | 新增原指令/原写 | 当前存活纹理/创建世代 |
| --- | ---: | ---: | ---: | --- | --- |
| neutral_running | 47 | 449 | 394 | 2883213/1500426 | 9/10 |
| timeout_before_combat | 47 | 396 | 352 | 2322217/1168538 | 7/10 |

两例前向累计32228951条原指令、19173767次原写；均无pending任务。每例60个原COM调用，峰值9/7张纹理，10个创建世代均由原代码实际释放；当前清理根数为13/11。两份新完整原生实例复现全部累计摘要、完整内存/57CPU及实际清理。

新增专项70项、直接相关父单元20项静态/守卫回归通过。固定父76项与验收本体、递归原资产/存档/私有检查点保全另验。大型source及诊断以analysis/terminal-replacement-local-evidence-v2-20261028.json为大小/SHA及备份位置清单，未新增普通Git大对象。


## 复现

使用新名字保留不可变证据：

```bash
.venv-audit/Scripts/python.exe -X utf8 -m tools.terminal_replacement_emulation --out analysis/terminal-replacement-source-NEW.json.gz
.venv-audit/Scripts/python.exe -X utf8 -m tools.terminal_replacement_verification --report analysis/terminal-replacement-source-NEW.json.gz --out analysis/terminal-replacement-proof-NEW.json
TERMINAL_REPLACEMENT_REPORT=analysis/terminal-replacement-source-NEW.json.gz .venv-audit/Scripts/python.exe -X utf8 -m unittest tools.tests.test_terminal_replacement_source tools.tests.test_terminal_replacement
.venv-audit/Scripts/python.exe -X utf8 -m tools.terminal_replacement_preservation --out analysis/terminal-replacement-preservation-NEW.json
```

省略环境变量时专项测试默认读取已验收的source-v2。最终只修正了测试文件的默认报告路径字面量；原生证明所用四个实现模块和全部测试函数体不变，通过逆向替换该字面量重建原测试文件SHA，并另跑默认输入专项验证。原证明文件保持原字节，差异说明见terminal-replacement-test-default-update-v1-20261028.json。

原代码下一确认以后、完整终局、实际draw/Present、原生外层同寿命、其它场景、任务退出/奖励及学校连续性交接仍未完成。Godot未改，R3/R4/R5/R6及2026-11-20目标保持。
