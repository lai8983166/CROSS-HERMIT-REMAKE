# 第四周剧情与第五周到达验收

变更add-school-story-week-continuation，六项完成。默认项目可操作链：

编班/选课 → 授课成长 → 确认记录 → MVP → 两段原版剧情 → 4月第5周到达。

原文162条合并为109个阅读页；两张原版背景、三张组合立绘。版本2存档保留剧情游标和周结果，支持原version1迁移。第五周到达可回顾第四周结果、保存、确认重开和往返独立战斗预览。没有打开第五周课程。

## 验证结果

- Godot57套件377项、0失败，见godot-tests.log。
- Python新增来源/导出8项、0失败，见python-tests.log；素材逐字节重生一致。
- 输入检查：编班80、成长/恢复72、场景导航26、剧情76、第五周/战斗往返51、旧学校导航22、旧MVP窗口73，全部0失败。
- 实际渲染：剧情83、第五周/战斗往返56，全部0失败；12张截图逐一查看。
- OpenSpec严格28项全部通过，见spec-validation.json。
- acceptance.json记录日志统计、截图SHA、未变的四个来源规则与原版证据SHA、验证边界。

剧情截图在[阅读验收](../school-story-reader-20261008/verification.json)，包括开场、人物出现、最长对白、第二段剧情、重新打开、跳过确认和完成。第五周截图在[到达验收](../school-week-arrival-20261008/verification.json)，包括到达、旧周成长回顾、恢复、战斗预览及返回。PNG均为1024×768。

## 复验

项目根目录运行：

    .venv-audit/Scripts/python.exe -m unittest tools.tests.test_school_story_week_emulation tools.tests.test_school_story_export -v
    ~/bin/godot --headless --path prototype --script res://sim/tests/test_runner.gd
    ~/bin/godot --headless --path prototype --script res://ui/tests/test_school_story_window.gd
    ~/bin/godot --headless --path prototype --script res://ui/tests/test_school_week_arrival_window.gd
    openspec validate --all --strict --json

原版完整隔离复跑需要新的报告名：

    .venv-audit/Scripts/python.exe -m tools.school_story_week_emulation --out analysis/新的原版续篇审计.json

这里的Python测试核对固定的原版报告、源指令顺序、写入守卫与导出结果；该报告来自本轮独立完整原版执行，测试自身不重新跑完整native报告。展示导出使用tools.school_story_export。需要渲染截图时使用不带--headless的同一UI脚本，传入-- --capture-dir=一个新建目录；既有verification.json不会覆盖。

## 边界

初始4/4是声明样例，前四周经历未重建。原版结果/剧情/周指令在同CPU执行，但显示就绪、辅助标记及任务调度消费为声明边界。CH001只载入到入口，正文、新周剧情及第五周学校初始化未执行。战斗预览阵容/奖励仍独立。MVP台词、音频与原版渐变未复现。原版SAV未修改，历史证据保留原字节；仅清理本轮未提交的试探报告和素材预览。

六个阶段分别本地提交，未push。OpenSpec变更保留，尚未归档。
