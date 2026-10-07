# 授课MVP与剧情入口交接

本变更仅作用于声明日期4/4的独立来源课程示例。完整新局前四周、Chapter016/017正文、后继任务7周推进与存档仍有待闭合。

## 原版顺序

`4C1AA0` 的普通模式0：`4BD870`结算成长/选择MVP → `4BDAC0`结果演出及真实MVP VM → 右侧按钮确认 → `4C1350`关系/职业/本周记录 → `4D0750`清理 → MVP次数夹到0..5 → 加载CH003（结束后任务7）→ 请求ADV任务6。本步没有正常模式周推进。

`4C00C0`按五班、每班四位学生的顺序比较`package+0x20`结算累计值。只有ID<13且严格大于当前最大值的学生能成为MVP；最大值初始0，所以平手保留先出现者，待命学生不参与。`7E1182`保留其增加前的次数。实际MVP主脚本通过GETUNITWK选择学生子脚本，子脚本按旧次数选择台词，然后执行真实END。没有正值接收者时原函数保留-1；原型拒绝这一输入，不执行负索引写入。

CH003通过真实月份/周次分派在4/4装载Chapter016；下一次VM执行前停止，保留“章节入口边界”。Chapter016还会SCRIPTEXEC到Chapter017，不能把首次装载当成剧情结束。

## 来源和边界

`tools/school_course_result_handoff_emulation.py`复用来源新局初始化、编班/课程和成长指令，在同一CPU执行完整结果任务，再执行CH003分派。声明输入包括4/4日期、mode0、固定时钟4660、零结果任务、界面/按键就绪、绘图/音频和锁。资源I/O只供应明确白名单下原版YBC字节，指令读取、分支、定时和END保留原生执行；按钮只将右侧确认为按下。等待案例按yield上限停止，不返回伪造完成。

独立选择探针明确把staged totals作为反事实输入并跳过重复成长，真实`4C00C0`用于核对平手次序、全零和后出现更高值。它们不能作为完整结果任务完成证据。所有证据的持久写入、学校初始化完成、交互学校实机证据与live witness标志均为false。

运行规则只保存来源指纹、有限比较/封顶字段、脚本SHA和原初始化的零次数，不包含期望结果。Godot纯模块从冻结的学校班级顺序、成长记录和次数计算MVP/交接；拒绝无正值、未知日期/名单/班级或被改动的规则。

## 验证命令

```bash
PYTHONIOENCODING=utf-8 .venv-audit/Scripts/python.exe -m tools.school_course_result_handoff_emulation --out analysis/new-course-result.json --godot-out analysis/new-course-result-fixture.json
PYTHONIOENCODING=utf-8 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_school_course_result_handoff_emulation
/c/Users/lai/bin/godot --headless --path prototype -s res://sim/tests/test_runner.gd
```

输出必须使用新文件名。已有成长/确认报告保持原字节，不扩展其已声明边界。

2026-10-07来源阶段：五组完整结果/等待案例、四组独立选择探针；Python4项在152.923秒通过并逐字节再生成一致，Godot纯模块3项通过。报告SHA为`4d62f393f524b11590fd4324e6b56d7dfb7f926be992366bafcc3e5787220d9b`，期望SHA为`db29c6572f8d784bdb0c6796ed7a4b799fa82501dfd54925b189688da675c072`，规则SHA为`01704f531df3b9cf127d2529b5715f343f96f6750ac26b88bc52e6a72043937d`。普通课程10的MVP为3，学生3待命则为4；全零探针没有接收者。结算累计值、技能、属性、等级与成长池在MVP后保持，仅确认职业进度影响派生职业合计。

## 会话API

`NewGameSchoolSession.complete_course_result(rules, expected_revision)`只接受已确认的独立第4周示例。它剥除传入期望/接收者等无关字段，校验来源与当前整数revision，从内部冻结学校和原结算记录选择MVP，使用来源初始化次数产生一次写入。`read_mvp_counts()`、`read_result_handoff()`和`view().course_result_handoff`返回深拷贝。

成功只增加一个revision，同一revision下依次发布`course_mvp_count`、`course_adv_request`两条日志；学校、日期、成长与确认记录保持。重复且规则相符的当前revision请求返回duplicate，不加次数或日志；过期/浮点revision、未确认/第0周学校、被改动规则或缺少正值MVP全部拒绝，不发表半成品。后续改课/移动继续保留已冻结的MVP；新Session重开时没有MVP次数或交接字段。

会话4项覆盖普通/学生3待命的原版完整结果、重复/拒绝原子性、深拷贝、后续计划编辑和源会话隔离。2026-10-07全套Godot55套件367项零失败，日志见`analysis/godot-regression-course-result-20261007.txt`。

## 可操作界面

进入独立第4周示例，在课程安排中安排课程、结算成长、确认关系/职业后，切换“授课结果”并点击“完成授课结果”。页面显示冻结MVP、累计比较值和次数变化，以及本周剧情待播放/日期仍4月第4周。普通课程10显示学生3、24150、0→1；学生3待命时显示学生4、22890、0→1。这里呈现结果字段，没有播放MVP台词或Chapter016正文。

重复按钮、键盘和模拟战斗tick不重复发布；改课/移动、切换第0周、关闭/重开面板保留已完成结果，显式重开课程示例才清空。独立结果页避免挤占成长与确认摘要；课程列表留白高度140→128，新增整个确认面板及页脚的1024×768边界检查。输入测试在每次点击前等待三帧布局稳定，控件不可见/超出视口时立即失败退出；实际渲染串行运行，避免窗口焦点相互影响。

最终Godot结果窗口73项离屏输入/78项实际渲染、确认66/71、成长81/86、课程77/83、编班94/99、跨会话导航22、旧返回两路线79项输入检查全部通过。最新五组v4截图共26张全部逐一检查，检查记录含SHA。Python来源4项和既有课程/运行规则/MVP静态来源兼容20项均通过；OpenSpec全部26项严格通过。历史报告、期望与运行规则保持原字节。阶段提交后仍不push。
