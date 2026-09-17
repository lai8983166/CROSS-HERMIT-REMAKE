extends "res://sim/tests/test_base.gd"
## Battle 循环验收 (tasks 2.1-2.3)

func _load_setup() -> Dictionary:
	return JSON.parse_string(FileAccess.get_file_as_string("res://data/battle_setup.json"))


func test_unit_setup_derivation() -> void:
	var setup := _load_setup()
	var u := BattleUnit.new()
	u.setup(setup.units[0])
	assert_true(u.hp_max > 0 and u.hp == u.hp_max, "HP 初值=派生上限")
	assert_true(u.mp_max >= 30, "MP 下限钳位")
	assert_true(absf(u.engage_left - SimEngage.engage_seconds(10)) < 0.001, "ENGAGE=表值")
	assert_eq(u.state, BattleUnit.State.IDLE, "初始 idle")
	assert_true(u.atk_power >= 1, "普攻威力快照")


func test_battle_runs_to_finish() -> void:
	var b := Battle.start(_load_setup(), 42)
	b.run_to_finish()
	assert_true(b.finished, "战斗结束")
	assert_true(b.winner == 0 or b.winner == 1, "有胜方")
	var has_attack := false
	var has_dead := false
	var has_move := false
	for e in b.events:
		if " hit " in e:
			has_attack = true
		if " dead" in e:
			has_dead = true
		if " move " in e:
			has_move = true
	assert_true(has_attack, "日志含命中")
	assert_true(has_dead, "日志含阵亡")
	assert_true(has_move, "日志含移动")


func test_determinism_same_seed() -> void:
	var a := Battle.start(_load_setup(), 42)
	a.run_to_finish()
	var b := Battle.start(_load_setup(), 42)
	b.run_to_finish()
	assert_eq(a.frame, b.frame, "tick 数一致")
	assert_eq(a.winner, b.winner, "胜负一致")
	assert_eq(a.events.size(), b.events.size(), "日志条数一致")
	for i in a.events.size():
		if a.events[i] != b.events[i]:
			assert_eq(a.events[i], b.events[i], "第 %d 条不一致" % i)
			return
	assert_true(true, "同种子整场一致")


func test_seed_matters() -> void:
	var a := Battle.start(_load_setup(), 42)
	a.run_to_finish()
	var diff_found := false
	for seed in [7, 1234]:
		var b := Battle.start(_load_setup(), seed)
		b.run_to_finish()
		if b.events != a.events:
			diff_found = true
	assert_true(diff_found, "不同种子产生不同序列")


func test_engage_withdraw() -> void:
	# 蓝方单兵 ENGAGE 覆盖为极短 → 撤退触发红胜 (engage_seconds 可选字段, 见 setup _meta)
	var setup := _load_setup()
	var blue_only := []
	for u in setup.units:
		if u.faction == 1:
			u["engage_seconds"] = 1.0
			blue_only.append(u)
	setup.units = setup.units.slice(0, 1) + blue_only.slice(0, 1)   # 1v1, 蓝方 1 秒撤退
	var b := Battle.start(setup, 42)
	b.run_to_finish()
	assert_true(b.finished, "结束")
	assert_eq(b.winner, 0, "蓝撤退 → 红胜")
	var has_withdraw := false
	for e in b.events:
		if " withdraw" in e:
			has_withdraw = true
	assert_true(has_withdraw, "日志含撤退")


func test_battle_paths_around_wall() -> void:
	# 隔墙 1v1 (task 2.1): 中间竖墙留缺口, BFS 绕行, 战斗打完且 move 不踩墙
	var m := SimMapData.new()
	m.cell_w = 7
	m.cell_h = 5
	var cells := 35
	var obj: Array = []
	obj.resize(cells)
	obj.fill(0)
	for y in 4:
		obj[y * 7 + 3] = 1          # x=3 竖墙 y=0..3, y=4 留缺口
	var zero: Array = []
	zero.resize(cells)
	zero.fill(0)
	m._layers = {"terrain": zero.duplicate(), "variant": zero.duplicate(), "object": obj}
	var rules := {"blocked_terrain": [], "blocked_variant": [], "blocked_objects": "nonzero"}
	var setup := {
		"move_interval": 6, "attack_interval": 30,
		"units": [
			{"name": "L", "faction": 0, "job_id": 1, "level": 5,
			 "stats": {"strength": 30, "agility": 18, "constitution": 30}, "pos": [1, 2]},
			{"name": "R", "faction": 1, "job_id": 1, "level": 5,
			 "stats": {"strength": 28, "agility": 18, "constitution": 28}, "pos": [5, 2]},
		]}
	var b := Battle.start(setup, 7, m)
	b.walk_rules = rules
	b.run_to_finish()
	assert_true(b.finished, "隔墙战斗结束")
	assert_true(b.winner == 0 or b.winner == 1, "有胜方")
	for e in b.events:
		if " move " in e:
			var parts := e.split(" ")[-1].split(",")
			var x: int = int(parts[0])
			var y: int = int(parts[1])
			assert_true(m.is_walkable(x, y, rules), "move 落点 %d,%d 可走" % [x, y])


func test_setup_positions_walkable() -> void:
	# task 2.3: 实战布阵全员初始格可行走 (MAP01 + 默认规则)
	var m := SimMapData.load_map("01")
	var rules := _load_setup()
	var rules_json: Dictionary = JSON.parse_string(
			FileAccess.get_file_as_string("res://data/walk_rules.json"))
	for u in rules.units:
		assert_true(m.is_walkable(u.pos[0], u.pos[1], rules_json),
			"%s 初始格 (%d,%d) 可走" % [u.name, u.pos[0], u.pos[1]])
