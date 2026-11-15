# 5月第1周返校授课

`prototype/sim/school_return_courses.gd` 接收战后真实返校 bundle，支持教师101与学生3/4/9/5的排课、课程成长、职业/历史/关系确认及一次MVP次数。它不从4/4示例重新初始化成长或历史，也不改变旧课程模块的4/4、三人准入边界。

## 原版依据与同周选择

- `4A3CA0`、`4A2DA0`、`4A8BC0`：每班activity为冒险0或授课1；强制冒险门非零时切授课仍为0。课程必须来自该班教师当前未阻塞的已持有列表；改模式保留原课程字段。
- `4A6A10`、`4C00C0`、`4C0400`、`4D3600`：按五班、四槽顺序，只给实际授课成员应用该课程训练表、关系均值、成长池上限、原CRT随机序列和技能候选逻辑。待命者不获课程成长，技能资格读取成长前属性。继续复用旧模块的点包、属性/等级及总点数纯核。
- `4C1350`、`4BF9E0`：全部在校学生的当前职业进度增加；历史索引`(月-4)*5+周-1`，5/1为5。授课记录写`[1,类别,类别内key]`；待命只写首字节3，保留后两字节。关系逐次夹到1..100，待命→参与者减1没有反向扣减。
- `4C00C0`、`4C1AA0`：MVP按参与槽严格大于比较，平手保留先出现者；旧次数供台词选择，随后次数增加并夹到5，再交CH003及任务7。本模块保留CH003待执行请求，不声称已播放MVP/剧情或推进到5/2。

当前只有教师101，因此只有一个可行动班。5/1可以选择授课，或切到冒险准备；完成授课结果后不能重新打开同周出击/授课。原版多教师的混合班结算不属于当前四人入口。

既有来源解释器为`tools/school_course_settlement_emulation.py`（SHA-256 `48c1b01863e738ae642041ddb468df3d2747d851335a45bbb0f814d00b625a70`）及`tools/school_course_confirmation_emulation.py`（`5654199bc87505a93fce7fb61a426c3c760fd6b5ef4bd2490d304e4baa176717`），反编译文件位于`analysis/decomp_all/`。镜像`analysis/hermit_game.exe`核对为`588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005`。原镜像、原资产、旧记录及公共核函数未改。

## 接口和提交边界

四个纯接口均返回`supported`，失败不发布`after`，不修改传入对象：

- `list_courses(bundle, group)`：返回三类当前课程行。5/1实际持有1、2、3、4、5、10、11、12；不可把原表16个训练记录全部视为可选课。
- `set_mode(bundle, group, teaching)`：复用原模式规则及重新评级。
- `assign_course(bundle, group, work_id)`：由教师当前列表推导类别、序号和页，不接受调用方自填工作字段。
- `settle(bundle, seed=4660)`：完整预校验后计算成长、确认、MVP，再一次返回完整bundle。只接受当前5/1四人状态及合法授课班；随机种子是重制声明输入。

`settle`成功后`after.phase="courses_confirmed"`，`after.course_result`与返回`summary`含点包、随机结果、学生前后属性/等级、新技能、MVP旧次数、历史索引及关系调用。全校成长、历史、次数、participants、当前编班、待命、装备和既有flags全部接续；实际成长/职业字段同步到participants。日期保持5/1，周推进交上层Flow。

完成状态同种子重复结算返回深复制`duplicate`，改变种子拒绝；完成状态拒绝再次排课。没有正成长MVP的结果按旧端口安全边界拒绝，避免原程序负ID写入。上层必须从可信起点重放计划/结果命令并验证摘要，不能把外来bundle直接当存档认证结果；本模块不自行提供原版存档写入权限。

## 小型原指令对照

新增`prototype/data/school_return_courses_source.json`仅保存五个声明5/1课程1–5的输入/输出成长记录、点包和随机结果，14,066字节，SHA-256 `6a390c7edb26a87c504cb3d27ee72d823be48264c332aea1457bb4876f6fa595`。复用现有解释器一次初始化，先声明4/4取得旧课，再声明5/1解锁新课，连续执行五门新课作为局部函数对照；这些同日连续探针不是正常游戏时间线，也不是四人原生寿命见证。每次结算仍有既有有限写守卫与指令上限。该JSON不用于运行时计算；Godot测试独立比对全部成长字段、点包和随机序列。

复现步骤（输出使用新路径；Python参数`-B -X utf8`，临时目录在F盘）：

```python
import json
from pathlib import Path
from tools.school_course_settlement_emulation import CourseSettlementEmulator
expected = json.loads(Path('prototype/data/school_return_courses_source.json').read_text('utf8'))
e = CourseSettlementEmulator(seed=4660)
e.initialize()
e.declare_date(4, 4)
e.declare_date(5, 1)
e.run('teaching', 'mode')
for course in range(1, 6):
    e.clear_trace('planning_rate')
    category, row = next((c, n) for c, rows in enumerate(e.planning_snapshot()['work_rows'])
                         for n, entry in enumerate(rows) if entry[1] == course)
    e.run('assign', 'course', category=category, row=row)
    result = e.settle('course' + str(course))
    for key in ('before_records', 'after_records', 'packets', 'learning_draws',
                'rand_state', 'bonus', 'skill_display_needed', 'declared_clock_seed'):
        assert result[key] == expected['cases'][course-1][key], (course, key)
```

首个开发探针在课程1完成后，未复位跟踪阶段就进入下一次选课，既有守卫拒绝学校视图写入；修正调用方阶段后继续验证，未改守卫或课程解释器，也未留下完整失败转储。

顺序探针需深复制返回的`learning_draws`；解释器内部会复用该列表。开发草稿遗漏复制，使早期案例的draw列表被最后一例覆盖，完整记录、点包及最终RNG对照发现此收集器错误。修正收集器并重取来源，课程算法未改变；不把由末态推算的随机序列充作观察值。

测试同时复用旧八个原指令成长案例，覆盖封顶、不同种子、待命和移班；新四人测试覆盖八门实际可用课、既有成长/历史保留、待命旧累计值不参与MVP、单向关系、participants同步、MVP一次性、计划JSON重放以及非法输入原子拒绝。全程无窗口、截图、原生游戏或桌面输入；最终原生验收及`STOPPED_SCOPE_GUARD`不变。

2026-11-15针对无窗口验证：`test_school_return_courses.gd`七项全部通过，无脚本错误；其中完整核对既有八例及新增五例原指令成长输出。成功日志为`.venv-audit/return-courses-check/result.log`。开发失败草稿及重复Godot日志在成功后按明确文件路径清理；保留小型来源、复现说明与一份成功日志，本地临时复现脚本、测试入口及日志合计2,101字节。
