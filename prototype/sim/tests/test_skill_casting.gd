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


func test_技能29固定阶段与120tick空白同步() -> void:
	var battle := _battle()
	assert_true(battle.start_skill(battle.units[0], battle.units[1], 29), "技能可启动")
	for _i in 221:
		battle.tick()
	var phases: Array = battle.skill_events.map(func(event): return String(event.phase))
	var starts: Array = battle.skill_events.map(func(event): return int(event.frame))
	assert_eq(phases, ["cast", "release", "sync", "impact", "recovery"], "阶段顺序")
	assert_eq(starts, [0, 60, 86, 146, 176], "阶段起始固定")
	assert_eq(int(battle.skill_events[2].duration_frames), 60,
		"3017 的120动画tick换算为60逻辑帧")
	assert_eq(int(battle.skill_events[3].global_id), 3032, "同步结束后才启动命中")
	assert_eq(battle.units[0].state, BattleUnit.State.IDLE, "恢复完成后待机")


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
	assert_eq(int(enemy.condition_slots[0].get("ticks_remaining", 0)), 3746, "状态按原版时长递减")
	assert_eq(int(enemy.condition_slots[0].get("tick_counter", 0)), 54, "状态辅助计数按原版180 tick回绕")
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
	assert_eq(int(gameplay_result.get("resolved_frame", -1)), int(impact_event.get("frame", -2)),
		"技能29记录玩法结算帧")


func test_技能22仅命中敌方且目标离开选定格时不写入状态() -> void:
	var battle := _battle()
	var caster: BattleUnit = battle.units[0]
	var ally: BattleUnit = battle.units[1]
	var enemy: BattleUnit = battle.units[2]
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
	for _i in 93:
		applicable.tick()
	assert_eq(int(target_a.condition_slots[0].get("ticks_remaining", 0)), 190,
		"AGI20 的3800基础值被5%魔抗通道缩至190，超过183")

	var resisted := _battle()
	var caster_b: BattleUnit = resisted.units[0]
	var target_b: BattleUnit = resisted.units[2]
	target_b.unit.magic_resist = 96
	resisted.start_skill(caster_b, target_b, 22)
	for _i in 93:
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
	assert_eq(int(target.condition_slots[0].get("ticks_remaining", 0)), 280,
		"恢复阶段结束前已有40个30Hz更新经过")
	assert_true(battle.start_skill(caster, target, 22), "同一施法者可再次施放")
	for _i in 93:
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
	var target: BattleUnit = battle.units[1]
	battle.start_skill(caster, target, 29)
	assert_eq(caster.skill_phase_started_frame, 0, "首轮施法起点")
	assert_eq(caster.skill_action, 12, "首轮 action12")
	for _i in 221:
		battle.tick()
	assert_true(battle.start_skill(caster, target, 29), "第二轮可启动")
	assert_eq(caster.skill_phase_started_frame, 221, "第二轮使用新起点")
	assert_eq(caster.skill_action, 12, "第二轮仍从 action12 开始")


func test_特效生命周期与锚点由阶段事件决定() -> void:
	var battle := _battle()
	battle.start_skill(battle.units[0], battle.units[1], 29)
	assert_eq(battle.active_fx_events().size(), 1, "施法特效启动")
	assert_eq([int(battle.active_fx_events()[0].global_id), battle.active_fx_events()[0].anchor],
		[2050, "source"], "2050 位于源格")
	for _i in 60:
		battle.tick()
	var release := battle.active_fx_events()
	assert_eq(release.size(), 1, "释放时持续施法已清除")
	assert_eq(int(release[0].global_id), 2098, "释放实例唯一")
	for _i in 86:
		battle.tick()
	var impact := battle.active_fx_events()
	assert_eq(impact.size(), 1, "命中特效启动")
	assert_eq([int(impact[0].global_id), impact[0].anchor, impact[0].to_cell],
		[3032, "target", [12, 10]], "3032 位于目标格")
	for _i in 75:
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


func test_技能29可见演示使用多帧施法动作() -> void:
	var setup: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/battle_setup.json"))
	var demo: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/skill_demo.json"))
	var caster: Dictionary = setup["units"][int(demo["caster_unit"])]
	var sprites: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/unit_sprites.json"))
	var unit: Dictionary = sprites["units"].get(String(caster["anim_id"]), {})
	assert_false(unit.is_empty(), "演示施法者精灵档存在")
	for direction in ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]:
		var entry := AnimTimeline.unit_action_entry(unit, 12, direction)
		var timeline := AnimTimeline.resolve(unit, entry)
		var visible_frames := {}
		for step: Dictionary in timeline.get("steps", []):
			for layer: Dictionary in step.get("layers", []):
				visible_frames[int(layer.get("frame", -1))] = true
		assert_true(visible_frames.size() >= 2,
			"演示 action12 的 %s 方向必须肉眼可见地变化" % direction)
