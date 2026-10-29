# 终局三行及跨图层对白

connect-terminal-multiline-dialogue接续322b23e5封存的PC256/268 wait1。固定父109项及其验收本体、原资产/存档/私有检查点保持。

| 分支 | 原指令组 | 目标边界 |
| --- | --- | --- |
| neutral_running | 256:43/config4，264:44，268/274/280:17/text6/7/8，286:50，290:51 | PC294 wait1 |
| timeout_before_combat | 268:43/config4，276:44，280:17/text8，286:43/config8，294:44，298:17/text9，304:50，308:51 | PC312 wait1 |

config4选择图层7、config8选择图层5。胜利原44只清count，旧两行由原405160→403730逐记录Describe/Release后重建，第三行原count导出record2。超时两个图层分别重写record0，保留所有其它存活对象及原生所有权。新采集周期沿76/77 idle/press/release原raw256由原键盘代码更新A00，各帧仍为heads/arena/input/task四根；原任务写PC/wait，无新增VM/handler根或主机派生写回。

每次新创建独立typed projection域，父guest地址、顺序和已验FU指针/退役表面绑定保持。原HeapAlloc/LockRect及padding不归一化。使用当前真实GDI、原转换/纹理上传与全表面读回，核对全量当前CRT/GDI/GPU协议及实际原释放。独立引擎保留来源完整PE初始映射、RX/RW权限和快照分区，不过滤事件、不改原计数；父全前向、新阶段全内存/57CPU/逐帧队列/累计摘要及当前清理分别核对。两新完整原生实例另行复现。

正式来源v1完整写入并备份为1,816,900,562字节。首次专项在整份JSON的UTF8解码阶段内存不足，未进入动态验收；当前读入改为有界缓冲流式解析，各字符串/数值仍由标准JSON解码器解释。全部字段、值、原内存/像素字节及gzip原文件保持，仅共享完全相同的不可变长字符串；没有抽样或缩减证据。跨块Unicode/转义/数值/重复键与坏格式拒绝另有标准解码对照测试，失败记录保留。

## 实测验收

| 分支 | 新增/累计完整任务 | 全映射区域 | 新增原指令/原写 | 存活纹理/创建世代 |
| --- | --- | ---: | --- | --- |
| neutral_running | 59/543 | 444 | 3973317/1942124 | 10/14 |
| timeout_before_combat | 38/546 | 461 | 2362354/1215905 | 10/15 |

两例前向累计46787394条原指令、26906392次原写，各57CPU，无pending。当前84/90次原COM、峰值10/10张live、14/15创建世代全部实际原释放，补充原清理根14/14。两个新完整原生实例复现全部累计摘要、全内存/57CPU和当前清理。专项60项及父守卫38项通过，父109项和验收本体、递归原资产/存档/检查点保全另验。

neutral_running各新文字上传非零字节数：[1337, 4761, 3144]；原ANSI/GDI结果原样保持，不据此称实际正确显示完成。

timeout_before_combat各新文字上传非零字节数：[0, 2475]；原ANSI/GDI结果原样保持，不据此称实际正确显示完成。

完整来源及诊断按analysis/terminal-multiline-local-evidence-v1-20261029.json清单保存在本地和仓库外逐字节备份，Git只保存代码和必要小报告。


## 复现

```bash
.venv-audit/Scripts/python.exe -X utf8 -m tools.terminal_multiline_emulation --out analysis/terminal-multiline-source-NEW.json.gz
.venv-audit/Scripts/python.exe -X utf8 -m tools.terminal_multiline_verification --report analysis/terminal-multiline-source-NEW.json.gz --out analysis/terminal-multiline-proof-NEW.json
TERMINAL_MULTILINE_REPORT=analysis/terminal-multiline-source-NEW.json.gz .venv-audit/Scripts/python.exe -X utf8 -m unittest tools.tests.test_terminal_multiline_source tools.tests.test_terminal_multiline
.venv-audit/Scripts/python.exe -X utf8 -m tools.terminal_multiline_preservation --out analysis/terminal-multiline-preservation-NEW.json
```

大型来源和失败诊断保存在本地及仓库外逐字节备份，Git只留代码、小报告及大小/SHA/获取位置。原ANSI/GDI实际字节保留，不补画空白/乱码；实际draw/Present、后继确认、完整终局、原外层同寿命、任务退出/奖励/学校及R3–R6仍待完成，Godot与2026-11-20目标保持。
