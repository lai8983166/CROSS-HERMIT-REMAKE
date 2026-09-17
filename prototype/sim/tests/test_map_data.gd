extends "res://sim/tests/test_base.gd"
## SimMapData 验收 (tasks 2.1): 加载/格值/换算往返/越界

func test_load_map01() -> void:
	var m := SimMapData.load_map("01")
	assert_eq(m.cell_w, 64, "cell_w")
	assert_eq(m.cell_h, 96, "cell_h")
	assert_true(m.has_layer("terrain") and m.has_layer("variant") and m.has_layer("object"), "三层齐")
	assert_eq(m._layers["terrain"].size(), 64 * 96, "terrain 长度 6144")

func test_cell_value_matches_json() -> void:
	# 与磁盘 JSON 自洽对照 (取若干格)
	var m := SimMapData.load_map("01")
	var parsed: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/map01.json"))
	var terrain: Array = parsed["layers"]["terrain"]
	for xy in [[0, 0], [31, 47], [63, 95], [10, 5]]:
		assert_eq(m.layer_value("terrain", xy[0], xy[1]),
			terrain[xy[1] * 64 + xy[0]], "(%d,%d) 与 JSON 一致" % [xy[0], xy[1]])

func test_roundtrip_all_cells() -> void:
	var m := SimMapData.load_map("01")
	for y in m.cell_h:
		for x in m.cell_w:
			var w: Vector2 = m.cell_to_world(x, y)
			var back: Vector2i = m.world_to_cell(w)
			if back.x != x or back.y != y:
				assert_eq(back, Vector2i(x, y), "往返失败于 (%d,%d)" % [x, y])
				return
	assert_true(true, "64×96 全格往返恒等")

func test_out_of_range() -> void:
	var m := SimMapData.load_map("01")
	assert_eq(m.layer_value("terrain", -1, 0), -1, "负 x")
	assert_eq(m.layer_value("terrain", 64, 0), -1, "x 越界")
	assert_eq(m.layer_value("terrain", 0, 96), -1, "y 越界")
	assert_eq(m.layer_value("no_such_layer", 0, 0), -1, "未知层")

func test_world_to_cell_diamond() -> void:
	var m := SimMapData.new()
	# 格心 (0,0) 局部 (0,0); 其右下 45° 方向仍属 (1,0) 或 (0,1) 的判定
	assert_eq(m.world_to_cell(Vector2(0, 0)), Vector2i(0, 0), "原点")
	assert_eq(m.world_to_cell(Vector2(8, 4)), Vector2i(1, 0), "右下方向 → (1,0)")
	assert_eq(m.world_to_cell(Vector2(-8, 4)), Vector2i(0, 1), "左下方向 → (0,1)")
