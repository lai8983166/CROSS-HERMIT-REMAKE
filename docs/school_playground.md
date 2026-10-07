# 学校养成试玩

本轮新增独立的图形化第四周学校试玩，使用已验证的新局学校会话。当前编班/授课样例覆盖教师101和学生3、4、9，日期4月第4周为独立输入，尚无真实前四周经历。

## 展示素材

`python -m tools.school_presentation_export` 从原版 `ADV/BIN/HAN001.BIN` 裁出四张头像，从 `BG001_A.BIN` 导出背景。输出在 `prototype/assets/school`，catalog.json记录原文件SHA、矩形与输出SHA；四个姓名对应已有中文角色ID资料。课程10/11/12使用根据源成长表编写的描述性名称“全面训练/综合研习/身心锻炼”，并非已恢复的原版课程标题。显示文案可独立修改，不参与来源规则指纹。

2026-10-08：6个输出在临时目录逐字节重新生成一致；头像对照见 `analysis/school-playground-assets-20261008/portraits.png`。原素材及历史证据保持原字节。
