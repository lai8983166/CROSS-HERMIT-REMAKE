# 学校学生移动数据操作

原版4A4680学生分支的37组证据见 `battle_return_audit.md` §76–78。初始教师、班级、四学生排序字段和鼠标输入明确声明；语音、渲染、音效与教师工作表为边界。本模块未接入现有零教师返回演示，学校窗口仍只支持浏览和待命排序。

```bash
.venv-audit/Scripts/python.exe -m tools.school_student_movement_emulation --out analysis/<新的报告名>.json --godot-out analysis/<新的样例名>.json
.venv-audit/Scripts/python.exe -m unittest tools.tests.test_school_student_movement_emulation -v
godot --headless --path prototype -s sim/tests/test_runner.gd
```

`prototype/sim/school_student_movement.gd` 的 `move_student(before, command, profiles, group_rules, sort_rules)` 返回原版拖动函数的即时数据。输入采用教师/班级独立快照，额外带待命排序模式、拖动身份/来源和任务拖动控制；不能直接传入现有CampaignResultState的学校目录。

`command` 包含 `kind="student"`、`student_id`、`source_group`、`source_slot`、`target_group`、`target_slot`、`released`。组范围0–4，源组−1表示待命，此时源槽是当前待命列表索引；目标组/槽均−1表示外部。班级学生槽范围0–3。来源必须同时匹配原始成员和快照的拖动身份/来源控制；老师身份、过期来源、非法目标或非布尔释放输入拒绝。

| 情况 | 即时效果 |
|---|---|
| 未释放、悬停有效教师班槽 | 改选中班和任务拖动状态，保留成员与拖动来源 |
| 待命学生放入空槽 | 从待命移除，目标槽加入，目标原始人数加一 |
| 待命学生替换已有槽 | 原成员回到待命，新成员占槽，人数不变 |
| 班内学生放入空槽 | 来源清空、目标加入，原始人数暂时保留 |
| 班内学生放入已有槽 | 两槽交换；同一槽也按原版处理 |
| 班内学生放到外部或无教师班级 | 来源清空、学生回到待命；人数暂时保留 |
| 待命学生放到外部或无教师班级 | 保留待命顺序，不自动排序 |

有效目标即时重算该班的派生成员/名单索引。其他班的派生字段和部分人数可暂时过时，本模块不偷偷提前修正。有效放入或班内移出会按当前学生排序模式自动整理待命；释放后清空拖动身份/来源并清零任务命令，源语音等级保持。随机语音选择没有移植为数据操作。

后续完整整理必须显式调用 `school_student_movement.reconcile(after, group_rules)`，它复用来源班级清理，并将学生/教师排序模式重置0；待命顺序此时按全局学生名单重建，不等于立即做等级排序。再调用 `school_teacher_group_replay.rate(cleaned, group_rules)` 得到五班评级和完整派生成员。原版这三步在证据中也是独立调用，没有声称鼠标放手必然自动完成整个学校循环。

输入学生1–12、教师117/118，复用已验证的教师/班级及排序规则。全局学生必须一一分配到班槽或待命，教师待命必须匹配未分班教师；原始人数和派生索引必须已经核对。`profiles` 是每位当前学生的职业、等级和七属性，必须完整匹配名单；它们是声明输入，不由记录哈希反推出成长档。实际需要的双向关系缺失时拒绝，不发布半个移动结果。

成功返回深拷贝 `after`、`status`（held/released）及 `execution_scope="isolated_student_movement_data"`。拒绝不返回after，不改任何输入。学校完整初始化、原版交互就绪、实机见证和存档写入标记始终false。日期、总点数、学生记录哈希、有向关系、工作字和无关元数据保持。

新增7项Godot专项对照37组原版即时、整理与评级检查点，验证鼠标持有到释放、拒绝输入、过期名单、目标关系缺失、计数/派生滞后、双向交换、深拷贝与无关字段保留。完整42套件307项通过。原版专项10项通过，报告与紧凑补丁样例重生成逐字节一致；旧冻结资料未改写。

下一步先核对教师移动和4A2980教师工作表，并明确教师进入当前会话的合法来源及目录归属，再设计编班窗口操作。
