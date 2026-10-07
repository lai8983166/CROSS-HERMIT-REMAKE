# 授课确认字段窗口验收（2026-10-07）

Godot4.7.2、Windows OpenGL/NVIDIA RTX3060Ti，1024×768。66项离屏真实输入及71项实际渲染检查全部通过，零失败。五张截图均逐一检查，成长与确认摘要/日期提示无溢出或遮挡；检查范围和SHA-256见 [verification.json](verification.json)。

| 截图 | 验收内容 |
|---|---|
| [成长后待确认](growth_pending_confirmation.png) | 成长只执行一次，单独启用关系/职业确认 |
| [课程10确认](confirmed_course10.png) | 三学生职业进度、本周授课记录及十二条关系+1；日期不变 |
| [确认后编班](confirmed_grouping.png) | 原版班级关系均值65→66、成长等级保持 |
| [重开示例](restart_confirmation.png) | 新示例清空确认，另一个第0周会话保留 |
| [学生9待命](confirmed_waiting9.png) | 待命仍增加职业；待命→参课关系−1的两条变化可见 |

输入使用实际Viewport鼠标/按键，包括嵌入下拉窗口。逐字段核对原版完整学校/职业/历史/职业合计；摘要核对每人进度与周记录，重复、改课、导航、按键/战斗tick隔离、重开、控件边界及两会话隔离通过。运行时不消费原版期望快照。原确认按钮/MVP VM、奖励/次数、ADV与真实周历/存档未执行，见 [来源及API](../../docs/school_course_confirmation.md)。
