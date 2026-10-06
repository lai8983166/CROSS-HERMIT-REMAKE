# 新局编班窗口验收 · 2026-10-06

Godot4.7.2兼容渲染器、NVIDIA RTX3060Ti、1024×768。`prototype/ui/tests/test_new_game_school_window.gd` 使用真实Viewport鼠标/键盘事件，离屏94项、实际渲染99项检查零失败；渲染报告 `verification.json` 含截图SHA-256和三次来源目录观察。

截图已检查：入口、新局起点、教师移至2班后学生待命、学生进入指定格、重开后恢复初态。班级格、待命区域和按钮均在视口内，中文显示完整。课程安排/存档未开放提示可见。

- [入口](launcher.png)
- [来源1班](source_class.png)
- [教师移班](teacher_relocated.png)
- [学生重新编班](second_class_filled.png)
- [重新开始](restart.png)

新增 `test_school_navigation.gd` 另行完成22项真实输入检查，确认返回学校与新局编班分别保留会话，导航和编班不改变旧战果/周历/点数，恢复默认战斗仍有效。

这证明本地原型操作与渲染，不是原版学校菜单实机见证，不操作存档。原始初始化、课程和鼠标边界仍见来源文档。
