# 学校课程日期解锁

## 来源与范围

`tools/school_course_unlock_emulation.py`实际执行原映像4A2BA0及4A24A0，白名单分别为4A2BA0–4A2D60和4A24A0–4A2700；仅调试栈检查为桩。4A5A60在4A5CBF调用解锁函数，这是静态调用来源，本工具没有执行完整学校boot。

映像SHA-256为588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005。模板基址74BED0、步长96、ID1..100，字段偏移2/3为月/周，4/6/8为元数据/类别/键，58..77为20教师标记。字段按ID顺序编码为`id:month:week:metadata:category:key:mask0:...:mask19;`，SHA-256 cf7c1a6b640a930e9ce9ccafd339c93ad4178d6683013d8163c9aa77bfdab890。

报告analysis/school-course-unlock-v1-20261006.json SHA-256 bd1c291a452a55652bd6972e08798db522bd8759b7d4d264cab9ae4f8ca81605；纯模块样例prototype/data/school_course_unlock_evidence.json SHA-256 25459ee898bd1278914114aa36ee74a6ec931405ab9dd86bd475d0b8c05b0817。报告包含非栈写集合、入口/执行地址哈希和实际工作缓冲哈希，样例去除执行覆盖字段，保留原指令产生的检查点。原有报告未改写。

## 实际规则

当前短整型日期序号为month×6+week，逐课程ID升序检查：全局标记为零、模板日期已到、类别与键均非零才解锁。ID32类别零，保持未解锁；有效但无教师标记的条目（如100）仍设置全局标记。任何非零标记均跳过，不要求值恰好为1。教师是否在名单或可用不参与判定，教师slot0..19对应外部ID101..120。

每个标记教师调用4A24A0：100条10字节记录中，按既有count将offset0..7从尾向后移一格；offset8/9不复制，留在物理槽。新表头enabled=1、blocked=0、workID=源ID、metadata=模板短整型、progress=0，count加一。多个新课程因此倒序出现在表头。已有进度和阻塞字段只随定义字段移动。重复或回退日期不撤销已有解锁，也不再插入。该函数不登记教师、不推进日期、不刷新4A2980工作视图、不开始授课。

15组样例包含11个日期、已有进度/阻塞/非标准字节及物理槽哨兵、非零标记、连续日期推进/回退和恰好100槽。初始日期、零教师名单、已有记录和全局标记是声明输入。9项Python专项覆盖重新执行逐字节一致、模板与调用字节、阈值/多教师、空掩码/无效模板、头插/哨兵/重复、有限写集合及非目标字段。溢出未在原版执行；纯模块必须预先拒绝。

## 教师来源边界

新局初始化49E930的49EDA8调用4D3E90，参数准备从49ED9D开始，实际16字节为`6aff6a006a65b910117e00e8e3500300`，即登记teacher101、group0、slot−1。随后三个调用登记学生3/4/9。此处只证明原版初始化调用来源，没有执行整个初始化。已有Chapter012教师117证据只执行加入前缀，没有证明当前日期剧情结束。

因此当前回放teacher_count=0是声明场景的边界，不能将其当作完整原版新局事实；也不能直接把101或117塞入已冻结返回目录。后续需完整初始化/教师字段归属与一致的会话迁移，再接编班。课程解锁证据可以先补齐，且不需要用户操作原版。完整学校就绪、实机见证和存档写入权限仍为false。

## 纯数据API

`prototype/sim/school_course_unlocking.gd`提供`unlock_courses(before, rules)`。rules必须包含上述原映像SHA、模板字段SHA及完整100条顺序模板，模型重新编码核对全部日期/元数据/类别/键/掩码；模板病例不作为运行时课程来源。

before必需month（整数0..255）、week（整数0..5）、course_unlocked_flags（101字节值）、course_counts（20个整数0..100）、course_buffers（20组稀疏物理记录）。日期域保证原版短整型month×6+week不溢出，周0保留原版初始化语义，不改为自然日历。每条稀疏记录格式为`[slot, enabled, blocked, work_id, metadata, progress, opaque0, opaque1]`，槽0..99严格升序且唯一；字节字段0..255，三个word字段−32768..32767。全零槽须省略，未提供的槽默认零；记录可包含count之外的物理哨兵。此处是原始缓冲边界，未把历史记录ID/启用值强行解释为合法排课项目。

成功返回supported=true、reason为unlocked或unchanged、after的深拷贝，以及本次升序unlocked_work_ids（也包含有效空掩码课程）。拒绝返回supported=false和reason，不含after；不修改任何输入。先验证全状态，再预检所有教师新增条数，任何投影count>100返回course_capacity_exceeded，避免部分教师已写入而后续溢出。规则错误为unsupported_course_rules，状态格式错误为invalid_course_state。日期、名单、可用标记、旧工作视图和其他附加元数据保持；没有发布当前会话、刷新工作列表或授课。四个权限标记始终false。

7项Godot专项逐一对照15组原指令病例的所有检查点，同时验证容量恰好100与溢出整体拒绝、全部源字段篡改、类型/范围/顺序拒绝、物理尾槽与已有进度、无人教师/空掩码/非零标记、输入/规则/两份输出深隔离及重复状态。

## 验证命令

```bash
PYTHONIOENCODING=utf-8 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_school_course_unlock_emulation -v
```

新报告生成命令必须指定未存在的两个路径；工具拒绝覆盖已冻结输出：

```bash
PYTHONIOENCODING=utf-8 .venv-audit/Scripts/python.exe -m tools.school_course_unlock_emulation --out analysis/new-course-report.json --godot-out prototype/data/new_course_fixture.json
```
