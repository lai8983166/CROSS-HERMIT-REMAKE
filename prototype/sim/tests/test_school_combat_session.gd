extends "res://sim/tests/test_base.gd"
const Combat := preload("res://sim/school_combat_session.gd")
const Playground := preload("res://sim/school_playground.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")


func _school():
	var model := Playground.new()
	var fixture: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_playground_legacy_v3.json")))
	assert_true(model.restore(fixture["cases"][1]["save"])["supported"])
	for op in ["workroom_open","work_start","work_skip","school_enter"]: assert_true(model.execute({"op":op})["supported"])
	return model


func _combat(model):
	var session := Combat.new()
	assert_true(session.open(model.adventure_preparation(),model.adventure_combat_limits()))
	return session


func _declared_nearby_geometry(session, enemy_id := 1243) -> void:
	# Explicit local test geometry; never an original world/placement witness.
	var player: Dictionary = session.find_unit(3); var enemy: Dictionary = session.find_unit(enemy_id)
	for y in range(-3,4):
		for x in range(-3,4):
			var cell: Vector2i = enemy["cell"]+Vector2i(x,y)
			if cell == enemy["cell"] or not session.walkable(cell) or session._blocked(3).has(cell): continue
			player["cell"] = cell; player["from_cell"] = cell
			return
	assert_true(false,"declared encounter has a valid nearby source cell")


func test_source_initial_actors_current_students_and_unique_instance_ids() -> void:
	var model = _school(); var before: Dictionary = model.state(); var save: Dictionary = model.export_save()
	var session = _combat(model)
	assert_eq(session.units.size(),14); assert_eq(session.enemies().size(),7)
	assert_eq(session.controlled_units().map(func(u): return u["character_id"]),[3,4,9])
	var keys := {}
	for unit in session.units:
		assert_false(keys.has(session.unit_key(unit))); keys[session.unit_key(unit)] = true
		if not unit["controllable"]:
			var actor: Dictionary = session.source_actors[session.unit_key(unit)]
			assert_eq(unit["cell"],Vector2i(actor["cell"][0],actor["cell"][1]))
			assert_eq(unit["limits"],actor["limits"])
	assert_eq(session.find_unit(3)["combat"]["power"],27)
	assert_eq(session.find_unit(4)["combat"]["accuracy"],91)
	assert_eq(session.find_unit(9)["combat"]["magic_resist"],53)
	assert_eq(model.state(),before); assert_eq(model.export_save(),save)


func test_player_attack_moves_then_hits_without_moving_source_stationary_opponents() -> void:
	var session = _combat(_school())
	var source_positions: Dictionary = {}
	for enemy in session.enemies(): source_positions[enemy["instance_id"]] = enemy["cell"]
	assert_true(session.command_attack(3,1243))
	for index in range(1600): session.tick()
	assert_false(session.events.is_empty(),"actual local scheduler moves into source range and releases attacks")
	assert_lt(session.find_unit(1243)["limits"]["hp"],162)
	for key in source_positions: assert_eq(session.find_unit(key)["cell"],source_positions[key],"source movement_rate0 never chases")
	assert_eq(session.find_unit(3)["limits"]["mp"],445,"basic attacks invent no skill resource spending")


func test_protected_invalid_dead_and_nonplayer_commands_refuse_atomically() -> void:
	var session = _combat(_school())
	assert_true(session.command_attack(3,1243))
	var before: Array = session.read_units()
	for key in [101,9999,3,4,1249,1248,1247,1217]:
		assert_false(session.command_attack(3,key)); assert_eq(session.read_units(),before)
	assert_false(session.command_attack(1243,3)); assert_false(session.select(1243))
	assert_false(session.command_move(1243,Vector2i(10,20)))
	session.find_unit(1243)["limits"]["hp"] = 0
	before = session.read_units()
	assert_false(session.command_attack(3,1243)); assert_eq(session.read_units(),before)


func test_ranged_attack_reaches_firing_cell_without_enemy_adjacency() -> void:
	var session = _combat(_school())
	var player: Dictionary = session.find_unit(3); var enemy: Dictionary = session.find_unit(1243)
	# Declared obstruction geometry exercises range seeking, rather than original placement.
	var blockers := [1249,1248,1247,1217]
	for index in range(4):
		var obstacle: Dictionary = session.find_unit(blockers[index])
		obstacle["cell"] = enemy["cell"]+[Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN][index]
		obstacle["from_cell"] = obstacle["cell"]
	var path: Array = session._attack_path(player,enemy)
	assert_false(path.is_empty(),"ranged firing cell is reachable even when all adjacent cells are occupied")
	var goal: Vector2i = path.back()
	var distance := absi(goal.x-enemy["cell"].x)+absi(goal.y-enemy["cell"].y)
	assert_true(distance > 1 and distance <= player["combat"]["attack_range"])
	for cell in path:
		assert_true(session.walkable(cell,player["movement_type"]))
		assert_false(session._blocked(3).has(cell))


func test_nearby_cast_pause_stop_and_enemy_retaliation() -> void:
	var session = _combat(_school()); _declared_nearby_geometry(session)
	assert_true(session.command_attack(3,1243)); session.tick()
	assert_true(session.phases.has(3)); assert_eq(session.find_unit(3)["visual"],"cast")
	var before: Array = session.read_units(); var phases: Dictionary = session.phases.duplicate(true); var frame: int = session.frame
	session.paused = true; session.advance(1000); session.tick()
	assert_eq(session.frame,frame); assert_eq(session.read_units(),before); assert_eq(session.phases,phases)
	session.paused = false
	assert_true(session.stop(3)); assert_false(session.phases.has(3)); assert_eq(session.find_unit(3)["target"],-1)
	for index in range(400): session.tick()
	assert_eq(session.find_unit(1243)["limits"]["hp"],162,"stopped player attack cannot release delayed damage")
	assert_lt(session.find_unit(3)["limits"]["hp"],117,"nearby source opponent retaliates under declared trial scheduler")


func test_seeded_attack_replay_and_nonoverlapping_paths_are_deterministic() -> void:
	var model = _school(); var a = _combat(model); var b = _combat(model)
	for session in [a,b]: assert_true(session.command_attack(3,1243))
	for index in range(1400):
		a.tick(); b.tick()
		assert_eq(a.events,b.events)
		assert_eq(a.read_units(),b.read_units())
		var used := {}
		for unit in a.units:
			if unit["limits"]["hp"] <= 0: continue
			assert_false(used.has(unit["cell"])); used[unit["cell"]] = true


func test_death_cancels_phases_and_completion_has_no_school_authority() -> void:
	var model = _school(); var state: Dictionary = model.state(); var save: Dictionary = model.export_save()
	var session = _combat(model)
	for enemy in session.enemies().duplicate():
		_declared_nearby_geometry(session,enemy["instance_id"])
		for index in range(200):
			if enemy["limits"]["hp"] <= 0: break
			session._hit(session.find_unit(3),enemy)
		assert_eq(enemy["limits"]["hp"],0); assert_false(session.phases.has(enemy["instance_id"]))
		assert_false(session._blocked(3).has(enemy["cell"]),"dead trial actor releases collision")
	session.tick(); assert_true(session.trial_complete); assert_true(session.enemies().is_empty())
	assert_eq(model.state(),state); assert_eq(model.export_save(),save)
	assert_eq(model.fifth_session.read_snapshot()["adventure_gate"],1)
	session.close(); assert_true(session.units.is_empty()); assert_true(session.phases.is_empty()); assert_true(session.events.is_empty())
	assert_true(session.open(model.adventure_preparation(),model.adventure_combat_limits()))
	assert_eq(session.enemies().size(),7); assert_eq(session.find_unit(1243)["limits"]["hp"],162); assert_eq(session.frame,0)


func test_invalid_reopen_and_waiting_squad_preserve_owned_state() -> void:
	var model = _school(); var session = _combat(model); var units: Array = session.read_units()
	assert_false(session.open({},model.adventure_combat_limits())); assert_eq(session.read_units(),units)
	assert_false(session.open(model.adventure_preparation(),model.adventure_combat_limits(),"{}")); assert_eq(session.read_units(),units)
	assert_true(model.execute({"op":"plan_move","kind":"student","member_id":9,"target_group":-1,"target_slot":-1})["supported"])
	var save: Dictionary = model.export_save()
	assert_true(session.open(model.adventure_preparation(),model.adventure_combat_limits()))
	assert_eq(session.units.size(),13); assert_true(session.find_unit(9).is_empty()); assert_eq(session.enemies().size(),7)
	assert_eq(model.export_save(),save)


func test_requested_exit_consumes_results_in_order_without_damage_or_school_writes() -> void:
	var model = _school(); var school: Dictionary = model.state(); var save: Dictionary = model.export_save()
	var session = _combat(model)
	assert_true(session.command_attack(3,1243)); session.paused = true
	assert_true(session.request_return(), "return works while combat is paused")
	var started: Dictionary = session.ending_snapshot()
	assert_eq(started["phase"],"consuming"); assert_eq(started["outcome"],"player_exit")
	assert_false(started["consumer"]["result_consumed"], "end trigger does not skip the first wait")
	assert_false(session.request_return(), "duplicate exit cannot replace the pending frame")
	assert_true(session.take_handoff().is_empty(), "cannot leave before result consumption")
	var units: Array = session.read_units(); var events: Array = session.events.duplicate(true)
	assert_false(session.command_attack(3,1243)); assert_false(session.command_move(3,Vector2i(1,1)))
	assert_false(session.stop(3)); assert_false(session.select(4))
	session.advance(1.0/240.0)
	assert_eq(session.ending_snapshot()["consumer"]["action"],"call_replay_record")
	assert_true(session.take_handoff().is_empty())
	session.advance(10.0)
	assert_eq(session.ending_snapshot()["consumer"]["wait_ordinal"],2)
	session.tick()
	assert_eq(session.ending_snapshot()["consumer"]["wait_ordinal"],3)
	assert_eq(session.ending_snapshot()["phase"],"consuming")
	session.advance_exit()
	assert_eq(session.ending_snapshot()["phase"],"summary")
	assert_eq(session.ending_snapshot()["replay_record_calls"],1)
	assert_eq(session.read_units(),units); assert_eq(session.events,events)
	var handoff: Dictionary = session.take_handoff()
	assert_eq(handoff["successor"],"school_adventure_preparation")
	assert_false(handoff["authorizes_persistent_write"]); assert_false(handoff["native_equivalence_verified"])
	assert_false(handoff["summary"]["rewards_applied"]); assert_false(handoff["summary"]["campaign_advanced"])
	assert_true(session.take_handoff().is_empty(), "one handoff only")
	assert_eq(model.state(),school); assert_eq(model.export_save(),save)
	session.close()
	assert_true(session.units.is_empty()); assert_true(session.phases.is_empty()); assert_true(session.events.is_empty())
	assert_eq(session.ending_snapshot()["phase"],"closed")
	assert_true(session.open(model.adventure_preparation(),model.adventure_combat_limits()))
	assert_eq(session.ending_snapshot()["phase"],"active"); assert_eq(session.enemies().size(),7)


func test_last_actual_trial_hit_starts_the_end_flow() -> void:
	var model = _school(); var save: Dictionary = model.export_save(); var session = _combat(model)
	# Explicit local near-terminal fixture. The last HP change comes from the
	# actual remake attack scheduler, not a fabricated completion/consumer flag.
	for enemy in session.enemies(): enemy["limits"]["hp"] = 1 if enemy["instance_id"] == 1243 else 0
	_declared_nearby_geometry(session)
	assert_true(session.command_attack(3,1243))
	for index in range(600):
		session.tick()
		if session.ending_snapshot()["phase"] != "active": break
	assert_eq(session.find_unit(1243)["limits"]["hp"],0)
	assert_true(session.events.any(func(event): return event["target"] == 1243 and event["after_hp"] == 0))
	assert_true(session.trial_complete); assert_eq(session.ending_snapshot()["outcome"],"initial_enemies_cleared")
	assert_false(session.ending_snapshot()["consumer"]["result_consumed"])
	for index in range(4): session.advance_exit()
	var summary: Dictionary = session.ending_snapshot()["summary"]
	assert_eq(summary["remaining_enemies"],0); assert_eq(summary["defeated_enemies"],7)
	assert_eq(session.ending_snapshot()["phase"],"summary")
	assert_eq(model.export_save(),save, "clearing initial enemies is not formal adventure completion")


func test_squad_down_and_invalid_reopen_preserve_the_pending_end() -> void:
	var model = _school(); var session = _combat(model)
	for student in session.controlled_units(): student["limits"]["hp"] = 0
	session.tick()
	assert_eq(session.ending_snapshot()["outcome"],"squad_defeated")
	assert_false(session.trial_complete)
	var pending: Dictionary = session.ending_snapshot(); var units: Array = session.read_units()
	assert_false(session.open({},model.adventure_combat_limits()))
	assert_eq(session.ending_snapshot(),pending); assert_eq(session.read_units(),units)
	pending["summary"]["outcome"] = "changed externally"
	assert_eq(session.ending_snapshot()["summary"]["outcome"],"squad_defeated")
	for index in range(4): session.advance_exit()
	assert_eq(session.ending_snapshot()["phase"],"summary")
	assert_eq(session.ending_snapshot()["summary"]["surviving_students"],0)
	assert_eq(session.ending_snapshot()["summary"]["remaining_enemies"],7)
