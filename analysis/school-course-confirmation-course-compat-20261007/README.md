# 确认接入后的课程窗口兼容验收（2026-10-07）

原课程窗口77项离屏/83项Windows渲染重新通过，零失败；Godot4.7.2，1024×768。六张截图逐一检查，三按钮、课程列表、班级关系/安排及日期提示正常；哈希见 [verification.json](verification.json)。

- [来源编班](source_grouping.png) 与 [第0周无课程](source_no_courses.png)：来源会话不开放示例结算/确认。
- [第4周课程](example_available.png) 与 [课程安排](example_assigned.png)：教师101课程12/11/10、模式/选课/安排可操作；安排后仍需成长才能确认。
- [教师移班](example_teacher_moved.png)：课程清除与待命名单保持来源规则。
- [重开](example_restart.png)：另建示例，各会话独立。

实际Viewport输入/嵌入下拉命中沿用已验收测试；示例日期不代表执行前四周，也不推进日历或存档。
