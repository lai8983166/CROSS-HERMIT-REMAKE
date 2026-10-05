# 待命名单排序验收（2026-10-05）

Godot原型主场景，使用明确的原版回放规则与输入；没有操作原版游戏。两路线通过Viewport鼠标/键盘事件打开嵌入下拉菜单、选择全部三种排序、保留学生选择、切页、重复选择、滚动、重开及恢复默认战斗。

最终离屏79项检查通过，Windows/OpenGL兼容渲染86项检查通过、零失败；七张1024×768截图已目检，中文及菜单选择可读。`verification.json` SHA-256：`2c826791aeca133b1bb2e0b387843c8f814832e1e13c77ccdf35ca3a3ae5884d`，包含逐截图哈希。

- `default.png`：默认战斗原型入口。
- `route_0_result.png` / `route_1_result.png`：两源路线不同战果。
- `route_0_school.png` / `route_1_school.png`：职业类别顺序5/4/9/3，学生#5仍选中。
- `route_0_attributes.png` / `route_1_attributes.png`：属性合计顺序3/5/4/9，学生#5仍选中；详情保留此前滚轮阅读位置。

两路线日期均5月第1周，点数35881/53324。学校初始revision6，三个有效排序操作后revision9；重复相同排序不发布。完整Godot40套件293项通过，新原指令Python专项9项通过，OpenSpec16项严格检查通过。教师人数为0，编班/排课仍未开放。原版完整学校就绪、实机见证及存档写入标记仍false。详见 `docs/battle_return_audit.md` §70–72；重新运行应使用新的输出目录。
