# 编班页面兼容验收（2026-10-07）

Godot4.7.2、Windows OpenGL/NVIDIA RTX3060Ti，1024×768。94项离屏真实输入/99项实际渲染检查全部通过，零失败。5张截图逐一检查，控件和文本无截断/遮挡。检查范围与SHA见[verification.json](verification.json)，输入/渲染日志随目录保存。

- [launcher.png](launcher.png)
- [restart.png](restart.png)
- [second_class_filled.png](second_class_filled.png)
- [source_class.png](source_class.png)
- [teacher_relocated.png](teacher_relocated.png)

本轮新增授课结果页；完成MVP后保留4月第4周与待播放本周剧情。MVP次数按冻结结算选择一次，后续编辑不能重选；重复、按键/战斗隔离、来源/旧返回会话隔离及显式重开均验证。整个确认面板/页脚边界补充检查通过，课程列表留白缩短以适配视口；点击前等待三帧布局，渲染串行执行。原版隔离MVP/CH003入口与原型显示的边界见[来源与API](../../docs/school_course_result_handoff.md)。章节正文、周推进和原版存档尚未执行。
