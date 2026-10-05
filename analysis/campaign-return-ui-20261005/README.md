# 返回流程演示验收（2026-10-05）

这是Godot原型截图，使用明确的原版样例输入演示返回数据链，不是原版实机战斗或学校交互见证。

`verification.json`记录实际运行的44项检查、两路线观察值和各截图SHA-256，零失败。Godot4.7.2，Windows/OpenGL兼容渲染；主场景离屏模式的39项交互检查也通过。全部模拟/页面回归为39套件284项通过。详情见 `docs/battle_return_audit.md` §67–69。

- `default.png`：默认八单位战斗及返回演示入口。
- `route_0_result.png` / `route_1_result.png`：实际本地终局和不同源路线计算出的战果。
- `route_0_school.png` / `route_1_school.png`：确认后返回学校，学生#5高亮且详情一致，长内容可滚动。

截图1024×768。教师课程、编班/排课仍未开放；所有原版见证/存档写入标记保持false。验收脚本是 `prototype/ui/tests/test_campaign_return_window.gd`；重新生成时使用新输出目录，不覆盖本次已归档文件。
