extends "res://sim/tests/test_base.gd"
## EFCT 全局特效：表加载、最终描述符帧、多图层、事件字段与回退。

const Timeline := preload("res://sim/anim_timeline.gd")


func _effects() -> Dictionary:
	return JSON.parse_string(FileAccess.get_file_as_string("res://data/attack_effects.json"))


func test_特效表加载() -> void:
	var parsed := _effects()
	assert_eq(int(parsed["_meta"].get("schema_version", 0)), 3, "schema v3")
	assert_true(String(parsed["_meta"].get("source", "")).ends_with("EFCT.BIN"), "权威资源 EFCT.BIN")
	var animations: Dictionary = parsed.get("animations", {})
	assert_eq([int(animations["2042"].block), int(animations["2042"].animation)],
		[1, 42], "2042 全局映射")
	assert_eq([int(animations["3027"].block), int(animations["3027"].animation)],
		[2, 27], "3027 全局映射")
	for global_id in ["2050", "2098", "3017", "3032"]:
		assert_true(animations.has(global_id), "技能29包含 %s" % global_id)


func test_最终时间线与复合层有效() -> void:
	var parsed := _effects()
	var animations: Dictionary = parsed["animations"]
	var frames: Dictionary = parsed["frames"]
	for global_id in animations:
		var timeline := Timeline.normalize(animations[global_id])
		for step: Dictionary in timeline["steps"]:
			for layer: Dictionary in step["layers"]:
				assert_true(frames.has(str(int(layer["frame"]))), "%s 图层帧已导出" % global_id)
	assert_eq([int(animations["2042"]["steps"][3]["layers"][0]["frame"]),
		int(animations["2042"]["steps"][3]["layers"][1]["frame"])],
		[899, 893], "复合层保持绘制顺序")
	assert_eq(int(animations["3017"].duration_ticks), 120, "空白同步时长保留")


func test_EFCT导入纹理保留颜色与透明通道() -> void:
	var tex: Texture2D = load("res://assets/fx/EFCT/frame_1305.png")
	assert_true(tex != null, "命中特效纹理可加载")
	var image := tex.get_image()
	var transparent := 0
	var colored := 0
	for y in image.get_height():
		for x in image.get_width():
			var pixel := image.get_pixel(x, y)
			if pixel.a < 0.1:
				transparent += 1
			elif absf(pixel.r - pixel.g) > 0.05 or absf(pixel.g - pixel.b) > 0.05:
				colored += 1
	assert_true(transparent > 0, "导入后仍有透明像素")
	assert_true(colored > 0, "导入后仍有非灰白颜色")


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
		assert_eq(int(event.get("gameplay_effect_id", -1)), 0, "样例普通攻击玩法效果为0")
		var visuals: Dictionary = event.get("visual_ids", {})
		assert_eq([int(visuals.get("cast", -1)), int(visuals.get("release", -1)),
			int(visuals.get("sync", -1)), int(visuals.get("impact", -1))],
			[0, 0, 0, 0], "普通攻击不生成独立外置特效")
		assert_false(event.has("effect_id"), "旧 effect_id 字段已移除")
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
	assert_eq(attacker.gameplay_effect_id, 0, "普通攻击玩法效果 ID 为0")
	assert_eq([attacker.cast_fx, attacker.release_fx, attacker.sync_fx, attacker.impact_fx],
		[0, 0, 0, 0], "普通攻击视觉 ID 均为0")


func test_显式职业覆盖与无映射回退() -> void:
	var setup: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/battle_setup.json"))
	var parsed := _effects()
	assert_false(parsed.get("animations", {}).has("0"), "global_id 0 明确表示无外置特效")
	assert_false(parsed.get("animations", {}).has("9999"), "未知全局动画由视图跳过")
