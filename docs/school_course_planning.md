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

## 持有会话

`initialize_course_example(origin_rules, course_rules, movement_rules)` 仅在独立空会话中建立4/4课程示例；不接受任意日期或外部快照。先完整计算候选状态，再发布初始化revision1、声明日期revision2、来源解锁/整理/工作列表/评级revision3及五条日志。源输入冲突/无操作规则拒绝不留半个会话；相同输入重复保留已有编班。原`initialize`及第0周准备行为保持。

`list_courses(group)` 返回该班教师当前可用三类课程的深复制，只读、不发布版本。`set_class_mode(group, teaching, expected_revision)` 发布模式和评级两个阶段；`assign_course(group, work_id, expected_revision)` 从持有教师记录推导类别、行/页和源列表，再发布视图/选择/评级三个阶段。每个成功逻辑操作只有一个版本，重复不增加版本/日志；过期或非整数版本、无教师、无课程或非授课模式拒绝时所有数据不变。

课程示例与原新局目录独立，仍可用既有成员移动。教师离开班级会按原规则清除类别/key两个word，保留原版未清除的其他word；UI只把有教师且类别/key有效的安排作为当前课程显示。当前仅安排课程，不执行授课完成或自动推进日期。

## 操作窗口

启动Godot原型后，从顶部“新局编班”进入学校。“编班”和“课程安排”切换页面；“第0周新局”和“第4周课程示例”分别保留两份会话。第0周仍无教师可用课程；点击第4周示例，选择1班、切换“授课”、点选初级课程并点击“安排选中课程”。当前课程随即显示，编班页的班级情况也显示课程ID。

无教师班禁用模式/安排，冒险模式或没有选中课程时禁用安排。课程以来源ID标示，中/高级分类在4/4为空。返回战斗后重新进入保留当前会话和页面；“重开学校新局”只重置当前选中的来源新局或示例，另一会话保留。顶部与页底明确标示示例日期边界。

窗口使用实际Viewport鼠标事件，包括在主视口坐标中命中嵌入式下拉窗口；测试不直接发送控件信号代替点击。课程77项离屏/83项Windows渲染检查，编班94项离屏/99项渲染检查，跨会话导航22项及旧返回两路线79项均零失败。截图和哈希见 [课程验收](../analysis/school-course-ui-20261007/README.md) 和 [编班兼容验收](../analysis/school-grouping-course-compat-20261007/README.md)。
