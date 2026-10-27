# 原终局层7整组对白资源

2026-10-26开始，2026-10-27继续验收，`connect-terminal-panel-dialogue`。接续已封存的PC142/wait0原CreateFontA入口，在同一当前CRT/GDI/GPU寿命内完成层7一组原对白、完整任务、显示就绪及新的确认等待。

## 原脚本与记录

真实T0004段2的本组是142的17/text1，148的50，152的51，下一条156为30。段11是142/148/154的17/text1/2/3，160的50、164的51，下一条168为43。本轮不跨新的确认；两次无输入完整任务保持156/168的wait1。

本组均无op44，原4CAD2D..4CAD77按OBJECT+16h的WORD计数定位`OBJECT+28h+count*110h`，4CAD94..4CADA2递增计数。层7对象与旧层5首句对象不同，三行各有独立纹理记录并存，不能套用school第四句先清层再替换的路径。旧GYBC、姓名、肖像及层5首句四纹理继续存活，当前助手既有十张容量足够五/七张峰值。

## 方法与验证边界

从原挂起EIP/ESP连续恢复，第一段不设新根，直到原454CF0自然返回。后续仍只调用原队列表头/arena复位、请求复位和完整任务四根；PC、wait、文字计数和派生键位由原指令产生。沿用已验采集后的松开状态，不发送新的OS输入，无解锁要求。

每行复用当前NativeGDI及测量DC，给真实DIB单独的新映射，执行原字体、清底/阴影/前景三阶段、原两带转换及实际纹理上传/整表面读回。每行完成后另读回旧四纹理，最终再读回全部存活新纹理。补充原403730逐record析构后才执行前驱四资源清理，不计任务退出。

原字节与字体保持。本机ACP936的ANSI效果单独观察，不能根据Big5文本意义补画或换字节。主Agent独立GDI实验在原宽高0、字重400下测得胜利text1为80×20，转换全零；超时三行为280×20、100×20、380×20，转换非零字节2654、668、3489。主来源审查已把本轮实际原调用参数、三个阶段和全部texel与这份独立实验逐字节比较一致。仍不称可见正确对白，ANSI/Big5编码未修。

新增每段保留57CPU与原PC/写入摘要，每帧全区域重新读取SHA并保留完整队列；资源/就绪/确认等关键边界保留全hex内存及原栈。前驱固定时钟用于保证PC142全部guest字节/CPU/累计摘要与已封存父来源相等。原始当前CRT/GDI/GPU身份和回执另核验，不以历史证明代替当前平台执行。

本轮不新增旧终态清理CPU或累计SHA投影；固定父guest前缀与新增局部摘要分开验证，全累计摘要另由完整新当前资源重放复现。不得声称仅从父hexdigest续算出新的累计SHA。

固定前缀不把不同原生堆的未初始化输入强求相同。实际HeapAlloc(flags0)初始buffer完整绑定本轮真实CRT回执，并独立执行原CRT构造核对原写入、CPU及中间边界；PC142全部拥有字节/57CPU/累计原摘要仍与父来源相等。内容寻址库的父两页仅被旧final_state/terminal_state/VM/pages/0、/4引用，新终态会替换它们；所有前驱中间页保全，当前所有blob及实际page引用按SHA/长度核验。开发期诊断保留，不改原始报告或把任意堆字节当成可屏蔽的身份。

资源初始化的独立夹具从首snapshot及首资源根的57CPU执行原8根，核对各根CPU/原计数、全部实际原写域/API输出、新映射、CRT六区及MAIN的资源结果；不声称重新执行了此前战斗或恢复完整战斗后栈。三处分配的末对齐padding分别12/12/4字节，原debug allocator没有覆盖它们，也须保留当前平台原字节并核验，不能统一归零。肖像的两处分配另经既有独立原IMAGE构造执行器核对。

开发期另发现旧的孤立文字时序模型未包含真实4CBF00绘制路径写入record的owner、坐标、颜色、alpha及图层元数据，也未表达其返回AL=1；本轮按原指令补齐独立模型后仍比较整个AB8字节文字对象，不据差异修改游戏代码。Windows会复用已销毁的GDI句柄，相同GetStockObject回执也可在多行重复，独立验证按实际叶调用区间和顺序归属各句，保留完整IAT、栈参数和回执核对。

首轮60项专项中，截短清理快照的负向测试发现冻结比较器在相同前缀的短hex上抛出StopIteration。仅本轮验证器增加每个区域hex实际长度与声明bytes相等的检查，保留原比较器及测试断言；失败v1原日志留存。

首轮新资源证明实际完成胜利PC156后，在前驱肖像所有权表的元数据比较处拒绝，未生成证明文件。运行中的CRT分配表以整数guest地址作键，JSON报告将同一键编码为字符串；本轮只统一这种键编码，并拒绝编码碰撞及不支持的键类型，全部值、内存与回执hex不变。主独立合成元数据检查见`analysis/terminal-panel-dialogue-json-key-review-v1-20261027.json`，不将该夹具冒充原游戏执行；失败证明及观察器原日志保留。

另一次运行没有留下正常退出记录或最终证明，未作验收；其原日志也保留。后续由主Agent独立后台监督进程调用未修改的公开验证CLI，记录实际Python PID、创建时间、命令、正常退出码及最终输出SHA，避免把会话结束当成验证完成。

## 实测来源与任务

| 分支 | 新增完整任务 | 累计完整任务 | 原区间 | 最终映射 | 新增原指令 | 新增原写入 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 中立首帧胜利 | 30 | 290 | 118 | 299 | 1,205,575 | 694,736 |
| 战斗前超时 | 54 | 314 | 218 | 320 | 2,598,194 | 1,329,614 |

各例第一新增完整任务补完父pending任务，之后29/53次新的完整任务调用；最终无pending任务。胜利frame26原50清wait，27进入新确认，28/29保持；超时frame50清wait，51进入新确认，52/53保持。多行间隔由原12节拍及全部就绪判定产生，不能按单句26次等待硬编码。

两例前向累计19,387,522条原指令/12,210,497次原写入。新每行27次GDI/字符串叶和4次原COM叶，实际GPU原始协议55/79项，峰值5/7张当前纹理；每句完成和终点四旧资源读回、新行全表面读回及原释放均记录。

前向冻结后分别补充执行9/11个原清理根，独立重放29,793/30,091条原指令及26,468/26,616次原写入；每个新record的清理前后完整内存/57CPU与实际native缓冲核对，纹理和游戏字节计数回到保留基线。该补充清理不解除新的确认等待，也不计原任务退出。

来源`analysis/terminal-panel-dialogue-source-v1-20261026.json.gz`为434400806字节，SHA256 `d2be32fc2c14d47f4824aa456956c568f7cf86bc9adbf6b8a3207a692074edd3`。主独立像素与原脚本/record反汇编在`analysis/terminal-panel-dialogue-main-raster-review-v1-20261026.json.gz`；最终稳定实现的主来源/调用栈/整表面与验证范围复核在`analysis/terminal-panel-dialogue-main-review-v3-20261027.json`，绑定四个当前实现SHA、完整smoke-success-v3及JSON键主审证据。62项专项v3自然退出0；39项确认及355项相关历史回归分别通过，共456项。

最终独立证明`analysis/terminal-panel-dialogue-proof-v2-20261027.json`为19063字节，SHA256 `7f1a8df210b6cc9fe7bbff76a8756000d083faba79543671d75c8b2c65082f7b`。两例各从原完整前驱流程创建新CRT/GDI/GPU资源，全初末内存、57CPU、全部关键边界/逐帧全域/队列及完整累计原摘要复现一致，实际新边界的9/11个原清理根亦通过。来源与证明的实际Python正常退出0分别见source-process-review-v2、proof-process-review-v2；新后台启动身份记录在proof-process-start-v1，运行期原日志均保留。最终封存与逐文件字节清单以`analysis/terminal-panel-dialogue-acceptance-v1-20261027.json`为准。

最终新资源证明完成后，`analysis/terminal-panel-dialogue-preservation-v3-20261027.json`再核对固定父42项、父验收本体及递归原资产/存档/检查点/历史报告，全部通过；总规格和属性文件仅有本单元允许的更新。

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.terminal_panel_dialogue_emulation --out analysis/terminal-panel-dialogue-source-NEW.json.gz
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.terminal_panel_dialogue_verification --report analysis/terminal-panel-dialogue-source-NEW.json.gz --out analysis/terminal-panel-dialogue-proof-NEW.json
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_terminal_panel_dialogue
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.terminal_panel_dialogue_preservation --out analysis/terminal-panel-dialogue-preservation-NEW.json
```

所有输出使用新文件名，历史来源、失败诊断与已封存验收不覆盖。较大的来源、独立重放及专项分时执行，避免同时装入多个完整报告。

## 交接

原冷CRT六区335字节、设备/绘制门/几何、测量DC和有界队列等方法输入沿用；它不是完整原加载/外层线程同寿命连接。实际draw/Present、下一确认后的角色/命令、完整终局、退出/奖励和学校交接继续待验，Godot未改，R3/R4/R5/R6及2026-11-20目标保持。
