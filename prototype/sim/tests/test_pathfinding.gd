extends "res://sim/tests/test_base.gd"
## SimPath 寻路验收 (tasks 1.1-1.4)


func _rules() -> Dictionary:
	return JSON.parse_string(FileAccess.get_file_as_string("res://data/walk_rules.json"))


func _mini_map(w: int, h: int, walls: Array) -> SimMapData:
	# 构造迷你地图: walls = [[x,y], ...] 全部记到 object 层 (默认规则即阻挡)
	var m := SimMapData.new()
	m.cell_w = w
	m.cell_h = h
	var cells := w * h
	var obj: Array = []
	obj.resize(cells)
	obj.fill(0)
	for p in walls:
		obj[p[1] * w + p[0]] = 1
	var zero: Array = []
	zero.resize(cells)
	zero.fill(0)
	m._layers = {"terrain": zero.duplicate(), "variant": zero.duplicate(), "object": obj}
	return m


func test_walkable_rules() -> void:
	var m := _mini_map(4, 4, [[1, 1]])
	var rules := _rules()
	assert_false(m.is_walkable(1, 1, rules), "object=1 阻挡")
	assert_true(m.is_walkable(0, 0, rules), "object=0 可走")
	assert_false(m.is_walkable(-1, 0, rules), "越界不可走")
	var custom := {"blocked_terrain": [5], "blocked_variant": [], "blocked_objects": "nonzero"}
	var m2 := _mini_map(3, 3, [])
	m2._layers["terrain"][0] = 5
	assert_false(m2.is_walkable(0, 0, custom), "自定义 terrain 阻断")


func test_straight_path() -> void:
	var m := _mini_map(8, 3, [])
	var path := SimPath.find_path(m, _rules(), Vector2i(2, 1), Vector2i(5, 1))
	assert_eq(path.size(), 3, "直线长度")
	assert_eq(path[0], Vector2i(3, 1), "首步")
	assert_eq(path[2], Vector2i(5, 1), "终点")


func test_around_u_wall() -> void:
	# U 形墙: x=3 竖墙 y=0..2, 顶部 x=1..3 封住 — 绕底走
	var walls := [[3, 0], [3, 1], [3, 2]]
	var m := _mini_map(6, 5, walls)
	var path := SimPath.find_path(m, _rules(), Vector2i(1, 1), Vector2i(5, 1))
	assert_true(path.size() > 0, "可达")
	assert_eq(path[path.size() - 1], Vector2i(5, 1), "终点正确")
	for p in path:
		assert_true(m.is_walkable(p.x, p.y, _rules()), "路径格可走 (%d,%d)" % [p.x, p.y])


func test_unreachable() -> void:
	var walls := [[2, 0], [2, 1], [2, 2], [2, 3], [2, 4]]
	var m := _mini_map(5, 5, walls)   # 整列封死
	var path := SimPath.find_path(m, _rules(), Vector2i(1, 2), Vector2i(4, 2))
	assert_eq(path.size(), 0, "不可达返回空")


func test_deterministic_path() -> void:
	var m := _mini_map(10, 10, [[4, 4], [5, 5], [6, 6]])
	var a := SimPath.find_path(m, _rules(), Vector2i(0, 0), Vector2i(9, 9))
	var b := SimPath.find_path(m, _rules(), Vector2i(0, 0), Vector2i(9, 9))
	assert_eq(a, b, "同输入同路径")


func test_occupied_detour_and_degenerate() -> void:
	var m := _mini_map(7, 3, [])
	var rules := _rules()
	# 占格绕行: (3,1) 被占
	var blocked := {Vector2i(3, 1): true}
	var path := SimPath.find_path(m, rules, Vector2i(1, 1), Vector2i(5, 1), blocked)
	assert_eq(path[path.size() - 1], Vector2i(5, 1), "绕行后仍达")
	assert_false(path.has(Vector2i(3, 1)), "路径避开占格")
	# 目标本身被占 → 退化到目标的可走邻格
	var path2 := SimPath.find_path(m, rules, Vector2i(1, 1), Vector2i(3, 1), blocked)
	assert_true(_is_neighbor_of(path2[path2.size() - 1], Vector2i(3, 1)), "终点为目标邻格")


func _is_neighbor_of(a: Vector2i, b: Vector2i) -> bool:
	return absi(a.x - b.x) + absi(a.y - b.y) == 1


func test_perf_real_map() -> void:
	var m := SimMapData.load_map("01")
	var rules := _rules()
	var t0: int = Time.get_ticks_msec()
	for i in 1000:
		SimPath.find_path(m, rules, Vector2i(2, 2), Vector2i(60, 90))
	var ms: int = Time.get_ticks_msec() - t0
	assert_true(ms < 1000, "1000 次跨图 BFS < 1s (实际 %d ms)" % ms)
