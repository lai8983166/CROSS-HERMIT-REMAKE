## 0. 九月底跨月

- [ ] 0.1 从九月第 5 周已有存档进入十月第 1 周，核对原版日期路由、剧情和学校状态，验证保存、读取及继续推进。

## 1. 周循环状态机

- [ ] 1.1 创建 `prototype/sim/school_year_loop.gd`，实现五阶段状态机（planning → execution → settlement → story → next_week）
- [ ] 1.2 为每个状态添加进入/退出条件与守卫，防止跳步或重复结算
- [ ] 1.3 编写单周推进测试（10 月第 1 周 → 第 2 周），验证状态转换

## 2. 转职资格判定

- [ ] 2.1 创建 `prototype/sim/school_job_eligibility.gd`，读取 `job_table.json` 并解析转职条件字段
- [ ] 2.2 实现 `calculate_eligibility(student)` 函数，根据职业熟练度、等级、任务完成判定可转职列表
- [ ] 2.3 在周结算后调用转职判定，更新学生状态中的 `job_eligibility` 字段
- [ ] 2.4 编写转职判定测试，对照已知原版案例验证

## 3. 多周累积验收

- [ ] 3.1 创建原版对照工具 `tools/school_year_loop_emulation.py`，执行 10 月第 1 周至 11 月第 1 周的原版规则
- [ ] 3.2 生成对照文件 `prototype/data/school_year_loop_evidence_oct_nov.json`，记录每周结算后的学生快照
- [ ] 3.3 在 Godot 中实现每周快照对比测试，验证属性、技能、关系、职业进度与原版一致
- [ ] 3.4 扩展验收至 10 月至 3 月完整 30 个日历周位（分阶段：10 月、11-12 月、1-3 月）

## 4. 周进度持久化

- [ ] 4.1 扩展存档格式，增加 `current_week`、`job_eligibility`、`accumulated_mvp` 字段
- [ ] 4.2 实现 `save_week_state()` 和 `load_week_state()`，支持周中保存与恢复
- [ ] 4.3 编写存档迁移测试（version2 → version3），确保九月试玩存档兼容
- [ ] 4.4 验证跨周保存/读取：10 月第 1 周保存，读档后继续推进到第 2 周

## 5. 学年循环试玩场景

- [ ] 5.1 创建 `prototype/ui/school_year_trial.gd`，提供从 10 月第 1 周开始的循环试玩入口
- [ ] 5.2 在 UI 中显示当前周、可选课程/冒险、学生转职资格
- [ ] 5.3 接通完整 30 个日历周位流程：按原版逐周区分可操作与剧情推进，并核对实际结算、转职刷新和日期
- [ ] 5.4 验证 3 月第 5 周结算后的边界行为（结束学年或触发特殊事件）

## 6. 文档与验收

- [ ] 6.1 编写 `docs/school_year_loop.md`，记录状态机设计、转职规则来源、对照文件格式
- [ ] 6.2 运行所有回归测试（单周、多周、存档迁移），确保既有功能未破坏
- [ ] 6.3 生成验收报告 `analysis/school-year-loop-acceptance.json`，记录 30 个日历周位的对等验证结果
- [ ] 6.4 提交代码，更新 README.md 说明 M2 完成状态
