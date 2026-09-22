extends "res://sim/tests/test_base.gd"
## DxAnim v2：数据完整性、八方向、时间线选择、相位重置、坐标和旧 schema 兼容。

const Timeline := preload("res://sim/anim_timeline.gd")


func _sprites() -> Dictionary:
	return JSON.parse_string(FileAccess.get_file_as_string("res://data/unit_sprites.json"))


func test_v2帧表与八方向完整() -> void:
	var parsed := _sprites()
	assert_eq(int(parsed["_meta"].get("schema_version", 0)), 2, "schema v2")
	assert_true(float(parsed["_meta"].get("tick_seconds", 0.0)) > 0.0, "tick 单位为正")
	var directions := ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
	var expected := {"N": [11, 0], "NE": [12, 1], "E": [13, 1], "SE": [14, 1],
		"S": [15, 0], "SW": [14, 0], "W": [13, 0], "NW": [12, 0]}
	for id in parsed["units"]:
		var unit: Dictionary = parsed["units"][id]
		var frames: Array = unit.get("frames", [])
		assert_eq(frames.size(), int(unit.get("frame_count", -1)), "%s 帧数" % id)
		var mapping: Dictionary = unit.get("anim_map", {}).get("walk_by_dir", {})
		for direction in directions:
			assert_true(mapping.has(direction), "%s 有 %s 方向" % [id, direction])
			var entry: Dictionary = mapping.get(direction, {})
			assert_eq(int(entry.get("block", -1)), 0, "%s 直接使用 block0" % direction)
			assert_eq([int(entry.get("anim", -1)), int(entry.get("flags", -1))], expected[direction],
				"%s 使用角度表指定动画和镜像" % direction)


func test_时间线图层全部界内() -> void:
	var parsed := _sprites()
	for id in parsed["units"]:
		var unit: Dictionary = parsed["units"][id]
		var frame_count: int = unit.get("frames", []).size()
		for animation: Dictionary in unit.get("anims", []):
			var timeline := Timeline.normalize(animation)
			assert_true(not timeline.get("steps", []).is_empty(), "%s anim#%d 非空" % [id, animation["id"]])
			for step: Dictionary in timeline["steps"]:
				assert_true(int(step.get("duration_ticks", 0)) > 0, "持续 tick 为正")
				for layer: Dictionary in step.get("layers", []):
					var frame := int(layer.get("frame", -1))
					assert_true(frame >= 0 and frame < frame_count, "%s 图层帧界内" % id)
		var blocks: Dictionary = unit.get("anim_blocks", {})
		for block_id in blocks:
			var animations: Dictionary = blocks[block_id]
			for animation_id in animations:
				var timeline := Timeline.normalize(animations[animation_id])
				assert_true(not timeline["steps"].is_empty(), "%s block%s/%s 非空" % [id, block_id, animation_id])
				for step: Dictionary in timeline["steps"]:
					assert_true(int(step["duration_ticks"]) > 0, "附加动画持续 tick 为正")
					for layer: Dictionary in step["layers"]:
						var frame := int(layer.get("frame", -1))
						assert_true(frame >= 0 and frame < frame_count, "%s 附加动画帧界内" % id)


func test_A0A与B1A移动黄金序列() -> void:
	var parsed := _sprites()
	var expected := {
		"A0A": {11: [244,245,246,247,248,249], 12: [238,239,240,241,242,243],
			13: [232,233,234,235,236,237], 14: [226,227,228,229,230,231],
			15: [220,221,222,223,224,225]},
		"B1A": {11: [224,225,226,227,228,229], 12: [218,219,220,221,222,223],
			13: [212,213,214,215,216,217], 14: [206,207,208,209,210,211],
			15: [200,201,202,203,204,205]},
	}
	for id in expected:
		var animations: Array = parsed["units"][id]["anims"]
		for animation in expected[id]:
			var timeline: Dictionary = animations[int(animation)]
			assert_eq(int(timeline.get("loop_from", -1)), 0, "%s #%d 从0循环" % [id, animation])
			var got: Array = []
			for step: Dictionary in timeline["steps"]:
				got.append(int(step["layers"][0]["frame"]))
			assert_eq(got, expected[id][animation], "%s #%d 最终帧" % [id, animation])


func test_攻击八方向与单次播放() -> void:
	var parsed := _sprites()
	var expected := {"N": [21, 0], "NE": [22, 1], "E": [23, 1], "SE": [24, 1],
		"S": [25, 0], "SW": [24, 0], "W": [23, 0], "NW": [22, 0]}
	for id in ["A0A", "B1A"]:
		var unit: Dictionary = parsed["units"][id]
		var mapping: Dictionary = unit["anim_map"]["attack_by_dir"]
		for direction in expected:
			var entry: Dictionary = mapping[direction]
			assert_eq([int(entry["anim"]), int(entry["flags"])], expected[direction],
				"%s %s action5 映射" % [id, direction])
			assert_eq(int(entry["action"]), 5, "原版动作号")
		var north := Timeline.resolve(unit, mapping["N"])
		var total := Timeline.total_ticks(north)
		assert_eq(total, 36 if id == "A0A" else 48, "%s 攻击总时长" % id)
		assert_true(Timeline.step_at(north, total - 1, false).has("step"), "末 tick 可见")
		assert_true(Timeline.step_at(north, total, false).is_empty(), "结束后不循环")


func test_旧单帧记录兼容() -> void:
	var timeline := Timeline.normalize({"records": [
		{"frame": 3, "dur": 2}, {"frame": -1, "dur": 1}, {"frame": 4, "dur": 3}]})
	assert_eq(timeline["steps"].size(), 3, "旧 records 转为三个 step")
	assert_eq(int(timeline["steps"][0]["layers"][0]["frame"]), 3, "旧帧保留")
	assert_true(bool(timeline["steps"][0]["layers"][0]["legacy_anchor"]), "使用旧 anchor")
	assert_true(timeline["steps"][1]["layers"].is_empty(), "-1 转为空白层")
	assert_eq(int(Timeline.step_at(timeline, 6, true)["step"]["layers"][0]["frame"]), 3,
		"无 loop_from 的旧单位序列整段循环")


func test_相位在动作或方向变化时重置() -> void:
	var clock := {}
	assert_eq(Timeline.clock_elapsed(clock, "MOVE/E/12/0", 100), 0, "首次从0开始")
	assert_eq(Timeline.clock_elapsed(clock, "MOVE/E/12/0", 104), 4, "同身份继续")
	assert_eq(Timeline.clock_elapsed(clock, "MOVE/N/14/1", 104), 0, "换方向重置")
	assert_eq(Timeline.clock_elapsed(clock, "IDLE/N/7/0", 110), 0, "换动作重置")


func test_技能动作与空槽待机回退() -> void:
	var parsed := _sprites()
	var d0: Dictionary = parsed["units"]["D0A"]
	var cast := Timeline.unit_action_entry(d0, 12, "N")
	var recover := Timeline.unit_action_entry(d0, 15, "N")
	assert_eq([int(cast.anim), int(cast.action)], [56, 12], "技能29施法 action12")
	assert_eq([int(recover.anim), int(recover.action)], [71, 15], "技能29恢复 action15")
	var a0: Dictionary = parsed["units"]["A0A"]
	var fallback := Timeline.unit_action_entry(a0, 13, "N")
	assert_eq(int(fallback.anim), int(a0["anim_map"]["IDLE"].anim), "空动作回退待机")


func test_技能22动作31跨块解析与空档回退() -> void:
	var parsed := _sprites()
	var c1: Dictionary = parsed["units"]["C1A"]
	var cast := Timeline.unit_action_entry(c1, 13, "N")
	var release := Timeline.unit_action_entry(c1, 31, "N")
	var recover := Timeline.unit_action_entry(c1, 16, "N")
	assert_eq([int(cast.block), int(cast.anim)], [0, 61], "C1A 施法 action13")
	assert_eq([int(release.block), int(release.anim)], [1, 6], "C1A 释放 action31")
	assert_eq([int(recover.block), int(recover.anim)], [0, 76], "C1A 恢复 action16")
	var release_timeline := Timeline.resolve(c1, release)
	assert_eq(int(release_timeline.block), 1, "从 block1 解析")
	assert_true(release_timeline.steps.size() >= 10, "释放有多帧")
	var d0: Dictionary = parsed["units"]["D0A"]
	var d0_release := Timeline.unit_action_entry(d0, 31, "N")
	assert_eq([int(d0_release.block), int(d0_release.anim)], [0, 101], "D0A 特例在 block0")
	var e0: Dictionary = parsed["units"]["E0A"]
	var e0_release := Timeline.unit_action_entry(e0, 31, "N")
	assert_eq(int(e0_release.anim), int(e0["anim_map"]["IDLE"].anim), "E0A 缺失动作回待机")


func test_多图层坐标与顺序() -> void:
	var frame := {"w": 40, "h": 51, "canvas": {"w": 128, "h": 128, "x": 41, "y": 54},
		"anchor": {"x": 23, "y": 74}}
	var rect := Timeline.layer_rect(frame, {"descriptor": 569, "x": 0, "y": -40})
	assert_eq(rect.position, Vector2(-23, -50), "描述符使用画布中心+局部偏移")
	var legacy := Timeline.layer_rect(frame, {"legacy_anchor": true, "x": 0, "y": 0})
	assert_eq(legacy.position, Vector2(-23, -74), "旧记录位置保持旧 anchor")
	assert_eq(Timeline.combined_flip({"flip_x": false, "flip_y": false}, 1), Vector2i(1, 0),
		"方向表 bit0 水平镜像")
	assert_eq(Timeline.combined_flip({"flip_x": true, "flip_y": false}, 1), Vector2i(0, 0),
		"逐层镜像与方向镜像按异或合并")
	assert_eq(Timeline.combined_flip({"flip_x": false, "flip_y": false}, 2), Vector2i(0, 1),
		"方向表 bit1 垂直镜像")
	var fx: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/attack_effects.json"))
	var composite: Dictionary = fx["animations"]["2042"]
	assert_eq([int(composite["steps"][3]["layers"][0]["frame"]),
		int(composite["steps"][3]["layers"][1]["frame"])], [899, 893], "复合层保持绘制顺序")


func test_朝向向量和移动起始帧() -> void:
	var setup: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/battle_setup.json"))
	var battle := Battle.start(setup, 7, null)
	var moved := false
	for _i in 600:
		battle.tick()
		for unit in battle.units:
			if unit.from_cell != unit.cell:
				moved = true
				assert_true(absi(unit.facing.x) <= 1 and absi(unit.facing.y) <= 1, "facing 分量")
				assert_true(unit.facing != Vector2i.ZERO, "facing 非零")
				assert_true(unit.move_started_frame > 0, "移动起始帧已记录")
	assert_true(moved, "600 tick 内应有移动")


func test_资源存在与无效id回退() -> void:
	var parsed := _sprites()
	for id in parsed["units"]:
		var frames: Array = parsed["units"][id].get("frames", [])
		for index in range(0, frames.size(), 25):
			var path := "res://assets/unit/%s/%s" % [id, frames[index].get("file", "")]
			assert_true(ResourceLoader.exists(path), "帧资源存在 " + path)
	assert_false(parsed["units"].has("__no_such__"), "无效 anim_id 由视图回退色块")
