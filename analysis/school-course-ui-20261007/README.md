# 课程窗口验收 · 2026-10-07

Godot4.7.2兼容渲染器、NVIDIA RTX3060Ti、1024×768。`prototype/ui/tests/test_school_course_window.gd` 使用实际Viewport鼠标/键盘事件，课程页77项离屏、83项Windows渲染检查零失败。嵌入下拉菜单通过主视口实际坐标点击；没有用控件信号或直接调用安排函数替代输入。

验证第0周空列表及模式修改、第4周独立来源课程12/11/10、授课/冒险禁用、选择/替换/重复安排、无教师班、课程字段/评级、教师移班清除课程、两份会话往返保留、各自重开、关闭再进、返回会话隔离及战斗输入/tick隔离。`verification.json` 保存环境、检查结果和六图SHA-256。

六张截图已检查，页面/按钮/五班待命区在视口内，中文完整；当前课程、独立第4周示例标示及第0周不可用说明可见。

- [来源编班](source_grouping.png)
- [第0周无可用课程](source_no_courses.png)
- [第4周可用课程](example_available.png)
- [已安排课程10](example_assigned.png)
- [示例教师移至2班](example_teacher_moved.png)
- [示例单独重开](example_restart.png)

这是本地原型验收；示例日期为声明输入，来源解锁/列表/安排/评级按已核对规则计算。没有执行日历推进、授课成长或原版存档。
