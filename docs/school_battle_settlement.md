# 当前场景5的战果确认字段

2026-11-15接入：可玩战斗已按本场实际命中记录生成战果，依次显示本轮战果、总战果/成长与MVP、确认后的CH003交接停点。`school_battle_settlement.gd`拥有本次结果；UI的`last_battle_handoff`保留单次回执。当前重开仍从出发前学校开始，结算不加入version4命令存档，不能把重开试验当成重复领取到持久库存。CH003/Chapter020/021的完整正文、永久加入、下一周及返校存档接续仍待实现；这次不是原生完整验收。

## 本场输入与阶段

- `school_playground.adventure_result_context()`来自当前学校档案、课程后的真实成长池、周后技能/职业记录和MVP次数；准备参数必须与实际出场准备完全一致。固定来源JSON仅读取`rules`，从不把历史fixture的`cases/expected`或1000初始分数作为当前战果。
- `4799C0`死亡处理的AA为击破计数、AC为目标记录+A8贡献值之和、AE为倒下次数，均采用原有符号范围溢出时保留旧值。只收初始工作槽0..19的实际出场学生；法娜的临时工作槽249不加入评分分母。记录独立于64项显示事件列表，清掉显示日志不会清掉战果。
- `473860`使用108000减剩余时间；耗时≤18000为1，≤36000为2，其余3。当前`4307B0`条件覆盖仍显示的敌人及未激活的非召唤敌方储备；Godot的state3是本地30帧死亡显示期映射，不声称原record state3也属于原state1分类。未激活life_kind3召唤储备不阻止清敌档。固定配置目标槽0为33→work217宝箱；其余15槽0。宝箱当前未提供占领输入，所以自然运行不会凭空获得该目标奖励。
- 班级加成由7A52A8组号索引7A529C+group*70，对应当前`class_ratings.relationship_mean`。原4BBD40参与人数1..3均使用count bonus索引0。本轮只对新增1/2人范围重跑原计分体（5秒/500000指令上限），并逐包比对Godot；完整原生寿命未运行。原1秒调用上限在2人时不足，未改变公共助手或旧报告，新增案例保留独立有界调用。
- 此前新游戏49E930清零道具word并把任务grade初始化5。当前Godot首次scene5之前没有冒险发奖/道具获得命令，因此本次结果从零库存、grade5开始；不适用于导入任意旧存档。场内终止条件selector而非UI退出决定是否进入计分。固定loot和growth seed4660是本地可复现随机输入，不称为原场时钟或原生随机状态。
- 源顺序4BBCC0先等级/道具再点包；确认本轮后才发布4C00C0成长，确认总战果且MVP就绪后才发布职业/历史/关系/MVP次数和ADV请求。纯校验可先算完所有阶段以保证失败原子性，但未确认阶段的数据不通过snapshot发布。旧完整世界验证器保持不变，只抽取其既有成长计算为共享函数。
- 当前有限敌人和再生记录保守贡献上界124；Score保留每人1000、至多3人的旧数字界限，不覆盖原signed16贡献分母溢出情形。模拟AI节奏、结束脚本呈现及真实线程等待仍不以本轮认证。

测试及保全摘要见`analysis/godot-scene5-settlement-closeout-v1-20261115.json`。无截图、无宿主窗口/输入、无VM或新工具后端；原八项验收仍2/8。

`prototype/sim/school_battle_confirmation.gd`新增独立纯投影，不放宽旧`AllResultRoleReplay`或`CampaignSchoolLayout`。输入限定当前4月第5周、学校学生3/4/9及教师101、一场scene5，以及由当前编班重新验证的准备结果。实际出场学生可以是该名单的非空子集，法娜的场景NPC身份不加入本轮评分参与者。

接口`apply(school, records, growth, counts, preparation, grade)`的school是成长前的学校快照；records为3/4/9完整职业及周记录，counts为三人的MVP次数；growth仅含实际出场者的`character_id/attributes/level_50/staged_total`；preparation是`SchoolAdventurePreparation.project(...).prepared`，grade为0..4。模块先验证全部输入，再返回独立的after、records、counts和有序relationship_calls。它不写存档、不变更日期，不负责确认按键、MVP演出完成或事务去重；调用者须只发布一次。成长池、技能等成长阶段数据由上层持有，本模块只同步传入的档案显示字段。

原映像SHA-256为`588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005`。依据既有反编译、原字节与来源：

- `4AB7A0`菜单返回8后调用`4A6A10`；任务5的selector低11位为1，该分支遍历state2班级，实际把`7AAA12+group*1C`教师ID写入`7A52FA`，并递增`7A5304`支援数量。既有`tools/school_adventure_preparation_emulation.py:50`读取`7A529A+60/+6A`，故输出字段`teacher_ids:[101]`在这个已核分支也确为本场支援列表。不能将任意教师名单泛化成支援名单。
- `4C1350`从`7A5210/7A5260`取得全学校学生（包括待命）；职业计数保留100哨兵，执行有符号byte加法后钳至0..99。当前历史索引为4，出场班级写`[2,work_fields[0],work_fields[1]]`；待命学生只覆盖首字节3，后两字节保留。
- `4BF9E0`先处理待命学生的同类别/同等级各+1、互相+2、待命→分班学生−1；随后同班学生有向关系+1、学生↔班教师各+1；最后按本场grade表`[3,2,1,0,-1]`更新同场学生及学生↔支援者。每一次`4D3960`调用分别钳至1..100。教师101在原关系表使用slot46（ID>100减55），本模块沿用学校的逻辑ID101，绝不用旧隔离样例的raw slot0冒充教师。
- `4C00C0`按组/槽次序严格大于选择正的staged_total，同分保留先出现者；`4C1AA0`普通分支将该学生MVP次数加1并钳至0..5。缺少正候选直接拒绝，不能伪造recipient。

职业分类与初始记录复用经固定字段摘要验证的`school_course_confirmation_rules.json`；准备规则复用`school_adventure_preparation_rules.json`。已存在的学校准备来源包含初始组、学生9待命、第五组和两条未就绪分支。本模块测试以这些真实来源的学校/准备输入加显式声明的成长与等级，验证纯逻辑边界；不是本次新原生执行或整条链重放。

普通模式下，确认后输出`state6 + adv/dat/ch003.ybc + next_task7`请求。CH003在4/5分派Chapter020（法娜永久加入），随后Chapter021 END才请求新周7；5/1的CH001→Chapter022/208、职务室8、CH002、学校9仍是后续阶段。该请求不等于剧情、周结算或返校已完成。结果selector1..5不是直接返校/升周开关；特殊模式及15/4分支不在本模块范围。
