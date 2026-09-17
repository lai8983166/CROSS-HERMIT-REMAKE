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
	# 文件默认 = 全开放 (object 层实测为条纹装饰, 见 walk_rules.json _meta)
	var m := _mini_map(4, 4, [[1, 1]])
	assert_true(m.is_walkable(1, 1, _rules()), "默认全开放")
	assert_false(m.is_walkable(-1, 0, _rules()), "越界仍不可走")
	# 自定义规则生效
	var nonzero := {"blocked_terrain": [], "blocked_variant": [], "blocked_objects": "nonzero"}
	assert_false(m.is_walkable(1, 1, nonzero), "nonzero 规则阻挡 object=1")
	assert_true(m.is_walkable(0, 0, nonzero), "object=0 可走")
	var custom := {"blocked_terrain": [5], "blocked_variant": [], "blocked_objects": []}
	var m2 := _mini_map(3, 3, [])
	m2._layers["terrain"][0] = 5
	assert_false(m2.is_walkable(0, 0, custom), "自定义 terrain 阻断")


func test_straight_path() -> void:
	var m := _mini_map(8, 3, [])
	var path := SimPath.find_path(m, _rules(), Vector2i(2, 1), Vector2i(5, 1))
	assert_eq(path.size(), 3, "直线长度")
	assert_eq(path[0], Vector2i(3, 1), "首步")
	assert_eq(path[2], Vector2i(5, 1), "终点")


func _nonzero() -> Dictionary:
	return {"blocked_terrain": [], "blocked_variant": [], "blocked_objects": "nonzero"}


func test_around_u_wall() -> void:
	# U 形墙: x=3 竖墙 y=0..2, 顶部 x=1..3 封住 — 绕底走 (显式 nonzero 规则)
	var walls := [[3, 0], [3, 1], [3, 2]]
	var m := _mini_map(6, 5, walls)
	var path := SimPath.find_path(m, _nonzero(), Vector2i(1, 1), Vector2i(5, 1))
	assert_true(path.size() > 0, "可达")
	assert_eq(path[path.size() - 1], Vector2i(5, 1), "终点正确")
	for p in path:
		assert_true(m.is_walkable(p.x, p.y, _nonzero()), "路径格可走 (%d,%d)" % [p.x, p.y])


func test_unreachable() -> void:
	var walls := [[2, 0], [2, 1], [2, 2], [2, 3], [2, 4]]
	var m := _mini_map(5, 5, walls)   # 整列封死 (显式 nonzero 规则)
	var path := SimPath.find_path(m, _nonzero(), Vector2i(1, 2), Vector2i(4, 2))
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
	# 裸 BFS 实测 ~30ms/次(GDScript) → 预算: 单次跨图 < 100ms; 战斗侧靠路径缓存兜住帧率
	var m := SimMapData.load_map("01")
	var rules := _rules()
	var t0: int = Time.get_ticks_msec()
	SimPath.find_path(m, rules, Vector2i(2, 2), Vector2i(60, 90))
	var ms: int = Time.get_ticks_msec() - t0
	assert_true(ms < 100, "单次跨图 BFS < 100ms (实际 %d ms)" % ms)
	# 带图整场预算 (缓存路径下): 3000 ticks < 10s
	var setup: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/battle_setup.json"))
	var b := Battle.start(setup, 42, m)
	var t1: int = Time.get_ticks_msec()
	for i in 3000:
		if b.finished:
			break
		b.tick()
	var battle_ms: int = Time.get_ticks_msec() - t1
	assert_true(battle_ms < 10000, "带图 3000 ticks < 10s (实际 %d ms)" % battle_ms)
