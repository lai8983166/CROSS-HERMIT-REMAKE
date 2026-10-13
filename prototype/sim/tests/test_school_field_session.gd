extends "res://sim/tests/test_base.gd"
const Field := preload("res://sim/school_field_session.gd")
const Playground := preload("res://sim/school_playground.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")


func _school():
	var model := Playground.new()
	var fixture: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_playground_legacy_v3.json")))
	assert_true(model.restore(fixture["cases"][1]["save"])["supported"])
	for op in ["workroom_open","work_start","work_skip","school_enter"]:
		assert_true(model.execute({"op":op})["supported"])
	return model


func _field(model):
	var field := Field.new()
	assert_true(field.open(model.adventure_preparation(),model.adventure_combat_limits()))
	return field


func test_native_formation_three_squads_current_limits_and_preservation() -> void:
	var native: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_formation_placement_evidence.json")))
	var edits: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_combat_records_evidence.json")))
	for index in range(3):
		var model = _school()
		for command in edits["cases"][index]["commands"]:
			var move: Dictionary = command.duplicate(true); move["op"] = "plan_move"
			assert_true(model.execute(move)["supported"])
		var state: Dictionary = model.state(); var save: Dictionary = model.export_save()
		var field = _field(model)
		assert_eq(field.units.map(func(u): return [u["cell"].x,u["cell"].y]),native["cases"][index]["formation_placement"]["positions"].map(func(p): return p["xy"]))
		assert_eq(field.units.map(func(u): return u["limits"]),model.adventure_combat_limits()["students"].map(func(u): return u["limits"]))
		assert_eq(field.units.map(func(u): return u["character_id"]),model.adventure_preparation()["prepared"]["rounds"][0]["student_ids"])
		assert_true(field.find_unit(101).is_empty(),"teacher remains leader rather than invented combat unit")
		assert_eq(model.state(),state); assert_eq(model.export_save(),save)


func test_actual_navigation_is_contiguous_exact_and_unique() -> void:
	var model = _school(); var state: Dictionary = model.state(); var save: Dictionary = model.export_save()
	var field = _field(model)
	var destination := Vector2i(12,20)
	assert_true(field.command_move(3,destination))
	var previous: Vector2i = field.find_unit(3)["cell"]
	for frame in range(180):
		field.tick()
		var current: Vector2i = field.find_unit(3)["cell"]
		assert_true(absi(current.x-previous.x)+absi(current.y-previous.y) <= 1)
		assert_true(field.walkable(current))
		assert_false(field._reserved.has(current))
		var occupied := {}
		for unit in field.units:
			assert_false(occupied.has(unit["cell"])); occupied[unit["cell"]] = true
		previous = current
	assert_eq(field.find_unit(3)["cell"],destination)
	assert_true(field.find_unit(3)["path"].is_empty())
	assert_eq(field.find_unit(3)["visual"],"idle")
	assert_eq(model.state(),state); assert_eq(model.export_save(),save)


func test_refused_commands_keep_pending_path_and_limits() -> void:
	var field = _field(_school())
	assert_true(field.command_move(3,Vector2i(12,20)))
	var before: Array = field.read_units()
	var blocked := Vector2i(-1,-1)
	for y in range(96):
		for x in range(64):
			if not field.walkable(Vector2i(x,y)): blocked = Vector2i(x,y); break
		if blocked.x >= 0: break
	for destination in [blocked,Vector2i(-1,16),Vector2i(64,96),field.find_unit(4)["cell"],Vector2i(5,17)]:
		assert_false(field.command_move(3,destination)); assert_eq(field.read_units(),before)
	assert_false(field.command_move(101,Vector2i(12,20)))
	assert_false(field.select(101)); assert_eq(field.selected_id,3)
	var unit: Dictionary = field.find_unit(3)
	var origin: Vector2i = unit["cell"]
	for delta in SimPath.DIRS: field._reserved[origin+delta] = true
	assert_false(field.command_move(3,Vector2i(12,20)))
	assert_eq(field.reason,"unreachable"); assert_eq(field.read_units(),before)


func test_deterministic_multi_student_pause_stop_and_bounded_clock() -> void:
	var model = _school(); var a = _field(model); var b = _field(model)
	for field in [a,b]:
		assert_true(field.command_move(3,Vector2i(12,20)))
		assert_true(field.command_move(4,Vector2i(12,20)))
	for index in range(240):
		a.tick(); b.tick()
		assert_eq(a.read_units(),b.read_units())
		assert_true(a.find_unit(3)["cell"] != a.find_unit(4)["cell"])
	a.paused = true
	var before: Array = a.read_units(); var frame: int = a.frame
	a.advance(1000); a.tick()
	assert_eq(a.frame,frame); assert_eq(a.read_units(),before)
	a.paused = false; a.advance(1000)
	assert_eq(a.frame,frame+6,"long frame is capped at six local logic steps")
	for value in [-1.0,NAN,INF,0.0]: a.advance(value)
	assert_eq(a.frame,frame+6)
	assert_true(a.stop(4)); assert_true(a.find_unit(4)["path"].is_empty())
	assert_eq(a.find_unit(4)["destination"],Vector2i(-1,-1))


func test_invalid_open_is_atomic_and_read_values_are_owned() -> void:
	var model = _school(); var field = _field(model); var before: Array = field.read_units()
	var preparation: Dictionary = model.adventure_preparation(); var combat: Dictionary = model.adventure_combat_limits()
	for bad in [{},{"supported":true,"ready":true,"prepared":true}]:
		assert_false(field.open(bad,combat)); assert_eq(field.read_units(),before)
	assert_false(field.open(preparation,combat,"{}")); assert_eq(field.read_units(),before)
	for pair in [["hp",1],["hp_max",1]]:
		var bad: Dictionary = combat.duplicate(true); bad["students"][0]["limits"][pair[0]] = pair[1]
		assert_false(field.open(preparation,bad)); assert_eq(field.read_units(),before)
	var bad: Dictionary = combat.duplicate(true); bad["students"][0]["input"]["equipped_items"][0] = 1
	assert_false(field.open(preparation,bad))
	bad = combat.duplicate(true); bad["students"][1] = bad["students"][0].duplicate(true)
	assert_false(field.open(preparation,bad))
	bad = combat.duplicate(true); bad["students"][0]["input"]["job"] = 6
	assert_false(field.open(preparation,bad))
	field.read_units()[0]["limits"]["hp"] = 1
	assert_eq(field.read_units(),before)


func test_close_reopen_and_waiting_edits_never_settle_school() -> void:
	var model = _school(); var field = _field(model)
	assert_true(field.command_move(3,Vector2i(12,20)))
	for index in range(100): field.tick()
	field.close(); assert_false(field.ready); assert_true(field.units.is_empty())
	assert_false(field.command_move(3,Vector2i(12,20)))
	assert_true(model.execute({"op":"plan_move","kind":"student","member_id":9,"target_group":-1,"target_slot":-1})["supported"])
	var state: Dictionary = model.state(); var save: Dictionary = model.export_save()
	assert_true(field.open(model.adventure_preparation(),model.adventure_combat_limits()))
	assert_eq(field.units.map(func(u): return u["character_id"]),[3,4])
	assert_eq(field.find_unit(3)["cell"],Vector2i(10,17)); assert_eq(field.frame,0)
	assert_eq(model.fifth_session.read_snapshot()["adventure_gate"],1)
	assert_eq(model.state(),state); assert_eq(model.export_save(),save)
