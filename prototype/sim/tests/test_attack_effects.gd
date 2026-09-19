extends "res://sim/tests/test_base.gd"
## 攻击特效 v2：表加载、最终描述符帧、多图层、事件字段、配置与回退。

const Timeline := preload("res://sim/anim_timeline.gd")


func _effects() -> Dictionary:
	return JSON.parse_string(FileAccess.get_file_as_string("res://data/attack_effects.json"))


func test_特效表加载() -> void:
	var parsed := _effects()
	assert_eq(int(parsed["_meta"].get("schema_version", 0)), 2, "schema v2")
	var files: Dictionary = parsed.get("files", {})
	assert_true(files.has("01E"), "01E 已导出")
	var entry: Dictionary = files.get("01E", {})
	assert_eq(entry.get("frames", []).size(), int(entry.get("frame_count", -1)), "帧数一致")
	var effects: Dictionary = parsed.get("effects", {})
	assert_false(parsed.has("default"), "不得为未映射攻击提供全局默认特效")
	for effect_id in parsed.get("effect_ids", {}):
		assert_true(int(effect_id) > 0, "仅允许非零原版效果 ID")
		assert_true(effects.has(String(parsed["effect_ids"][effect_id])), "效果 ID 指向已定义效果")
	for effect_name in effects:
		assert_true(files.has(String(effects[effect_name].get("file", ""))),
			"%s 指向已导出档" % effect_name)


func test_最终时间线与复合层有效() -> void:
	var parsed := _effects()
	var entry: Dictionary = parsed["files"]["01E"]
	var animations: Array = entry["anims"]
	for effect_name in parsed["effects"]:
		var config: Dictionary = parsed["effects"][effect_name]
		var animation_id := int(config.get("anim", -1))
		assert_true(animation_id >= 0 and animation_id < animations.size(), "%s anim id" % effect_name)
		var timeline := Timeline.normalize(animations[animation_id])
		assert_true(timeline["steps"].size() >= 4, "%s 至少4个 step" % effect_name)
		for step: Dictionary in timeline["steps"]:
			for layer: Dictionary in step["layers"]:
				assert_true(int(layer["frame"]) >= 0 and int(layer["frame"]) < entry["frames"].size(),
					"%s 图层帧界内" % effect_name)
	var slash: Dictionary = animations[int(parsed["effects"]["slash"]["anim"])]
	assert_eq(int(parsed["effects"]["slash"]["anim"]), 21, "斩击使用正确程序")
	assert_eq([int(slash["steps"][4]["layers"][0]["frame"]),
		int(slash["steps"][4]["layers"][1]["frame"])], [40, 4], "父层与紫色斩击并发")
	var orb: Dictionary = animations[int(parsed["effects"]["orb"]["anim"])]
	var orb_frames: Array = []
	for step: Dictionary in orb["steps"]:
		orb_frames.append(int(step["layers"][0]["frame"]))
	assert_eq(orb_frames, [18, 19, 20, 21, 22, 6], "旋转体最终帧链")


func test_攻击事件字段与上限() -> void:
	var setup: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/battle_setup.json"))
	var battle := Battle.start(setup, 7, null)
	for _i in 2000:
		battle.tick()
		if battle.finished:
			break
	assert_true(battle.fx_events.size() > 0, "应产生攻击特效事件")
	for event in battle.fx_events:
		assert_eq(event.get("type", ""), "attack", "事件类型")
		assert_true(event.get("from_cell", []).size() == 2 and event.get("to_cell", []).size() == 2,
			"双方格坐标")
		assert_true(event.get("hit") is bool and int(event.get("damage", -1)) >= 0, "命中和伤害字段")
		assert_true(int(event.get("attack_id", -1)) >= 0, "包含攻击条目 ID")
		assert_eq(int(event.get("effect_id", -1)), 0, "样例普通攻击无外置命中特效")
	assert_true(battle.fx_events.size() <= battle.fx_events_keep, "事件流受上限约束")


func test_普通攻击记录起始帧并朝向目标() -> void:
	var setup := {"move_interval": 99, "attack_interval": 1, "units": [
		{"name": "a", "faction": 0, "job_id": 1, "level": 10,
			"stats": {}, "pos": [10, 10], "anim_id": "A0A"},
		{"name": "d", "faction": 1, "job_id": 3, "level": 10,
			"stats": {}, "pos": [9, 10], "anim_id": "B1A"},
	]}
	var battle := Battle.start(setup, 7, null)
	battle.tick()
	var attacker: BattleUnit = battle.units[0]
	assert_eq(attacker.attack_started_frame, battle.frame, "攻击起始帧")
	assert_eq(attacker.facing, Vector2i(-1, 0), "朝向左侧目标")
	assert_eq(attacker.attack_id, 101, "职业1默认攻击")
	assert_eq(attacker.effect_id, 0, "普通攻击效果 ID 为0")


func test_显式职业覆盖与无映射回退() -> void:
	var setup: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/battle_setup.json"))
	var parsed := _effects()
	var effects: Dictionary = parsed["effects"]
	for key in setup.get("attack_effects", {}):
		assert_true(effects.has(String(setup["attack_effects"][key])),
			"attack_effects[%s] 指向已定义效果" % key)
	assert_false(parsed.get("effect_ids", {}).has("0"), "effect 0 明确表示无外置特效")
	assert_false(effects.has("__nope__"), "未知效果名由视图跳过")
