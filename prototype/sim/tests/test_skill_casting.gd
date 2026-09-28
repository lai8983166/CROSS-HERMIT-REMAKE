extends "res://sim/tests/test_base.gd"


func _battle() -> Battle:
	var setup := {"move_interval": 9999, "attack_interval": 9999, "units": [
		{"name": "caster", "faction": 0, "job_id": 9, "level": 10,
			"stats": {"strength": 20, "agility": 20, "constitution": 30},
			"pos": [10, 10], "anim_id": "D0A"},
		{"name": "target", "faction": 0, "job_id": 1, "level": 10,
			"stats": {"strength": 20, "agility": 1, "constitution": 99},
			"pos": [12, 10], "anim_id": "B1A"},
		{"name": "enemy", "faction": 1, "job_id": 1, "level": 10,
			"stats": {"strength": 20, "agility": 1, "constitution": 99},
			"pos": [30, 10], "anim_id": "B1A"},
	]}
	return Battle.start(setup, 29, null)


func _impact_event(battle: Battle) -> Dictionary:
	for index in range(battle.skill_events.size() - 1, -1, -1):
		var event: Dictionary = battle.skill_events[index]
		if String(event.get("phase", "")) == "impact":
			return event
	return {}


func test_C1A人物恢复不等待2029且释放特效与命中重叠() -> void:
	var battle := _battle()
	var caster: BattleUnit = battle.units[0]
	caster.anim_id = "C1A"
	assert_true(battle.start_skill(caster, battle.units[2], 22), "黄金档可施放")
	for _i in 92:
		battle.tick()
	assert_eq(caster.skill_action, 31, "命中时人物仍是释放动作")
	assert_eq(battle.active_fx_events().map(func(event): return int(event.global_id)),
		[3027, 2029], "184tick命中时3027还没自然结束")
	assert_eq(int(_impact_event(battle)["trigger"]["signal"]["tick"]), 34, "来源于C1A事件")
	for _i in 6:
		battle.tick()
	assert_eq([caster.skill_action, caster.skill_phase_started_tick], [16, 196],
		"46次更新完成后进入恢复，不用47tick图层总长")
	assert_eq(battle.active_fx_events().map(func(event): return int(event.global_id)),
		[2029], "人物恢复时目标命中特效仍在播放")
	for _i in 30:
		battle.tick()
	assert_eq(caster.state, BattleUnit.State.IDLE, "256tick演员完成")
	assert_eq(battle.pending_skill_signals.size(), 0, "无信号残留")


func test_同步按人物根与特效槽顺序消费并保留目标先后差异() -> void:
	for target_mode in ["later", "earlier", "self"]:
		var battle := _battle()
		var caster: BattleUnit = battle.units[0]
		var target: BattleUnit = battle.units[1]
		if target_mode == "earlier":
			battle.units = [target, caster, battle.units[2]]
		elif target_mode == "self":
			target = caster
		assert_true(battle.start_skill(caster, target, 29), "技能29启动")
		for _i in 73:
			battle.tick()
		var event := _impact_event(battle)
		var expected_tick := 121 if target_mode == "earlier" else 120
		assert_eq(int(event.source_tick), expected_tick, "%s: 目标槽消费顺序" % target_mode)
		assert_eq(int(event.gameplay_result.resolved_source_tick), expected_tick + 23,
			"0x08相对于命中视觉，不能跟随演员阶段")
		assert_eq(int(event.gameplay_result.resolved_frame), 72, "两次60Hz更新投影到同逻辑帧")


func test_多施法者结果按实例关联而非最近事件() -> void:
	var battle := _battle()
	var first: BattleUnit = battle.units[0]
	var second: BattleUnit = battle.units[1]
	second.anim_id = "C1A"
	second.mp_max = 100
	second.mp = 100
	assert_true(battle.start_skill(first, second, 29), "首个友方技能")
	assert_true(battle.start_skill(second, battle.units[2], 22), "第二个敌方技能")
	for _i in 100:
		battle.tick()
	var impacts: Array = battle.skill_events.filter(func(event): return event.phase == "impact")
	assert_eq(impacts.size(), 2, "两个命中视觉实例")
	assert_eq([int(impacts[0].instance_id), int(impacts[1].instance_id)], [1, 2], "确定性实例号")
	assert_eq(String(impacts[0].gameplay_result.outcome), "friendly_effect_unresolved",
		"技能29的延迟结果关联原事件，期间已经记录第二个人的cast")
	assert_eq(String(impacts[1].gameplay_result.outcome), "applied", "技能22状态属于第二次施放")
	assert_eq([int(impacts[0].gameplay_result.resolved_source_tick),
		int(impacts[1].gameplay_result.resolved_source_tick)], [143, 184], "各自结算时钟")
	assert_eq(battle.skill_resource_events.size(), 2, "各自一次扣费")


func test_无动作完成证据时拒绝而非使用待机时长() -> void:
	var battle := _battle()
	battle.units[0].anim_id = "E0A"
	var mp_before: int = battle.units[0].mp
	assert_false(battle.start_skill(battle.units[0], battle.units[2], 22), "E0A原始action31缺失")
	assert_eq(battle.units[0].mp, mp_before, "拒绝不扣费用")
	assert_eq(battle.skill_events.size(), 0, "不产生虚构技能时间线")


func test_命中快照在04计算且08不重新选择移动后的目标() -> void:
	var battle := _battle()
	var caster: BattleUnit = battle.units[0]
	var enemy: BattleUnit = battle.units[2]
	caster.anim_id = "C1A"
	caster.atk_power = 10
	caster.atk_power_range = 0
	enemy.unit.magic_resist = 0
	enemy.unit.magic_resist_modifier = 0
	enemy.unit.body = 0
	enemy.unit.body_modifier = 100
	battle.units = [enemy, caster, battle.units[1]]
	assert_true(battle.start_skill(caster, enemy, 22), "目标先于施法者")
	for _i in 92:
		battle.tick()
	var event := _impact_event(battle)
	assert_eq(int(event.source_tick), 184, "04创建命中视觉")
	assert_false(event.has("gameplay_result"), "目标已经更新，08须等下个source tick")
	caster.atk_power = 999
	enemy.cell.x += 1
	battle.tick()
	assert_eq(int(event.gameplay_result.mp_result.computed_damage), 10,
		"08应用04缓存的数值，不能重新读取施法者攻击力")
	assert_eq(int(event.gameplay_result.resolved_source_tick), 185, "下一次目标更新结算")
	assert_eq(String(event.gameplay_result.outcome), "applied", "04已选中的单位移动后仍接收命中")


func test_MP不足拒绝且不改变动作或事件() -> void:
	var battle := _battle()
	var caster: BattleUnit = battle.units[0]
	caster.mp = 9
	assert_eq(int(SimTables.attack(22).get("mp_cost", -1)), 10, "原版技能22费用")
	assert_false(battle.start_skill(caster, battle.units[2], 22), "9MP不足")
	assert_eq(caster.mp, 9, "拒绝不扣MP")
	assert_eq(caster.state, BattleUnit.State.IDLE, "拒绝不改变人物状态")
	assert_eq(battle.skill_events.size(), 0, "无演出事件")
	assert_eq(battle.skill_resource_events.size(), 0, "无扣费事件")
	assert_eq(battle.active_skills.size(), 0, "无技能实例")


func test_释放前死亡或撤离停止演员和依附施法且不扣费() -> void:
	for exit_state in [BattleUnit.State.DEAD, BattleUnit.State.WITHDRAWN]:
		var battle := _battle()
		var caster: BattleUnit = battle.units[0]
		var mp_before := caster.mp
		assert_true(battle.start_skill(caster, battle.units[2], 22), "启动施法")
		battle.tick()
		caster.state = exit_state
		battle.tick()
		assert_eq(caster.state, exit_state, "中断不能把退出状态写回待机")
		assert_eq(caster.skill_id, -1, "清除演员技能")
		assert_eq(battle.active_skills.size(), 0, "实例不再推进")
		assert_eq(battle.pending_skill_signals.size(), 0, "无根队列残留")
		assert_eq(battle.active_fx_events().size(), 0, "清除依附持续施法FX")
		assert_eq(caster.mp, mp_before, "未释放不扣费")
		assert_eq(battle.skill_resource_events.size(), 0, "无费用事件")
		assert_eq(String(battle.skill_events[-1].phase), "interrupted", "有中断诊断")
		assert_false(battle.start_skill(caster, battle.units[2], 22), "退出单位不能再施法")


func test_释放后死亡不退费且保留独立释放视觉但取消人物04() -> void:
	var battle := _battle()
	var caster: BattleUnit = battle.units[0]
	caster.anim_id = "C1A"
	var mp_before := caster.mp
	battle.start_skill(caster, battle.units[2], 22)
	for _i in 75:
		battle.tick()
	caster.state = BattleUnit.State.DEAD
	battle.tick()
	assert_eq(caster.mp, mp_before - 10, "已释放费用不退")
	assert_eq(battle.skill_resource_events.size(), 1, "保持单次费用")
	assert_eq(battle.active_fx_events().map(func(event): return int(event.global_id)),
		[3027], "独立释放特效不随人物死亡删除")
	assert_eq(battle.pending_skill_signals.size(), 0, "未来人物根04取消")
	for _i in 30:
		battle.tick()
	assert_true(_impact_event(battle).is_empty(), "没有捏造尚未发出的攻击")
	assert_eq(battle.active_fx_events().size(), 0, "独立释放特效自然消退")


func test_已产生的命中视觉在源退出后保留但08玩法被抑制() -> void:
	for exit_state in [BattleUnit.State.DEAD, BattleUnit.State.WITHDRAWN]:
		var battle := _battle()
		var caster: BattleUnit = battle.units[0]
		var enemy: BattleUnit = battle.units[2]
		caster.anim_id = "C1A"
		battle.units = [enemy, caster, battle.units[1]]
		battle.start_skill(caster, enemy, 22)
		for _i in 92:
			battle.tick()
		var mp_before := enemy.mp
		caster.state = exit_state
		battle.tick()
		assert_eq(String(_impact_event(battle).gameplay_result.outcome), "source_unavailable",
			"4919F0再次验证源单位，不施加已排队的玩法")
		assert_eq(enemy.mp, mp_before, "未应用缓存MP伤害")
		assert_true(enemy.condition_slots[0].is_empty(), "未应用效果6")
		assert_true(battle.active_fx_events().any(func(event): return int(event.global_id) == 2029),
			"已生成的命中视觉继续播放")
		assert_eq(battle.pending_skill_signals.size(), 0, "08已消费，无孤立队列")


func test_目标退出拒绝准入并抑制已释放08() -> void:
	var battle := _battle()
	var caster: BattleUnit = battle.units[0]
	var target: BattleUnit = battle.units[1]
	target.state = BattleUnit.State.DEAD
	assert_false(battle.start_skill(caster, target, 29), "失效目标不能准入")
	target.state = BattleUnit.State.IDLE
	battle.start_skill(caster, target, 29)
	for _i in 60:
		battle.tick()
	target.state = BattleUnit.State.WITHDRAWN
	for _i in 12:
		battle.tick()
	assert_eq(String(_impact_event(battle).gameplay_result.outcome), "target_unavailable",
		"目标退出后消费08但不执行玩法")
	assert_eq(battle.active_skills.size(), 1, "目标退出不是源演员中断")
	assert_eq(battle.pending_skill_signals.size(), 0, "目标队列正常排空")


func test_ENGAGE撤离在本帧事件后清理技能() -> void:
	var battle := _battle()
	var caster: BattleUnit = battle.units[0]
	battle.start_skill(caster, battle.units[2], 22)
	caster.engage_left = 0.0
	battle.tick()
	assert_eq(caster.state, BattleUnit.State.WITHDRAWN, "归零进入退出")
	assert_eq(battle.active_skills.size(), 0, "本帧退出即停止技能")
	assert_eq(battle.active_fx_events().size(), 0, "持续施法停止")
	assert_eq(battle.skill_resource_events.size(), 0, "未进入释放")


func test_MP恰好足够在释放扣费一次且与目标伤害分开() -> void:
	var battle := _battle()
	var caster: BattleUnit = battle.units[0]
	var enemy: BattleUnit = battle.units[2]
	caster.mp = 10
	assert_true(battle.start_skill(caster, enemy, 22), "恰好足够可施放")
	for _i in 74:
		battle.tick()
	assert_eq(caster.mp, 10, "施法期间不扣费")
	assert_eq(battle.skill_resource_events.size(), 0, "释放前无扣费记录")
	battle.tick()
	assert_eq(caster.mp, 0, "释放帧扣10MP")
	assert_eq(battle.skill_resource_events.size(), 1, "释放恰好一次")
	var event: Dictionary = battle.skill_resource_events[0]
	assert_eq([int(event.frame), int(event.requested_cost), int(event.applied_cost)],
		[75, 10, 10], "费用与发生帧独立记录")
	for _i in 100:
		battle.tick()
	assert_eq(battle.skill_resource_events.size(), 1, "命中与恢复不再次扣费")
	assert_eq(int(_impact_event(battle).get("gameplay_result", {}).get("mp_result", {})
		.get("mp_after", -1)), enemy.mp, "目标MP伤害仍由玩法结果记录")


func test_施法期间MP下降释放不重检并钳制到零() -> void:
	var battle := _battle()
	var caster: BattleUnit = battle.units[0]
	caster.mp = 10
	assert_true(battle.start_skill(caster, battle.units[2], 22), "开始时通过准入")
	caster.mp = 3
	for _i in 75:
		battle.tick()
	assert_eq(caster.state, BattleUnit.State.RELEASE, "原版释放入口没有再次拒绝")
	assert_eq(caster.mp, 0, "472550钳制")
	var event: Dictionary = battle.skill_resource_events[0]
	assert_eq([int(event.requested_cost), int(event.applied_cost)], [10, 3],
		"记录费用和实际扣除差异")


func test_技能29同步首帧事件与独立人物恢复() -> void:
	var battle := _battle()
	assert_true(battle.start_skill(battle.units[0], battle.units[1], 29), "技能可启动")
	for _i in 221:
		battle.tick()
	var phases: Array = battle.skill_events.map(func(event): return String(event.phase))
	var starts: Array = battle.skill_events.map(func(event): return int(event.frame))
	assert_eq(phases, ["cast", "release", "sync", "impact", "recovery"], "阶段顺序")
	assert_eq(starts, [0, 60, 60, 60, 84], "3017首指令触发而非等待120tick")
	assert_eq(battle.skill_events.map(func(event): return int(event.source_tick)),
		[0, 120, 120, 120, 167], "保留奇数tick完成信号，不丢失半帧")
	assert_eq(int(battle.skill_events[2].duration_frames), 60,
		"3017 的120动画tick换算为60逻辑帧")
	assert_eq(int(battle.skill_events[3].global_id), 3032, "同步0x04信号启动命中视觉")
	assert_eq(battle.units[0].state, BattleUnit.State.IDLE, "恢复完成后待机")


func test_技能22动作完成独立于释放与命中特效寿命() -> void:
	var battle := _battle()
	var caster: BattleUnit = battle.units[0]
	var enemy: BattleUnit = battle.units[2]
	assert_true(battle.start_skill(caster, enemy, 22), "技能22对敌方启动")
	assert_eq([caster.skill_action, caster.skill_phase_started_frame], [13, 0],
		"action13施法从阶段首帧开始")
	for _i in 75:
		battle.tick()
	assert_eq([caster.skill_action, caster.skill_phase_started_frame], [31, 75],
		"150个原版施法tick后进入action31")
	assert_eq([int(battle.active_fx_events()[0].get("global_id", 0)),
		battle.active_fx_events()[0].get("anchor", "")], [3027, "source"],
		"3027在源点播放并独立于施法特效")
	for _i in 18:
		battle.tick()
	var impact_fx := battle.active_fx_events()
	assert_eq([int(impact_fx[0].get("global_id", 0)), impact_fx[0].get("anchor", ""),
		impact_fx[0].get("to_cell", [])], [2029, "target", [30, 10]],
		"2029由人物0x04信号启动，不依赖3027结束")
	for _i in 10:
		battle.tick()
	assert_eq([caster.skill_action, caster.skill_phase_started_frame], [16, 103],
		"action31根完成55tick后切换action16")
	assert_eq(battle.active_fx_events().size(), 0, "恢复阶段没有残留特效")
	for _i in 30:
		battle.tick()
	assert_eq(caster.state, BattleUnit.State.IDLE, "恢复时长结束回待机")
	var phases: Array = battle.skill_events.map(func(event): return String(event.phase))
	var starts: Array = battle.skill_events.map(func(event): return int(event.frame))
	var durations: Array = battle.skill_events.map(func(event): return int(event.duration_frames))
	var actions: Array = battle.skill_events.map(func(event): return int(event.action))
	var visual_ids: Array = battle.skill_events.map(func(event): return int(event.global_id))
	assert_eq(phases, ["cast", "release", "impact", "recovery"], "缺失sync不生成假阶段")
	assert_eq(starts, [0, 75, 90, 103], "人物信号与演员生命周期独立")
	assert_eq(durations, [75, 28, 10, 30], "release记录演员完成时长，不是FX时长")
	assert_eq(actions, [13, 31, 31, 16], "action13/31/16按人物阶段切换")
	assert_eq(visual_ids, [2044, 3027, 2029, 0], "视觉链不混入玩法ID")
	assert_eq(battle.skill_events.map(func(event): return int(event.source_tick)),
		[0, 150, 179, 205], "0x04在29tick，人物根完成55tick")
	assert_eq(battle.active_skills.size(), 0, "完整演出结束后无活动技能残留")


func test_技能事件含完整且分离的数据() -> void:
	var battle := _battle()
	battle.start_skill(battle.units[0], battle.units[1], 29)
	var event: Dictionary = battle.skill_events[0]
	assert_eq([int(event.cast_action), int(event.release_action), int(event.recover_action)],
		[12, 7, 15], "三个动作")
	assert_eq([int(event.cast_fx), int(event.release_fx), int(event.sync_fx), int(event.impact_fx)],
		[2050, 2098, 3017, 3032], "四个视觉 ID")
	assert_eq(int(event.gameplay_effect_id), 0, "玩法效果 ID 独立")
	assert_eq(int(event.target_filter), 3, "技能29保留友方/自身目标筛选")
	assert_eq(event.from_cell, [10, 10], "源格")
	assert_eq(event.to_cell, [12, 10], "目标格")


func test_技能29只接受友方或自身目标且不伪造伤害() -> void:
	var battle := _battle()
	var caster: BattleUnit = battle.units[0]
	# This target-filter regression requests two casts; provide two real costs.
	caster.mp_max = 2 * int(SimTables.attack(29).get("mp_cost", 0))
	caster.mp = caster.mp_max
	var ally: BattleUnit = battle.units[1]
	var enemy: BattleUnit = battle.units[2]
	assert_false(battle.start_skill(caster, enemy, 29), "敌方目标应被筛选值3拒绝")
	assert_true(battle.start_skill(caster, ally, 29), "友方目标可接受")
	var hp_before := ally.hp
	for _i in 147:
		battle.tick()
	assert_eq(ally.hp, hp_before, "玩法效果未还原前不得把友方技能伪造成物理伤害")
	for _i in 74:
		battle.tick()
	assert_true(battle.start_skill(caster, caster, 29), "筛选值3允许对自身施放")


func test_技能22效果6写入限时状态且不伪造HP物理伤害() -> void:
	var battle := _battle()
	var caster: BattleUnit = battle.units[0]
	var enemy: BattleUnit = battle.units[2]
	var hp_before := enemy.hp
	assert_true(battle.start_skill(caster, enemy, 22), "效果6允许敌方目标")
	for _i in 120:
		battle.tick()
	assert_eq(enemy.hp, hp_before, "效果6不得套用普通物理伤害")
	assert_eq(int(enemy.condition_slots[0].get("condition_id", 0)), 6, "效果6写入状态槽0")
	assert_eq(int(enemy.condition_slots[0].get("source_skill_id", -1)), 22, "状态记录来源技能")
	assert_eq(int(enemy.condition_slots[0].get("ticks_remaining", 0)), 3740, "新命中帧90后的30次更新")
	assert_eq(int(enemy.condition_slots[0].get("tick_counter", 0)), 60, "辅助计数经过60原版tick")
	var impact_event := _impact_event(battle)
	var gameplay_result: Dictionary = impact_event.get("gameplay_result", {})
	var application: Dictionary = gameplay_result.get("application", {})
	var expected_mp_loss: int = mini(caster.atk_power, enemy.mp_max)
	assert_eq(int(impact_event.get("gameplay_effect_id", 0)), 6, "事件记录玩法效果6")
	assert_eq(int(impact_event.get("global_id", 0)), 2029, "命中特效ID仍独立")
	assert_eq(String(gameplay_result.get("outcome", "")), "applied", "记录状态应用结果")
	assert_eq(int(gameplay_result.get("resolved_frame", -1)), int(impact_event.get("frame", -2)),
		"记录结算帧")
	var mp_result: Dictionary = gameplay_result.get("mp_result", {})
	assert_eq(int(mp_result.get("computed_damage", 0)), caster.atk_power,
		"技能22的瞬时MP伤害取魔法命中快照，而非3600状态时长")
	assert_eq(int(mp_result.get("applied_damage", 0)), expected_mp_loss,
		"记录实际扣除MP")
	assert_eq(int(mp_result.get("mp_after", enemy.mp_max)), enemy.mp_max - expected_mp_loss,
		"MP命中效果从目标当前值扣减")
	assert_eq([int(gameplay_result.get("condition_id", 0)),
		int(gameplay_result.get("slot_index", -1)), int(application.get("ticks_remaining", 0))],
		[6, 0, 3800], "记录效果参数和原始应用值")


func test_技能22抵抗结果进入impact事件且视觉ID独立() -> void:
	var battle := _battle()
	var caster: BattleUnit = battle.units[0]
	var enemy: BattleUnit = battle.units[2]
	enemy.unit.magic_resist = 96
	assert_true(battle.start_skill(caster, enemy, 22), "技能22对敌人启动")
	for _i in 100:
		battle.tick()
	var impact_event := _impact_event(battle)
	var gameplay_result: Dictionary = impact_event.get("gameplay_result", {})
	assert_eq(int(impact_event.get("gameplay_effect_id", 0)), 6, "抵抗分支仍记录玩法效果6")
	assert_eq(int(impact_event.get("global_id", 0)), 2029, "抵抗不混淆命中特效ID")
	assert_eq(String(gameplay_result.get("outcome", "")), "resisted", "事件记录抵抗")
	assert_eq(int(gameplay_result.get("condition_id", 0)), 6, "记录被判定的状态参数")
	assert_eq(int(enemy.condition_slots[0].get("condition_id", 0)), 0, "抵抗不写入状态")
	var mp_result: Dictionary = gameplay_result.get("mp_result", {})
	assert_eq(String(mp_result.get("outcome", "")), "drained",
		"状态时长抵抗不抵消独立的魔法MP伤害")
	assert_eq(int(enemy.mp), int(mp_result.get("mp_after", -1)), "抵抗事件保留实际MP结果")


func test_技能22瞬时MP伤害按原版下限钳制并记录实际值() -> void:
	var battle := _battle()
	var caster: BattleUnit = battle.units[0]
	var enemy: BattleUnit = battle.units[2]
	enemy.mp = 1
	assert_true(battle.start_skill(caster, enemy, 22), "技能22对敌人启动")
	for _i in 100:
		battle.tick()
	var gameplay_result: Dictionary = _impact_event(battle).get("gameplay_result", {})
	var mp_result: Dictionary = gameplay_result.get("mp_result", {})
	assert_true(int(mp_result.get("computed_damage", 0)) >= 1, "魔法命中至少计算1点")
	assert_eq([int(mp_result.get("applied_damage", 0)), int(mp_result.get("mp_after", -1)),
		int(enemy.mp)], [1, 0, 0], "MP应用遵循472550的0下限")


func test_技能29impact结果保持其玩法和视觉字段兼容() -> void:
	var battle := _battle()
	assert_true(battle.start_skill(battle.units[0], battle.units[1], 29), "技能29对友方启动")
	for _i in 147:
		battle.tick()
	var impact_event := _impact_event(battle)
	var gameplay_result: Dictionary = impact_event.get("gameplay_result", {})
	assert_eq(int(impact_event.get("gameplay_effect_id", -1)), 0, "技能29玩法ID保持原值")
	assert_eq(int(impact_event.get("global_id", 0)), 3032, "技能29视觉ID保持原值")
	assert_eq(String(gameplay_result.get("outcome", "")), "friendly_effect_unresolved",
		"未逆向的友方玩法结果显式记录但不伪造")
	assert_eq([int(impact_event.get("source_tick", -1)),
		int(gameplay_result.get("resolved_source_tick", -1)),
		int(gameplay_result.get("resolved_frame", -1))], [120, 143, 72],
		"视觉首帧不等于3032途中0x08结算时刻")


func test_技能22仅命中敌方且目标离开选定格时不写入状态() -> void:
	var battle := _battle()
	var caster: BattleUnit = battle.units[0]
	var ally: BattleUnit = battle.units[1]
	var enemy: BattleUnit = battle.units[2]
	assert_eq(int(SimTables.attack(22).get("target_filter", -1)), 2,
		"技能22原始目标筛选为敌方")
	assert_false(battle.start_skill(caster, caster, 22), "target_filter=2 拒绝自身目标")
	assert_false(battle.start_skill(caster, ally, 22), "target_filter=2 拒绝友方目标")
	assert_true(battle.start_skill(caster, enemy, 22), "target_filter=2 接受敌方目标")
	enemy.cell += Vector2i(1, 0)
	for _i in 100:
		battle.tick()
	assert_eq(int(enemy.condition_slots[0].get("condition_id", 0)), 0,
		"技能22的单格落点已空，不应跟随离开的目标施加状态")


func test_技能22效果6按魔抗缩放并执行原版下限() -> void:
	var applicable := _battle()
	var caster_a: BattleUnit = applicable.units[0]
	var target_a: BattleUnit = applicable.units[2]
	target_a.unit.magic_resist = 95
	applicable.start_skill(caster_a, target_a, 22)
	for _i in 90:
		applicable.tick()
	assert_eq(int(target_a.condition_slots[0].get("ticks_remaining", 0)), 190,
		"AGI20 的3800基础值被5%魔抗通道缩至190，超过183")

	var resisted := _battle()
	var caster_b: BattleUnit = resisted.units[0]
	var target_b: BattleUnit = resisted.units[2]
	target_b.unit.magic_resist = 96
	resisted.start_skill(caster_b, target_b, 22)
	for _i in 90:
		resisted.tick()
	assert_eq(int(target_b.condition_slots[0].get("condition_id", 0)), 0,
		"AGI20 的3800基础值被4%缩至152，低于184而拒绝")


func test_技能22效果6过期并在重复施放时刷新() -> void:
	var battle := _battle()
	var caster: BattleUnit = battle.units[0]
	var target: BattleUnit = battle.units[2]
	caster.unit.agility = 0
	target.unit.magic_resist = 90
	battle.start_skill(caster, target, 22)
	for _i in 133:
		battle.tick()
	assert_eq(int(target.condition_slots[0].get("ticks_remaining", 0)), 274,
		"命中帧90之后已有43个30Hz状态更新")
	assert_true(battle.start_skill(caster, target, 22), "同一施法者可再次施放")
	for _i in 90:
		battle.tick()
	assert_eq(int(target.condition_slots[0].get("ticks_remaining", 0)), 360,
		"相同优先级重新施加并刷新时长")
	for _i in 180:
		battle.tick()
	assert_eq(int(target.condition_slots[0].get("condition_id", 0)), 0,
		"180个30Hz更新后状态过期")


func test_技能22效果6同种子保留相同状态和随机流() -> void:
	var a := _battle()
	var b := _battle()
	var target_a: BattleUnit = a.units[2]
	var target_b: BattleUnit = b.units[2]
	a.start_skill(a.units[0], target_a, 22)
	b.start_skill(b.units[0], target_b, 22)
	for _i in 93:
		a.tick()
		b.tick()
	assert_eq(target_a.condition_slots, target_b.condition_slots,
		"相同种子应得到相同的条件6应用结果")
	assert_eq(a.rng.state, b.rng.state,
		"抵抗分支即使忽略随机值也要在两场战斗中消耗相同随机流")


func test_同种子阶段序列完全一致() -> void:
	var a := _battle()
	var b := _battle()
	a.start_skill(a.units[0], a.units[1], 29)
	b.start_skill(b.units[0], b.units[1], 29)
	for _i in 221:
		a.tick()
		b.tick()
	assert_eq(a.skill_events, b.skill_events, "相同种子阶段事件一致")
	assert_eq(a.units[1].hp, b.units[1].hp, "战斗结果一致")


func test_连续施放动作时钟均从首帧开始() -> void:
	var battle := _battle()
	var caster: BattleUnit = battle.units[0]
	caster.mp_max = 2 * int(SimTables.attack(29).get("mp_cost", 0))
	caster.mp = caster.mp_max
	var target: BattleUnit = battle.units[1]
	battle.start_skill(caster, target, 29)
	assert_eq(caster.skill_phase_started_frame, 0, "首轮施法起点")
	assert_eq(caster.skill_action, 12, "首轮 action12")
	for _i in 221:
		battle.tick()
	assert_true(battle.start_skill(caster, target, 29), "第二轮可启动")
	assert_eq(caster.skill_phase_started_frame, 221, "第二轮使用新起点")
	assert_eq(caster.skill_action, 12, "第二轮仍从 action12 开始")


func test_特效寿命与人物恢复允许重叠() -> void:
	var battle := _battle()
	battle.start_skill(battle.units[0], battle.units[1], 29)
	assert_eq(battle.active_fx_events().size(), 1, "施法特效启动")
	assert_eq([int(battle.active_fx_events()[0].global_id), battle.active_fx_events()[0].anchor],
		[2050, "source"], "2050 位于源格")
	for _i in 60:
		battle.tick()
	var release := battle.active_fx_events()
	assert_eq(release.map(func(event): return int(event.global_id)), [2098, 3017, 3032],
		"释放时施法已清除；释放、同步和命中视觉同时存在")
	for _i in 24:
		battle.tick()
	var impact := battle.active_fx_events()
	assert_eq(battle.units[0].state, BattleUnit.State.RECOVER, "演员已进入恢复")
	assert_eq(impact.size(), 3, "恢复不会提前删除仍存活的特效")
	assert_eq([int(impact[2].global_id), impact[2].anchor, impact[2].to_cell],
		[3032, "target", [12, 10]], "3032 位于目标格")
	for _i in 45:
		battle.tick()
	assert_eq(battle.active_fx_events().size(), 0, "恢复完成后无特效残留")


func test_演示配置可切换技能或关闭() -> void:
	var base := {"move_interval": 9999, "attack_interval": 9999, "units": [
		{"name": "caster", "faction": 0, "job_id": 9, "level": 10,
			"stats": {}, "pos": [10, 10], "anim_id": "D0A"},
		{"name": "target", "faction": 1, "job_id": 1, "level": 10,
			"stats": {}, "pos": [12, 10], "anim_id": "B1A"},
	], "skill_demo": {"enabled": true, "skill_id": 22, "caster_unit": 0,
		"target_unit": 1, "start_frame": 1, "repeat": false, "exclusive": true}}
	var switched := Battle.start(base, 7, null)
	switched.tick()
	assert_eq(int(switched.skill_events[0].skill_id), 22, "只改配置即可切换技能")
	base["skill_demo"]["enabled"] = false
	var disabled := Battle.start(base, 7, null)
	for _i in 20:
		disabled.tick()
	assert_eq(disabled.skill_events.size(), 0, "配置可关闭演出")


func test_技能22演示绑定敌方和黄金动作档() -> void:
	var setup: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/battle_setup.json"))
	var demo: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/skill_demo.json"))
	var caster: Dictionary = setup["units"][int(demo["caster_unit"])]
	var target: Dictionary = setup["units"][int(demo["target_unit"])]
	assert_eq(int(demo["skill_id"]), 22, "可见样例运行技能22")
	assert_true(int(caster["faction"]) != int(target["faction"]), "样例目标为敌方")
	var sprites: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/unit_sprites.json"))
	var unit: Dictionary = sprites["units"].get(String(caster["anim_id"]), {})
	assert_eq(String(caster["anim_id"]), "C1A", "演示使用任务1.3选定的黄金动作档")
	assert_false(unit.is_empty(), "演示施法者C1A精灵档存在")
	setup["skill_demo"] = demo
	var battle := Battle.start(setup, int(setup.get("seed", 42)), null)
	for _i in int(demo["start_frame"]):
		battle.tick()
	assert_eq(battle.skill_events.size(), 1, "配置时刻只启动一个施法阶段")
	if battle.skill_events.is_empty():
		return
	assert_eq(int(battle.skill_events[0].get("skill_id", -1)), 22, "样例事件来自技能22")
	for direction in ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]:
		for action in [13, 31, 16]:
			var entry := AnimTimeline.unit_action_entry(unit, action, direction)
			var timeline := AnimTimeline.resolve(unit, entry)
			assert_false(timeline.get("steps", []).is_empty(),
				"C1A action%d 的 %s 方向时间线存在" % [action, direction])
			var visible_frames := {}
			for step: Dictionary in timeline.get("steps", []):
				for layer: Dictionary in step.get("layers", []):
					visible_frames[int(layer.get("frame", -1))] = true
			assert_true(visible_frames.size() >= (2 if action == 31 else 1),
				"C1A action%d 的 %s 方向达到演示可见帧要求" % [action, direction])
