# 新局学校来源与独立会话

## 原指令边界

`tools/new_game_school_emulation.py`完整执行49E930及实际名单重置、4D3E90登记、学生点数/技能/解锁、关系复制和事件辅助函数，再显式执行4A2BA0课程解锁、4A5F40班级整理/真实4A2980工作表及五班4A95F0评级。每次有指令数、时间、返回地址和栈检查；初始化及准备分阶段使用不同有限写入守卫。

原映像SHA-256为588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005。学生0..44在进入函数前从6F5088+ID×1184的原模板复制到7E17E8+ID×1184，这是声明的源模板加载输入，前驱加载器没有执行。初始化memset是只接受(7A50E8,0,306D4)的明确边界；另外只有调试检查是桩。完整初始化函数执行不等于完整新局/剧情/学校菜单执行。

49E930在49EDA8/49EDB8/49EDC8/49EDD8分别实际登记101/3/4/9：教师101在班0、slot−1，学生在班0的slot0/1/2。日期4/0，difficulty1，总点数0，reset_groups1。原始学生40槽、教师20槽尾部是零，不是旧回放的−1；导出同时保留原始缓冲，将非活动目录20槽映射为−1供纯班级模块使用。

班0初始化原始人数仍0，但原始学生ID和派生ID/索引已经填3/4/9、0/1/2；五班活动初值1。后续整理才将班0人数设3、活动0、选中班0和reset0。评级得到班0state3、关系均值65、档位5，其他班state0。4月第0周有效无教师掩码课程可设全局解锁，但教师课程计数均0。

## 教师与学生资料归属

教师101的职业1、level_50为0、七属性全1，来自不可变6F5088教师模板；它不占用学生持久记录7E17E8+101×1184。学生模板加载到学生记录后，4D3E90会重算level_50：成长点数加status3/5/6技能的来源费用，经4D5590来源等级阈值计算；difficulty1使装备技能设为status6。学生3模板level_50=45，实际登记后31，学生4/9分别8/7。因此纯构造必须由点数/技能规则计算，不能直接抄模板等级。

源规则包含4个验证过的调用参数、4个成员模板哈希/职业/属性/等级、12条原始有向关系、三学生成长点数/技能状态/装备技能，以及50等级阈值和84技能费用。编码顺序为调用字段`call_va:member_id:group:slot;`，竖线，成员`member_id:job:level:七属性:storage_kind:template_sha;`，竖线，关系`from:to:value;`，竖线，学生`member_id:七成长池:84状态:八装备技能;`，竖线，阈值冒号连接，竖线，费用冒号连接。源字段SHA-256 d06bdeb2e5951237481a121d0ccec4b46db3e3f9c5509622d19a5b9444a08f76。期望初始化/准备快照不作为运行时输入。

## 回放与限制

报告analysis/new-game-school-v1-20261006.json SHA-256 9536cfc4642a9e269fd23b4d0bf73b0668098c415f48fee23c2f5b8763bf186f；Godot样例prototype/data/new_game_school_evidence.json SHA-256 552dcec9291a5e8223aaeb7c53709fc7b4ebe7dead77993845808c9e33586e7d。8项Python专项通过，重新执行报告/导出逐字节一致。

三组病例覆盖零状态、A5脏状态，以及准备后人为改课程再重新初始化。每组保存初始化、解锁、整理和评级检查点；重复初始化清除课程/班级，但不重置函数外部的selected_group，已有0会保留。纯构造接收显式工作区选择−1或0，新会话默认−1。待命/选择/工作视图缓冲在函数外声明为零，不冒充49E930初始化效果。

报告保留每次写入实际守卫，导出确定的8058项初始化非栈写次数、顺序哈希、合并地址范围、实际入口/地址哈希、memset边界、成员记录哈希及加入入口调用来源。模块只移植学校字段与所列成员资料；完整学生包/道具/成长结构虽在CPU执行，未声明全部移植。现有返回演示保持零教师冻结场景，未插入新局教师。完整学校就绪、实机与存档权限均false。

## 来源构造与会话API

`new_game_school_origin.construct(origin_rules, selected_group=-1)`只读已验证源字段，重新编码绑定源字段SHA，按四条登记调用构造学校字段，并从原成长/技能资料计算学生等级。selected_group仅接受原指令病例核对的−1/0，表示函数外工作区状态。返回after深拷贝；非法源、类型、调用顺序、关系、点数/阈值或选择值拒绝且无after。原始尾零与规范目录尾−1同时保留。`group_rules()`返回单独的新局101规则域。

既有`school_teacher_group_replay`只在teacher_scope=new_game_initializer、49E930及源字段SHA一致时允许教师101；旧Chapter012规则继续只允许117/118，旧`TEACHERS`与`_domain`保持。新局规则也不能调用旧117登记接口。名单、原始/派生教师、待命和关系两端均检查各自规则域，避免把允许101扩散到旧移动规则。

`new_game_school_session.initialize(origin_rules, course_rules)`创建独立会话，只有源规则字段及各行白名单被保留，嵌套expected_after等字段也被丢弃。校验初始化和课程规则全部成功后才发布revision1及initialize日志。相同输入重复初始化返回duplicate且保留现态；不同输入返回school_origin_input_conflict，无发布。当前返回CampaignResultState不被修改。

`prepare_school(expected_revision)`仅接受当前整数版本；过期、浮点、布尔、未初始化调用拒绝。按课程解锁、班级整理、评级预计算全部三步，全部成功才发布单个revision2及三个顺序日志；中途缺关系等失败不发布任何部分状态。prepared后以当前版本重复调用返回duplicate。`school_data_prepared`说明数据准备完成，完整原版school_initialized/interactive_school_ready/live_witness/存档权限仍false。

`read_snapshot()`、`journal()`及`read_teacher_profile(101)`返回独立深拷贝，教师资料明确是静态源模板；无其他教师来源的ID拒绝。多会话互不共享可变数据。该会话尚无编班移动或排课操作，下一步扩展101移动规则并接独立新局学校窗口。

## 验证

```bash
PYTHONIOENCODING=utf-8 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_new_game_school_emulation -v
godot --headless --path prototype -s sim/tests/test_runner.gd
```

生成新报告必须使用两个尚未存在的路径，工具拒绝覆盖输出：

```bash
PYTHONIOENCODING=utf-8 .venv-audit/Scripts/python.exe -m tools.new_game_school_emulation --out analysis/new-origin-report.json --godot-out prototype/data/new_origin_fixture.json
```
