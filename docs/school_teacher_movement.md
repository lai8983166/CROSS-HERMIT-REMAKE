# 教师移动与工作列表

本模块实现来源教师117/118的独立移动和工作列表投影，原版证据见 `battle_return_audit.md` §79–81。现有返回会话仍无教师，学校窗口的编班/排课入口尚未开放。

```bash
.venv-audit/Scripts/python.exe -m tools.school_teacher_movement_emulation --out analysis/<新的报告名>.json --godot-out analysis/<新的样例名>.json
.venv-audit/Scripts/python.exe -m unittest tools.tests.test_school_teacher_movement_emulation -v
godot --headless --path prototype -s sim/tests/test_runner.gd
```

生成工具拒绝覆盖已有报告。新实例实际执行原版4A4680教师分支、4A8BF0、4A8B50和4A2980；即时移动、显式4A5F40整理和五班4A95F0评级独立记录。鼠标释放/矩形命中、渲染与声音是声明边界；初始教师班级和工作可用/阻塞标记也为声明输入。

`prototype/sim/school_teacher_movement.gd` 的接口：

| API | 作用 |
|---|---|
| `move_teacher(before, command, student_profiles, group_rules, sort_rules, work_rules)` | 返回原版教师拖放的即时数据，状态held或released |
| `select_group(before, group, group_rules, work_rules)` | 显式选班并刷新该教师工作列表，组−1清空选择/列表 |
| `reconcile(before, group_rules, work_rules)` | 显式完整班级整理，找到可用班时选首班并刷新工作列表 |

输入采用教师/班级与学生移动的独立快照，额外携带 `teacher_work_records`、工作列表计数/当前页/页上限/活动行。它与CampaignResultState目录不同。`command` 字段为kind="teacher"、teacher_id、source_group、source_slot、target_group、released；组范围0–4，源组−1代表待命且源槽为当前教师待命索引，班内教师源槽为−1，目标组−1代表外部。来源必须匹配快照拖动控制和实际名单。

| 动作 | 原版即时效果 |
|---|---|
| 鼠标持有 | 保留成员、选班、工作和拖动来源；仅任务拖动状态置2 |
| 待命教师加入空班 | 从待命移除；目标工作short+6/+8清空；门槛非零时活动置0，否则保持 |
| 待命教师替换 | 原教师回到待命，学生仍在原班，活动保持，目标工作short+6/+8清空 |
| 班内教师移到空班 | 原班学生按槽追加到待命，来源工作清空/活动置1，目标活动由门槛决定 |
| 班内教师交换或同班放手 | 教师交换，学生留在各班，双方工作short+6/+8清空，活动保持 |
| 班内教师移到外部 | 教师和原班学生回到待命，清来源工作/活动并排序学生及教师 |
| 待命教师外部放手 | 不改名单、不排序 |

有效目标选班并实际刷新工作表，但不即时评级班级，原始学生人数和派生索引可能暂时保留旧值。移到空班追加的学生不立即排序；外部移出才按当前学生模式排序。原映像教师117/118的职业、等级和属性排序键相同，教师三种排序都保留输入顺序；本模块不泛化到其他教师。释放清空拖动身份/来源及任务命令；工作short+10/+12、日期、点数、原始记录哈希和关系保持。

`teacher_work_records` 用字符串键117/118对应稀疏记录数组，每条含slot（0–99）、enabled、blocked和work_id；未列出的槽默认零。enabled=1且blocked=0时必须引用原版有效模板。模型按槽号读取，按源category分成三类，输出 `[sort_key, work_id, 类内序号]`，不按sort_key重新排序。可以重复工作ID，不能重复槽号。原映像1–100中有99个有效模板，ID32无有效分类；有效ID100与最多100个槽位是两件事。禁用/阻塞条目不参与列表。

三类分页当前页重置0；条数≤10时页上限0，超过10时截断 `(count-9)/2`，100条上限45。清除选择或选择无教师班级时清空活动列表和分页；原版非活动缓冲尾部并未全部清零，模型不将它们暴露为有效行。源模板字段编码哈希固定为7206ac045306b139a742d678b52ba1c29d602e73245e90cb06774d6801ac651e；修改模板类别/键或教师排序字段会被拒绝。

后续整理显式调用reconcile，再调用 `school_teacher_group_replay.rate`。完整整理重建成员人数/待命并重置学生/教师排序模式；如果没有任何可用班级，原版不会调用选班刷新函数，旧选班和旧工作显示暂时保留。需要清除时必须显式select_group(-1)，不能在即时移动里提前模拟尚未执行的界面处理。

所有输入先验证。拒绝不返回after、不改输入；成功返回深拷贝，范围为isolated_teacher_movement_and_work_data。学生目录必须完整、一一分配且派生索引已整理，教师源位置、工作槽/列表及规则必须一致。当前工作标记不是剧情解锁见证，尚未执行日期解锁4A2BA0、课程选择/执行、教师成长或存档。完整学校就绪、实机及存档权限标记保持false。

新增7项Godot专项逐字段比较52例移动的即时/整理/评级及11例选班/列表输出，另覆盖工作源规则篡改、过期来源、槽重复、无效模板/分页、鼠标持有再释放、旧工作显示和输出隔离。完整43套件314项通过，零失败；原版10项专项通过，冻结报告/导出重生成逐字节一致；现有返回和学生移动模块不变。

下一阶段明确教师进入当前会话的合法来源、工作日期解锁及目录归属，再接入可操作编班界面。
