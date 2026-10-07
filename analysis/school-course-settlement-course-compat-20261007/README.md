# 成长接入后的课程窗口兼容验收（2026-10-07）

已有课程窗口重新执行77项离屏/83项Windows渲染检查，全部通过，零失败。Godot 4.7.2，1024×768；输入为实际Viewport事件。六张截图均已检查，课程列表、安排/结算按钮及日期边界显示正常；哈希见 [verification.json](verification.json)。

| 截图 | 场景 |
|---|---|
| [来源编班](source_grouping.png) | 第0周原始目录 |
| [来源无课程](source_no_courses.png) | 第0周无教师课程，隐藏示例结算 |
| [示例可用课程](example_available.png) | 4/4来源课程12/11/10 |
| [示例安排](example_assigned.png) | 模式切换、选课和安排，启用结算 |
| [教师移班](example_teacher_moved.png) | 原班课程视图清除，结算门槛更新 |
| [示例重开](example_restart.png) | 新起点恢复，各会话独立 |

这是本地原型输入验收，示例4/4为声明日期；未执行真实周历/剧情或存档。完整成长交互另见 [结算验收](../school-course-settlement-ui-20261007/README.md)。
