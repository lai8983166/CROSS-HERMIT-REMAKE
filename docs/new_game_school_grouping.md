# 新局编班

## 来源移动

`tools/new_game_school_movement_emulation.py` 在同一隔离CPU执行完整49E930初始化、课程解锁、整理和评级，再连续执行20次教师101/学生3/4/9移动。源模板加载、鼠标命中/松开和声音/头像仍为明确边界；没有要求用户操作原版。

每次记录4A4680移动、4A5F40整理及五班4A95F0评级，保留中间人数/派生位置暂时不同的结果。只允许班级、待命、拖动及工作视图缓冲写入；角色、名单、日期、点数和课程记录保持不变。教师移至空班会让原班全部学生退回待命；无教师的学生目标按原版视为班外。

冻结报告 `analysis/new-game-school-movement-v1-20261006.json` SHA-256 `3e8ac9cdfb977a3b81cbf029357f5a2b9ac1f56c9cbf4c466574cfdc7871ae2b`；Godot期望 `prototype/data/new_game_school_movement_evidence.json` SHA-256 `a249010e146052764b36ef698e0ced005a31d885184acb15592af1540727843c`。这些是测试期望，运行时只允许来源规则输入。

教师纯模块按班级规则选择域：原有Chapter012域只接受117/118；新局域只接受101，工作规则额外绑定初始化字段指纹，静态教师资料为job1、level0、七属性1。旧规则和报告保持原样。

```bash
PYTHONIOENCODING=utf-8 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_new_game_school_movement_emulation
```

20个连续案例包含等待/班级来源、学生空位/换位/替换/班外/无教师目标、教师空班/班外/同班、等待无效目标，以及两个未松开探针。未松开探针单独取证；会话用户操作将只提交松开后的逻辑移动。没有新增教师交换证据，因为新局只有教师101。

## 会话操作

运行时仅加载 `prototype/data/new_game_school_rules.json` 的来源初始化/课程/排序/教师工作规则，不加载期望快照。文件可由 `tools/new_game_school_rules.py --out <新文件>` 从原映像重新导出。来源规则未知字段逐层去除，已知字段的指纹/资料和职业类别哈希严格核对。

`NewGameSchoolSession.initialize(origin_rules, course_rules, movement_rules)` 保留两参只读会话用法；第三参提供 `sort_rules`、`work_rules` 后允许操作。初始化与 `prepare_school(1)` 仍分别是版本1/2，原有来源快照不新增拖动字段。

`move_member({kind, member_id, target_group, target_slot}, expected_revision)` 只接受逻辑目标。kind为student或teacher；班外target_group为−1，班内为0..4；教师target_slot必须−1，学生班内为0..3、班外为−1。源位置、待命索引、关系评级、学生资料、教师工作记录均从会话自身推导。

会话先完整计算移动→整理→评级，再发布一个版本和三条分阶段日志；日志使用规范学校字段，临时拖动控件不会泄漏到持有快照。无状态变化返回duplicate，不增加版本/日志。过期版本、无资料成员、额外源字段/after字段及无效目标全部拒绝，任何拒绝不会部分发布。所有读取和返回对象均为深复制；仍不操作原版存档。
