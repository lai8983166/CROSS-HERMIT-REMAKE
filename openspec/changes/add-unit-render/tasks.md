# Tasks: add-unit-render

## 1. 数据与单位

- [ ] 1.1 `prototype/data/battle_setup.json`：{seed, move_interval, attack_interval,
       units:[{name, faction, job_id, level, stats{七属性}, pos:[x,y]}]} 红蓝各 4，
       对称布阵。验证：JSON 加载测试（单位数 8、字段齐）
- [ ] 1.2 `prototype/sim/battle_unit.gd`（class_name BattleUnit）：组合 SimUnit + 战斗字段
       （cell/faction/hp/mp/engage_left/state）；`setup()` 走 SimDerive 派生上限 + SimEngage
       初始 + 职业默认攻击（job 表 default_attack → attack 表条目缓存威力/命中）。
       验证：GUT——构造后 hp==hp_max、engage==SimEngage 表值、state==idle

## 2. 战斗循环

- [ ] 2.1 `prototype/sim/battle.gd`（class_name Battle）：`start(setup, seed)` 布阵；
       `tick()` 全员状态机（最近敌/直线步进/射程1 普攻/死亡/撤退）；事件日志追加；
       胜负判定与 finish 事件。验证：GUT——构造 1v1（同值单位），tick 循环至 finish，
       日志含 move/attack/hit|miss/dead/finish 且胜负一方非空
- [ ] 2.2 确定性：GUT——seed=42 同 setup 跑两场，事件日志逐条相等、tick 数相等；
       不同 seed 至少一场结果序列不同（证明种子真实参与）
- [ ] 2.3 ENGAGE 撤退：GUT——构造超短 ENGAGE（mod 参数）单位，验证归零后 withdrawn、
       不再被选为目标、触发全灭结算

## 3. 渲染与交互

- [ ] 3.1 main.gd 接入 Battle：_physics_process 固定步长累积调 tick（×time_scale）；
       单位绘制（阵营色菱形/死亡暗/撤退半透明）+ 头顶 HP/ENGAGE 双条；地图三层渲染保留。
       验证：窗口 `--quit-after 600` 无脚本错误，人工看移动/掉血
- [ ] 3.2 点击单位回显单位摘要 + 战斗结束 HUD（胜负/耗时）+ `R` 重开（新种子）。
       验证：人工点击与重开；HUD 数值与 setup 派生一致抽查
- [ ] 3.3 回归：全部测试套件绿（新增 battle/battle_unit 套件）。
       验证：runner 汇总 0 failures exit=0
- [ ] 3.4 提交 + README 更新（战斗视图说明/操作键位/battle_setup 魔改说明）
