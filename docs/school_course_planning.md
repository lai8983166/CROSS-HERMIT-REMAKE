# 班级课程安排

## 原指令来源

`tools/school_course_planning_emulation.py` 执行4A3CA0模式菜单、4A2DA0课程点击和实际4A8BC0选择班级读取，操作后另行执行五班4A95F0评级。仍使用完整来源新局初始化；日期4/4、6/5、11/5为明确输入，课程由实际4A2BA0/4A24A0解锁，不表示执行了日历/剧情推进。

教师101在4/0和4/1都无课程，最早4/4解锁10/11/12。课程视图按物理槽次序构造：4/4初级列表为课程12、11、10。完整晚期列表有9项初级、4项中级、1项高级，无合法第二页；端口拒绝越界页和行，不仿造无效原版调用。

菜单1..5设置对应班activity=0（冒险），6..10设置activity=1（授课）；adventure_gate非零时授课被强制改回0。模式切换保留已安排课程。授课模式点击有效课程，将类别、类别内key−1、workID和列表序号写入班级offset6/8/10/12；仅悬停、冒险模式或空类别不写入这些字段。课程详情控件另有显示输入边界，鼠标按下位为命中结构pointer+4。

已验收v2报告 `analysis/school-course-planning-v2-20261007.json` SHA-256 `1625070008f0e98a4a8f33cd00776a8c10dfb213be38d8e2baa0fc7e61905edd`；Godot期望 `prototype/data/school_course_planning_evidence_v2.json` SHA-256 `35105cc34933d63ac650537cc6bc9df1ac937e98e4e04182ab3f0250bffc867e`。15案例分别记录操作与评级，原成员资料/名单、关系、点数、日期与课程进度均不由安排操作改变。最初鼠标输入草稿按下位错误，未验收v1已移至临时目录，不作为来源期望。

## 纯模块

`SchoolCoursePlanning.set_mode(before, group, teaching, group_rules, work_rules)` 支持有教师班级的来源模式切换。

`select_course(before, {group, category, row, page, clicked}, group_rules, work_rules)` 只支持已整理教师课程视图中的有效选择。before附带course_category、detail_work_id、detail_previous_work_id及既有教师工作/班级字段。严格核对当前班级/类别/页、记录阻塞状态、源模板和重新计算的课程列表；冒险、无教师、空类别、过期视图或越界输入拒绝且不修改before。返回深复制，四个原版权限标记保持false。

模式、选择与评级不执行授课完成、学生成长、周结算或原版存档。

```bash
PYTHONIOENCODING=utf-8 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_school_course_planning_emulation
```
