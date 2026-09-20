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
