# 教师登记与班级数据

本阶段完成独立数据模块，不改变现有返回演示。原版证据见 `battle_return_audit.md` §73–74，26组输入来自 `analysis/school-teacher-group-v1-20261006.json`，对应测试样例为 `prototype/data/school_teacher_group_evidence.json`。

```bash
.venv-audit/Scripts/python.exe -m tools.school_teacher_group_emulation --out analysis/<新的报告名>.json --godot-out analysis/<新的样例名>.json
.venv-audit/Scripts/python.exe -m unittest tools.tests.test_school_teacher_group_emulation -v
godot --headless --path prototype -s sim/tests/test_runner.gd
```

生成工具拒绝覆盖已有报告。使用经SHA核对的原版映像及实际Chapter012脚本；教师、学生、班级槽和关系初态为声明输入。原版4A2980工作表选择边界由桩替代，没有执行实际拖放命令4A4680。

`prototype/sim/school_teacher_group_replay.gd` 提供三个纯函数，成功返回深拷贝的 `after`，失败仅返回原因，不改调用方输入：

| API | 输入和作用 |
|---|---|
| `register_teacher(before, context, rules)` | Chapter012加入前缀登记教师117；直接辅助函数变体可同时登记指定班级教师和名单索引。可用教师再次调用不重复登记，也不移动位置。 |
| `reconcile(before, rules)` | 重建教师/学生待命名单，清空不可用教师及其学生、不可用学生、后出现的重复学生槽；重置工作字，保留无关字节。 |
| `rate(before, rules)` | 对已经清理的班级重建成员ID/名单索引，返回五班状态、双向关系平均值、等级和有定义的工作字段。 |

`before` 使用本阶段独立快照：121项可用标记、20槽学生/教师名单、5×28原始班级字节、派生成员/索引、待命名单、当前班级、工作控制与有向关系。它与现有返回目录的学校快照不同，不能直接互换。规则必须匹配归档的原映像SHA、Chapter012 SHA、opcode144、脚本文件偏移20及评级阈值。

当前移植域是学生ID1–12、教师117/118；教师加入仅支持已取证的117。虽然原版教师ID从101起，本模块未宣称支持完整教师目录，也不把教师作为学生成长档。全局名单和可用标记必须一致，活动名单无重复、剩余槽为−1；重复班级教师拒绝。原始班级可包含待清理的不可用成员和重复学生，由 `reconcile` 处理；`rate` 拒绝这些未清理输入。关系为不同成员之间1–100的有向数值，拒绝重复关系和未知身份，评级必须有全部实际成员配对。

好感矩阵使用教师外部ID−55，例如117映射62。教师及学生的所有有向不同成员配对参与平均，截断后按16/31/46/61/76/91分为1–7级。评级状态0无教师、1无学生、2已选课程、3课程未选、4已选冒险、5冒险未选；仅2/4返回四个工作字，其余状态返回空数组，原版未初始化栈值不作为有效数据。

日期、总点数、学生记录哈希和其他不参与计算的元数据原样保留。它们的保留不能证明整个原版内存或存档兼容。成功和拒绝结果的 `school_initialized`、`interactive_school_ready`、`live_witness`、`authorizes_persistent_write` 均为false；成功结果的范围明确为 `isolated_teacher_group_data`。

新增7项Godot专项逐字段核对全部26组登记、重复登记、清理及评级检查点，覆盖拒绝输入、源规则、待清理状态、缺失双向关系、未初始化工作字和深拷贝隔离。完整41套件300项通过。现有学校页面仍仅支持浏览与待命排序；开放编班前还需要取证实际移动命令、教师工作表，以及教师进入当前会话的合法来源和目录归属。
