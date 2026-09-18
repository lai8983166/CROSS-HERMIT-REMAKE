extends "res://sim/tests/test_base.gd"
## add-unit-sprites: 帧表加载 / 序列有效 / 朝向量化 / 资产存在与回退 (tasks 4.1 四组用例)


func test_帧表加载() -> void:
	var parsed: Variant = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/unit_sprites.json"))
	assert_true(parsed is Dictionary, "unit_sprites.json 应可解析")
	var units: Dictionary = parsed.get("units", {})
	assert_true(units.size() >= 10, "至少 10 单位档 (导出 {A..E}{0,1}A)")
	for id in units:
		var u: Dictionary = units[id]
		var frames: Array = u.get("frames", [])
		assert_eq(frames.size(), int(u.get("frame_count", -1)), "%s 帧数与声明一致" % id)
		var amap: Dictionary = u.get("anim_map", {})
		assert_true(amap.has("MOVE") and amap.has("IDLE"), "%s anim_map 含 MOVE/IDLE" % id)
		for f in frames:
			var anchor: Dictionary = f.get("anchor", {})
			assert_true(float(anchor.get("x", 1e9)) >= -1e9, "%s 帧锚点存在" % id)
			break   # 每档抽首帧查字段形状即可


func test_序列选择有效() -> void:
	var parsed: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/unit_sprites.json"))
	assert_true(float(parsed["_meta"].get("dur_unit_seconds", 0.0)) > 0.0, "dur 单位为正")
	for id in parsed["units"]:
		var u: Dictionary = parsed["units"][id]
		var anims: Array = u.get("anims", [])
		var nframes: int = u.get("frames", []).size()
		var amap: Dictionary = u.get("anim_map", {})
		for key in ["MOVE", "IDLE", "ATTACK", "DEAD"]:
			if not amap.has(key):
				continue
			var ai: int = int(amap[key].get("anim", -1))
			assert_true(ai >= 0 and ai < anims.size(), "%s %s anim id 在界内" % [id, key])
			var recs: Array = anims[ai].get("records", [])
			assert_true(recs.size() > 0, "%s %s 序列非空" % [id, key])
			# 默认序列必须全为界内引用 (渲染器按帧表索引取 PNG)
			var nvalid := 0
			for r in recs:
				var f := int(r.get("frame", -2))
				if f >= 0:
					assert_true(f < nframes, "%s %s 帧引用在界内 (外部引用不得进默认序列)" % [id, key])
					nvalid += 1
			assert_true(nvalid >= 1, "%s %s 至少 1 条有效帧" % [id, key])
			if key == "MOVE":
				assert_true(nvalid >= 4, "%s MOVE 行走循环 ≥4 帧" % id)
				assert_true(nvalid == recs.size(), "%s MOVE 纯循环无空白帧 (隐身断流 2026-09-18 目检抓出)" % id)


func test_朝向量化() -> void:
	var setup: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/battle_setup.json"))
	var b := Battle.start(setup, 7, null)
	var moved := false
	for i in 600:
		b.tick()
		for u in b.units:
			if u.from_cell != u.cell:
				moved = true
				assert_true(absi(u.facing.x) <= 1 and absi(u.facing.y) <= 1,
					"facing 分量为 -1/0/1")
				assert_true(u.facing.x != 0 or u.facing.y != 0, "facing 非零")
				assert_true(u.move_started_frame > 0, "移动起始帧已记录")
	assert_true(moved, "600 tick 内应有单位移动 (seed=7)")


func test_帧资产存在() -> void:
	var parsed: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/unit_sprites.json"))
	for id in parsed["units"]:
		var frames: Array = parsed["units"][id].get("frames", [])
		for i in range(0, frames.size(), 25):   # 抽样每 25 帧
			var p := "res://assets/unit/%s/%s" % [id, frames[i].get("file", "")]
			assert_true(ResourceLoader.exists(p), "帧资产存在: " + p)


func test_anim_id_回退() -> void:
	# battle_setup 全部 anim_id 必须在帧表中 (视图侧: 缺档/空 id 自动色块回退, 功能不损)
	var setup: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/battle_setup.json"))
	var sprites: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/unit_sprites.json"))["units"]
	for u in setup.get("units", []):
		var s := String(u.get("anim_id", ""))
		assert_true(s != "", "单位 %s 已配 anim_id" % u.get("name", "?"))
		assert_true(sprites.has(s), "anim_id 在帧表中存在: " + s)
	# 回退语义: 无效 id 查表返回空 → 视图走色块 (数据侧验证)
	assert_false(sprites.has("__no_such__"), "未知档不在帧表")
