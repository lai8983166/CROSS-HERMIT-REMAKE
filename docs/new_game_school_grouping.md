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
